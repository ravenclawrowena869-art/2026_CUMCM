from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve()
PROJECT = HERE.parents[1]
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))

from src.exact_runner_adapter import (
    build_q80_margin_for_forecast,
    make_zero_margin_table,
    simulate_period,
    validate_exact_trace,
)


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def forecast_causality_report(forecast: pd.DataFrame) -> dict:
    decision = pd.to_datetime(forecast['decision_time'])
    load_src = pd.to_datetime(forecast['load_source_target_ts'])
    pv_src = pd.to_datetime(forecast['pv_max_training_target_ts'])
    load_bad = int((load_src >= decision).sum())
    pv_bad = int((pv_src >= decision).sum())
    future_count = int(forecast.get('future_count', pd.Series(0, index=forecast.index)).sum())
    equality_count = int(forecast.get('equality_cutoff_count', pd.Series(0, index=forecast.index)).sum())
    return {
        'status': 'PASS' if load_bad == pv_bad == future_count == equality_count == 0 else 'FAIL',
        'load_cutoff_violations': load_bad,
        'pv_cutoff_violations': pv_bad,
        'future_count': future_count,
        'equality_cutoff_count': equality_count,
        'rule': 'observation_target_ts < decision_time',
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=PROJECT)
    ap.add_argument('--forecast', type=Path, required=True)
    ap.add_argument('--model', choices=['M1', 'M2'], required=True)
    ap.add_argument('--start-date', default='2025-02-01')
    ap.add_argument('--end-date', default='2025-12-31')
    ap.add_argument('--initial-soc-kwh', type=float, default=6000.0)
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--label', required=True)
    args = ap.parse_args()

    root = args.root.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    forecast = pd.read_csv(args.forecast)
    causal = forecast_causality_report(forecast)
    if causal['status'] != 'PASS':
        write_json(output / f'{args.label}_forecast_causality.json', causal)
        raise RuntimeError('forecast causality gate failed')

    if args.model == 'M1':
        margin = make_zero_margin_table(forecast)
        margin_provenance = {'mode': 'POINT_ZERO_MARGIN', 'risk_margin_rebuilt': False}
    else:
        margin = build_q80_margin_for_forecast(root, forecast)
        margin.to_csv(output / f'{args.label}_q80_margin_audit.csv', index=False)
        margin_provenance = {
            'mode': 'SIGNED_RESIDUAL_Q80_MARGIN_R1',
            'risk_margin_rebuilt': True,
            'cutoff_all_pass': bool(margin['cutoff_pass'].astype(bool).all()),
            'rows': int(len(margin)),
        }

    result = simulate_period(
        root,
        forecast=forecast,
        margin=margin,
        start_date=args.start_date,
        end_date=args.end_date,
        initial_soc_kwh=args.initial_soc_kwh,
        policy_label=args.label,
    )
    slot = result['slot_replay']
    daily = result['daily_metrics']
    plan = result['day_ahead_plan']
    validator = validate_exact_trace(slot, plan, initial_soc_kwh=args.initial_soc_kwh)

    slot.to_csv(output / f'{args.label}_slot_replay.csv', index=False)
    daily.to_csv(output / f'{args.label}_daily_metrics.csv', index=False)
    plan.to_csv(output / f'{args.label}_day_ahead_plan.csv', index=False)
    result['planner_log'].to_csv(output / f'{args.label}_planner_log.csv', index=False)
    result['recourse_log'].to_csv(output / f'{args.label}_recourse_log.csv', index=False)
    write_json(output / f'{args.label}_validator.json', validator)
    write_json(output / f'{args.label}_forecast_causality.json', causal)

    summary = {
        'label': args.label,
        'model': args.model,
        'start_date': str(args.start_date),
        'end_date': str(args.end_date),
        'initial_soc_kwh': float(args.initial_soc_kwh),
        'end_soc_kwh': float(result['end_soc_kwh']),
        'days': int(daily.shape[0]),
        'slots': int(slot.shape[0]),
        'normal_purchase_kWh': float(slot['q_DA_kWh'].sum()),
        'normal_cost_yuan': float(slot['normal_cost_yuan'].sum()),
        'emergency_kWh': float(slot['emergency_kWh'].sum()),
        'emergency_cost_yuan': float(slot['emergency_cost_yuan'].sum()),
        'realized_total_cost_yuan': float(slot['normal_cost_yuan'].sum() + slot['emergency_cost_yuan'].sum()),
        'emergency_slot_count': int((slot['emergency_kWh'] > 1e-7).sum()),
        'emergency_day_count': int((daily['emergency_kWh'] > 1e-7).sum()),
        'paid_unused_normal_kWh': float(slot['paid_unused_normal_kWh'].sum()),
        'pv_curtailment_kWh': float(slot['pv_curtailment_kWh'].sum()),
        'battery_throughput_kWh': float((slot['charge_exec_kWh'] + slot['discharge_exec_kWh']).sum()),
        'fallback_count': int(slot['fallback_used'].sum()),
        'validator_status': validator['status'],
        'forecast_causality_status': causal['status'],
        'margin_provenance': margin_provenance,
    }
    write_json(output / f'{args.label}_summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    return 0 if validator['status'] == 'PASS' else 2


if __name__ == '__main__':
    raise SystemExit(main())

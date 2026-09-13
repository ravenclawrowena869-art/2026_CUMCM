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
    build_exact_oracle_forecast,
    build_q80_margin_for_forecast,
    make_zero_margin_table,
    simulate_period,
    validate_exact_trace,
)


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=PROJECT)
    ap.add_argument('--oracle', choices=['O1', 'O2'], required=True)
    ap.add_argument('--model', choices=['M1', 'M2'], required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    args = ap.parse_args()

    root = args.root.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    base = pd.read_csv(root / 'inputs' / 'F1_K7_annual_forecast.csv')
    oracle_forecast, provenance = build_exact_oracle_forecast(
        root, base, mode=args.oracle, start_date='2025-11-01', end_date='2025-12-31'
    )

    prefix_summary = json.loads((root / 'outputs' / 'exact_tuning' / f'K7_{args.model}' / f'K7_{args.model}_summary.json').read_text())
    initial_soc = float(prefix_summary['end_soc_kwh'])
    if args.model == 'M1':
        margin = make_zero_margin_table(oracle_forecast)
        margin_meta = {'mode': 'POINT_ZERO_MARGIN'}
    else:
        margin = build_q80_margin_for_forecast(root, oracle_forecast)
        margin.to_csv(output / f'{args.oracle}_{args.model}_q80_margin_audit.csv', index=False)
        margin_meta = {
            'mode': 'SIGNED_RESIDUAL_Q80_MARGIN_R1',
            'rows': int(len(margin)),
            'cutoff_all_pass': bool(margin['cutoff_pass'].astype(bool).all()),
        }

    result = simulate_period(
        root,
        forecast=oracle_forecast,
        margin=margin,
        start_date='2025-11-01',
        end_date='2025-12-31',
        initial_soc_kwh=initial_soc,
        policy_label=f'{args.oracle}_{args.model}_DIAGNOSTIC_ONLY',
    )
    slot = result['slot_replay']
    plan = result['day_ahead_plan']
    daily = result['daily_metrics']
    validator = validate_exact_trace(slot, plan, initial_soc_kwh=initial_soc)

    tag = f'{args.oracle}_{args.model}'
    slot.to_csv(output / f'{tag}_nov_dec_slot_replay.csv', index=False)
    plan.to_csv(output / f'{tag}_nov_dec_day_ahead_plan.csv', index=False)
    daily.to_csv(output / f'{tag}_nov_dec_daily_metrics.csv', index=False)
    result['planner_log'].to_csv(output / f'{tag}_planner_log.csv', index=False)
    result['recourse_log'].to_csv(output / f'{tag}_recourse_log.csv', index=False)
    write_json(output / f'{tag}_validator.json', validator)
    write_json(output / f'{tag}_provenance.json', {**provenance, 'model': args.model, 'margin': margin_meta,
                                                      'initial_soc_source': f'F1_K7_{args.model}_Oct31_end_SOC',
                                                      'initial_soc_kwh': initial_soc})

    emergency = slot['emergency_kWh']
    late = slot['slot'].astype(int) >= 109
    summary = {
        'oracle': args.oracle,
        'model': args.model,
        'label': 'DIAGNOSTIC_ONLY / FUTURE_LEAKAGE_BY_DESIGN',
        'deployable': False,
        'future_leakage_by_design': True,
        'scope': '2025-11-01..2025-12-31',
        'initial_soc_kwh': initial_soc,
        'end_soc_kwh': float(result['end_soc_kwh']),
        'slots': int(len(slot)),
        'total_cost_yuan': float(slot['normal_cost_yuan'].sum() + slot['emergency_cost_yuan'].sum()),
        'normal_cost_yuan': float(slot['normal_cost_yuan'].sum()),
        'emergency_cost_yuan': float(slot['emergency_cost_yuan'].sum()),
        'emergency_kWh': float(emergency.sum()),
        'emergency_slots': int((emergency > 1e-7).sum()),
        'emergency_days': int(slot.loc[emergency > 1e-7, 'date'].nunique()),
        'emergency_18_24_share': float(emergency[late].sum() / emergency.sum()) if emergency.sum() > 1e-12 else 0.0,
        'paid_unused_normal_kWh': float(slot['paid_unused_normal_kWh'].sum()),
        'pv_curtailment_kWh': float(slot['pv_curtailment_kWh'].sum()),
        'fallback_count': int(slot['fallback_used'].sum()),
        'validator_status': validator['status'],
        'runner_sha256': '5a2ab76328a70a939ab9ada31bb7603ce5acb45d6a0c2d2a18783524f8bb8e47',
    }
    write_json(output / f'{tag}_summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    return 0 if validator['status'] == 'PASS' else 2


if __name__ == '__main__':
    raise SystemExit(main())

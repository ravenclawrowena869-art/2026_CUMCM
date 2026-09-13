from __future__ import annotations

import hashlib
import importlib.util
import shutil
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np
import pandas as pd

FROZEN_RUNNER_SHA256 = '5a2ab76328a70a939ab9ada31bb7603ce5acb45d6a0c2d2a18783524f8bb8e47'
ATTACHMENT1_SHA256 = '66b87134f5ecccd68184d3539bb1293ef039f9e0fdd955a589b9bfa7f227c377'
ATTACHMENT2_SHA256 = '2e95fd446bfafa0d8c59577b5c2e2ea8b3f1def20dde54a3062556f4da9b4c72'
N = 144


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_frozen_runner(root: Path) -> ModuleType:
    path = root / 'authority_snapshot' / 'FROZEN_Q2_CURRENT' / 'run_q80_year.py'
    observed = _sha256(path)
    if observed != FROZEN_RUNNER_SHA256:
        raise RuntimeError(f'frozen runner hash mismatch: {observed}')
    spec = importlib.util.spec_from_file_location('q2_frozen_current_run_q80_year', path)
    if spec is None or spec.loader is None:
        raise RuntimeError('cannot import frozen Q2 runner snapshot')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_official_actuals(root: Path) -> tuple[pd.DatetimeIndex, np.ndarray, np.ndarray, np.ndarray]:
    att1 = root / 'inputs' / 'official_attachment1.xlsx'
    att2 = root / 'inputs' / 'official_attachment2.xlsx'
    if _sha256(att1) != ATTACHMENT1_SHA256 or _sha256(att2) != ATTACHMENT2_SHA256:
        raise RuntimeError('official attachment hash mismatch')
    load_df = pd.read_excel(att2, sheet_name='小区负载', header=0)
    pv_df = pd.read_excel(att2, sheet_name='光伏发电实际功率', header=0)
    dates = pd.DatetimeIndex(pd.to_datetime(load_df.iloc[:, 0]).dt.normalize())
    pv_dates = pd.DatetimeIndex(pd.to_datetime(pv_df.iloc[:, 0]).dt.normalize())
    if not dates.equals(pv_dates):
        raise RuntimeError('attachment2 date mismatch')
    load = load_df.iloc[:, 1:145].to_numpy(float)
    pv = pv_df.iloc[:, 1:145].to_numpy(float)
    tariff_df = pd.read_excel(att1, sheet_name=0, header=0)
    tariff = tariff_df.iloc[:N, 1].to_numpy(float)
    if load.shape != (365, N) or pv.shape != (365, N) or tariff.shape != (N,):
        raise RuntimeError('unexpected official input shape')
    return dates, load, pv, tariff


def make_zero_margin_table(forecast: pd.DataFrame) -> pd.DataFrame:
    out = forecast[['date', 'slot']].copy().reset_index(drop=True)
    out['reserve_margin_kWh'] = 0.0
    return out


def simulate_period(
    root: Path,
    *,
    forecast: pd.DataFrame,
    margin: pd.DataFrame,
    start_date: str | pd.Timestamp,
    end_date: str | pd.Timestamp,
    initial_soc_kwh: float,
    policy_label: str,
) -> dict[str, Any]:
    """Run the frozen Q2 planner + P2 causal storage controller on a contiguous period.

    All optimization and physical/accounting semantics are delegated to the byte-pinned
    frozen runner. This adapter only supplies forecast/margin inputs and period bounds.
    """
    runner = load_frozen_runner(root)
    dates, load, pv, tariff = read_official_actuals(root)
    date_to_idx = {pd.Timestamp(d): i for i, d in enumerate(dates)}
    start = pd.Timestamp(start_date).normalize()
    end = pd.Timestamp(end_date).normalize()
    if end < start:
        raise ValueError('end_date before start_date')
    days = pd.date_range(start, end, freq='D')

    f = forecast.copy()
    m = margin.copy()
    f['date'] = f['date'].astype(str)
    m['date'] = m['date'].astype(str)

    e = float(initial_soc_kwh)
    all_rows: list[dict[str, Any]] = []
    planner_log: list[dict[str, Any]] = []
    recourse_log: list[dict[str, Any]] = []
    day_rows: list[dict[str, Any]] = []
    plan_rows: list[dict[str, Any]] = []

    for d in days:
        ds = d.date().isoformat()
        fd = f[f['date'].eq(ds)].sort_values('slot')
        md = m[m['date'].eq(ds)].sort_values('slot')
        if len(fd) != N or len(md) != N:
            raise RuntimeError(f'missing forecast/margin rows for {ds}: {len(fd)}/{len(md)}')
        fc_load = fd['forecast_load_kW'].to_numpy(float)
        fc_pv = fd['forecast_pv_kW'].to_numpy(float)
        margin_kwh = md['reserve_margin_kWh'].to_numpy(float)
        planning = fc_load * runner.DELTA + margin_kwh
        solar = fc_pv * runner.DELTA
        day_e0 = float(e)
        x, evid = runner.solve_day_ahead(planning, solar, tariff, e)
        q = x[:N]
        c_ref = x[N:2*N]
        d_ref = x[2*N:3*N]
        for row in evid:
            planner_log.append({'date': ds, **row})
        for t in range(N):
            plan_rows.append({
                'date': ds,
                'slot': t + 1,
                'target_ts': runner.target_ts(d, t + 1).isoformat(),
                'decision_time': d.isoformat(),
                'contract_id': runner.CONTRACT_ID,
                'time_mapping_version': runner.TIME_MAPPING,
                'experiment_policy_label': policy_label,
                'day_initial_SOC_kWh': day_e0,
                'q_DA_kWh': float(q[t]),
                'charge_ref_kWh': float(c_ref[t]),
                'discharge_ref_kWh': float(d_ref[t]),
                'spill_ref_kWh': float(x[3*N+t]),
                'SOC_ref_kWh': float(x[4*N+t]),
                'forecast_load_kWh': float(fc_load[t] * runner.DELTA),
                'forecast_pv_kWh': float(fc_pv[t] * runner.DELTA),
                'reserve_margin_kWh': float(margin_kwh[t]),
                'risk_adjusted_planning_load_kWh': float(planning[t]),
                'tariff': float(tariff[t]),
            })
        idx = date_to_idx[d]
        rows, e, solver_rows = runner.execute_p2(
            d, q, c_ref, d_ref, load[idx], pv[idx], tariff, e,
            margin_kwh, fc_load, fc_pv,
        )
        for row in rows:
            row['experiment_policy_label'] = policy_label
        all_rows.extend(rows)
        recourse_log.extend(solver_rows)
        day_df = pd.DataFrame(rows)
        day_rows.append({
            'date': ds,
            'day_initial_SOC_kWh': day_e0,
            'SOC_end_kWh': float(e),
            'normal_cost_yuan': float(day_df['normal_cost_yuan'].sum()),
            'emergency_cost_yuan': float(day_df['emergency_cost_yuan'].sum()),
            'total_cost_yuan': float(day_df['normal_cost_yuan'].sum() + day_df['emergency_cost_yuan'].sum()),
            'emergency_kWh': float(day_df['emergency_kWh'].sum()),
            'emergency_slots': int((day_df['emergency_kWh'] > runner.TOL).sum()),
            'fallback_count': int(day_df['fallback_used'].sum()),
        })

    slot_df = pd.DataFrame(all_rows)
    daily_df = pd.DataFrame(day_rows)
    return {
        'slot_replay': slot_df,
        'daily_metrics': daily_df,
        'day_ahead_plan': pd.DataFrame(plan_rows),
        'planner_log': pd.DataFrame(planner_log),
        'recourse_log': pd.DataFrame(recourse_log),
        'end_soc_kwh': float(e),
        'policy_label': policy_label,
    }


def build_q80_margin_for_forecast(root: Path, forecast: pd.DataFrame) -> pd.DataFrame:
    """Rebuild the current Q80 residual margin using frozen-runner semantics.

    Full-year inputs delegate byte-for-byte to the frozen helper.  A contiguous
    Feb-01 prefix uses the same signed-residual/order-statistic rule but stops at
    the last supplied day, which is required for pre-registered Sep-Oct tuning.
    """
    runner = load_frozen_runner(root)
    dates, load, pv, _ = read_official_actuals(root)
    date_to_idx = {pd.Timestamp(d): i for i, d in enumerate(dates)}
    f = forecast.copy()
    f['date'] = f['date'].astype(str)

    supplied = pd.DatetimeIndex(sorted(pd.to_datetime(f['date']).dt.normalize().unique()))
    if len(supplied) == 0 or supplied[0] != runner.START_DATE:
        raise RuntimeError('Q80 forecast scope must start at formal START_DATE')
    target_days = pd.date_range(runner.START_DATE, supplied[-1], freq='D')
    if not supplied.equals(target_days):
        raise RuntimeError('Q80 forecast scope must be a contiguous daily prefix')

    rows: list[dict[str, Any]] = []
    for d in target_days:
        ds = d.date().isoformat()
        fd = f[f['date'].eq(ds)].sort_values('slot')
        if len(fd) != N:
            raise RuntimeError(f'missing forecast rows for {ds}: {len(fd)}')
        idx = date_to_idx[d]
        actual_net = load[idx] - pv[idx]
        fc_net = fd['forecast_load_kW'].to_numpy(float) - fd['forecast_pv_kW'].to_numpy(float)
        for j in range(N):
            rows.append({
                'date': ds,
                'slot': j + 1,
                'target_ts': runner.target_ts(d, j + 1).isoformat(),
                'forecast_net_load_kW': float(fc_net[j]),
                'actual_net_load_kW': float(actual_net[j]),
                'net_residual_kW': float(actual_net[j] - fc_net[j]),
            })
    residual = pd.DataFrame(rows)

    with tempfile.TemporaryDirectory(prefix='q2_q80_exact_') as td:
        troot = Path(td)
        (troot / 'inputs').mkdir()
        (troot / 'results').mkdir()
        src = root / 'authority_snapshot' / 'FROZEN_Q2_CURRENT' / 'january_final_residuals.csv'
        shutil.copy2(src, troot / 'inputs' / 'january_final_residuals.csv')
        if target_days[-1] == runner.END_DATE:
            return runner.build_q80_audit(troot, residual).copy()

        jan = pd.read_csv(troot / 'inputs' / 'january_final_residuals.csv')
        byslot: dict[int, list[tuple[pd.Timestamp, float]]] = {s: [] for s in range(1, N + 1)}
        for x in jan.itertuples(index=False):
            byslot[int(x.slot)].append((runner.target_ts(x.date, int(x.slot)), float(x.net_residual)))
        for x in residual.itertuples(index=False):
            byslot[int(x.slot)].append((pd.Timestamp(x.target_ts), float(x.net_residual_kW)))
        for s in byslot:
            byslot[s].sort(key=lambda z: z[0])

        out: list[dict[str, Any]] = []
        for d in target_days:
            for slot in range(1, N + 1):
                eligible = [(ts, v) for ts, v in byslot[slot] if ts < d]
                vals = sorted(v for _, v in eligible)
                n = len(vals)
                if n <= 0:
                    raise RuntimeError('No residual history')
                k = int(np.ceil(runner.ALPHA * n))
                q = float(vals[k - 1])
                latest = max(ts for ts, _ in eligible)
                out.append({
                    'date': d.date().isoformat(), 'slot': slot, 'decision_time': d.isoformat(),
                    'n_history': n, 'k_rank': k, 'alpha': runner.ALPHA, 'q80_residual_kW': q,
                    'reserve_margin_kW': max(0.0, q),
                    'reserve_margin_kWh': max(0.0, q) * runner.DELTA,
                    'latest_residual_target_ts': latest.isoformat(), 'cutoff_pass': bool(latest < d),
                })
        df = pd.DataFrame(out)
        f1 = df[df.date == '2025-02-01']
        if not ((f1.iloc[:143].n_history == 24).all() and (f1.iloc[:143].k_rank == 20).all()
                and int(f1.iloc[143].n_history) == 23 and int(f1.iloc[143].k_rank) == 19):
            raise RuntimeError('Feb01 Q80 history anchor failed')
        if not df.cutoff_pass.all():
            raise RuntimeError('Q80 cutoff leak')
        return df


def build_exact_oracle_forecast(
    root: Path,
    base_forecast: pd.DataFrame,
    *,
    mode: str,
    start_date: str | pd.Timestamp,
    end_date: str | pd.Timestamp,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Create diagnostic-only perfect-information forecast substitutions.

    O1 replaces PV only; O2 replaces load and PV inside the requested window.
    Provenance columns are intentionally marked as future-leaking so this object
    cannot be mistaken for a deployable causal forecast.
    """
    m = mode.upper()
    if m not in {'O1', 'O2'}:
        raise ValueError('mode must be O1 or O2')
    start = pd.Timestamp(start_date).normalize()
    end = pd.Timestamp(end_date).normalize()
    if end < start:
        raise ValueError('end_date before start_date')
    dates, load, pv, _ = read_official_actuals(root)
    date_to_idx = {pd.Timestamp(d): i for i, d in enumerate(dates)}
    out = base_forecast.copy()
    out['date'] = out['date'].astype(str)
    out['oracle_substitution_mode'] = 'NONE'
    out['oracle_future_leakage'] = False
    substituted_days = 0
    for d in pd.date_range(start, end, freq='D'):
        ds = d.date().isoformat()
        mask = out['date'].eq(ds)
        day = out.loc[mask].sort_values('slot')
        if len(day) != N:
            raise RuntimeError(f'missing base forecast rows for oracle day {ds}: {len(day)}')
        idx = date_to_idx.get(d)
        if idx is None:
            raise RuntimeError(f'missing official actuals for oracle day {ds}')
        ordered_index = day.index
        out.loc[ordered_index, 'forecast_pv_kW'] = pv[idx]
        out.loc[ordered_index, 'pv_max_training_target_ts'] = out.loc[ordered_index, 'target_ts'].astype(str).to_numpy()
        if m == 'O2':
            out.loc[ordered_index, 'forecast_load_kW'] = load[idx]
            out.loc[ordered_index, 'load_source_target_ts'] = out.loc[ordered_index, 'target_ts'].astype(str).to_numpy()
        out.loc[ordered_index, 'oracle_substitution_mode'] = m
        out.loc[ordered_index, 'oracle_future_leakage'] = True
        if 'future_count' in out.columns:
            out.loc[ordered_index, 'future_count'] = 1
        substituted_days += 1
    meta = {
        'mode': m,
        'label': 'DIAGNOSTIC_ONLY / FUTURE_LEAKAGE_BY_DESIGN',
        'deployable': False,
        'future_leakage_by_design': True,
        'oracle_window': [start.date().isoformat(), end.date().isoformat()],
        'substituted_day_count': substituted_days,
        'substituted_fields': ['PV'] if m == 'O1' else ['LOAD', 'PV'],
        'base_forecast': 'selected F1 outside oracle window',
    }
    return out, meta


def validate_exact_trace(
    slot_replay: pd.DataFrame,
    day_ahead_plan: pd.DataFrame,
    *,
    initial_soc_kwh: float,
    tolerance: float = 1e-7,
) -> dict[str, Any]:
    df = slot_replay.sort_values(['date', 'slot']).reset_index(drop=True).copy()
    plan = day_ahead_plan.sort_values(['date', 'slot']).reset_index(drop=True).copy()
    if len(df) != len(plan) or len(df) == 0:
        return {'status': 'FAIL', 'reason': 'ROW_COUNT_MISMATCH', 'replay_rows': len(df), 'plan_rows': len(plan)}

    q_imm = np.abs(df['q_DA_kWh'].to_numpy(float) - plan['q_DA_kWh'].to_numpy(float))
    bal = (
        df['q_DA_kWh'].to_numpy(float) - df['paid_unused_normal_kWh'].to_numpy(float)
        + df['emergency_kWh'].to_numpy(float) + df['actual_pv_kWh'].to_numpy(float)
        + df['discharge_exec_kWh'].to_numpy(float) - df['actual_load_kWh'].to_numpy(float)
        - df['charge_exec_kWh'].to_numpy(float) - df['pv_curtailment_kWh'].to_numpy(float)
    )
    soc_rec = (
        df['SOC_end_kWh'].to_numpy(float)
        - (df['SOC_start_kWh'].to_numpy(float) + 0.9 * df['charge_exec_kWh'].to_numpy(float)
           - df['discharge_exec_kWh'].to_numpy(float) / 0.9)
    )
    starts = df['SOC_start_kWh'].to_numpy(float)
    ends = df['SOC_end_kWh'].to_numpy(float)
    continuity = np.empty(len(df), float)
    continuity[0] = starts[0] - float(initial_soc_kwh)
    continuity[1:] = starts[1:] - ends[:-1]

    charge = df['charge_exec_kWh'].to_numpy(float)
    discharge = df['discharge_exec_kWh'].to_numpy(float)
    emergency = df['emergency_kWh'].to_numpy(float)
    w = df['paid_unused_normal_kWh'].to_numpy(float)
    v = df['pv_curtailment_kWh'].to_numpy(float)
    q = df['q_DA_kWh'].to_numpy(float)
    pv = df['actual_pv_kWh'].to_numpy(float)
    tariff = df['tariff'].to_numpy(float)
    normal_cost_resid = df['normal_cost_yuan'].to_numpy(float) - tariff * q
    emergency_cost_resid = df['emergency_cost_yuan'].to_numpy(float) - 5.0 * tariff * emergency

    checks = {
        'q_immutability_max_abs_kWh': float(np.max(q_imm)),
        'balance_max_abs_kWh': float(np.max(np.abs(bal))),
        'soc_recursion_max_abs_kWh': float(np.max(np.abs(soc_rec))),
        'soc_continuity_max_abs_kWh': float(np.max(np.abs(continuity))),
        'soc_min_kWh': float(min(float(initial_soc_kwh), float(np.min(ends)))),
        'soc_max_kWh': float(max(float(initial_soc_kwh), float(np.max(ends)))),
        'power_charge_max_kWh': float(np.max(charge)),
        'power_discharge_max_kWh': float(np.max(discharge)),
        'simultaneous_charge_discharge_count': int(np.sum((charge > tolerance) & (discharge > tolerance))),
        'emergency_charging_count': int(np.sum((emergency > tolerance) & (charge > tolerance))),
        's1_w_lower_violation_max_kWh': float(max(0.0, -float(np.min(w)))),
        's1_w_upper_violation_max_kWh': float(max(0.0, float(np.max(w - q)))),
        's1_v_lower_violation_max_kWh': float(max(0.0, -float(np.min(v)))),
        's1_v_upper_violation_max_kWh': float(max(0.0, float(np.max(v - pv)))),
        'normal_cost_max_abs_residual_yuan': float(np.max(np.abs(normal_cost_resid))),
        'emergency_cost_max_abs_residual_yuan': float(np.max(np.abs(emergency_cost_resid))),
        'fallback_count': int(df['fallback_used'].sum()),
    }
    arg = int(np.argmax(np.abs(continuity)))
    checks['soc_continuity_argmax'] = {
        'date': str(df.iloc[arg]['date']), 'slot': int(df.iloc[arg]['slot']),
        'residual_kWh': float(continuity[arg]),
    }
    max_power = 5000.0 / 6.0
    failures = []
    scalar_limits = [
        ('q_immutability_max_abs_kWh', tolerance),
        ('balance_max_abs_kWh', tolerance),
        ('soc_recursion_max_abs_kWh', tolerance),
        ('soc_continuity_max_abs_kWh', tolerance),
        ('s1_w_lower_violation_max_kWh', tolerance),
        ('s1_w_upper_violation_max_kWh', tolerance),
        ('s1_v_lower_violation_max_kWh', tolerance),
        ('s1_v_upper_violation_max_kWh', tolerance),
        ('normal_cost_max_abs_residual_yuan', tolerance),
        ('emergency_cost_max_abs_residual_yuan', tolerance),
    ]
    for key, limit in scalar_limits:
        if checks[key] > limit:
            failures.append(key)
    if checks['soc_min_kWh'] < 1200.0 - tolerance: failures.append('SOC_MIN')
    if checks['soc_max_kWh'] > 10800.0 + tolerance: failures.append('SOC_MAX')
    if checks['power_charge_max_kWh'] > max_power + tolerance: failures.append('CHARGE_POWER')
    if checks['power_discharge_max_kWh'] > max_power + tolerance: failures.append('DISCHARGE_POWER')
    for key in ('simultaneous_charge_discharge_count','emergency_charging_count','fallback_count'):
        if checks[key] != 0: failures.append(key)
    checks['status'] = 'PASS' if not failures else 'FAIL'
    checks['failures'] = failures
    checks['rows'] = int(len(df))
    return checks

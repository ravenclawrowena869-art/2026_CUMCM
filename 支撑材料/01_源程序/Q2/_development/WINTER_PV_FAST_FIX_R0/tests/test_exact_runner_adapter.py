from pathlib import Path
import hashlib
import pandas as pd
import numpy as np

from src.exact_runner_adapter import (
    FROZEN_RUNNER_SHA256,
    load_frozen_runner,
    make_zero_margin_table,
    simulate_period,
)

ROOT = Path(__file__).resolve().parents[1]


def test_frozen_runner_snapshot_hash_is_pinned():
    p = ROOT / 'authority_snapshot' / 'FROZEN_Q2_CURRENT' / 'run_q80_year.py'
    assert hashlib.sha256(p.read_bytes()).hexdigest() == FROZEN_RUNNER_SHA256
    mod = load_frozen_runner(ROOT)
    assert mod.CONTRACT_ID == 'CUMCM2026_C_Q2_MATH_CONTRACT_R1'


def test_zero_margin_table_preserves_scope_and_is_exact_zero():
    f = pd.read_csv(ROOT / 'inputs' / 'F0_L2_P3_annual_forecast.csv')
    z = make_zero_margin_table(f)
    assert len(z) == 48096
    assert z[['date', 'slot']].equals(f[['date', 'slot']])
    assert np.array_equal(z['reserve_margin_kWh'].to_numpy(), np.zeros(len(z)))


def test_exact_adapter_reproduces_frozen_feb01_p2_slot_trace():
    f = pd.read_csv(ROOT / 'inputs' / 'F0_L2_P3_annual_forecast.csv')
    q = pd.read_csv(ROOT / 'authority_snapshot' / 'FROZEN_Q2_CURRENT' / 'q80_margin_audit.csv')
    actual = pd.read_csv(ROOT / 'authority_snapshot' / 'FROZEN_Q2_CURRENT' / 'Q80_P2_CAUSAL_slot_replay.csv')
    out = simulate_period(
        ROOT,
        forecast=f,
        margin=q,
        start_date='2025-02-01',
        end_date='2025-02-01',
        initial_soc_kwh=6000.0,
        policy_label='M2_Q80_P2',
    )
    exp = actual[actual['date'].eq('2025-02-01')].reset_index(drop=True)
    got = out['slot_replay'].reset_index(drop=True)
    assert len(got) == 144
    cols = [
        'q_DA_kWh','charge_ref_kWh','discharge_ref_kWh',
        'charge_exec_kWh','discharge_exec_kWh','emergency_kWh',
        'paid_unused_normal_kWh','pv_curtailment_kWh',
        'SOC_start_kWh','SOC_end_kWh','normal_cost_yuan','emergency_cost_yuan',
    ]
    for c in cols:
        np.testing.assert_allclose(got[c].to_numpy(float), exp[c].to_numpy(float), rtol=0, atol=1e-9)
    assert abs(out['end_soc_kwh'] - float(exp.iloc[-1]['SOC_end_kWh'])) <= 1e-9
    assert int(got['fallback_used'].sum()) == 0


def test_f0_q80_margin_rebuild_matches_frozen_authority():
    from src.exact_runner_adapter import build_q80_margin_for_forecast
    f = pd.read_csv(ROOT / 'inputs' / 'F0_L2_P3_annual_forecast.csv')
    got = build_q80_margin_for_forecast(ROOT, f)
    exp = pd.read_csv(ROOT / 'authority_snapshot' / 'FROZEN_Q2_CURRENT' / 'q80_margin_audit.csv')
    assert len(got) == len(exp) == 48096
    for c in ['n_history','k_rank','alpha','q80_residual_kW','reserve_margin_kW','reserve_margin_kWh']:
        np.testing.assert_allclose(got[c].to_numpy(float), exp[c].to_numpy(float), rtol=0, atol=1e-12)
    assert got['latest_residual_target_ts'].astype(str).tolist() == exp['latest_residual_target_ts'].astype(str).tolist()
    assert got['cutoff_pass'].astype(bool).all()


def test_exact_adapter_exports_plan_and_replay_q_is_immutable():
    f = pd.read_csv(ROOT / 'inputs' / 'F0_L2_P3_annual_forecast.csv')
    q = pd.read_csv(ROOT / 'authority_snapshot' / 'FROZEN_Q2_CURRENT' / 'q80_margin_audit.csv')
    out = simulate_period(
        ROOT, forecast=f, margin=q,
        start_date='2025-02-01', end_date='2025-02-01',
        initial_soc_kwh=6000.0, policy_label='M2_Q80_P2',
    )
    plan = out['day_ahead_plan'].sort_values(['date','slot']).reset_index(drop=True)
    replay = out['slot_replay'].sort_values(['date','slot']).reset_index(drop=True)
    assert len(plan) == len(replay) == 144
    np.testing.assert_allclose(plan['q_DA_kWh'], replay['q_DA_kWh'], rtol=0, atol=0)
    assert (plan['decision_time'] == '2025-02-01T00:00:00').all()


def test_exact_trace_validator_passes_frozen_day_and_detects_soc_tamper():
    from src.exact_runner_adapter import validate_exact_trace
    f = pd.read_csv(ROOT / 'inputs' / 'F0_L2_P3_annual_forecast.csv')
    q = pd.read_csv(ROOT / 'authority_snapshot' / 'FROZEN_Q2_CURRENT' / 'q80_margin_audit.csv')
    out = simulate_period(
        ROOT, forecast=f, margin=q,
        start_date='2025-02-01', end_date='2025-02-01',
        initial_soc_kwh=6000.0, policy_label='M2_Q80_P2',
    )
    report = validate_exact_trace(out['slot_replay'], out['day_ahead_plan'], initial_soc_kwh=6000.0)
    assert report['status'] == 'PASS'
    assert report['fallback_count'] == 0
    assert report['q_immutability_max_abs_kWh'] == 0.0
    bad = out['slot_replay'].copy()
    bad.loc[10, 'SOC_start_kWh'] += 1.0
    bad_report = validate_exact_trace(bad, out['day_ahead_plan'], initial_soc_kwh=6000.0)
    assert bad_report['status'] == 'FAIL'
    assert bad_report['soc_continuity_max_abs_kWh'] >= 1.0 - 1e-12


def test_partial_q80_rebuild_matches_frozen_prefix():
    from src.exact_runner_adapter import build_q80_margin_for_forecast
    f = pd.read_csv(ROOT / 'inputs' / 'F0_L2_P3_annual_forecast.csv')
    partial = f[pd.to_datetime(f['date']) <= pd.Timestamp('2025-10-31')].copy()
    got = build_q80_margin_for_forecast(ROOT, partial)
    exp = pd.read_csv(ROOT / 'authority_snapshot' / 'FROZEN_Q2_CURRENT' / 'q80_margin_audit.csv')
    exp = exp[pd.to_datetime(exp['date']) <= pd.Timestamp('2025-10-31')].reset_index(drop=True)
    assert len(got) == len(exp) == 273 * 144
    for c in ['n_history','k_rank','alpha','q80_residual_kW','reserve_margin_kW','reserve_margin_kWh']:
        np.testing.assert_allclose(got[c].to_numpy(float), exp[c].to_numpy(float), rtol=0, atol=1e-12)
    assert got['latest_residual_target_ts'].astype(str).tolist() == exp['latest_residual_target_ts'].astype(str).tolist()
    assert got['cutoff_pass'].astype(bool).all()


def test_exact_oracle_forecast_is_labeled_future_leakage_and_substitutes_requested_fields():
    from src.exact_runner_adapter import build_exact_oracle_forecast
    f1 = pd.read_csv(ROOT / 'inputs' / 'F1_K7_annual_forecast.csv')
    o1, meta1 = build_exact_oracle_forecast(ROOT, f1, mode='O1', start_date='2025-11-01', end_date='2025-12-31')
    o2, meta2 = build_exact_oracle_forecast(ROOT, f1, mode='O2', start_date='2025-11-01', end_date='2025-12-31')
    pre = f1[f1['date'].astype(str).eq('2025-10-31')].sort_values('slot').reset_index(drop=True)
    assert np.allclose(o1[o1['date'].astype(str).eq('2025-10-31')].sort_values('slot')['forecast_pv_kW'], pre['forecast_pv_kW'])
    day1 = o1[o1['date'].astype(str).eq('2025-11-01')].sort_values('slot').reset_index(drop=True)
    day2 = o2[o2['date'].astype(str).eq('2025-11-01')].sort_values('slot').reset_index(drop=True)
    _, load, pv, _ = __import__('src.exact_runner_adapter', fromlist=['read_official_actuals']).read_official_actuals(ROOT)
    idx = (pd.date_range('2025-01-01','2025-12-31',freq='D') == pd.Timestamp('2025-11-01')).argmax()
    np.testing.assert_allclose(day1['forecast_pv_kW'].to_numpy(float), pv[idx], rtol=0, atol=0)
    np.testing.assert_allclose(day2['forecast_pv_kW'].to_numpy(float), pv[idx], rtol=0, atol=0)
    np.testing.assert_allclose(day2['forecast_load_kW'].to_numpy(float), load[idx], rtol=0, atol=0)
    assert meta1['label'] == 'DIAGNOSTIC_ONLY / FUTURE_LEAKAGE_BY_DESIGN'
    assert meta1['deployable'] is False and meta2['deployable'] is False
    assert meta1['substituted_fields'] == ['PV']
    assert meta2['substituted_fields'] == ['LOAD','PV']
    assert (pd.to_datetime(day1['pv_max_training_target_ts']) >= pd.to_datetime(day1['decision_time'])).all()
    assert (pd.to_datetime(day2['load_source_target_ts']) >= pd.to_datetime(day2['decision_time'])).all()

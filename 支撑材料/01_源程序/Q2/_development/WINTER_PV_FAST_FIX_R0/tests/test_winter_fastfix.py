from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))

from winter_fastfix import (
    compute_amp_correction,
    select_k_from_tuning,
    compute_forecast_diagnostics,
    build_residual_history,
)


def test_amp_correction_uses_only_complete_prior_days_and_median():
    days=pd.to_datetime(['2025-08-28','2025-08-29','2025-08-30','2025-08-31','2025-09-01'])
    base={
        '2025-08-28': np.array([2.,2.]),
        '2025-08-29': np.array([4.,4.]),
        '2025-08-30': np.array([8.,8.]),
        '2025-08-31': np.array([16.,16.]),
        '2025-09-01': np.array([100.,100.]),
    }
    actual={
        '2025-08-28': np.array([1.,1.]),
        '2025-08-29': np.array([8.,8.]),
        '2025-08-30': np.array([8.,8.]),
        '2025-08-31': np.array([999.,999.]),
        '2025-09-01': np.array([999.,999.]),
    }
    corr,rho,meta=compute_amp_correction('2025-09-01',4,base,actual,delta_h=1.0)
    assert rho == 1.0
    assert np.allclose(corr,base['2025-09-01'])
    assert meta['eligible_dates']==['2025-08-28','2025-08-29','2025-08-30']
    assert '2025-08-31' not in meta['eligible_dates']
    assert '2025-09-01' not in meta['eligible_dates']
    assert meta['fallback_reason']=='INSUFFICIENT_VALID_PRIOR_RATIOS'
    assert meta['history_shortfall']==1


def test_amp_correction_excludes_zero_denominator_and_logs_fallback():
    base={'2025-08-30':np.array([0.,0.]),'2025-08-31':np.array([2.,2.]),'2025-09-01':np.array([5.,5.])}
    actual={'2025-08-30':np.array([3.,3.]),'2025-08-31':np.array([4.,4.]),'2025-09-01':np.array([9.,9.])}
    corr,rho,meta=compute_amp_correction('2025-09-01',7,base,actual,delta_h=1/6)
    assert rho==1.0
    assert np.allclose(corr,[5.,5.])
    assert meta['excluded_zero_denominator_dates']==['2025-08-30']
    assert meta['fallback_reason']=='NO_VALID_PRIOR_RATIOS'


def test_select_k_prefers_lowest_combined_cost_and_larger_k_on_tie():
    rows=pd.DataFrame([
        {'K':7,'M1_total_cost':100.,'M2_total_cost':100.},
        {'K':14,'M1_total_cost':90.,'M2_total_cost':100.},
        {'K':28,'M1_total_cost':90.00000001,'M2_total_cost':99.99999999},
    ])
    selected,detail=select_k_from_tuning(rows,rel_tie_tol=1e-6)
    assert selected==28
    assert detail['tie_break_applied'] is True


def test_diagnostics_sign_conventions():
    actual_pv=np.array([1.,2.,3.,4.])
    pred_pv=np.array([2.,1.,5.,4.])
    actual_load=np.array([10.,10.,10.,10.])
    pred_load=np.array([9.,9.,9.,9.])
    d=compute_forecast_diagnostics(actual_load,actual_pv,pred_load,pred_pv)
    assert np.isclose(d['pv_signed_error_mean'],0.5)
    expected=(actual_load-actual_pv)-(pred_load-pred_pv)
    assert np.isclose(d['net_load_signed_error_mean'],expected.mean())
    assert d['positive_net_load_underprediction_count']==int(np.sum(expected>0))


def test_residual_history_is_actual_minus_forecast_net_load():
    frame=pd.DataFrame({
        'date':['2025-01-01','2025-01-01'], 'slot':[1,2],
        'actual_load_kw':[10.,20.], 'actual_pv_kw':[1.,2.],
        'forecast_load_kw':[9.,18.], 'forecast_pv_kw':[2.,1.],
    })
    r=build_residual_history(frame)
    assert np.allclose(r['net_residual'].to_numpy(),[(10-1)-(9-2),(20-2)-(18-1)])


def test_soc_canonicalization_snaps_only_numerical_boundary_noise():
    from fastfix_experiment import canonicalize_soc
    assert canonicalize_soc(1200.0 + 2e-8, 1200.0, 10800.0, tol=1e-7) == 1200.0
    assert canonicalize_soc(10800.0 - 2e-8, 1200.0, 10800.0, tol=1e-7) == 10800.0
    assert canonicalize_soc(1200.001, 1200.0, 10800.0, tol=1e-7) == 1200.001


def test_amendment_a1_collects_exact_k_strictly_complete_days_with_backfill_and_causal_provenance():
    base={
        '2025-08-26': np.array([10.,10.]),
        '2025-08-27': np.array([10.,10.]),
        '2025-08-28': np.array([10.,10.]),
        '2025-08-30': np.array([10.,10.]),
        '2025-08-31': np.array([10.,10.]),
        '2025-09-01': np.array([10.,10.]),
    }
    actual={
        '2025-08-26': np.array([5.,5.]),
        '2025-08-27': np.array([10.,10.]),
        '2025-08-28': np.array([20.,20.]),
        '2025-08-30': np.array([30.,30.]),
        '2025-08-31': np.array([999.,999.]),
        '2025-09-01': np.array([999.,999.]),
    }
    prov={
        d:{'decision_time':f'{d}T00:00:00','max_training_target_ts':(pd.Timestamp(d)-pd.Timedelta(minutes=10)).isoformat(),
           'future_count':0,'equality_cutoff_count':0}
        for d in ['2025-08-26','2025-08-27','2025-08-28','2025-08-30','2025-08-31','2025-09-01']
    }
    prov['2025-08-28']['max_training_target_ts']=prov['2025-08-28']['decision_time']
    corr,rho,meta=compute_amp_correction(
        '2025-09-01',3,base,actual,delta_h=1.0,eps_E_kwh=1e-9,
        forecast_provenance_by_day=prov,
    )
    assert meta['eligible_dates']==['2025-08-26','2025-08-27','2025-08-30']
    assert meta['valid_ratio_count']==3
    assert meta['latest_complete_history_date']=='2025-08-30'
    assert '2025-08-31' not in meta['eligible_dates']
    assert '2025-08-28' in meta['excluded_noncausal_forecast_dates']
    assert meta['history_shortfall']==0
    assert rho==1.0
    assert np.allclose(corr,base['2025-09-01'])


def test_amendment_a4_uses_prefrozen_energy_epsilon_and_never_clips_rho():
    base={
        '2025-08-28':np.array([1.,1.]),
        '2025-08-29':np.array([0.0002,0.0002]),
        '2025-08-30':np.array([1.,1.]),
        '2025-09-01':np.array([2.,2.]),
    }
    actual={
        '2025-08-28':np.array([100.,100.]),
        '2025-08-29':np.array([9.,9.]),
        '2025-08-30':np.array([100.,100.]),
        '2025-09-01':np.array([0.,0.]),
    }
    prov={
        d:{'decision_time':f'{d}T00:00:00','max_training_target_ts':(pd.Timestamp(d)-pd.Timedelta(minutes=10)).isoformat(),
           'future_count':0,'equality_cutoff_count':0}
        for d in base
    }
    corr,rho,meta=compute_amp_correction(
        '2025-09-01',2,base,actual,delta_h=1.0,eps_E_kwh=1e-3,
        forecast_provenance_by_day=prov,
    )
    assert '2025-08-29' not in meta['eligible_dates']
    assert meta['excluded_denominator_dates'][0]['date']=='2025-08-29'
    assert meta['excluded_denominator_dates'][0]['reason']=='FORECAST_ENERGY_LE_EPS'
    assert rho==100.0
    assert np.allclose(corr,[200.,200.])
    assert meta['rho_clipped'] is False


def test_amendment_a2_a4_frozen_experiment_config_is_predeclared():
    import json
    cfg_path=ROOT/'config'/'winter_fastfix_config.json'
    cfg=json.loads(cfg_path.read_text(encoding='utf-8'))
    assert cfg['evaluation_window_label']=='pre-designated winter evaluation window'
    assert cfg['tuning_window']==['2025-09-01','2025-10-31']
    assert cfg['winter_evaluation_window']==['2025-11-01','2025-12-31']
    assert cfg['relative_tie_tol']==1e-6
    assert cfg['eps_E_kwh']==1e-9
    assert cfg['rho_clip'] is None
    assert cfg['formal_start']=='2025-02-01'
    assert cfg['initial_soc_kwh']==6000.0


def test_build_ampcorr_maps_enforces_prefrozen_eps_and_daily_forecast_provenance():
    from fastfix_experiment import build_ampcorr_maps
    f0_pv={'2025-02-01':np.array([2.,2.])}
    actual_pv={'2025-02-01':np.array([0.,0.])}
    jan_f={
        '2025-01-27':np.array([1.,1.]),
        '2025-01-28':np.array([1.,1.]),
        '2025-01-29':np.array([0.0002,0.0002]),
        '2025-01-30':np.array([1.,1.]),
        '2025-01-31':np.array([1.,1.]),
    }
    jan_a={k:np.array([100.,100.]) for k in jan_f}
    prov={
        d:{'decision_time':f'{d}T00:00:00',
           'max_training_target_ts':(pd.Timestamp(d)-pd.Timedelta(minutes=10)).isoformat(),
           'future_count':0,'equality_cutoff_count':0}
        for d in jan_f
    }
    prov['2025-01-28']['max_training_target_ts']=prov['2025-01-28']['decision_time']
    out,meta=build_ampcorr_maps(2,'2025-02-01',f0_pv,actual_pv,jan_f,jan_a,
                                forecast_provenance_by_day=prov,eps_E_kwh=1e-3)
    row=meta.iloc[0]
    assert row['eligible_dates']==['2025-01-27','2025-01-30']
    assert row['excluded_noncausal_forecast_dates']==['2025-01-28']
    assert row['excluded_denominator_dates'][0]['date']=='2025-01-29'
    assert row['latest_complete_history_date']=='2025-01-30'
    assert row['valid_ratio_count']==2
    assert np.allclose(out['2025-02-01'],[200.,200.])

def test_daily_p3_provenance_builders_preserve_strict_cutoff_fields():
    from fastfix_experiment import daily_p3_provenance_from_f0, daily_p3_provenance_from_january_audit
    f0=pd.DataFrame({
        'date':['2025-02-01','2025-02-01'],
        'slot':[1,2],
        'decision_time':['2025-02-01T00:00:00']*2,
        'pv_max_training_target_ts':['2025-01-31T23:50:00']*2,
        'future_count':[0,0],
        'equality_cutoff_count':[0,0],
    })
    pf=daily_p3_provenance_from_f0(f0)
    assert pf['2025-02-01']['decision_time']=='2025-02-01T00:00:00'
    assert pf['2025-02-01']['max_training_target_ts']=='2025-01-31T23:50:00'
    assert pf['2025-02-01']['future_count']==0
    assert pf['2025-02-01']['equality_cutoff_count']==0

    audit=pd.DataFrame({
        'target_date':['2025-01-08','2025-01-08','2025-01-08'],
        'target_slot':[1,2,3],
        'model':['ETS_HW_DAILY','ETS_HW_DAILY','LAG7'],
        'decision_time':['2025-01-08 00:00:00']*3,
        'max_training_target_ts':['2025-01-07 23:50:00','2025-01-07 23:50:00','2025-01-01 00:10:00'],
        'future_count':[0,0,0],
        'equality_cutoff_count':[0,0,0],
    })
    pj=daily_p3_provenance_from_january_audit(audit)
    assert list(pj)==['2025-01-08']
    assert pj['2025-01-08']['decision_time']=='2025-01-08T00:00:00'
    assert pj['2025-01-08']['max_training_target_ts']=='2025-01-07T23:50:00'


def test_oracle_maps_substitute_future_actual_only_inside_winter_window():
    from fastfix_experiment import build_oracle_forecast_maps
    dates=['2025-10-31','2025-11-01','2025-12-31']
    f0_l={d:np.array([10.,11.]) for d in dates}
    f0_p={d:np.array([2.,3.]) for d in dates}
    act_l={d:np.array([20.,21.]) for d in dates}
    act_p={d:np.array([4.,5.]) for d in dates}
    l1,p1,meta1=build_oracle_forecast_maps('O1',f0_l,f0_p,act_l,act_p,'2025-11-01','2025-12-31')
    assert np.allclose(l1['2025-10-31'],f0_l['2025-10-31'])
    assert np.allclose(p1['2025-10-31'],f0_p['2025-10-31'])
    assert np.allclose(l1['2025-11-01'],f0_l['2025-11-01'])
    assert np.allclose(p1['2025-11-01'],act_p['2025-11-01'])
    assert meta1['label']=='DIAGNOSTIC_ONLY / FUTURE_LEAKAGE_BY_DESIGN'
    assert meta1['oracle_window']==['2025-11-01','2025-12-31']

    l2,p2,meta2=build_oracle_forecast_maps('O2',f0_l,f0_p,act_l,act_p,'2025-11-01','2025-12-31')
    assert np.allclose(l2['2025-10-31'],f0_l['2025-10-31'])
    assert np.allclose(p2['2025-10-31'],f0_p['2025-10-31'])
    assert np.allclose(l2['2025-11-01'],act_l['2025-11-01'])
    assert np.allclose(p2['2025-11-01'],act_p['2025-11-01'])
    assert meta2['deployable'] is False

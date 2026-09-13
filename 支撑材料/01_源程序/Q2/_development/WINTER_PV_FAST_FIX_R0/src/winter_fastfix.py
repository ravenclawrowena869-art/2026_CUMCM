from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping
import math
import numpy as np
import pandas as pd

SLOTS=144
DELTA_H=1/6


def _dkey(x) -> str:
    return pd.Timestamp(x).normalize().strftime('%Y-%m-%d')


def compute_amp_correction(
    target_day,
    K:int,
    base_p3_by_day:Mapping[str,np.ndarray],
    actual_pv_by_day:Mapping[str,np.ndarray],
    delta_h:float=DELTA_H,
    eps_E_kwh:float=1e-9,
    forecast_provenance_by_day:Mapping[str,dict]|None=None,
):
    """Strict-causal P3 daily-energy amplitude correction.

    Amendment A1: at decision d00, the latest legal *complete* natural day is
    d-2 because day d-1 slot144 targets d00 and equality is forbidden. Search
    backward until K valid complete days are collected. If the available source
    history cannot supply K valid ratios, keep the deployable forecast unchanged
    (rho=1) and expose the shortfall; this avoids silently calling a smaller
    history window "K".

    Amendment A4: the denominator epsilon is an explicit pre-frozen input and
    rho is never clipped.
    """
    if int(K) <= 0:
        raise ValueError('K must be positive')
    if not (math.isfinite(float(eps_E_kwh)) and float(eps_E_kwh) >= 0.0):
        raise ValueError('eps_E_kwh must be finite and nonnegative')
    d=pd.Timestamp(target_day).normalize()
    current_key=_dkey(d)
    if current_key not in base_p3_by_day:
        raise KeyError(f'missing current-day P3 forecast: {current_key}')

    # Search starts at d-2.  Restrict the backward walk to dates that actually
    # exist in either formal or January causal forecast authority.
    hist_keys=sorted(set(base_p3_by_day).intersection(actual_pv_by_day))
    hist_dates=[pd.Timestamp(k).normalize() for k in hist_keys if pd.Timestamp(k).normalize() <= d-pd.Timedelta(days=2)]
    earliest=min(hist_dates) if hist_dates else d

    accepted_desc=[]
    ratios_desc=[]
    excluded_den=[]
    excluded_noncausal=[]
    excluded_missing=[]
    cursor=d-pd.Timedelta(days=2)
    while cursor >= earliest and len(accepted_desc) < int(K):
        key=_dkey(cursor)
        # Completion check is explicit even though cursor starts at d-2.
        max_target_ts=cursor+pd.Timedelta(days=1)
        if not (max_target_ts < d):
            cursor-=pd.Timedelta(days=1); continue
        if key not in base_p3_by_day or key not in actual_pv_by_day:
            excluded_missing.append(key); cursor-=pd.Timedelta(days=1); continue

        if forecast_provenance_by_day is not None:
            pr=forecast_provenance_by_day.get(key)
            causal=False
            if pr is not None:
                try:
                    decision=pd.Timestamp(pr['decision_time'])
                    train_max=pd.Timestamp(pr['max_training_target_ts'])
                    causal=(decision == cursor and train_max < decision
                            and int(pr.get('future_count',0)) == 0
                            and int(pr.get('equality_cutoff_count',0)) == 0)
                except Exception:
                    causal=False
            if not causal:
                excluded_noncausal.append(key); cursor-=pd.Timedelta(days=1); continue

        f=np.asarray(base_p3_by_day[key],dtype=float)
        a=np.asarray(actual_pv_by_day[key],dtype=float)
        if f.shape!=a.shape or f.ndim!=1:
            raise ValueError(f'PV shape mismatch on {key}')
        if not (np.all(np.isfinite(f)) and np.all(np.isfinite(a))):
            raise ValueError(f'non-finite PV values on {key}')
        den=float(np.sum(f)*delta_h)
        num=float(np.sum(a)*delta_h)
        if not math.isfinite(den) or den <= float(eps_E_kwh):
            excluded_den.append({'date':key,'forecast_energy_kwh':den,'reason':'FORECAST_ENERGY_LE_EPS'})
            cursor-=pd.Timedelta(days=1); continue
        ratio=float(num/den)
        if not math.isfinite(ratio):
            excluded_den.append({'date':key,'forecast_energy_kwh':den,'reason':'NONFINITE_RATIO'})
            cursor-=pd.Timedelta(days=1); continue
        accepted_desc.append(key); ratios_desc.append(ratio)
        cursor-=pd.Timedelta(days=1)

    eligible=list(reversed(accepted_desc))
    ratios=list(reversed(ratios_desc))
    shortfall=max(0,int(K)-len(ratios))
    if len(ratios)==int(K):
        rho=float(np.median(np.asarray(ratios,dtype=float)))
        fallback=None
    elif len(ratios)==0:
        rho=1.0; fallback='NO_VALID_PRIOR_RATIOS'
    else:
        rho=1.0; fallback='INSUFFICIENT_VALID_PRIOR_RATIOS'

    current=np.asarray(base_p3_by_day[current_key],dtype=float)
    corr=np.maximum(0.0,rho*current)
    meta={
        'target_date':current_key,'K':int(K),'rho':rho,
        'eligible_dates':eligible,'ratios':[float(x) for x in ratios],
        'valid_ratio_count':len(ratios),'history_shortfall':shortfall,
        'excluded_zero_denominator_dates':[x['date'] for x in excluded_den],
        'excluded_denominator_dates':excluded_den,
        'excluded_noncausal_forecast_dates':excluded_noncausal,
        'excluded_missing_dates':excluded_missing,
        'fallback_reason':fallback,
        'known_at':d.strftime('%Y-%m-%d 00:00:00'),
        'latest_complete_history_date':eligible[-1] if eligible else None,
        'eps_E_kwh':float(eps_E_kwh),
        'rho_clipped':False,
    }
    return corr,rho,meta


def select_k_from_tuning(rows:pd.DataFrame, rel_tie_tol:float=1e-6):
    req={'K','M1_total_cost','M2_total_cost'}
    if not req.issubset(rows.columns): raise ValueError(f'missing {req-set(rows.columns)}')
    x=rows.copy(); x['combined_cost']=x['M1_total_cost'].astype(float)+x['M2_total_cost'].astype(float)
    best=float(x['combined_cost'].min())
    scale=max(abs(best),1.0)
    tied=x.loc[(x['combined_cost']-best).abs()<=rel_tie_tol*scale].copy()
    selected=int(tied['K'].max())
    return selected,{
        'selected_K':selected,'relative_tie_tolerance':float(rel_tie_tol),
        'best_combined_cost':best,'tied_K':sorted(tied['K'].astype(int).tolist()),
        'tie_break_applied':len(tied)>1,
    }


def _wape(actual,pred):
    a=np.asarray(actual,float); p=np.asarray(pred,float); den=float(np.sum(np.abs(a)))
    return float(np.sum(np.abs(p-a))/den) if den>1e-12 else float('nan')


def compute_forecast_diagnostics(actual_load,actual_pv,forecast_load,forecast_pv):
    L=np.asarray(actual_load,float); P=np.asarray(actual_pv,float); Lf=np.asarray(forecast_load,float); Pf=np.asarray(forecast_pv,float)
    if not (L.shape==P.shape==Lf.shape==Pf.shape): raise ValueError('shape mismatch')
    pe=Pf-P; ne=(L-P)-(Lf-Pf); pos=ne[ne>0]
    return {
        'n':int(L.size),
        'pv_signed_error_mean':float(np.mean(pe)),
        'pv_mae':float(np.mean(np.abs(pe))),
        'pv_rmse':float(np.sqrt(np.mean(pe*pe))),
        'pv_wape':_wape(P,Pf),
        'net_load_signed_error_mean':float(np.mean(ne)),
        'positive_net_load_underprediction_count':int(pos.size),
        'p90_positive_net_load_underprediction':float(np.quantile(pos,.90)) if pos.size else 0.0,
        'p95_positive_net_load_underprediction':float(np.quantile(pos,.95)) if pos.size else 0.0,
    }


def build_residual_history(frame:pd.DataFrame)->pd.DataFrame:
    out=frame.copy()
    out['load_residual']=out['actual_load_kw'].astype(float)-out['forecast_load_kw'].astype(float)
    out['pv_residual']=out['actual_pv_kw'].astype(float)-out['forecast_pv_kw'].astype(float)
    out['actual_net_load']=out['actual_load_kw'].astype(float)-out['actual_pv_kw'].astype(float)
    out['forecast_net_load']=out['forecast_load_kw'].astype(float)-out['forecast_pv_kw'].astype(float)
    out['net_residual']=out['actual_net_load']-out['forecast_net_load']
    return out

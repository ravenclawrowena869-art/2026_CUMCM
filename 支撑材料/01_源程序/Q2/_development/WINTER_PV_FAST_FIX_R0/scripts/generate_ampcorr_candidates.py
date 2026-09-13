from __future__ import annotations
import json, sys
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from fastfix_experiment import (
    load_f0_forecast, forecast_maps_from_f0, load_actual_and_tariff,
    january_maps_from_residuals, daily_p3_provenance_from_f0,
    build_ampcorr_maps, sha256_file,
)


def main() -> None:
    cfg=json.loads((ROOT/'config/winter_fastfix_config.json').read_text(encoding='utf-8'))
    f0=load_f0_forecast(ROOT/'inputs/F0_L2_P3_annual_forecast.csv')
    _,pv0=forecast_maps_from_f0(f0)
    prov=daily_p3_provenance_from_f0(f0)
    _,_,actual_pv=load_actual_and_tariff(ROOT/'inputs/official_attachment1.xlsx',ROOT/'inputs/official_attachment2.xlsx')
    jan_f,jan_a=january_maps_from_residuals(ROOT/'inputs/january_final_residuals.csv')

    # Current c488... January residual authority binds values but does not expose
    # daily P3-generation provenance. A1 therefore forbids those days from the
    # amplitude-ratio history; no provenance is borrowed from a different file.
    evidence={
        'policy':'A1_STRICT_PROVENANCE_REQUIRED',
        'formal_f0_daily_provenance_count':len(prov),
        'january_residual_days_present':len(jan_f),
        'january_days_admitted_to_ampcorr_history':0,
        'formal_f0_sha256':sha256_file(ROOT/'inputs/F0_L2_P3_annual_forecast.csv'),
        'january_residual_sha256':sha256_file(ROOT/'inputs/january_final_residuals.csv'),
        'eps_E_kwh':cfg['eps_E_kwh'],
        'rho_clip':cfg['rho_clip'],
    }
    (ROOT/'evidence').mkdir(exist_ok=True)
    (ROOT/'evidence/A1_HISTORICAL_P3_PROVENANCE_POLICY.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')

    for K in cfg['k_candidates']:
        corr,meta=build_ampcorr_maps(
            K,'2025-10-31',pv0,actual_pv,jan_f,jan_a,
            forecast_provenance_by_day=prov,eps_E_kwh=cfg['eps_E_kwh'])
        rows=[]
        for d in pd.date_range('2025-02-01','2025-10-31',freq='D'):
            ds=d.strftime('%Y-%m-%d')
            g=f0.loc[f0['date'].eq(ds)].sort_values('slot').copy()
            g['forecast_pv_kW']=corr[ds]
            g['forecast_net_load_kW']=g['forecast_load_kW']-g['forecast_pv_kW']
            g['pv_model']=f'P3_AMPCORR_K{K}'
            rows.append(g)
        out=pd.concat(rows,ignore_index=True)
        out.to_csv(ROOT/f'inputs/F1_K{K}_through_oct31.csv',index=False)
        (ROOT/f'inputs/P3_AMPCORR_K{K}_rho_through_oct31.json').write_text(
            json.dumps(meta.to_dict(orient='records'),indent=2),encoding='utf-8')

if __name__=='__main__':
    main()

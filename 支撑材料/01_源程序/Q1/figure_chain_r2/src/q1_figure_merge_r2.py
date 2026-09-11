from __future__ import annotations
import csv
from pathlib import Path
def _read(p):
    with Path(p).open("r",encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def _write(p,fields,rows):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
def export_final_interfaces(fig_csv,cost_csv,out_dir):
    out=Path(out_dir); rows=_read(fig_csv)
    if len(rows)!=144: raise ValueError("expected 144")
    sf=["slot_id","physical_start","physical_end","time_hour_end","price_yuan_per_kwh","load_kw","pv_kw","grid_purchase_kw","charge_kw","discharge_kw"]
    _write(out/"Q1_MAIN_FIGURE_SLOT_DATA_R2.csv",sf,[{k:r[k] for k in sf} for r in rows])
    soc=[{"boundary_id":0,"time_hour":"0","time_label":"00:00","soc_kwh":rows[0]["soc_start_kwh"]}]
    for i,r in enumerate(rows,1):
        soc.append({"boundary_id":i,"time_hour":r["time_hour_end"],"time_label":r["physical_end"],"soc_kwh":r["soc_end_kwh"]})
    _write(out/"Q1_MAIN_FIGURE_SOC_DATA_R2.csv",["boundary_id","time_hour","time_label","soc_kwh"],soc)
    c=_read(cost_csv); o=[]
    for r in c:
        isb=r["方案"]=="无储能基线"
        o.append({"scenario":r["方案"],"total_cost_cny":r["总购电成本_元"],"savings_absolute_cny":r["相对基线节省额_元"],"savings_percent":r["相对基线节省率_百分比"],"baseline_definition":"no-storage structural baseline; no storage; no selling; PV surplus curtailed" if isb else "comparison against the same no-storage structural baseline"})
    _write(out/"Q1_COST_COMPARISON_R2.csv",["scenario","total_cost_cny","savings_absolute_cny","savings_percent","baseline_definition"],o)

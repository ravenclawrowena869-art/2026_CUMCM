from __future__ import annotations
import csv
from pathlib import Path
import matplotlib.pyplot as plt

def _read_csv(path):
    with Path(path).open("r",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def build_soc_series(rows):
    return [0.0]+[float(r["time_hour_end"]) for r in rows], [float(rows[0]["soc_start_kwh"])]+[float(r["soc_end_kwh"]) for r in rows]

def render_q1_main_figure(data_path, output_dir):
    rows=_read_csv(data_path)
    if len(rows)!=144: raise ValueError("requires 144 slots")
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    dt=float(rows[0]["dt_hours"])
    edges=[0.0]+[float(r["time_hour_end"]) for r in rows]
    centers=[(edges[i]+edges[i+1])/2 for i in range(144)]
    price=[float(r["price_yuan_per_kwh"]) for r in rows]
    load=[float(r["load_kw"]) for r in rows]
    pv=[float(r["pv_kw"]) for r in rows]
    grid=[float(r["grid_purchase_kw"]) for r in rows]
    charge=[float(r["charge_kw"]) for r in rows]
    discharge=[float(r["discharge_kw"]) for r in rows]
    xs,soc=build_soc_series(rows)
    plt.rcParams["font.sans-serif"]=["AR PL UMing CN","DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"]=False
    plt.rcParams["svg.hashsalt"]="CUMCM2026_Q1_MAIN_FIGURE_R2"
    fig,ax=plt.subplots(4,1,figsize=(10.5,9.2),sharex=True,constrained_layout=True)
    ax[0].stairs(price,edges,linewidth=1.35); ax[0].set_ylabel("电价\n(元/kWh)"); ax[0].grid(alpha=.25)
    imin=min(range(144),key=price.__getitem__); imax=max(range(144),key=price.__getitem__)
    for i,label in ((imin,"最低价 05:40"),(imax,"最高价 20:40")):
        ax[0].annotate(label,xy=(edges[i+1],price[i]),xytext=(0,10),textcoords="offset points",ha="center",fontsize=8)
    ax[1].stairs(load,edges,label="负荷",linewidth=1.15)
    ax[1].stairs(pv,edges,label="光伏预测功率",linewidth=1.15)
    ax[1].stairs(grid,edges,label="优化购电功率",linewidth=1.15)
    ax[1].set_ylabel("功率 (kW)"); ax[1].legend(ncol=3,loc="upper center",frameon=False); ax[1].grid(alpha=.25)
    ax[2].bar(centers,discharge,width=dt*.82,label="放电功率（正）")
    ax[2].bar(centers,[-v for v in charge],width=dt*.82,label="充电功率（负）")
    ax[2].axhline(0,linewidth=.8); ax[2].set_ylabel("功率 (kW)"); ax[2].legend(ncol=2,loc="upper center",frameon=False); ax[2].grid(axis="y",alpha=.25)
    ax[3].plot(xs,soc,linewidth=1.3)
    ax[3].axhline(1200,linestyle="--",linewidth=1,label="SOC 下界 1200 kWh")
    ax[3].axhline(10800,linestyle="--",linewidth=1,label="SOC 上界 10800 kWh")
    ax[3].scatter([0,24],[soc[0],soc[-1]],s=18,zorder=3)
    ax[3].annotate("6000",(0,soc[0]),xytext=(5,5),textcoords="offset points",fontsize=8)
    ax[3].annotate("6000",(24,soc[-1]),xytext=(-28,5),textcoords="offset points",fontsize=8)
    ax[3].set_ylabel("SOC (kWh)"); ax[3].set_xlabel("物理时间 (h)"); ax[3].set_xlim(0,24); ax[3].set_xticks([0,4,8,12,16,20,24])
    ax[3].legend(ncol=2,loc="upper center",frameon=False,fontsize=8); ax[3].grid(alpha=.25)
    base=out/"Q1_MAIN_FIGURE_R2"
    files=[base.with_suffix(s) for s in [".png",".pdf",".svg"]]
    fig.savefig(files[0],dpi=300,bbox_inches="tight")
    fig.savefig(files[1],bbox_inches="tight",metadata={"Creator":"CUMCM2026 Q1 Figure Chain R2"})
    fig.savefig(files[2],bbox_inches="tight",metadata={"Creator":"CUMCM2026 Q1 Figure Chain R2"})
    plt.close(fig)
    return [str(p) for p in files]

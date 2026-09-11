from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import json

HERE = Path(__file__).resolve().parent
DATA = pd.read_csv(HERE / "Q1_FROZEN_FIGURE_DATA_R1.csv")
with open(HERE / "Q1_FIGURE_METRICS_R1.json", "r", encoding="utf-8") as f:
    METRICS = json.load(f)

candidates = ["Noto Sans CJK SC","Noto Sans CJK JP","Source Han Sans SC","WenQuanYi Zen Hei","SimHei","Arial Unicode MS"]
available = {f.name for f in fm.fontManager.ttflist}
font_name = next((x for x in candidates if x in available), None)
if font_name:
    plt.rcParams["font.sans-serif"] = [font_name]
plt.rcParams["axes.unicode_minus"] = False

x = DATA["time_hour"].to_numpy()
ticks = np.arange(0, 25, 4)

fig = plt.figure(figsize=(10.5, 5.8))
plt.plot(x, DATA["load_kw"], linewidth=1.7, label="小区负荷")
plt.plot(x, DATA["pv_kw"], linewidth=1.7, label="光伏发电")
plt.plot(x, DATA["grid_optimized_kw"], linewidth=1.7, label="电网购电")
plt.plot(x, DATA["storage_net_kw_positive_discharge"], linewidth=1.5, label="储能净功率（正放电、负充电）")
plt.axhline(0, linewidth=0.8)
plt.xlim(0, 24)
plt.xticks(ticks, [f"{int(t):02d}:00" for t in ticks])
plt.xlabel("时刻")
plt.ylabel("功率 / kW")
plt.title("问题1：购电与储能联合调度结果")
plt.grid(True, linewidth=0.5, alpha=0.35)
plt.legend(ncol=2, frameon=False)
plt.tight_layout()
fig.savefig(HERE / "Q1_FIG_01_购电与储能联合调度结果.png", dpi=300, bbox_inches="tight")
fig.savefig(HERE / "Q1_FIG_01_购电与储能联合调度结果.pdf", bbox_inches="tight")
fig.savefig(HERE / "Q1_FIG_01_购电与储能联合调度结果.svg", bbox_inches="tight")
plt.close(fig)

fig = plt.figure(figsize=(10.5, 5.8))
plt.plot(x, DATA["grid_baseline_no_storage_kw"], linewidth=1.8, label="无储能基线")
plt.plot(x, DATA["grid_optimized_kw"], linewidth=1.8, label="储能优化后")
plt.xlim(0, 24)
plt.xticks(ticks, [f"{int(t):02d}:00" for t in ticks])
plt.xlabel("时刻")
plt.ylabel("购电功率 / kW")
plt.title("问题1：储能优化前后购电曲线对比")
plt.grid(True, linewidth=0.5, alpha=0.35)
plt.legend(frameon=False)

annotation = (
    f"无储能成本：{METRICS['baseline_total_cost_cny']:.2f} 元\n"
    f"优化后成本：{METRICS['total_cost_cny']:.2f} 元\n"
    f"节省：{METRICS['savings_absolute_cny']:.2f} 元（{METRICS['savings_percent']:.2f}%）"
)
plt.text(0.985, 0.97, annotation, transform=plt.gca().transAxes,
         ha="right", va="top", fontsize=10,
         bbox=dict(boxstyle="round,pad=0.4", alpha=0.15))
plt.tight_layout()
fig.savefig(HERE / "Q1_FIG_02_储能优化前后购电曲线对比.png", dpi=300, bbox_inches="tight")
fig.savefig(HERE / "Q1_FIG_02_储能优化前后购电曲线对比.pdf", bbox_inches="tight")
fig.savefig(HERE / "Q1_FIG_02_储能优化前后购电曲线对比.svg", bbox_inches="tight")
plt.close(fig)

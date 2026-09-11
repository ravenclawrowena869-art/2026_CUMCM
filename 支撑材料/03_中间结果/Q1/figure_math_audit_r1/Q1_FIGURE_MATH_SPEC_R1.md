# CUMCM 2026 C题 — Q1 Figure Mathematical Specification R1

Date: 2026-09-11  
Role: `XXT_MATHEMATICAL`  
Freeze authority: `CUMCM2026_C_Q1_FREEZE_R0_20260911`  
Figure selection: **NOT FROZEN**  
Legacy figure package: `DRAFT_REFERENCE_ONLY`

## 0. Scope

本规范只冻结 **Q1 图表允许表达的数学语义、单位、时间口径与 Claim 边界**。不修改 Q1 Frozen 模型、结果、result1 或论文版式，也不决定最终正文一定放几张图。

正式 Figure Data 必须来自：

`official Attachment1 -> frozen Q1 code/output -> figure data export -> figure/table -> paper claim`。

聊天数字、旧截图、手工抄值不得升级为正式 Figure Data。

## 1. Frozen mathematical anchors

- time contract: `C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`
- 144 slots, `Δt=1/6 h`
- Stage-1 exact optimum: `35126.948589289634 CNY`
- Stage-2 exported schedule cost: `35126.948689289624 CNY`
- no-storage baseline cost: `48052.046590846665 CNY`
- savings vs no-storage baseline: `26.89812155476249%`
- SOC range: `[1200,10800] kWh`
- `E0 = E144 = 6000 kWh`
- simultaneous charge/discharge slots: `0`
- primary efficiency: `eta_c=eta_d=0.9`

图中如出现“优化后费用”，默认必须指 **Stage-2 exported schedule cost**；Stage-1 exact 只能在明确标注为 Stage-1 时单独出现。

## 2. Time semantics

slot `t=1,...,144`：`I_t=(τ_{t-1},τ_t]`, `τ_t=t/6 h`。

raw `0:10` = slot 1 right endpoint = physical `(00:00,00:10]`；raw `0:00+1` = slot 144 right endpoint = physical `(23:50,24:00]`。

功率量在每个10 min槽内按该槽平均/等效功率解释。正式绘图优先用 **step/stairs** 表示 10 min piecewise-constant slot value，不应用普通直线插值让评委误以为槽间存在观测到的连续斜坡。

推荐：power series使用145个physical boundaries；SOC使用145 states并包含E0和E144；x-axis使用physical time 00:00–24:00。若保留普通折线，仅允许作为趋势浏览，不得对槽间插值形状作定量 Claim。

## 3. Field semantics

| field | formal meaning | unit | allowed source | mathematical note |
|---|---|---:|---|---|
| `load_kw` | 小区负载功率 | kW | Attachment1 / frozen schedule | Q1确定性输入 |
| `pv_kw` | **光伏预测功率** | kW | Attachment1 / frozen schedule | 不得标为 actual PV |
| `price_yuan_per_kwh` | 购电价格 | 元/kWh | Attachment1 / frozen schedule | 不与kW共享同一y轴做量值比较 |
| `grid_optimized_kw` | Stage-2冻结调度外网购电功率 | kW | `6*grid_kwh` | 正值表示购电，不允许售电 |
| `charge_kw` | 储能充电功率的非负幅值 | kW | `6*charge_kwh` | `>=0` |
| `discharge_kw` | 储能放电功率的非负幅值 | kW | `6*discharge_kwh` | `>=0` |
| `storage_net_kw_positive_discharge` | `discharge_kw-charge_kw` | kW | derived from frozen schedule | 正=放电，负=充电；必须在图例明示 |
| `soc_kwh` | 储电量状态 | kWh | frozen schedule 145 states | 含0:00初值与24:00末值 |
| `grid_baseline_no_storage_kw` | 无储能基线外网购电功率 | kW | baseline replay | `max(load-pv,0)` |
| `baseline_curtailment_kw` | 无储能基线PV弃用功率 | kW | baseline replay | `max(pv-load,0)` |

图使用功率时 `P_grid,t=g_t/Δt=6g_t`，charge/discharge同理；结果表使用电量时 `g_t=P_grid,tΔt`。严禁把kW与kWh混用。

## 4. Baseline contract

无储能基线固定定义：charge=discharge=0；PV优先供负荷；禁止售电；`grid_baseline=max(load-pv,0)`；`curtailment_baseline=max(pv-load,0)`；与正式方案使用相同价格曲线和144槽时间映射。

冻结证据：baseline purchase=`61789.9354 kWh`；Stage-2 purchase=`59482.69876179719 kWh`；baseline cost=`48052.046590846665 CNY`；Stage-2 cost=`35126.948689289624 CNY`；savings=`26.89812155476249%`。

正式savings固定为 `(C_baseline-C_stage2)/C_baseline`，不得用Stage-1 exact替代Stage-2 exported cost。

## 5. Mechanism figure evidence

数学上适合机制图：load / PV forecast / grid purchase；charge/discharge或signed storage net；SOC 145-state trajectory；如需解释低价充电、高价放电可增加price，但推荐独立对齐子图而非双轴。

机制图可支持能量跨时段转移、SOC约束、部分低价槽充电/高价槽放电、PV富余被储能吸收的时序机制，但不能替代hard-constraint replay、objective recomputation或sensitivity。

## 6. Better as table/text

更适合表格/文字：baseline vs Stage-2 cost和26.90%；Stage-1 exact vs Stage-2 exported cost；6个4h aggregate；SOC endpoints；hard residual；epsilon/efficiency sensitivity。

尤其26.90%是精确费用比较，表格比单纯曲线面积更直接；价格随时段变化，不能从购电功率曲线面积视觉上直接推出购电费用变化。

## 7. Dual-axis / scale restrictions

禁止在以下情形用双轴：事后调两轴制造相关；用kW与元/kWh比较曲线高度/斜率；用kW与kWh暗示同量纲；主Claim依赖跨轴“看起来一致”。

若确需双轴，仅用于时点背景，必须清晰标单位、预先固定轴范围、caption说明不同量纲不可比较高度，并禁止跨轴 slope/correlation Claim。默认推荐 aligned panels > dual axis。

baseline purchase与optimized purchase若拆图但要比较幅值，必须share y-scale；charge/discharge正幅值分面亦需一致比例尺。

## 8. Normalization restrictions

SOC边界、购电峰值、充放电功率限制、绝对购电量、费用节省等Claim不得用归一化曲线替代原单位证据。归一化仅用于shape/timing探索，必须标`SHAPE_ONLY`。

## 9. Window audit

默认Figure window=`FULL_HORIZON=00:00–24:00`。任何局部窗口必须记录start/end、selection rule、是否事前定义、selection reason、freeze version。事后窗口只能标`DIAGNOSTIC_WINDOW`，不得证明全天规律。

## 10. Claim boundaries

Allowed：Stage-2相对no-storage费用下降约26.90%；SOC满足[1200,10800]且首末6000；正式Stage-2无同时充放电；部分低价槽充电/高价槽放电；当前Q1正式调度curtailment=0。

Forbidden：
- “储能优化实现外网购电削峰”：baseline最大购电功率约`4956.50 kW`，optimized约`8458.83 kW`；
- 把Attachment1 PV称为实际出力；
- 把Stage-2说成无容差exact optimum；
- 说LP理论上天然禁止同槽充放电；
- 说0.9/0.9是90%效率唯一正确解释；
- 说“曲线面积更小所以费用低26.90%”。

## 11. Merge Gate interface

XXT只冻结数学允许域；CYQ决定正文相关性；FYQ负责从Frozen output生成可复现Figure Data与脚本；final figure必须过`Q1_FIGURE_VALIDATOR_SPEC_R1.md`。

`FIGURE_SELECTION_FROZEN = FALSE`。
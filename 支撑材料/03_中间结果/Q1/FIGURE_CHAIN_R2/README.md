# Q1 Figure Chain R2 — Repository Index

状态：`THREE_ROLE_MERGE_COMPLETE / READY_FOR_REVIEW`

Freeze：
`CUMCM2026_C_Q1_FREEZE_R0_20260911`

正式选择：
`Q1_FIGURE_SELECTION = SELECT_1_MAIN_FIGURE`

模型结果状态：
`Q1_MODEL_RESULT_FREEZE = PRESERVED`

本目录来自三角色并行 Figure Pipeline 合并结果：

- CYQ：Paper relevance / Figure Brief；
- FYQ：Frozen Output → Figure Data → editable script → figure / paper-table export；
- XXT：数学语义、单位、Claim 边界与旧图审计。

## 正式主图

四联 FULL_HORIZON：
1. 分时电价；
2. 负荷 + 光伏预测功率 + 优化购电功率；
3. 放电为正、充电为负；
4. 145-state SOC + 1200/10800 kWh 边界 + 首末 6000 kWh。

绘图脚本：`plots/make_q1_main_figure_r2.py`。

## 正式数据与表

- `generated/Q1_FIGURE_DATA_R2.csv`
- `generated/Q1_MAIN_FIGURE_SLOT_DATA_R2.csv`
- `generated/Q1_MAIN_FIGURE_SOC_DATA_R2.csv`
- `generated/Q1_COST_COMPARISON_R2.csv`
- `generated/Q1_FIGURE_REGISTRY_R2.csv`
- `generated/tables/`

## 重要结论边界

- no-storage vs optimized 经济性比较以紧凑表格表达，不再作为第二张论文主图。
- 禁止写“削峰”：当前 Frozen 调度降低的是价格加权购电成本，不保证降低最大购电功率。
- PV 标签固定为“光伏预测功率”。
- Stage-1 exact optimum 与 Stage-2 exported cost 全精度下必须区分。

Clean replay 与三角色 Merge 证据见 `provenance/`、`docs/`。

旧 `../FIGURES_A_R1/` 仅保留为 `DRAFT_REFERENCE_ONLY / LEGACY_REFERENCE`。

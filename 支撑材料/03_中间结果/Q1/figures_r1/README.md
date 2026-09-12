# Q1 中间图表归档 R1

Source of Truth:
- Freeze: `CUMCM2026_C_Q1_FREEZE_R0_20260911`
- Frozen R2 delivery SHA256: `a8acd57687c9a2380ab089e14c23bfec467dca7882b51f7777c9f97ed4977058`
- Primary model: `TWO_STAGE_CONTINUOUS_LP`
- Primary efficiency: `eta_c = eta_d = 0.9`
- Time mapping: `C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`

本目录保存 Q1 中间图表及其 Figure Registry/指标。两张 GitHub 预览 SVG 从 Frozen Figure Data R1 重绘，仅用于仓库浏览；不改变 Frozen 结果，也不等价于最终论文选图。

数学审计结论：旧 Figure Bundle 数据本身与 Frozen R2 一致，但属于 `VALID_REFERENCE_NOT_FINAL`。Figure 01 的 PV 应表述为“光伏预测功率”；Figure 02 不能表述为“削峰”，26.90% 节省必须由 `Σ p_t g_t` 独立复算支持。

完整旧版绘图脚本归档在 `支撑材料/01_源程序/Q1/figures/legacy_reference/make_q1_figures.py`。正式 result 文件位于 `支撑材料/05求解结果/result1.xlsx`。

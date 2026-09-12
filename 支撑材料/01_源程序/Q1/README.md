# Q1 源程序完整归档

Authority: `CUMCM2026_C_Q1_FREEZE_R0_20260911`。

本目录归档问题一实际使用的核心求解、官方 result1 写入与中间图表程序。本次仅做 GitHub 工件整理，不改变任何 Frozen 模型、参数或数值。

## 当前已归档
- `generate_result1.py`：仓库既有的官方模板 result1 生成入口。
- `src/optimizer.py`：词典序两阶段连续 LP 核心求解器。
- `src/source.py`：附件1严格只读解析与时间映射。
- `src/result1.py`：官方 result1 ordinal 写入与 readback。
- `src/io_utils.py`：CSV/JSON 与哈希工具。
- `figures/legacy_reference/make_q1_figures.py`：旧 Figure Bundle A R1 的可复现绘图脚本，仅作为中间/回归参考。
- `requirements.txt`：R2 technical delivery 声明依赖。

## 对应工件
- 中间图表、Figure Registry、图表数据：`支撑材料/03_中间结果/Q1/figures_r1/`
- Frozen R2 验证摘要：`支撑材料/03_中间结果/Q1/frozen_r2/`
- 正式结果文件：`支撑材料/05求解结果/result1.xlsx`

## 重要说明
旧 Figure Bundle 的数学数据与 Frozen R2 一致，但图表仍属于 `VALID_REFERENCE_NOT_FINAL`，不代表论文最终选图。Figure 01 中 PV 在正式论文中应表述为“光伏预测功率”；Figure 02 不得表述为“削峰”。

R2 技术源码中的历史状态字符串若出现 `CANDIDATE_NOT_FROZEN/HOLD`，仅代表当时工程快照；最终冻结状态以 Q1 Final Freeze Manifest 为唯一 authority，不得据此重开 Q1。

官方赛题附件不重复放入 `02_自主数据` 或源程序目录。

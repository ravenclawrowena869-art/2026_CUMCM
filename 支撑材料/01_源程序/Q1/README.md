# Q1 源程序完整归档

Authority: `CUMCM2026_C_Q1_FREEZE_R0_20260911`。

本目录补齐问题一实际使用的核心求解、验证、回放、result1 写入、敏感性和绘图程序。核心模型仍为 `TWO_STAGE_CONTINUOUS_LP`，本次仅做 GitHub 工件归档，不改变任何 Frozen 数值。

## 目录
- `generate_result1.py`：仓库既有的官方模板 result1 生成入口（保留原文件）。
- `src/`：R2 technical delivery 中的核心求解/验证/回放/result1 源码快照。
- `tests/`：R2 回归与验证测试。
- `analysis/Q1_EPSILON_SENSITIVITY_SCRIPT.py`：epsilon confirmatory sensitivity。
- `figures/export_q1_figure_data_r2.py`：从 Frozen schedule/baseline 导出正式 Figure Data，不重求解模型。
- `figures/make_q1_main_figure_r2.py`：Q1 当前选定四联主图的绘图脚本。
- `figures/legacy_reference/make_q1_figures.py`：旧 A_R1 图包绘图脚本，仅作为中间/回归参考。
- `requirements.txt`：R2 technical delivery 声明依赖。

## 重要说明
R2 源码快照内部保留了当时的 `CANDIDATE_NOT_FROZEN/HOLD` 历史状态字符串；最终冻结状态以 `支撑材料/03_中间结果/Q1/CUMCM2026_C_Q1_FINAL_FREEZE_MANIFEST_R0.md` 为唯一 authority。不要因源码中的历史状态字符串重开 Q1。

官方赛题附件不重复放入 `02_自主数据` 或源程序目录。需要重跑技术快照时，将官方附件1按复现说明放到本地 `source/` 目录。

# Q1 中间结果

保存支撑问题 1 论文结果的必要中间表、图、检验结果和赛中形成的工作思路。

## 当前正式状态

Q1 已完成 `MODEL_AND_RESULT` Freeze。正式模型、正式数字与论文接口以当前 Frozen Source of Truth / Final Paper Handoff 为准；本目录中的 IDEA 文件不得覆盖 Frozen 事实。

当前正式图表链位于：

`FIGURE_CHAIN_R2/`

其中包含三角色合并后的 Figure Registry R2、Figure Data、论文表格、可编辑绘图脚本对应输出、300 dpi PNG、PDF/SVG、数学/论文审查证据和 clean replay archive。当前论文视觉选择为 `SELECT_1_MAIN_FIGURE`。

历史 `FIGURES_A_R1/` 保留为 `DRAFT_REFERENCE_ONLY / legacy reference`，不得覆盖 R2 Figure Registry 与最终图表选择。

## IDEA 记录规则

本目录允许保存 `Q1-IDEA-xxx_*.md`，用于记录已经形成、值得后续验证或进入论文交付的具体思路。

这些文件默认：

`AUTHORITY = WORKING_IDEA_ONLY`

不得覆盖 Task / Mathematical Review / Handoff / Frozen Source of Truth。

原始 FYQ/XXT/CYQ 互动优先保留在 GitHub Issue comment；IDEA 文件只整理当前综合认知、证据状态和待验证问题。

当前 Q1 IDEA：

- `Q1-IDEA-001`：两阶段 LP 与 MILP 结构验证；
- `Q1-IDEA-002`：Stage-2 `epsilon_cost` 容差与敏感性；
- `Q1-IDEA-003`：储能效率语义与敏感性；
- `Q1-IDEA-004`：R2 收口与 Final Freeze 前状态；
- `Q1-IDEA-005`：Blind Red Team 独立复算。

其中带有“Freeze 前状态”的历史 IDEA 仅作过程记录，不得用于覆盖当前 Q1 Frozen 状态。

调试垃圾文件仍不得进入本目录。正式结果进入论文继续遵循 Paper Handoff / Figure Review。

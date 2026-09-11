# 2026 CUMCM C题 Current State — 2026-09-11 R1

文档性质：`CURRENT_STATE_INDEX / NON-SOLVER-ARTIFACT`

本文件用于把当前聊天、任务包、Review 与 GitHub 中间结果重新对齐。正式事实优先级仍为：官方材料 → Frozen Source / current Mathematical Review → canonical workflow → current Task/Handoff。

## Q1

状态：

- `Q1_FINAL_EVIDENCE_GATE = PASS_WITH_LIMITATION`
- `Q1_MATHEMATICAL_PASS = TRUE`
- `Q1_TECHNICAL_PASS = TRUE`
- `Q1_HARD_CONSTRAINT_REPLAY = PASS`
- `Q1_METRICS_RECOMPUTED = TRUE`
- `Q1_FROZEN = TRUE`
- `RESULT1_FROZEN = TRUE`
- `Q1_PAPER_LOCKED = FALSE`

正式模型：`TWO_STAGE_CONTINUOUS_LP`。

正式 R2 delivery SHA256：`a8acd57687c9a2380ab089e14c23bfec467dca7882b51f7777c9f97ed4977058`。

Frozen result1 SHA256：`7aa49ebaeb506a25029c467cacd0c634138eda2f09e05e7527b287ae204cd964`。

详细数字与论文边界见同目录 `Q1/Q1_FROZEN_STATUS_R1.md`。旧 `Q1_词典序两阶段LP建模草稿_v0.1.md` 属于历史建模草稿，不得覆盖当前 Freeze。

## Q2

当前正式状态：

- `Q2_MATH_CONTRACT_ID = CUMCM2026_C_Q2_MATH_CONTRACT_R1`
- `Q2_FORMAL_MATH_SPEC = PASS_WITH_LIMITATION`
- `S1 = S1_A_PAID_UNUSED_NORMAL_ENERGY / APPROVED_WITH_LIMITATION`
- `Q2_IMPLEMENTATION_RELEASE = READY_AFTER_INPUT_BINDING`
- `Q2_FORMAL_RESULT = NOT_RUN`
- `Q2_MATHEMATICAL_RESULT_PASS = FALSE`
- `Q2_FROZEN = FALSE`

Merged PR #4 已建立 authority supplement request。PR #5 与 PR #6 分别恢复 XXT R1 authority 与 FYQ Controller review，目前仍为 Draft、未 merge。

Q2 full-year implementation 继续等待 current-version authority completion / input binding / execution release；不得因为 stable contract ID 已存在就跳过上述 Gate。

## Q3

正式结果尚未运行。当前仅允许 Question Contract / information-set / adjustment-accounting / validator preflight。

官方核心条件：每天 `0:00 / 6:00 / 12:00 / 18:00` 获得未来 24 h 整点 PV forecast；后续 forecast 可用于调整购电；下降部分按交易时刻电价 50% 违约口径，上升超出部分按交易时刻电价 1.5 倍；总费用还包含正常计划和紧急购电。

当前状态：`Q3_FORMAL_RESULT = NOT_RUN`，`Q3_FROZEN = FALSE`。

## Q4

正式建模/结果尚未开始。官方要求使用附件4波动电价，分别重算 Q2 与 Q3，对应 `result4-2.xlsx` 与 `result4-3.xlsx`。

当前仅允许接口与实验矩阵预设计；不得提前填正式结果。

当前状态：`Q4_FORMAL_RESULT = NOT_RUN`，`Q4_FROZEN = FALSE`。

## Open repository work

- PR #3：旧 Q1/Q2 working-idea 整理，当前内容包含已过期的 Q1 pre-Freeze 状态；在 reconciliation 前不建议直接 merge。
- PR #5：XXT Q2 authority restoration，Draft。
- PR #6：FYQ Q2 Controller restoration，Draft。

## Taskbooks

当前用户操作与 XXT 非 Astra 任务统一放在：

`支撑材料/03_中间结果/TASKS/`

昂贵计算线（Q2 full-year、alpha full replay、delayed-actual full replay）保留给后续 CYQ Codex/Astra 执行窗口，必须等待 FYQ execution release。
# CUMCM 2026 C题｜用户当前操作任务书 R0

- 角色：Human Coordinator / Repository Owner
- 日期：2026-09-11
- 目的：推进 Q2 authority 补件、XXT 复核与后续 CYQ Codex/Astra 执行
- 本任务不要求用户亲自改模型、写代码或裁决数学争议。

## 0. 当前状态

Q1 已完成技术与数学 Freeze：
- `Q1_FROZEN = TRUE`
- `RESULT1_FROZEN = TRUE`
- `Q1_PAPER_LOCKED = FALSE`

Q2 当前：
- `Q2_MATH_CONTRACT_ID = CUMCM2026_C_Q2_MATH_CONTRACT_R1`
- `Q2_FORMAL_MATH_SPEC = PASS_WITH_LIMITATION`
- `Q2_FORMAL_RESULT = NOT_RUN`
- `Q2_FROZEN = FALSE`
- merged PR #4 已要求补齐 XXT authority 与 FYQ Controller material。
- PR #5：XXT authority restoration，Draft。
- PR #6：FYQ Controller restoration，Draft。

## 1. 立即动作

### U1 — 把 XXT 任务包发给 XXT

发送：`CUMCM2026_XXT_NON_ASTRA_TASKS_R0.zip`。

要求 XXT 先做：
1. `XXT_Q2_AUTHORITY_COMPLETION_R0_TASK.md`
2. 再做 `XXT_Q3_CONTRACT_PREFLIGHT_R0_TASK.md`

不要要求 XXT 跑 Q2 全年正式求解；当前任务主要是数学 authority、validator 与 Q3 contract preflight，不需要 Astra。

### U2 — 暂时不要 merge PR #5 / #6

等待 XXT 回传 Q2 authority completion / review。

放行顺序：
1. XXT 明确 `PR5_MATH_AUTHORITY_REVIEW = PASS`；
2. FYQ 确认 PR #6 没有改变 XXT 数学合同；
3. 先 merge PR #5；
4. 再 merge PR #6。

如 GitHub 显示冲突、branch 落后或文件差异异常，停止 merge，把 PR 链接/截图回传 FYQ。

### U3 — 不要现在启动 Q2 全年 Astra

只有 FYQ 后续明确签发 `Q2_EXECUTION_RELEASE = RELEASED` 并给出 current main commit / authority chain 后，才把执行包交给 CYQ Codex/Astra。

执行窗口必须使用：`ACTIVE_ROLE = FYQ_TECHNICAL_ORCHESTRATOR`。

CYQ 的机器/API 所属不改变任务角色。

### U4 — CYQ Codex/Astra 回包后

第一接收方仍是 FYQ Controller，不直接送论文定稿。

顺序：
`CYQ Codex candidate delivery -> FYQ technical review -> XXT current-version Mathematical Review -> Evidence Gate -> Q2 Freeze -> Paper Handoff`

## 2. 当前不要做

- 不手工修改 Q1 Frozen 数字。
- 不把 PR #3 的旧 Q1/Q2 working ideas 直接 merge 到 main；其 Q1 状态已经落后于 Final Freeze。
- 不让 CYQ Paper 线自己补猜 Q2 数学参数。
- 不把当前 Q2 `PASS_WITH_LIMITATION` 写成结果 Mathematical PASS。
- 不提前填 result2 正式数字。

## 3. 用户需要回传 FYQ 的材料

完成任一项后直接回传：
- XXT 新 authority/review ZIP；
- PR #5/#6 的 review 状态；
- merge 后的 main commit SHA；
- CYQ Codex/Astra 的 Q2 candidate delivery ZIP；
- GitHub 冲突或异常截图。

## 4. 完成定义

本任务完成条件：
- XXT Q2 authority completion 已回传；
- PR #5/#6 的 merge 决策有明确 review evidence；
- Q2 执行窗口拿到唯一 current-version authority chain；
- 用户无需自行解释任何数学歧义。
# Q2 中间结果

本目录保存问题 2 的必要中间表、图、检验结果，以及已经形成具体技术含义、值得继续验证或进入论文的方法思路。

## 当前正式状态

当前执行链已经完成 FYQ Controller binding，候选执行已 release：

- `Q2_PREVALIDATION_SPEC = PASS`
- `Q2_EXECUTION_RELEASE = RELEASED`
- `Q2_FORMAL_RESULT = NOT_RUN`
- `Q2_MATHEMATICAL_RESULT_PASS = FALSE`
- `Q2_FROZEN = FALSE`

因此当前可以做正式 candidate execution / validation，但任何未经过 FYQ Technical Review → XXT Mathematical Review → Evidence Gate 的数字都不得作为 Frozen 或 Paper 正式事实。

当前 FYQ 执行接口位于：

`FYQ_CONTROLLER/`

当前 XXT repository authority 位于：

`XXT_AUTHORITY/`

Q2 Modeling Plan / Astra Core Engine 任务若尚未进入 main，应以对应当前 PR/branch 为准，不从聊天或旧 draft 推断。

## 当前协作规则

- GitHub Issue / PR comment 保存原始互动过程；
- 本目录 `Q2-IDEA-xxx_*.md` 保存当前综合思路；
- Task / Handoff / Mathematical Review / Controller Review / Frozen Source of Truth 保存正式采用事实。

IDEA 文件默认：

`AUTHORITY = WORKING_IDEA_ONLY`

当前 IDEA 包括：

- `Q2-IDEA-001`：00:00 日前承诺与因果日内储能 recourse；
- `Q2-IDEA-002`：计划购电过剩的 S1 paid-unused normal energy 处理；
- `Q2-IDEA-003`：5×紧急购电下的 Q80 风险余量 candidate。

这些 IDEA 只用于保留思路演化，不得覆盖 current mathematical contract、FYQ Controller 接口或后续 Frozen 结论。

只保留能够支撑后续模型、验证或正文结论的版本，不放调试垃圾文件。

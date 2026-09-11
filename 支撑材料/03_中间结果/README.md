# 03_中间结果：问题级思路与证据索引

本目录同时保存两类内容：

1. 能够支撑论文正文的必要中间表、图、检验结果；
2. FYQ / XXT / CYQ 在赛中形成的、已经足够具体到值得继续验证或写入论文的方法思路。

## 双轨协作约定

GitHub Issue comment 保存“讨论过程”：谁提出、谁质疑、谁回复、原始措辞和时间线。

本目录中的 `Q1/Q2/Q3/Q4` 保存“当前综合思路”：把多轮 comment、Task、Review 和实验汇总成一份可追踪的工作认知。

正式 Task / Handoff / Frozen Source of Truth 保存“最终采用事实”。

因此这里的 IDEA 文件默认：

`AUTHORITY = WORKING_IDEA_ONLY`

除非对应文件明确写明已进入 Frozen Handoff，否则不得把这里的内容当作正式冻结数字、正式模型或最终论文事实。

## IDEA 文件最小字段

每个具体思路建议独立成一个 Markdown 文件，至少包含：

- `IDEA_ID`
- `STATUS`
- `AUTHORITY`
- `OWNER`
- `CREATED_AT / LAST_UPDATED`
- 来源 comment / Task / Review
- 当前综合思路
- 当前证据
- 反对意见 / 未解决问题
- 下一步验证
- 团队当前决定
- 若最终采纳，进入哪个 Paper Handoff / Frozen Source

推荐状态：

- `OPEN`
- `UNDER_REVIEW`
- `ADOPTED_METHOD_NOT_FROZEN`
- `REJECTED`
- `SUPERSEDED`

## Comment 标签建议

为了便于后续 AI 使用记录和人工追踪，Issue comment 可使用：

- `[Q1_IDEA][Q1-IDEA-xxx][FYQ/CYQ/XXT]`
- `[Q1_REPLY][Q1-IDEA-xxx][FYQ/CYQ/XXT]`
- `[Q1_MATH_REVIEW][Q1-IDEA-xxx][XXT]`

最终 AI Use Ledger 仍需单独记录 `human_verification / team_decision / human_changes / paper_location / artifact`，不能仅凭 comment 自动视为已披露完成。

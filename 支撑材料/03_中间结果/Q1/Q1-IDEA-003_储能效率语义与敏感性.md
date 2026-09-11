# Q1-IDEA-003 储能效率语义与敏感性

- IDEA_ID: Q1-IDEA-003
- STATUS: ADOPTED_METHOD_NOT_FROZEN
- AUTHORITY: WORKING_IDEA_ONLY
- OWNER: XXT / FYQ
- CREATED_AT: 2026-09-11
- LAST_UPDATED: 2026-09-11

## 来源互动与 Review

Issue #1 comment 5628455508 已根据 XXT/Astra Mathematical Review 更新效率语义：primary 为 `eta_c = eta_d = 0.9`，mandatory sensitivity 为 `eta_c = eta_d = sqrt(0.9)`。

Comment: https://github.com/ravenclawrowena869-art/2026_CUMCM/issues/1#issuecomment-5628455508

Q1 Blind Red Team 已独立复算两套效率语义，并与当前正式 candidate 的成本和 SOC sensitivity 指标匹配。

## 当前综合思路

题面“充放电效率 90%”存在两种合理解释：充电效率和放电效率分别为 0.9；或往返效率整体为 0.9，因此两侧取 `sqrt(0.9)`。

主模型采用 `eta_c = eta_d = 0.9`。第二种解释保留为必须运行的一因素敏感性。

## 当前证据

两种解释会对成本和 SOC 轨迹产生可见差异。当前 Review 与 Blind Red Team 均支持 alternative 会降低候选调度成本，最大点态 SOC 差约 623 kWh 量级，因此效率语义属于 material modeling assumption。

## 风险

不得写成“90%效率怎样解释结果都一样”；不得把 alternative 当成第二套长期主模型；sensitivity 数字在 Q1 最终 Freeze 前仍属于候选证据。

## 当前团队决定

采用 `0.9 / 0.9` 作为主解释，`sqrt(0.9) / sqrt(0.9)` 作为 mandatory one-factor sensitivity。

## Graduation

Q1 FINAL Paper Handoff → 模型假设 + 敏感性分析。

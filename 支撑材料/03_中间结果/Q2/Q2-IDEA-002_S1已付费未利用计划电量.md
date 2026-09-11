# Q2-IDEA-002 S1：已付费但未利用的计划购电余量

- IDEA_ID: Q2-IDEA-002
- STATUS: UNDER_REVIEW
- AUTHORITY: WORKING_IDEA_ONLY
- OWNER: FYQ / XXT
- CREATED_AT: 2026-09-11
- LAST_UPDATED: 2026-09-11

## 来源

XXT/Astra 在 Q2 Formal Optimization Spec R1 中提出：如果 0:00 已经锁定计划购电，而执行时负荷降低、光伏增加且电池已接近上界，在禁止售电的前提下，计划购电可能出现没有物理去向的可行性问题。

FYQ Controller 重新核对官方题面后，批准 S1-A，并明确它属于：

`MODELING_COMPLETION_ASSUMPTION`

而不是官方明确规定。

## 当前综合思路

定义：

- `q_committed >= 0`：00:00 锁定的计划购电量；
- `w >= 0`：已经计划、已经计费，但执行时未被负荷或储能利用的正常购电余量；
- `0 <= w <= q_committed`；
- 实际进入能量平衡的正常购电量为 `q_committed - w`。

经济口径：

- 正常购电费用仍按全部 `q_committed` 计；
- `w` 不退款；
- `w` 不产生售电收入；
- `w` 与 PV 弃光分开统计。

## 为什么需要它

官方明确“其他时间段的购电费用均按计划购电量计算”，但没有说明计划购电过多时的退款、售电或强制吸收机制。

若强制所有计划电量都物理进入微网，同时禁止售电和一般 dump，在 SOC 上界、低负荷、PV 过剩等情形可能导致人为不可行。

S1-A 是目前最小、可审计、不会获得退款收益的模型补全。

## 风险与限制

正式结果必须报告：

- `sum(w)`；
- `sum(p*w)`；
- `w / sum(q_committed)`；
- `w>0` 的槽数和天数；
- 最大单槽 / 单日 `w`；
- `w` 与 risk-aware candidate 的关系。

如果策略大量依赖 `w` 才取得优势，必须在论文中显式限制解释，并考虑更严格的可行子集 / 吸收约束 counterfactual。

## 当前团队决定

`S1_A_PAID_UNUSED_NORMAL_ENERGY = APPROVED_WITH_LIMITATION`

但 Q2 正式全年 run 尚未开始，不能提前判断该假设在实际结果中是否 material。

## Graduation

Q2 full replay 后，根据 `w` 使用规模决定是否进入正式 Paper Handoff，以及是否需要补结构 counterfactual。

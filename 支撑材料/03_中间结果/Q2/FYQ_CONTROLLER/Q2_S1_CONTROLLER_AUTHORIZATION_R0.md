# Q2 S1 Controller Authorization R0

日期：2026-09-11
ACTIVE_ROLE=`FYQ_TECHNICAL_ORCHESTRATOR`

## 1. Official wording checked

FYQ 本轮重新读取官方 C题。

Q2 明确：
- 微网提供电能不可低于负载；
- 低于负载时需要按交易时刻电价 5 倍紧急购电；
- “除紧急购电费用外，其他时间段的购电费用均按计划购电量计算”。

官方没有给出售电价格，也没有明确规定“计划购电量高于实际可利用电量”时的退款、回购或强制物理吸收机制。

## 2. S1 adjudication

批准 XXT R1 推荐的 `S1-A`，但把它明确标记为：

`MODELING_COMPLETION_ASSUMPTION`

而不是官方原文事实。

冻结语义：

- `q_committed >= 0`：00:00 锁定的正常计划购电量；
- 正常费用始终按 `p * q_committed` 全额计；
- `w >= 0`：已计划且已计费、但未被负荷/储能利用的正常购电余量；
- `0 <= w <= q_committed`；
- 实际进入能量平衡的正常电量为 `q_committed - w`；
- `w` 不退款、不产生售电收入，不得记为 PV 弃光；
- PV 弃光单独记为 `v`；
- 禁止通过负购电量实现售电。

这与 XXT 的 `S1-A` 数学形式一致。

## 3. Why accepted

若坚持 `w=0` 且禁止售电/一般 dump，在 SOC 上界、低负荷、PV/计划电量过剩等槽位，固定日前 commitment 可能产生无物理出口的不可行状态。

官方又要求正常费用按计划购电量计算，因此把“计划 commitment 的经济结算”和“实际被微网利用的电量”分开，是当前最小、可审计、不会获得退款收益的模型补全。

## 4. Required limitation/evidence

该假设不是官方显式给定，正式结果必须额外报告：

- `sum(w)`；
- `sum(p*w)` 作为已付费但未利用计划电量的费用规模；
- `w / sum(q_committed)`；
- `w>0` 的槽数和天数；
- 最大单槽 / 单日 `w`；
- `w` 与 risk-aware candidate 的关系。

如果正式策略大量依赖 `w` 才可行或才取得优势，不能只隐藏在 balance 变量中；必须作为结构假设敏感点解释，必要时回到 XXT 做 `S1-B` 可行子集/吸收约束 counterfactual。

## 5. Status

`normal_purchase_surplus_mode = S1_A_PAID_UNUSED_NORMAL_ENERGY`

`S1_CONTROLLER_AUTHORIZATION = PASS_WITH_LIMITATION`

本授权只解除数学合同的 S1 release blocker，不授予任何 Q2 正式结果 PASS/FREEZE。

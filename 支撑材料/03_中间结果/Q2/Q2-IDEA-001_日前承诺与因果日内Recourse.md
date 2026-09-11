# Q2-IDEA-001 日前承诺与因果日内 Recourse

- IDEA_ID: Q2-IDEA-001
- STATUS: UNDER_REVIEW
- AUTHORITY: WORKING_IDEA_ONLY
- OWNER: XXT / FYQ
- CREATED_AT: 2026-09-11
- LAST_UPDATED: 2026-09-11

## 来源互动与 Review

Issue #1 comment 5621499565 首先指出论文表述存在 future-actual leakage 风险：0:00 制定 normal purchase 时不能读取当天未来 actual。

Comment: https://github.com/ravenclawrowena869-art/2026_CUMCM/issues/1#issuecomment-5621499565

随后 XXT/Astra 完成 `CUMCM2026_C_Q2_MATH_CONTRACT_R1`，FYQ Controller 将其审为 `Q2_FORMAL_MATH_SPEC = PASS_WITH_LIMITATION`。

## 当前综合思路

Q2 采用两层因果结构：

1. 每天 0:00 锁定当天 normal purchase commitment；
2. 执行过程中，只允许使用当时已经发生、已经可得的信息做 intraday storage recourse 和 emergency balance。

因此未来实际负荷与未来实际光伏不能进入 0:00 的决策。

当前正式设计包含：

- `POINT_DA_LP_R1`：00:00 日前购电承诺；
- `Q2_RH_FIXED_Q_LP_R1`：固定日前 q 的因果日内储能控制；
- `DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE`：必须保留的 baseline。

## 当前证据

数学合同已明确 known_at 边界、5× emergency accounting、跨日 SOC、terminal sensitivity 和 independent validator contract。

## 未解决问题

- 当前数学合同允许右端点 actual 用于本槽 storage action；Freeze 前需要 `ONE_SLOT_DELAYED_ACTUAL` sensitivity / counterfactual；
- 24h daily truncation 可能在日末产生边界效应，需要正式 run 后检查；
- Q2 还没有运行正式全年结果，因此不能称为 Q2 Result PASS 或 Frozen。

## 当前团队决定

保留“00:00 commitment + causal intraday recourse”作为 Q2 主结构。正式 implementation 暂待 Q1 收口后释放。

## Graduation

Q2 implementation + replay + Mathematical Review 通过后，进入 Q2 Paper Handoff。

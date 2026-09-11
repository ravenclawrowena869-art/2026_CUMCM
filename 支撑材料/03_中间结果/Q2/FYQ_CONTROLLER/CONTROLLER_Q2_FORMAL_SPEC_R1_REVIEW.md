# FYQ Controller Review — XXT Q2 Formal Optimization Spec R1

## Integrity

Input:
`CUMCM2026_C_XXT_Q2_FORMAL_OPT_SPEC_R1_DELIVERY.zip`

- SHA256: `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`
- ZIP CRC: PASS
- top-level internal SHA256SUMS: 23/23 PASS
- stable ID: `CUMCM2026_C_Q2_MATH_CONTRACT_R1`

## Controller adjudication

XXT 本轮完成了任务要求的主要数学合同：

- Q2 fixed Attachment1 tariff；
- 00:00 normal commitment；
- current/past actual 与 future forecast 的 known_at 边界；
- `POINT_DA_LP_R1`；
- `Q2_RH_FIXED_Q_LP_R1` causal intraday controller；
- `DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE` baseline；
- `SIGNED_RESIDUAL_Q80_MARGIN_R1` risk-aware candidate；
- 5× emergency accounting；
- cross-day SOC；
- FREE/T1/T2 annual terminal；
- efficiency primary + sensitivity；
- risk parameter provenance；
- 18项 independent validator contract；
- W1 baseline-family causality adjudication。

风险分位 `alpha=0.8` 的解析锚点成立：
`J(q)=p q + 5p E[(N-q)+]`
给出边际条件 `F(q)=0.8`。
该推导只支持无储能单槽锚点；XXT 已正确限制其 Claim，不把它冒充全年带储能最优证明。

## S1

XXT 唯一 release blocker 是正常计划购电过剩的物理出口。

FYQ 本轮重新读取官方题面后批准：
`S1_A_PAID_UNUSED_NORMAL_ENERGY`

详见：
`Q2_S1_CONTROLLER_AUTHORIZATION_R0.md`

该项是 modeling-completion assumption，必须单独报告 `w` 使用规模，不得写成官方明确规定。

## Additional evidence requirements before Q2 Freeze

这些不阻止实现，但必须在正式 Freeze 前关闭：

1. **current-slot actual timing sensitivity**  
   当前合同允许右端点 actual 用于本槽 storage action。作为离散控制假设可以实现，但至少增加一个 `ONE_SLOT_DELAYED_ACTUAL` sensitivity / counterfactual，检查成本、emergency 与 SOC 结论是否被同槽信息优势 materially 改变。

2. **24h truncation tail diagnostic**  
   每日规划没有跨日 salvage value。正式 run 必须报告日末若干槽、次日开头的 emergency/SOC 统计；若出现明显 boundary artifact，再决定是否需要延长 horizon challenger。不要先机械扩模型。

3. **S1 usage audit**  
   按授权文件统计 `w`。若策略优势主要来自大量 paid-unused commitment，论文必须限制解释。

4. **risk alpha neighborhood replay**  
   按 XXT 协议重新规划并全期 replay `alpha=.75/.80/.85` 及有效秩邻域；不得在旧轨迹上重算。

5. **full provenance/input binding**  
   正式实现前绑定 W2 full forecast bytes、Attachment1 tariff hash、R14 bridge bytes、baseline preregistration evidence、官方表3日期和 result2 模板。

## Status

`Q2_MATH_CONTRACT_ID = CUMCM2026_C_Q2_MATH_CONTRACT_R1`

`Q2_FORMAL_MATH_SPEC = PASS_WITH_LIMITATION`

`Q2_IMPLEMENTATION_RELEASE = READY_AFTER_INPUT_BINDING`

`Q2_FORMAL_RESULT = NOT_RUN`

`Q2_MATHEMATICAL_RESULT_PASS = FALSE`

`Q2_FROZEN = FALSE`

为避免论文线认为技术线跳问，当前不立即派发 full-year Q2 implementation。先让 Q1 Blind Red Team + Q1 R2 收口；同时可以准备 Q2 input-binding package，不运行正式年度结果。

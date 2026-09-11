# Q1-IDEA-001 两阶段连续 LP 与 MILP 结构验证

- `IDEA_ID`: `Q1-IDEA-001`
- `STATUS`: `ADOPTED_METHOD_NOT_FROZEN`
- `AUTHORITY`: `WORKING_IDEA_ONLY`
- `OWNER`: `FYQ / XXT`
- `CREATED_AT`: `2026-09-11`
- `LAST_UPDATED`: `2026-09-11`

## 来源互动与证据

- Issue #1 comment `5628106032`：FYQ 发布 Q1 Mathematical Review 状态更新。
- Issue #1 comment `5628455508`：论文一致性巡检根据新 authority 更新 Q1 方法边界。
- XXT/Astra：`Q1_CURRENT_VERSION_MATH_PASS_WITH_ENGINEERING_HOLD`。
- FYQ Controller：接受 `LP_SUFFICIENT_MILP_AS_STRUCTURAL_VALIDATION`。
- Q1 Blind Red Team：独立复算再次得到 LP / MILP Stage-1 objective 一致、MILP gap=0、LP simultaneous C/D=0。

Comment：
- https://github.com/ravenclawrowena869-art/2026_CUMCM/issues/1#issuecomment-5628106032
- https://github.com/ravenclawrowena869-art/2026_CUMCM/issues/1#issuecomment-5628455508

## 当前综合思路

Q1 的主要决策量均为连续电量 / SOC，核心目标与约束可保持线性，因此正式主模型采用连续 LP。

为避免线性模型存在多组经济目标几乎等价、但储能轨迹不够简洁的退化解，采用词典序两阶段结构：

1. Stage 1 最小化全天购电费用；
2. Stage 2 在 Stage-1 最优费用的极小 cost-preserving tolerance 内最小化总充放电 throughput。

同时建立只增加充/放电互斥二元变量的 MILP challenger，其余数据、效率、目标和 hard constraints 保持一致。

## 当前证据

当前独立数学复核与 Blind Red Team 均支持：

- LP 与 mutex MILP 的 Stage-1 最优购电费用一致；
- MILP MIP gap = 0；
- LP 当前最优解没有实质性的同时充放电；
- 引入互斥 binary 没有获得目标值或可行性增益。

因此当前方法裁决：

`Q1_PRIMARY_MODEL = TWO_STAGE_CONTINUOUS_LP`

`MILP_ROLE = STRUCTURAL_VALIDATION_ONLY`

## 反对意见 / 风险

- 不能用“别人常用 MILP”或“为了创新不用 MILP”作为模型选择依据；
- Stage 2 的 tolerance 需要单独证明不是任意常数，见 `Q1-IDEA-002`；
- 当前方法已通过 Mathematical Review，但 Q1 尚未最终 Frozen。

## 下一步

- 等待 Q1 R2 epsilon exact-environment sensitivity；
- 完成 FYQ Final Evidence Gate；
- Freeze 后将该模型选择逻辑写入正式 Q1 Paper Handoff。

## 当前团队决定

保留连续 LP 作为正文主模型；MILP 仅作为结构交叉验证证据，不维护第二套长期主模型。

## Graduation

若最终 Freeze 无 P0：

`Q1 FINAL Paper Handoff → 模型选择 / 求解流程 / 验证证据`

# Q1-IDEA-002 Stage-2 `epsilon_cost` 容差与敏感性

- `IDEA_ID`: `Q1-IDEA-002`
- `STATUS`: `UNDER_REVIEW`
- `AUTHORITY`: `WORKING_IDEA_ONLY`
- `OWNER`: `FYQ / CYQ`
- `CREATED_AT`: `2026-09-11`
- `LAST_UPDATED`: `2026-09-11`

## 来源互动

CYQ 在 Issue #1 comment `5628557368` 指出：`epsilon_cost=1e-4 CNY` 不能解释成求解器自身 numerical tolerance，应视为人为设置的 cost-preserving tolerance，并建议做数量级敏感性。

FYQ 在 comment `5628673718` 接受该问题为 `P1_EVIDENCE_GAP`，完成一次独立 controller cross-check，并下发 exact-environment confirmatory sensitivity。

Q1 Post-Closeout R2 随后完成 exact-environment fresh sweep，并由 FYQ Controller 再次 fresh 复核。

Comment：
- https://github.com/ravenclawrowena869-art/2026_CUMCM/issues/1#issuecomment-5628557368
- https://github.com/ravenclawrowena869-art/2026_CUMCM/issues/1#issuecomment-5628673718

## 当前综合思路

Stage 2 的 `epsilon_cost` 用于允许在 Stage-1 经济最优值附近，从近似等价的轨迹中选择 throughput 更小、解释更干净的调度方案。

因此论文不能把 `1e-4 CNY` 写成“求解器误差”。准确语义为：

`人为设定的极小 cost-preserving tolerance`

正式默认继续使用：

`epsilon_cost = 1e-4 CNY`

本轮 sensitivity 用来验证该设计是否处在稳定区间，不把 retrospective sweep 伪装成事前参数最优化，也不声称 `1e-4` 是数学意义上的最优 epsilon。

## exact-environment sensitivity 证据

Q1 R2 在正式执行环境 fresh 重新求解：

`epsilon ∈ {1e-6,1e-5,1e-4,1e-3,1e-2} CNY`

五个点全部满足：

- Stage-1 optimum 不变；
- Stage-2 cost gap 满足各自 epsilon cap；
- hard-constraint replay PASS；
- simultaneous charge/discharge = 0；
- SOC 始终在 `[1200,10800] kWh`；
- 六个指定购电时段相对 `1e-4` 均无变化。

相对 `1e-4`：

- `1e-6` 至 `1e-3` 最大 SOC 差约 `0.0100847869 kWh`；
- `1e-6` 至 `1e-3` 最大 4h 聚合差约 `0.0112053188 kWh`；
- `1e-2` wider stress 最大 SOC 差约 `0.1109326561 kWh`；
- `1e-2` 最大 4h 聚合差约 `0.1232585068 kWh`；
- `1e-2` 的指定购电时段差仍为 `0`；
- 未发现会改变 Q1 正文结论的 material reversal。

FYQ Controller cross-check 与 exact-environment 返回结果在公共数值字段上的最大差约 `7.3e-12`。

## 参数证据裁决

当前证据支持：

`1e-4 CNY` 位于本次测试得到的稳定 plateau 内，可以作为 Stage-2 的固定数值设计继续使用。

当前不支持：

- `1e-4` 是“最优 epsilon”；
- `1e-4` 来源于求解器自身 numerical tolerance；
- 官方题目规定了某个货币最小结算精度，因此必须取 `1e-4`。

因此论文推荐写成：

> 第二阶段在第一阶段最优购电费用附近设置极小的 cost-preserving tolerance，并在该容差内最小化储能充放电总量。数量级敏感性结果表明，在所检验区间内核心调度结论保持稳定，因此本文采用 `1e-4 CNY` 作为固定的二阶段数值容差。

正式写作时仍应根据篇幅调整，不要把这段扩写成“epsilon 全局最优性证明”。

## 当前未解决项

- Q1 尚未进入最终 Freeze；
- final controller Freeze Manifest / provenance closure 尚待完成；
- AI/human adoption 与来源 limitation 仍需按最终 Gate 闭合。

## 当前团队决定

- 保留 `epsilon_cost=1e-4 CNY`；
- sensitivity evidence 已具备，可进入后续 Q1 Paper Handoff；
- 不改变正式 Q1 模型和 result1；
- 在 Q1 Freeze 前继续保持 `WORKING_IDEA_ONLY`。

## Graduation

若 Q1 Final Evidence Gate 通过：

`Q1 FINAL Paper Handoff → 参数/数值设计说明 + epsilon sensitivity evidence`

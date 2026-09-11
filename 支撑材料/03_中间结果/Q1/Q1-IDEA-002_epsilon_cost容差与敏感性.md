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

Comment：
- https://github.com/ravenclawrowena869-art/2026_CUMCM/issues/1#issuecomment-5628557368
- https://github.com/ravenclawrowena869-art/2026_CUMCM/issues/1#issuecomment-5628673718

## 当前综合思路

Stage 2 的 `epsilon_cost` 只是为了允许在 Stage-1 经济最优值附近，从近似等价的轨迹中选择 throughput 更小、解释更干净的调度方案。

因此论文不能把 `1e-4 CNY` 写成“求解器误差”。更准确的语义是：

`人为设定的极小 cost-preserving tolerance`

当前正式默认值仍为：

`epsilon_cost = 1e-4 CNY`

但该值进入最终论文前需要邻域/数量级稳定性证据。

## 当前证据

FYQ Controller 已先做独立 cross-check：

`epsilon ∈ {1e-6,1e-5,1e-4,1e-3,1e-2} CNY`

观察到：

- 各点 Stage-1 objective 不变；
- Stage-2 cost gap 与各自 epsilon 对应；
- simultaneous charge/discharge 均为 0；
- SOC 保持 hard-feasible；
- `1e-6` 至 `1e-3` 范围内关键 Q1 结论未发生 material reversal；
- `1e-2` 作为更宽 stress 点单独报告，不据此更改默认值。

该 cross-check 运行环境与正式 Windows frozen solver 环境不同，因此只能作为辅助证据。

## 未解决问题

- exact-environment sensitivity 尚待 Q1 R2 fresh 复跑；
- 不能把这轮 retrospective sweep 伪装成事前参数搜索；
- 官方题面没有给出最小货币结算单位，所以论文不要写“远低于官方结算精度”这类无来源 Claim。

## 下一步验证

Q1 R2 在正式执行环境重新求解：

`{1e-6,1e-5,1e-4,1e-3,1e-2}`

逐点检查费用、throughput、SOC、4h 聚合、关键时段和 hard constraints。

## 当前团队决定

在 exact-environment sensitivity 回来前：

- 默认 `1e-4` 不修改；
- 写作只称其为人为 cost-preserving tolerance；
- 不声称它已被证明是“最优 epsilon”。

## Graduation

若 R2 证据稳定：

`Q1 FINAL Paper Handoff → 参数/数值设计说明 + sensitivity evidence`

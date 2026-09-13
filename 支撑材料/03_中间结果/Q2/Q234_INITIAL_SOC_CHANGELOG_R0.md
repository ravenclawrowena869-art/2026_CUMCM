# Q2–Q4 2月1日初始 SOC 修订变更记录 R0

本轮只修订 Q2–Q4 的 formal-start 初始化语义，不修改 Q1 Frozen 数字，不生成新的 Q2/Q3/Q4 正式费用。

## 变更

- 将 `2025-02-01 00:00 SOC = 6000 kWh` 明确为模型假设，而非题目直接事实；
- January primary 角色改为 causal forecast/residual history，不再通过 Jan31 replay 强制推导 primary Feb1 SOC；
- Q2 input binding 升级至 R2；
- Q2 implementation interface 升级至 R3；
- Q3/Q4 current status 继承统一初始化假设；
- 新增 4000/6000/8000 kWh 单因素 sensitivity protocol；
- 新增论文安全表述 handoff。

## 未变更

- Q1；
- Q2 S1 accounting；
- Q2 risk/recourse/forecast contract；
- 2月1日以后 SOC 不按日重置；
- Q2–Q4 terminal semantics；
- Q3 adjustment accounting；
- Q4 dynamic-price semantics。

## 结果状态

`FORMAL_INITIAL_SOC_SENSITIVITY = PENDING_CURRENT_FULL_YEAR_ENGINE`

原因：current main authority 显示 Q2/Q3/Q4 formal full-year result 尚未完成，当前可用 evidence 不足以诚实生成 4000/6000/8000 的正式全年数字。协议已就绪，待 current full-year engine/result package 可执行时直接补跑。

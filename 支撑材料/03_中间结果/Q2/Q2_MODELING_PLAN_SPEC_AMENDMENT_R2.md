# CUMCM 2026 C题 Q2 建模计划定点修订 R2

> Amendment ID: `CUMCM2026_C_Q2_MODELING_PLAN_AMENDMENT_R2_20260913`  
> Upstream: `CUMCM2026_C_Q2_MODELING_PLAN_FREEZE_R1_20260911`  
> Scope: `FEB1_INITIAL_SOC_ONLY`  
> Status: `AMENDMENT_ACCEPTED / RESULT_NOT_RUN`

## 0. 修订原则

R1 冻结计划作为历史 provenance 保留，不直接覆盖、不删除。

本 R2 仅修订一个已发现的初始化语义问题：R1 将 January 同时作为 causal warm-up 与 Jan31→Feb1 SOC state bridge，并要求正式执行绑定 bridge artifact；但题目只直接给出 `2025-01-01 00:00 = 6000 kWh`，并没有直接给出 2 月 1 日 SOC。

经 Controller 决定，2 月 1 日的 6000 kWh 统一改为**明确的模型假设**，而不是通过 January storage replay 强制推导。

## 1. 被修订条款

R1 中以下要求在 primary execution 中被本 R2 supersede：

- `January：仅作为 causal warm-up 与 Jan31→Feb1 状态桥接` 中的“状态桥接”部分；
- 正式执行前必须绑定 `Jan31→Feb1 SOC bridge artifact SHA256`；
- 任何“2月1日初始 SOC 必须从1月31日最终 replay state 读取”的 execution binding。

## 2. 新 primary 条款

Q2 formal period 仍为：

`2025-02-01..2025-12-31`

primary 初始状态统一为：

`E(2025-02-01 00:00) = 6000 kWh`

分类：

`REASONABLE_MODELING_ASSUMPTION`

不是：

`OFFICIAL_DIRECTLY_STATED_FACT`

January 的 primary 角色改为：

`CAUSAL_FORECAST_AND_RESIDUAL_HISTORY`

即 1 月真实历史仍可按 known_at 规则用于 2 月 1 日及之后的预测/残差历史，但不再承担 primary SOC 初始化推导。

## 3. 不变条款

R1 中除上述初始化语义外的内容保持不变，包括但不限于：

- 10 min 时间尺度；
- Q1 Frozen battery physics；
- `NO_DAILY_RESET` 的 2–12 月跨日 SOC 连续性；
- `FREE_BOUNDED_YEAR_END` primary terminal；
- Q2 forecast/risk/recourse/S1 accounting；
- known_at / future leakage；
- validator、result2 writer、delayed-actual、risk-alpha、terminal、efficiency、24h-tail 等证据要求。

注意：`NO_DAILY_RESET` 从 2 月 1 日 formal start 后一直有效；本修订不是允许每天重置 SOC。

## 4. 新增 Gate

由于 Feb-1 SOC=6000 为人为模型假设，Final Paper/Figure Gate 前必须按：

`XXT_AUTHORITY/XXT_Q234_INITIAL_SOC_SENSITIVITY_PROTOCOL_R0.md`

至少比较 4000 / 6000 / 8000 kWh 三组单因素场景，并检查主要费用、紧急购电、全路径 SOC 可行性和策略/论文结论是否改变。

正式敏感性结果未跑出前，不允许写“初始 SOC 对结果影响很小”。

## 5. Execution binding

当前执行应读取：

- `FYQ_CONTROLLER/Q2_IMPLEMENTATION_INTERFACE_R3.json`
- `FYQ_CONTROLLER/Q2_INPUT_BINDING_R2.json`
- `XXT_AUTHORITY/XXT_Q234_FEB1_INITIAL_SOC_ASSUMPTION_R0.md`
- `XXT_AUTHORITY/XXT_Q234_INITIAL_SOC_SENSITIVITY_PROTOCOL_R0.md`

历史 R1/R2 文件仅作为 provenance 保留；若初始化条款冲突，以本 R2 amendment 为准。

## 6. 影响范围

- Q1：无影响，不重开、不重跑；
- Q2：初始化语义修订；正式结果尚未在 current main 冻结；
- Q3：继承同一 Feb-1=6000 模型假设；
- Q4：Q2-style / Q3-style 两条分支均继承同一初始假设。

本修订不自行宣布任何 Q2/Q3/Q4 正式结果或 Freeze。

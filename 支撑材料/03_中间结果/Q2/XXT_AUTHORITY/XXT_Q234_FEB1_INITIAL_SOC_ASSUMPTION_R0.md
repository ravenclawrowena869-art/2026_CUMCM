# Q2–Q4 2月1日初始 SOC 统一模型假设 R0

> Contract ID: `Q234_FEB1_INITIAL_SOC_ASSUMPTION_R0`  
> Date: 2026-09-13  
> Type: `CONTROLLER_DECISION / MODELING_ASSUMPTION`  
> Scope: Q2、Q3、Q4 共同初始化口径  
> Result impact at this commit: `NO_FORMAL_RESULT_REPLACEMENT`

## 1. 官方事实与模型假设必须分开

题目明确给出的储能初值是：

- `2025-01-01 00:00` 储电量为 `6000 kWh`。

题目并未直接规定：

- `2025-02-01 00:00` 储电量为 `6000 kWh`。

因此，今后任何代码说明、数学合同、论文和图表说明中，均不得把“2月1日初始 SOC=6000 kWh”写成题目直接给定。

## 2. Controller 统一决定

Q2–Q4 的 primary 正式计算统一采用：

`E(2025-02-01 00:00) = 6000 kWh`

其性质为：

`REASONABLE_MODELING_ASSUMPTION`

不是：

`OFFICIAL_DIRECTLY_STATED_FACT`

采用该假设的目的，是使 Q2、Q3、Q4 从同一储能状态起点进行公平比较，并避免把题目仅给出的 1 月 1 日初值错误搬运为“官方 2 月 1 日初值”。

## 3. 对 January 的含义

在本 primary contract 下：

- 1 月数据仍可作为 2 月 1 日及后续预测所需的 causal 历史信息；
- 1 月不再承担“通过储能运行轨迹推导 2 月 1 日初始 SOC”的 primary state-bridge 职责；
- 不允许为了让 1 月末 SOC 恰好回到 6000 kWh 而反向设计 1 月储能动作；
- 若后续另做 January physical bridge，只能作为 alternative sensitivity / diagnostic，不得静默替代本 primary assumption。

因此，本文件对旧 Q2 计划中“Jan31→Feb1 SOC bridge artifact 为正式执行必需输入”的要求形成**定点修订**：该项在 primary run 中改为 `NOT_REQUIRED_BY_PRIMARY_INITIALIZATION_CONTRACT`。

除这一初始化口径外，旧 Q2 计划和既有 Q2/Q3/Q4 数学合同的其他冻结/已接受内容不因本文件自动重开。

## 4. 跨问题继承关系

### Q2

正式区间从 2 月 1 日开始时，以 `6000 kWh` 作为初始 SOC。

### Q3

Q3 在 Q2 机制基础上重新进行同一正式区间的计算。Q3 继承同一初始 SOC 假设，不继承 Q2 的年末 SOC，也不把 Q2 的全年运行当作 Q3 的前置物理轨迹。

### Q4

Q4 在动态电价下分别重算 Q2-style 与 Q3-style 策略，两条分支均使用同一 `6000 kWh` 初始 SOC，保证价格机制比较的起点一致。

## 5. 论文允许表述

建议正文写法：

> 题目仅给定 2025 年 1 月 1 日 0:00 的储能电量为 6000 kWh。由于第 2–4 问的正式结果统计自 2 月 1 日开始，为统一不同策略的初始运行状态，本文假设 2 月 1 日 0:00 的储能电量为 6000 kWh，并通过初始 SOC 敏感性分析检验该设定对主要结论的影响。

禁止写法：

> 题目规定 2 月 1 日初始储电量为 6000 kWh。

## 6. Gate 要求

由于该值属于人为设定，正式 Paper/Figure Gate 前必须至少完成一次初始 SOC sensitivity，并保存：

- 运行配置与 solver/version；
- 不同初始 SOC 的正式同口径结果；
- total cost / emergency cost / emergency energy；
- SOC 全路径可行性与跨日连续性；
- 策略排序或核心结论是否改变；
- 结果来源链与文件哈希。

具体 protocol 见同目录：

`XXT_Q234_INITIAL_SOC_SENSITIVITY_PROTOCOL_R0.md`

## 7. 当前状态

`ASSUMPTION_CONTRACT = ACCEPTED`

`Q1_IMPACT = NONE`

`Q2_Q3_Q4_PRIMARY_INITIAL_SOC = 6000 kWh`

`INITIAL_SOC_SENSITIVITY = REQUIRED_BEFORE_FINAL_PAPER_CLAIM`

本文件不自行宣布 Q2/Q3/Q4 Frozen，也不生成新的正式费用数字。
# Q2–Q4 2月1日初始 SOC 论文交接 R0

## 正文建议表述

> 题目仅给定 2025 年 1 月 1 日 0:00 的储能电量为 6000 kWh。由于第 2–4 问的正式结果统计自 2 月 1 日开始，为统一不同策略的初始运行状态，本文假设 2 月 1 日 0:00 的储能电量为 6000 kWh，并通过初始 SOC 敏感性分析检验该设定对主要结论的影响。

## 禁止表述

不得写：

> 题目规定 2 月 1 日初始储电量为 6000 kWh。

也不得在敏感性正式跑完前写：

> 初始 SOC 对结果影响很小 / 结果对初值稳健。

## 一致性要求

- Q2、Q3、Q4 均使用同一 primary 初始 SOC = 6000 kWh；
- Q3 不继承 Q2 年末 SOC；
- Q4 的 Q2-style 与 Q3-style 分支从相同初始 SOC 出发；
- 4000/6000/8000 kWh sensitivity 的实际结果出来后，再补充稳健性结论和对应表/图；
- 若 sensitivity 改变策略排序或主要结论，必须回到模型/论文 Gate 重新审查，不得只改一句文字。

Authority：

- `XXT_AUTHORITY/XXT_Q234_FEB1_INITIAL_SOC_ASSUMPTION_R0.md`
- `XXT_AUTHORITY/XXT_Q234_INITIAL_SOC_SENSITIVITY_PROTOCOL_R0.md`
- `Q2_MODELING_PLAN_SPEC_AMENDMENT_R2.md`

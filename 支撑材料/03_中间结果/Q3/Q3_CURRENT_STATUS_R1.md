# Q3 Current Status R1

> Supersedes: `Q3_CURRENT_STATUS_R0.md` for current-status navigation.  
> Date: 2026-09-13

状态：`CONTRACT_PREFLIGHT_ONLY / FORMAL_RESULT_NOT_RUN`

## Shared initialization contract

Q3 正式计算继承 Q2–Q4 统一初始化假设：

`E(2025-02-01 00:00) = 6000 kWh`

该值是 `REASONABLE_MODELING_ASSUMPTION`，不是题目直接给定。

Authority：

`../Q2/XXT_AUTHORITY/XXT_Q234_FEB1_INITIAL_SOC_ASSUMPTION_R0.md`

Q3 是在相同正式区间上重新计算“增加 6:00 / 12:00 / 18:00 光伏预测更新与购电调整”的策略，不从 Q2 年末 SOC 接续运行。

## Sensitivity inheritance

primary 使用 6000 kWh。初始 SOC sensitivity 统一采用：

- 4000 kWh
- 6000 kWh
- 8000 kWh

Protocol：

`../Q2/XXT_AUTHORITY/XXT_Q234_INITIAL_SOC_SENSITIVITY_PROTOCOL_R0.md`

在 Q3 正式全年引擎尚未完成前，不生成或宣称 Q3 初始 SOC 敏感性结果。

## Existing Q3 state remains

原 `Q3_CURRENT_STATUS_R0.md` 中的 official facts、allowed work 与 not-yet-authorized 项继续有效；本 R1 只补充共享初始化口径，不修改 Q3 settlement、information set、forecast update 或 adjustment accounting。
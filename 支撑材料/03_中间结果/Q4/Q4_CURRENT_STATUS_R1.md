# Q4 Current Status R1

> Supersedes: `Q4_CURRENT_STATUS_R0.md` for current-status navigation.  
> Date: 2026-09-13

状态：`PRE-DESIGN / FORMAL_RESULT_NOT_RUN`

## Shared initialization contract

Q4 在动态电价下分别重算 Q2-style 与 Q3-style 策略，两条正式分支统一采用：

`E(2025-02-01 00:00) = 6000 kWh`

该值是 `REASONABLE_MODELING_ASSUMPTION`，不是题目直接给定。

Authority：

`../Q2/XXT_AUTHORITY/XXT_Q234_FEB1_INITIAL_SOC_ASSUMPTION_R0.md`

这样可保证固定电价/动态电价、Q2-style/Q3-style 的比较都从同一储能状态起点出发。

## Sensitivity inheritance

primary 使用 6000 kWh。初始 SOC sensitivity 统一采用：

- 4000 kWh
- 6000 kWh
- 8000 kWh

Protocol：

`../Q2/XXT_AUTHORITY/XXT_Q234_INITIAL_SOC_SENSITIVITY_PROTOCOL_R0.md`

在 Q4 正式全年引擎尚未完成前，不生成或宣称 Q4 初始 SOC 敏感性结果。

## Existing Q4 state remains

原 `Q4_CURRENT_STATUS_R0.md` 中的 official facts、allowed work 与 not-yet-authorized 项继续有效；本 R1 只补充共享初始化口径，不修改 dynamic-price known_at、settlement-time 或 causal-price/oracle boundary。
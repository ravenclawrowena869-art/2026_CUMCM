# Q2 Current Status R2

> Supersedes: `Q2_CURRENT_STATUS_R1.md` only for current-status navigation and Feb-1 initialization semantics.  
> Date: 2026-09-13

## Formal state

- `Q2_MATH_CONTRACT_ID = CUMCM2026_C_Q2_MATH_CONTRACT_R1`
- `Q2_FORMAL_MATH_SPEC = PASS_WITH_LIMITATION`
- `S1 = S1_A_PAID_UNUSED_NORMAL_ENERGY`
- `Q2_EXECUTION_RELEASE = RELEASED`
- `Q2_FORMAL_RESULT = NOT_RUN` on current main snapshot
- `Q2_MATHEMATICAL_RESULT_PASS = FALSE`
- `Q2_FROZEN = FALSE`

## Feb-1 initial SOC amendment

Controller 已统一决定：

`E(2025-02-01 00:00) = 6000 kWh`

该值属于 `REASONABLE_MODELING_ASSUMPTION`，不是题目直接给定。

Authority：

`XXT_AUTHORITY/XXT_Q234_FEB1_INITIAL_SOC_ASSUMPTION_R0.md`

由此，旧计划中的 Jan31→Feb1 SOC bridge 不再作为 primary initialization 的必需输入；1 月仍作为 forecast/history 的 causal 历史区间。

## Required before final paper claim

初始 SOC 必须按统一协议补做 sensitivity：

- 4000 kWh
- 6000 kWh primary
- 8000 kWh

Protocol：

`XXT_AUTHORITY/XXT_Q234_INITIAL_SOC_SENSITIVITY_PROTOCOL_R0.md`

在 current full-year engine / current result package 可执行前，不伪造 sensitivity 数字。

## Unchanged

除上述 Feb-1 initialization amendment 外，Q2 R1 数学合同、S1 accounting、causal information boundary、risk candidate、recourse baseline、terminal sensitivity 与其他 mandatory evidence 均保持原 authority，不因本文件自动修改。
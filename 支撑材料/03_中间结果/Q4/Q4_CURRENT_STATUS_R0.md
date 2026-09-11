# Q4 Current Status R0

状态：`PRE-DESIGN / FORMAL_RESULT_NOT_RUN`

## Official facts

Q4 要求针对外网实时波动电价建立微网当天购电策略模型，并使用：

- 附件2：小区负载与光伏 actual；
- 附件3：光伏 forecast；
- 附件4：波动电价；

在波动电价下分别重新计算 Q2 与 Q3，并输出：

- `result4-2.xlsx`
- `result4-3.xlsx`

## Current allowed work

- 定义 Q2-style / Q3-style 在 dynamic-price 下的接口；
- 明确 dynamic price 的 `known_at` 与 settlement time；
- 设计 causal price vs oracle boundary diagnostic；
- 预设公平 experiment matrix；
- 定义 validator 与 result4 writer requirements。

## Not yet authorized

- 正式 Q4 model selection；
- 正式全年求解；
- result4-2/result4-3 数字；
- Mathematical Result PASS；
- Freeze。

当前状态：

`Q4_FORMAL_RESULT = NOT_RUN`

`Q4_FROZEN = FALSE`
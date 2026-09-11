# Q3 Current Status R0

状态：`CONTRACT_PREFLIGHT_ONLY / FORMAL_RESULT_NOT_RUN`

## Official facts already fixed

- 每天 `0:00 / 6:00 / 12:00 / 18:00` 可获得未来 24 h 整点光伏功率预报；
- 0:00 可制定当天计划购电；
- 其他发布时间可用于调整购电；
- 计划购电量高于调整购电量的部分，违约电价为交易时刻电价的 `50%`；
- 调整购电量高于计划购电量的超出部分，电价为交易时刻电价的 `1.5×`；
- 总购电费用包含计划购电费用、紧急购电费用、调整购电相关费用；
- 正式输入涉及附件1电价、附件2 actual load/PV、附件3 forecast；
- 正式输出为 `result3.xlsx`。

## Current allowed work

当前允许 XXT 完成：

- forecast issue/target time mapping；
- 10 min 调度与整点 forecast 的接口；
- adjustment accounting 唯一合同；
- 0/6/12/18 information set；
- storage / emergency recourse interface；
- no-adjustment baseline vs rolling-adjustment candidate；
- independent validator spec。

## Not yet authorized

- 正式全年 Q3 求解；
- 正式费用数字；
- result3 写入；
- Mathematical Result PASS；
- Freeze。

当前状态：

`Q3_FORMAL_RESULT = NOT_RUN`

`Q3_FROZEN = FALSE`
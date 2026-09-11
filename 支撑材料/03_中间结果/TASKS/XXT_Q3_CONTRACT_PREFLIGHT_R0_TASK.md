# XXT TASK｜Q3 Mathematical Contract Preflight R0

- `ACTIVE_ROLE = XXT_MATHEMATICAL`
- 模块：2026 CUMCM C题 Q3
- 模式：CONTRACT PREFLIGHT / NO FORMAL RESULT
- Astra：不要求
- 前置：Q2 current-version authority 可读取；Q2 不必已有正式全年结果，但不得把未裁决 Q2 缺口当作已知事实。

## 0. Canonical first

fresh 读取 Dispatcher / Shared Core / XXT Profile / Evidence Gate / Parameter Protocol；若写 GitHub，再读取 collaboration rules。

## 1. Official Q3 facts

官方题面给出：
- 每天 `0:00 / 6:00 / 12:00 / 18:00` 可获得未来 24 小时整点光伏功率预报；
- 0:00 预报用于当天计划购电；
- 其他发布时间可用于调整购电；
- 计划购电量高于调整购电量的部分，违约电价为交易时刻电价 `50%`；
- 调整购电量高于计划购电量的超出部分，电价为交易时刻电价 `1.5×`；
- 总购电费用包括计划购电、紧急购电和调整购电相关费用；
- 使用附件1电价、附件2 actual load/PV、附件3 forecast；
- 正式输出为 `result3.xlsx`。

不要超出这些官方事实补猜。

## 2. 必须裁决的合同问题

### A. Forecast time mapping

附件3是未来24小时整点预测，而调度基本时间粒度为10 min。必须读取附件3实际 schema 后确定：forecast target timestamps、issue timestamp、映射到10 min slot的方式、是否需要插值/保持/其他转换、转换是否引入 future leakage。

未读附件3前不得拍脑袋决定插值方法。

### B. Adjustment semantics

必须显式裁决：
- 6/12/18 的调整相对 0:00 original plan，还是相对上一版 adjusted plan；
- 一天多次调整时最终计费如何避免重复计算；
- 已经执行的 past slots 是否完全冻结；
- 新 forecast 能影响哪些 future slots；
- 0.5× reduction 与 1.5× increase 是独立增量费用还是替代原购电费用的一部分。

优先依据官方文本、模板与经济一致性；官方不足时标 `MODELING_COMPLETION_ASSUMPTION`，不得伪装成官方明示。

### C. Emergency purchase

定义 emergency 发生时刻、是否仍按交易时刻基础电价5×、与 adjustment 费用是否重复收费、storage recourse 与 emergency 的事件顺序。

### D. Storage state

与 Q1/Q2 已确认的 efficiency semantics、SOC range、charge/discharge power、no-selling、cross-day continuity 保持接口一致，除非 Q3 官方要求改变。

### E. Information set

对 0/6/12/18 每次决策明确：available actual、latest forecast issue、past plan/adjusted plan、current SOC、future forbidden fields、`known_at` 与 event sequence。

## 3. Baseline / candidate

至少定义：
- baseline：`Q3_DA_ONLY_NO_INTRADAY_ADJUSTMENT`
- rolling candidate：允许 6/12/18 causal adjustment 的 policy

不要为了复杂度额外堆模型族。

用于回答“是否需要引入其他时刻预报”的比较必须保持同一 tariff、actual、storage physics、emergency accounting、evaluation horizon；唯一核心差异应是是否使用后续 forecast / adjustment。

## 4. Validator specification

至少覆盖：
- future forecast release leakage；
- past slot 被后续调整改写；
- adjustment 方向与费用符号错误；
- 多次调整重复收费；
- emergency 重复收费；
- SOC 全路径 replay；
- day boundary；
- result3 writer mapping；
- 0/6/12/18 decision snapshot provenance。

## 5. Output

生成：`CUMCM2026_C_Q3_MATH_CONTRACT_PREFLIGHT_R0.zip`

至少包含：
- `00_START_HERE.md`
- `Q3_QUESTION_CONTRACT_R0.md`
- `Q3_INFORMATION_SET_R0.md`
- `Q3_ADJUSTMENT_ACCOUNTING_R0.md`
- `Q3_STORAGE_AND_RECOURSE_INTERFACE_R0.md`
- `Q3_BASELINE_AND_COMPARISON_R0.md`
- `Q3_VALIDATOR_SPEC_R0.md`
- `Q3_HOLD_ITEMS_R0.md`
- `SHA256SUMS.txt`

## 6. GitHub

建议 branch：`xxt/q3-contract-preflight-20260911`。

目录：`支撑材料/03_中间结果/Q3/`。

创建 PR，不 merge。

## 7. Exit

本任务最多允许：`Q3_FORMAL_MATH_SPEC = PREFLIGHT_READY` 或 `HOLD_FOR_AUTHORITY`。

不得输出正式 Q3 费用、result3、Mathematical Result PASS 或 Freeze。
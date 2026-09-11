# Q2 AUTHORITY 补件任务书：XXT GPT 与 FYQ GPT

- 文档状态：`REQUEST_FOR_SUPPLEMENT / WORKING_HANDOFF`
- 模块：2026 CUMCM C 题问题二
- 当前执行角色：`FYQ_TECHNICAL_ORCHESTRATOR`
- 当前 Q2 状态：`FORMAL_MATH_SPEC = PASS_WITH_LIMITATION`；`FORMAL_RESULT = NOT_RUN`；`Q2_FROZEN = FALSE`
- 消费方：承担 Q2 全年实现与验证的 Codex/Astra 执行窗口
- 本文权限：只列补件要求，不修改既有数学合同、Q1 Frozen 结果或 Q2 模型

## 1. 为什么需要补件

当前执行窗口已经收到：

- 官方 C 题题面、附件 1—5；
- Q1 Final Freeze Manifest 与 Paper Handoff；
- `FYQ_Q2_FULLYEAR_R0_TASK`；
- Q2 Controller sealed snapshot；
- Q2 三份 working idea：日前承诺与因果 recourse、S1 已付费未使用电量、Q80 风险裕量。

当前执行窗口未收到两份原始 authority 文件：

1. XXT 的 Q2 Formal Optimization Spec R1 原始交付包，即包含
   `CUMCM2026_C_Q2_MATH_CONTRACT_R1` 的完整 ZIP；
2. FYQ 的 Q2 Formal Spec Controller Review 原始 ZIP。

启动材料记录的历史哈希为：

- XXT 原始交付 ZIP：
  `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`
- FYQ Controller Review ZIP：
  `d69fd9736a0a5736223e40f26211332534c31331afc834aa0e3ab5d0a325ccca`

以上哈希目前只来自启动材料记录。本执行窗口没有原始字节，尚不能重新核验。

现有 snapshot 只能确认策略名称及部分原则，不能唯一确定点预测、残差分位数、滚动优化和跨日 SOC 的实现。若直接由执行者补猜，会改变已通过审查的数学方案，也可能造成未来信息泄漏或不公平的策略比较。因此正式全年求解暂记：

`HOLD_FOR_AUTHORITY`

## 2. 已完成且无需两边重复做的工作

当前执行窗口已经完成：

- 附件 1、附件 2、官方 result2 模板的读取与哈希绑定；
- 365 天 × 144 槽，共 52,560 槽的日期、时槽、数值完整性检查；
- 原始数据 kW 到每槽 kWh 的单位映射；
- 正常购电按全部 commitment 计费、紧急购电按同槽电价 5 倍计费的基础函数及测试；
- S1 中 `w` 不退款、不产生售电收入且不与弃光混记的基础 accounting 测试；
- 原始 Excel XML 对已保存长表的逐槽独立核验；
- result2 覆盖 2025-02-01 至 2025-12-31，共 334 天、48,096 槽的确认；
- 模板时段标签与 Q1 右端点 ordinal 时间合同之间的差异记录。

XXT GPT 与 FYQ GPT 不需要重做上述数据预检。二者需要补齐的是各自权限内的正式 authority 和接口文件。

## 3. XXT GPT 需要提供的补充文件

### 3.1 首选交付：原始数学契约包

若 XXT GPT 所在窗口仍能访问原始文件，应直接回传原始：

`CUMCM2026_C_Q2_FORMAL_OPT_SPEC_R1.zip`

实际文件名可以不同，但必须满足：

- 包含 `CUMCM2026_C_Q2_MATH_CONTRACT_R1` 原文；
- 外层 SHA256 应与历史记录一致；如不一致，说明差异来源；
- ZIP CRC 与内部 `SHA256SUMS.txt` 全部通过；
- 不以聊天摘要、截图或 working idea 代替原始合同。

### 3.2 原始包确实不可得时：建立显式替代版本

如果无法取得原始字节，XXT GPT 应建立新的、明确 supersede 原件的数学补件包，例如：

`CUMCM2026_C_Q2_XXT_MATH_AUTHORITY_SUPPLEMENT_R2.zip`

包内至少包含：

```text
00_START_HERE.md
Q2_MATH_CONTRACT_R2.md
Q2_MATH_CONTRACT_R2.json
Q2_FORMAL_OPTIMIZATION_SPEC_R2.md
Q2_INFORMATION_SET_AND_FORECAST_SPEC_R2.md
Q2_RISK_MARGIN_SPEC_R2.md
Q2_STORAGE_AND_DAY_BOUNDARY_SPEC_R2.md
Q2_VALIDATOR_SPEC_R2.md
Q2_MATHEMATICAL_REVIEW_VERDICT_R2.md
SHA256SUMS.txt
```

### 3.3 XXT 必须补全的数学定义

#### A. 日前点预测与信息集

必须写清：

- 每天 0:00 可使用哪些历史日期、哪些变量和哪些时槽；
- 负载点预测与光伏点预测的精确公式或算法；
- 历史窗口长度、是否滚动更新、是否按时槽建模；
- 1 月是训练期、运行期还是两者兼有；
- 2 月 1 日首次正式输出时可用的历史范围；
- 缺少历史、极端值或负预测值的处理；
- 每个字段的 `known_at` 规则；
- 严禁进入 0:00 commitment 的字段清单。

不能只写“用历史数据预测”或“采用日前预测值”。

#### B. `SIGNED_RESIDUAL_Q80_MARGIN_R1` 的可复现定义

必须写清：

- residual 的符号和公式，例如实际净负荷减点预测还是相反；
- 净负荷的定义及单位；
- residual 使用训练内拟合值、滚动样本外预测误差，还是其他序列；
- 按全局、月份、时槽或其他分组计算分位数；
- 历史窗口、最少样本数和冷启动回退；
- 分位数插值/有效秩规则；
- risk margin 加在净负荷预测、日前购电量还是其他量上；
- `alpha=0.75/0.80/0.85` 改变后必须重新生成哪些决策；
- 若 margin 为负，是否截断以及截断位置；
- Q80 单槽解析锚点与全年带储能 Claim 的边界。

#### C. `POINT_DA_LP_R1` 的完整日前 LP

必须给出：

- 全部决策变量、参数、索引和单位；
- 第一阶段目标函数；
- 若存在第二阶段 tie-break，其目标、容差和顺序；
- 能量平衡、SOC、充放电、弃光、购电、`w` 的全部约束；
- 正常购电 commitment 与计划储能轨迹的关系；
- 禁止售电及过量计划电量的处理；
- 初始 SOC、计划终端 SOC 或终端惩罚；
- infeasible/unbounded/numerical failure 的数学回退规则。

#### D. `Q2_RH_FIXED_Q_LP_R1` 的完整因果日内模型

必须给出：

- 每一槽的决策发生时刻；
- same-slot actual 在何时可得以及可影响哪些动作；
- 未来槽使用何种预测，是否随时槽更新；
- commitment 固定后，允许调整的变量；
- receding horizon 的长度和每次执行哪一槽；
- 目标函数、tie-break 和 terminal treatment；
- 紧急购电是在优化变量、平衡后的被动量，还是两者的明确组合；
- `w`、弃光、充放电和紧急购电的优先关系；
- 求解失败时的可行回退。

#### E. baseline 的精确规则

`DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE` 必须写成可直接实现的算法，至少明确：

- 正常情况下执行哪条日前储能轨迹；
- 哪些条件触发 safety override；
- override 的充放电修正顺序与投影公式；
- SOC 上下界、充放电功率上限和能量平衡如何同时保持；
- 缺电时紧急购电何时介入；
- 过量时先使用 `w`、弃光还是充电；
- 并列和边界情况如何处理。

不能仅以策略名称作为 baseline 定义。

#### F. 跨日 SOC、24 h 截断与 1 月处理

必须裁决：

- 实际日末 SOC 是否传给次日；
- 日前 LP 的日末目标是固定值、区间、惩罚还是可达性约束；
- rolling horizon 在日末采用何种 terminal value/target；
- 2025-01-01 的 6000 kWh 如何传到 2025-02-01；
- 1 月是否计入成本、策略评价和输出；
- 12 月 31 日的年末 SOC 约束；
- 日末 tail advantage/disadvantage 的正式诊断指标。

Q1 的每日 `E_144=6000` 不能由执行窗口自动移植到 Q2。

#### G. `ONE_SLOT_DELAYED_ACTUAL` 的严格时序

必须逐槽定义：

- 槽 (t) 做储能动作时能看到的最新 actual；
- 槽 1 的初始信息；
- 延迟情形下本槽能量平衡和紧急购电怎样结算；
- 是否允许同槽紧急购电作为被动平衡；
- same-slot 与 delayed 两种情形中 commitment、预测和费用口径必须保持的共同部分。

#### H. Mathematical Review 和 validator contract

必须给出：

- 独立 replay 要检查的全部等式、边界与容差；
- objective/accounting 的独立复算公式；
- max violation、argmax location 和 terminal violation 的定义；
- FEASIBLE、COMPETITIVE 的准入条件；
- 哪些结论不允许称为 near-optimal；
- 当前 Mathematical Review 的明确状态；
- 未裁决项如仍存在，逐项标成 `HOLD_FOR_AUTHORITY`，不得用建议性文字伪装成正式合同。

### 3.4 XXT 交付验收条件

XXT 包通过以下检查后，才进入 FYQ Controller 复核：

- 数学公式与单位闭合；
- 不存在 future-actual leakage；
- 三个策略可由文档唯一实现；
- Q80/alpha 可复现；
- 跨日 SOC 和 1 月用途已定义；
- validator 能独立复算；
- 原始包或替代包的 authority 身份清楚；
- ZIP CRC、外层 SHA256、内部 checksums 一并报告。

XXT 不负责决定 Git 分支、代码目录和 result2 文件写入方式；这些由 FYQ 在不改变数学含义的前提下绑定。

## 4. FYQ GPT 需要提供的补充文件

### 4.1 首选交付：原始 Controller Review 包

若 FYQ GPT 所在窗口仍能访问原始文件，应直接回传原始：

`CUMCM2026_C_Q2_FORMAL_SPEC_CONTROLLER_REVIEW_R0.zip`

实际文件名可以不同，但必须满足：

- 外层 SHA256 应与历史记录一致；如不一致，说明差异来源；
- 包含 Controller 对当前 XXT 数学合同的逐项裁决；
- ZIP CRC 与内部 checksums 全部通过；
- 明确其所审查的 XXT 包版本与哈希。

### 4.2 原始包确实不可得时：建立 Controller 替代补件包

如果原始字节不可得，FYQ GPT 应在收到并核验 XXT 新补件后，建立新的 Controller 包，例如：

`CUMCM2026_C_Q2_FYQ_CONTROLLER_SUPPLEMENT_R1.zip`

包内至少包含：

```text
00_START_HERE.md
Q2_CONTROLLER_REVIEW_R1.md
Q2_AUTHORITY_CHAIN_R1.md
Q2_IMPLEMENTATION_INTERFACE_R1.json
Q2_INPUT_BINDING_R1.json
Q2_RESULT2_WRITER_CONTRACT_R1.md
Q2_EXECUTION_AND_ACCEPTANCE_R1.md
HANDOFF_TO_CYQ_CODEX_R1.md
SHA256SUMS.txt
```

### 4.3 FYQ 必须补全的工程与 authority 接口

#### A. 对 XXT 数学补件作 current-version Controller Review

必须记录：

- 被审查的 XXT ZIP 文件名、SHA256 和内部合同版本；
- 逐项接受、带限制接受或退回的结论；
- 数学合同与官方题面、Q1 Frozen 接口有无冲突；
- 所有仍未解决的数学歧义必须退回 XXT，FYQ 不自行裁决；
- Controller Review 的最终状态。

#### B. 正式输入绑定

`Q2_INPUT_BINDING_R1.json` 至少写明：

- 官方题面、附件 1、附件 2、result2 模板的文件哈希；
- sheet、行、列、日期范围、时槽范围和单位；
- 附件 1 固定日电价的读取方式；
- 附件 2 实际负载/PV 的离线评估用途；
- 哪些字段可以进入 planner、controller 和 validator；
- 任何 forecast/derived table 的生成脚本、版本和上游来源；
- 原始数据只读规则。

#### C. 实施接口和机器可读 schema

`Q2_IMPLEMENTATION_INTERFACE_R1.json` 至少写明：

- 三个策略的唯一 ID 和入口；
- planner、controller、accounting、validator 的输入输出字段；
- 每个字段的单位、粒度、允许范围和 `known_at`；
- SOC 状态在天与天之间的传递字段；
- solver status、fallback reason 和 failure behavior；
- alpha、information policy、S1 policy、terminal policy 的配置键；
- 必须保存的逐槽 provenance 字段。

#### D. result2 writer contract

必须裁决并记录：

- official result2 只覆盖 2—12 月的写入范围；
- 1 月仅训练、同时运行或其他用途，以 XXT 数学合同为准；
- 计划购电量页 B1—EO1 标签与原始右端点序列存在的一槽差异时如何映射；
- writer 是按 ordinal position 写入还是按文本标签解析；
- 全天购电量和全天购电费各自包含哪些组成；
- 充放电页的 4 h 聚合规则；
- 紧急购电连续区间的合并规则；
- 模板省略号行如何展开为完整日期；
- 保存后 readback 要检查的 sheet、单元格、公式和格式。

模板映射必须与官方要求和 XXT 数学输出一致；如涉及数学口径，应先交 XXT 确认。

#### E. 执行任务与验收 Gate

`Q2_EXECUTION_AND_ACCEPTANCE_R1.md` 至少写明：

- 允许修改的代码和结果路径；
- 禁止修改的 Q1 Frozen 与 Q2 authority 范围；
- solver、主要依赖和可复现命令；
- 小样本 smoke、全年 fresh run、clean-input rebuild 的顺序；
- 必做三策略、alpha 邻域、延迟信息、日边界和 S1 审计；
- 独立复算与逐槽 replay 的通过阈值；
- 完整 R0 candidate ZIP 的必需文件；
- 送 XXT current-version Mathematical Review 的条件；
- 禁止 self-Freeze 和直接写 main/merge 的边界。

#### F. 给执行窗口的最终交接

`HANDOFF_TO_CYQ_CODEX_R1.md` 应清楚列出：

- Source of Truth；
- 当前可执行版本；
- XXT 数学包和 FYQ Controller 包的哈希；
- 需要复制到执行目录的具体文件；
- 唯一启动命令；
- 已解决/未解决问题；
- 预期输出与验收标准；
- 若原始合同与当前补件冲突，哪个版本明确 supersede 哪个版本。

### 4.4 FYQ 交付验收条件

FYQ 包必须满足：

- 明确绑定已经通过 Controller Review 的 XXT current-version 数学补件；
- 不擅自改写目标、hard constraints、单位、费用或 terminal 语义；
- 输入、代码、结果和模板写入接口完整；
- 所有执行条件可由新窗口独立复现；
- ZIP CRC、外层 SHA256、内部 checksums 一并报告；
- 仍未解决的问题明确触发 STOP，不把缺口留给执行者补猜。

FYQ 不需要重新推导 Q80 的数学依据，也不应自行决定残差公式和跨日终端条件；这些属于 XXT 数学裁决。FYQ 的职责是审查、绑定、集成和交付可执行接口。

## 5. 两边的提交顺序

1. **XXT GPT 先交数学 authority 包。**
2. **FYQ GPT 核验 XXT 包，再交 Controller/implementation interface 包。**
3. 当前 Codex/Astra 执行窗口核验两包哈希、CRC 和内部 checksums。
4. 完成公式到代码映射及短段端到端测试。
5. 再运行三策略全年 replay、alpha 邻域、延迟 actual、日边界诊断和 S1 审计。
6. 形成 Q2 R0 candidate delivery，送 XXT current-version Mathematical Review。
7. 只有 Technical PASS、Mathematical PASS、hard constraints zero violation、metrics recomputed 和 Evidence Gate 全部满足后，才由 FYQ 进入 Freeze 流程。

## 6. 两边禁止只返回的内容

以下均不能解除阻断：

- 只返回策略名称；
- 只返回聊天总结；
- 只返回公式截图；
- 只说“按历史均值预测”而不给窗口、分组和冷启动；
- 只说“滚动优化”而不给时序、目标和 terminal；
- 只说“Q80”而不给 residual 与分位数定义；
- 只给结果表而不给代码/合同/provenance；
- 用当前 working idea 文件冒充已经通过审查的原始数学合同；
- 由 FYQ 替 XXT 裁决数学缺口，或由 XXT 替 FYQ决定工程版本与 writer。

## 7. 当前执行窗口已发现的两个接口风险

### 7.1 评分时域与原始时域不同

附件 2 覆盖 2025-01-01 至 2025-12-31，共 365 天；官方 result2 覆盖 2025-02-01 至 2025-12-31，共 334 天。1 月对预测训练、SOC warm-up、成本评价和 Feb 1 初始状态的用途必须同时在 XXT 数学合同和 FYQ 输入接口中写清。

### 7.2 模板标签存在时槽偏移风险

Q1 冻结时间合同把原始 `0:10` 作为第 1 槽右端点，即物理区间 `00:00—00:10`。result2 模板第 1 个计划购电标签为 `0:10—0:20`，末槽为 `0:00—0:10+1`。执行者不能在没有 authority 的情况下自行左移、右移或重新解释。FYQ writer contract 应对照官方要求作出唯一映射；若该选择改变数学输出含义，应由 XXT共同确认。

## 8. 本任务完成定义

只有当以下两项都取得，当前 `HOLD_FOR_AUTHORITY` 才能解除：

- XXT 数学包：完整、版本明确、可复现、通过 FYQ Controller Review；
- FYQ Controller 包：绑定当前数学包、官方输入与输出模板，并给出可执行接口。

本文自身不是数学合同、Controller Review、模型实现或 Freeze Manifest，不能被用作上述文件的替代品。

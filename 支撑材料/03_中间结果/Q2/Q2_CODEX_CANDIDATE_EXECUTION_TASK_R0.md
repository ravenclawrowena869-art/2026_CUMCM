# Q2 Codex 候选全年执行任务书 R0

## 0. 文档身份

- 问题：2026 CUMCM C 题，问题二（Q2）
- 任务版本：R0
- 编制日期：2026-09-11
- 发起人：CYQ
- 技术权威与复核人：FYQ
- 数学合同复核人：XXT
- 执行代理：CYQ/Codex
- 执行角色：`ACTIVE_ROLE=FYQ_TECHNICAL_ORCHESTRATOR`
- 推荐执行环境：Codex
- 推荐首轮模型：`gpt-6-astra`
- 推荐推理强度：`high`
- 状态：等待 PR #6 合入 `main` 后执行
- 截止时间：由 CYQ 另行指定；不得因未指定截止时间而跳过质量门

本任务书只授权生成候选全年结果及其验证证据，不授权宣布数学结果通过、冻结或写入论文。

## 1. 启动条件

同时满足以下条件后方可开始：

1. PR #5 与 PR #6 的当前权威材料已进入 `main`，或 CYQ 明确指定了等价且固定的执行基线；
2. PR #6 已解决冲突，全部 R2 文件可由仓库路径读取；
3. XXT R2 预验证包已在仓库中绑定明确路径及 SHA256；
4. W2 正式因果预测、残差历史接口、Jan31→Feb1 SOC bridge、官方结果2模板均可读取；
5. 下列权威文件的路径、版本与校验值一致。

若任一条件不满足，立即停止并提交 `HOLD_INPUT_BINDING` 报告，不得猜测、补造、替换或静默降级。

## 2. 权威边界

当前唯一有效执行链为：

`XXT R1 原始数学合同 + FYQ S1-A 授权 + XXT R2 预验证包 + FYQ R2 实现接口`

已绑定的包：

- XXT R1：`CUMCM2026_C_XXT_Q2_FORMAL_OPT_SPEC_R1_DELIVERY.zip`
- XXT R1 SHA256：`0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`
- XXT R2：`CUMCM2026_C_XXT_Q2_PREVALIDATION_Q3_PREFLIGHT_R2_20260911.zip`
- XXT R2 SHA256：`63c2494eac89b164830d9e26435332f6c06afedc0234ba5a05d25468f4d0a312`

PR #8 及其 SHA `d22609f9...` 的分类为：

`PARALLEL_NONCANONICAL_REPACKAGE / NOT_IN_CURRENT_AUTHORITY_CHAIN`

Codex 不得将 PR #8 作为正式实现依据，也不得用它覆盖当前权威链。

## 3. 强制阅读顺序

开始修改代码前，必须完整阅读：

1. `FYQ_CONTROLLER/XXT_R2_PREVALIDATION_BINDING_R1.md`
2. `FYQ_CONTROLLER/CONTROLLER_Q2_CURRENT_VERSION_REVIEW_R2.md`
3. `FYQ_CONTROLLER/Q2_AUTHORITY_CHAIN_R2.md`
4. `FYQ_CONTROLLER/Q2_IMPLEMENTATION_INTERFACE_R2.json`
5. `FYQ_CONTROLLER/Q2_INPUT_BINDING_R1.json`
6. `FYQ_CONTROLLER/Q2_RESULT2_WRITER_CONTRACT_R1.md`
7. `FYQ_CONTROLLER/Q2_DELAYED_ACTUAL_SENSITIVITY_PROTOCOL_R1.md`
8. `FYQ_CONTROLLER/Q2_RISK_HISTORY_COLD_START_BINDING_R1.md`
9. `FYQ_CONTROLLER/Q2_24H_TAIL_DIAGNOSTIC_PROTOCOL_R1.md`
10. `FYQ_CONTROLLER/Q2_EXECUTION_AND_ACCEPTANCE_R2.md`
11. `FYQ_CONTROLLER/Q2_EXECUTION_RELEASE_R1.md`
12. `FYQ_CONTROLLER/HANDOFF_TO_CYQ_CODEX_R2.md`
13. `FYQ_CONTROLLER/SHA256SUMS.txt`

相对路径基准为 `支撑材料/03_中间结果/Q2/`。

任何旧版 R1 执行/接口快照仅用于追溯，不得覆盖 R2。

## 4. Stage 0：输入闸门

在求解前生成机器可读和人工可读两份输入清单，至少核对：

- 文件路径、文件大小与 SHA256；
- 工作表、字段名、键、时区、时间粒度和单位；
- W2 正式预测的版本及覆盖期；
- 残差历史的来源、最小样本和冷启动状态；
- Jan31→Feb1 SOC 桥接值；
- 官方结果2模板的表名、列名、行数与写入范围；
- XXT R2 包内部 `SHA256SUMS`；
- 所有输入是否来自当前权威链。

阻塞状态统一写为：

`Q2_EXECUTION_STATUS = HOLD_INPUT_BINDING`

报告必须列明缺失项、实际发现路径、期望路径、期望哈希、实际哈希及下一责任人。

## 5. 实现任务

1. 严格按照 R2 接口实现 Q2 候选全年执行。
2. 不得擅自修改目标函数、变量定义、硬约束、单位、时间映射、5 倍应急成本、禁止售电、跨日 SOC 或结果2格式。
3. 保留并统一比较：
   - 题目给定运行基线；
   - B0：无储能或无灵活性结构基线；
   - B1：透明规则策略；
   - B2：正式优化策略。
4. 对等价最优解按权威合同执行第二阶段规则，不得自行引入新的二进制变量或惩罚项。
5. 重要参数、求解器、依赖版本、随机种子和运行命令必须进入配置或日志。
6. 原始附件只读；所有候选产物写入新目录。

## 6. 最低测试集

全年运行前至少通过：

- 权威哈希与输入模式测试；
- 锚点样例与合成 oracle 测试；
- 单日测试；
- 跨午夜事件顺序测试；
- 月界及 Jan31→Feb1 SOC 连续性测试；
- 储能 SOC 递推、功率边界和效率测试；
- 禁止售电与购电计费测试；
- 结果2写入及独立回读测试；
- 缺字段、错单位、重复键、缺时段等非法输入测试。

任何测试失败均不得继续形成正式候选结果。

## 7. 全年执行与独立复算

全年运行后必须独立重算：

- 求解状态、gap、运行时间和峰值内存；
- 目标函数各组成项及总值；
- 每区域、每时段能量平衡残差；
- 全部变量上下界与约束违反量；
- 初始、跨日和终端 SOC；
- 购电费用、售电收入、净运行成本；
- 碳排放及其核算边界；
- 实际购电峰值、售电峰值和净交换峰值；
- 光伏利用、弃光和储能吞吐；
- 延迟、迁移、超时及未服务任务；
- 六区域分项结果和系统汇总。

不得用求解器显示 `OPTIMAL` 代替上述复算。

## 8. 强制敏感性与风险检查

按 R2 协议执行并保留逐场景结果：

- `alpha = 0.75, 0.80, 0.85`；
- `ONE_SLOT_DELAYED_ACTUAL`；
- 充放电效率变化；
- 终端 SOC 条件；
- 风险历史冷启动与最小样本边界；
- 24 h tail/day-boundary 诊断；
- S1 相关边界；
- 权威文件要求的其他敏感性。

每项必须报告可行率、成本、碳排、峰值、延迟或服务质量变化，以及是否触发硬约束失败。

## 9. 交付物

在新的 candidate execution 分支和 PR 中提交：

1. 可复现源代码；
2. 依赖与环境说明；
3. 运行配置和完整命令；
4. 输入绑定清单与哈希；
5. 自动测试报告；
6. 全年候选结果；
7. 官方结果2文件及独立回读报告；
8. 指标、目标和约束独立复算报告；
9. 敏感性与风险检查结果；
10. 运行日志、状态、gap、耗时和内存；
11. `SHA256SUMS.txt`；
12. 已知风险、失败尝试和待 FYQ/XXT 审核事项；
13. 面向下一责任人的复现说明。

建议分支名：

`cyq/q2-candidate-full-year-r0-20260911`

建议 PR 标题：

`run(q2): produce candidate full-year results and validation evidence`

## 10. 禁止事项

Codex 不得：

- 直接修改或推送 `main`；
- 自行 merge；
- 采用 PR #8 替换当前权威链；
- 在输入不完整时猜测参数或补造数据；
- 为获得可行解静默放松硬约束；
- 修改官方结果2模板结构；
- 将候选结果写入论文或标记为最终值；
- 宣布 `Q2_MATHEMATICAL_RESULT_PASS = TRUE`；
- 宣布 `Q2_FROZEN = TRUE`。

## 11. 候选 PR 的强制状态

候选 PR 末尾必须明确写出：

```text
Q2_EXECUTION_RELEASE = RELEASED
Q2_FORMAL_RESULT = CANDIDATE_ONLY
Q2_MATHEMATICAL_RESULT_PASS = FALSE
Q2_FROZEN = FALSE
```

若未成功运行，则使用 `Q2_FORMAL_RESULT = NOT_RUN` 并说明阻塞原因。

## 12. 验收与下一交接

执行完成后的审查顺序为：

1. FYQ：技术实现、数据接口和数值证据审查；
2. XXT：数学合同一致性审查；
3. CYQ：Evidence Gate、论文口径和整体交付审查。

只有三方审查完成且证据链闭合后，才允许另行决定是否冻结。该决定不属于本任务书授权范围。

验收条件：

- 所有必需输入已固定并可追溯；
- 测试全部通过；
- 结果2可独立回读；
- 目标值和约束可独立复算；
- 强制敏感性完整；
- 候选 PR 可由另一执行者从干净环境复现；
- FYQ 与 XXT 均未提出阻断性问题。

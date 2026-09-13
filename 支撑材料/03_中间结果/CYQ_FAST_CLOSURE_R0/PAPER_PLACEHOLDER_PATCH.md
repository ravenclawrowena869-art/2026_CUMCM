# PAPER PLACEHOLDER PATCH R0

Status: `PAPER_PLACEHOLDERS_READY`  
Patch mode: incremental; **Q1 is out of scope**. Final q, accounting choices, objective values and annual metrics remain owned by FYQ/XXT.

## Global purge

Until a current Mathematical PASS/Frozen handoff arrives, old Q2/Q3/Q4 values in the live paper are stale draft content. Before final submission, full-text search abstract, body, conclusion/model evaluation, captions and appendix for:

- claims that `q=0.80` is empirically optimal, fully validated or final;
- old Q2 annual values including `1847.73` and `106.40`;
- old Q3 annual values including `1505.26`;
- old Q4 annual/oracle values including `1957.33` and `1586.57`;
- any wording that treats oracle/future information as deployable evidence;
- any “最终” caption not tied to a current Frozen source.

## Abstract placeholders

### Q2
对于问题二，本文在历史信息可得的约束下构造日前计划与日内补购机制，并针对冬季光伏预测偏差进行因果修正。Phase-B 审查已允许将 `L2 + P3_AMPCORR_K7` 作为下一步 M3 年度回放的预测输入；其中 `q=0.80` 仅保留为单时段 newsvendor 分析下的理论锚点，不作为已经验证的最终参数。最终风险分位数及全年费用、紧急购电等指标分别记为 `[[Q2_FINAL_Q]]`、`[[Q2_TOTAL_COST]]`、`[[Q2_EMERGENCY_ENERGY]]`，待 FYQ+XXT 完成年度回放、独立复算与 Mathematical PASS 后统一回填。

### Q3
对于问题三，针对 00:00、06:00、12:00 和 18:00 四个预测版本依次到达的特点，本文构造多版本滚动调整框架：每个更新时点只依据当时可获得的信息重算尚未执行的计划，并保持已执行决策和状态递推连续。模型的正式费用口径、调整成本及全年结果分别以 `[[Q3_OBJECTIVE_CONTRACT]]`、`[[Q3_ADJUSTMENT_ACCOUNTING]]`、`[[Q3_TOTAL_COST]]` 占位，待唯一数学合同锁定并完成正式年度求解后回填。

### Q4
对于问题四，在问题二与问题三的已冻结接口上引入动态电价：Q4-2 继承单次日前计划框架，Q4-3 继承多版本滚动调整框架，决策阶段只允许使用当时可获得的因果价格信息。完整未来价格只用于 oracle 诊断，不参与可部署策略排序。两种场景的年度费用、紧急购电和 oracle gap 以 `[[Q4_2_*]]`、`[[Q4_3_*]]` 占位，待动态价格信息与结算合同通过 XXT 审查并完成正式回放后回填。

## Q2

### Risk parameter
在不考虑跨时段状态耦合的简化单时段购电问题中，计划购电与紧急补购之间可写成 newsvendor 型权衡，因此由两类边际成本之比得到的分位数可作为风险参数的理论锚点。该推导用于解释风险余量的方向和量级，不直接等同于全年滚动优化下的经验最优值。当前 `q=0.80` 尚未通过本轮重新验证，正式取值记为 `q^*=[[Q2_FINAL_Q_PENDING_FYQ_XXT]]`。正式参数只能由当前 F1_K7 预测输入下的 q cheap closure、一次选定候选的 M3/SP 年度回放和独立 validator 共同确定。

### Winter-PV / amplitude correction
冬季样本的主要修正沿用因果历史窗口，不读取决策时点之后的真实光伏值。Phase-B 审查仅确认 `P3_AMPCORR_K7` 可随 `L2` 预测链进入 M3 年度回放，K 固定为 7；这一结论说明该预测输入具备继续回放的资格，并不同时证明风险参数、全年费用或 Q2 已冻结。因此正文只保留“因果、K=7、获准进入回放”三项事实，不扩写未经 handoff 支持的成本改进幅度。

### Result placeholders
`[[Q2_FINAL_Q]]`, `[[Q2_TOTAL_COST]]`, `[[Q2_DAYAHEAD_COST]]`, `[[Q2_EMERGENCY_COST]]`, `[[Q2_EMERGENCY_ENERGY]]`, `[[Q2_EMERGENCY_EVENT_COUNT]]`, `[[Q2_MAX_VIOLATION]]`, `[[Q2_HANDOFF_SHA]]`.

回填前结果段只说明：当前预测链已完成 Phase-B 有限通过，但风险参数与年度结果尚在收口；最终数字待一次正式年度回放、独立复算和 Mathematical PASS 后统一回填，并同步更新摘要与图表。

## Q3

### Lead-in
问题三允许在一天内多次获得更新预测并调整后续计划。其关键不在于把同一个日优化模型重复运行四次，而在于区分每个时点已经执行、已经承诺和尚可调整的决策，并保证储能状态与费用结算在相邻阶段之间连续。为此，本文采用 00:00、06:00、12:00、18:00 四阶段的多版本滚动调整框架；每次更新只使用当时可获得的预测和已实现状态，对未来未执行区间重新求解，为比较不同预测更新频率下的购电决策提供统一接口。

### Stage logic
设阶段集合 `S={00,06,12,18}`。阶段 `s` 到达时：冻结阶段开始前已经执行的功率、购电和 SOC；读取当时允许获得的预测版本与上一阶段仍有效的承诺；以实际到达阶段边界的 SOC 作为新求解初始状态；只对尚未执行的时段生成新计划；调整成本、取消/追加规则和最终结算严格引用 `[[Q3_LOCKED_ACCOUNTING_CONTRACT]]`；输出阶段计划、状态桥接量和独立复算账本。该结构强调信息集和状态边界，不预设新增阶段一定降低费用。

### Algorithm skeleton
输入：四个预测 vintage、Q2 冻结后的能源/储能接口、阶段时点、`[[Q3_LOCKED_ACCOUNTING_CONTRACT]]`。初始化：00:00 建立首个可执行计划，保存 commitment ledger 和 SOC 起点。循环：依次到达 06:00、12:00、18:00，冻结已执行区间，桥接当前 SOC，读取当前 vintage，只重算未来区间。硬检查：功率平衡、SOC 上下界、充放电功率、阶段桥接残差和合同规定的不可撤销项。失败分支：执行 `[[Q3_FALLBACK_RULE_FROM_HANDOFF]]`，论文端不自行定义。停止：完成 18:00 后最后一段执行并到达日终，按正式合同复算全天/全年费用与核心指标。

结果占位：`[[Q3_TOTAL_COST]]`, `[[Q3_ADJUSTMENT_COST]]`, `[[Q3_EMERGENCY_COST]]`, `[[Q3_EMERGENCY_ENERGY]]`, `[[Q3_MAX_VIOLATION]]`, `[[Q3_STAGE_ABLATION_METRICS]]`, `[[Q3_HANDOFF_SHA]]`。正式 run 与 stage-ablation 证据到达前，不写“四阶段显著优于……”之类排序结论。

## Q4

### Lead-in
问题四在前述能源计划机制上进一步引入随时间变化的电价。Q4-2 与 Q4-3 分别继承问题二与问题三的决策接口，只替换经 XXT 锁定的动态价格信息与结算模块，以便把结果变化归因于价格机制，而不混入未经说明的模型结构变化。

### Inheritance
`Q4-2 = frozen Q2 interface + [[Q4_CAUSAL_PRICE_INFORMATION_CONTRACT]] + [[Q4_PRICE_ACCOUNTING_CONTRACT]]`。

`Q4-3 = frozen Q3 interface + [[Q4_CAUSAL_PRICE_INFORMATION_CONTRACT]] + [[Q4_PRICE_ACCOUNTING_CONTRACT]]`。

Q4-3 四阶段仍遵循 00/06/12/18 的信息集边界。动态价格只能按照当前阶段允许观察/预测的字段进入决策，已经执行的计划不因后验价格变化被回写。

### Causal vs oracle
正式策略只使用 `[[Q4_CAUSAL_PRICE_INFORMATION_CONTRACT]]` 明确允许的价格信息。完整未来价格只用于 oracle diagnostic，估计信息不足造成的 gap 或检查机制上限；oracle 不进入正式策略排名、不作为参数选择依据，也不回写正式结果。任何 oracle 图表/数值均在标题或图注明确标记“诊断”。

Q4-2 占位：`[[Q4_2_TOTAL_COST]]`, `[[Q4_2_EMERGENCY_ENERGY]]`, `[[Q4_2_MAX_VIOLATION]]`, `[[Q4_2_ORACLE_GAP_DIAGNOSTIC]]`。  
Q4-3 占位：`[[Q4_3_TOTAL_COST]]`, `[[Q4_3_EMERGENCY_ENERGY]]`, `[[Q4_3_MAX_VIOLATION]]`, `[[Q4_3_ORACLE_GAP_DIAGNOSTIC]]`。  
共同来源：`[[Q4_CONTRACT_SHA]]`, `[[Q4_HANDOFF_SHA]]`。

## Handoff insertion record

每次批准 handoff 到达后记录：`question / handoff_path / handoff_sha_or_commit / mathematical_review / freeze_version / placeholders_replaced / stale_claim_sweep / abstract_updated / body_updated / conclusion_updated / caption_updated`。只有相关旧数字和旧强结论已从整篇论文移除，才标记该块 integrated。

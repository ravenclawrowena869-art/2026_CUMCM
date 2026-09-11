# CUMCM 2026 C题 Q2 建模与执行计划冻结 R1

> Freeze ID: `CUMCM2026_C_Q2_MODELING_PLAN_FREEZE_R1_20260911`  
> Freeze scope: `MODEL_PLAN_AND_EXECUTION_SPEC_ONLY`  
> Owner: `FYQ_TECHNICAL_ORCHESTRATOR`  
> Date: 2026-09-11  
> Status: `PLAN_FROZEN / RESULT_NOT_RUN`

## 0. 冻结边界

本文件冻结的是 Q2 的**建模方案、信息结构、候选策略矩阵、实验与验收计划**，用于后续实现、验证和论文交接保持一致。

它不等于 Q2 模型/结果最终冻结。当前仍保持：

- `Q2_PREVALIDATION_SPEC = PASS`
- `Q2_EXECUTION_RELEASE = RELEASED`
- `Q2_FORMAL_RESULT = NOT_RUN`
- `Q2_MATHEMATICAL_RESULT_PASS = FALSE`
- `Q2_FROZEN = FALSE`

只有 P0 级问题、官方口径变化、XXT Mathematical Veto，或正式执行证据证明当前结构不成立时，才允许重开本计划；重开必须建立新版本并说明影响范围。

## 1. Authority 与输入口径

正式执行采用以下 authority chain：

1. 官方 2026 CUMCM C题题面、附件与 result2 模板；
2. Q1 Frozen 的储能参数、单位和时间映射；
3. 原始 XXT Q2 数学合同包  
   `CUMCM2026_C_XXT_Q2_FORMAL_OPT_SPEC_R1_DELIVERY.zip`  
   SHA256  
   `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`;
4. FYQ S1-A Controller authorization；
5. XXT R2 prevalidation 包  
   `CUMCM2026_C_XXT_Q2_PREVALIDATION_Q3_PREFLIGHT_R2_20260911.zip`  
   SHA256  
   `63c2494eac89b164830d9e26435332f6c06afedc0234ba5a05d25468f4d0a312`;
6. FYQ current implementation/input/writer/execution interfaces；
7. current canonical `cumcm-rigorous-workflow`；
8. 当前明确的执行 Task/Handoff。

PR #8 的 `d22609f9...` 仅为 parallel noncanonical repackage，不进入本轮正式 execution chain。

正式执行前必须从真实 execution bytes 记录并核验：

- `FYQ_W2_FORMAL_CAUSAL_FORECAST.csv` SHA256；
- `FYQ_W2_RESIDUAL_HISTORY_INTERFACE.csv` SHA256；
- Jan31→Feb1 SOC bridge artifact SHA256；
- source/config SHA；
- solver/runtime/package versions。

任何 required input 缺失或不匹配，停止为 `HOLD_INPUT_BINDING`，禁止静默替代。

## 2. 时间尺度与正式区间

- 时间粒度：10 min；
- 每日槽数：144；
- `Δt = 1/6 h`；
- 时间映射：`C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`；
- January：仅作为 causal warm-up 与 Jan31→Feb1 状态桥接；
- 正式计费区间：2025-02-01 至 2025-12-31；
- 正式天数：334；
- 正式槽数：48096；
- 禁止按日重置 SOC。

## 3. 储能状态模型

使用 Q1 Frozen 储能口径：

- 容量：12000 kWh；
- SOC 下界：1200 kWh；
- SOC 上界：10800 kWh；
- 最大充电功率：5000 kW；
- 最大放电功率：5000 kW；
- 单槽最大充/放电量：`5000/6 = 833.333333... kWh`；
- primary efficiency：`η_c = η_d = 0.9`；
- 状态递推：
  `E_after = E_before + η_c c - d/η_d`；
- primary year-end terminal：
  `FREE_BOUNDED_YEAR_END`；
- terminal sensitivity：
  `EQ_INITIAL_6000`、`GE_INITIAL_6000`。

## 4. 信息结构与因果约束

### 4.1 日前时点

每天 00:00 形成并锁定 `q_DA`，之后当日不可修改。

日前决策只能使用 decision time 可知信息，未来真实负荷/光伏禁止进入日前计划。

### 4.2 日内储能

primary timing：

`CURRENT_SLOT_ACTUAL`

即当前槽可使用当前槽已到达的真实量控制储能，未来槽继续使用 00:00 冻结预测。

必须完整运行 sensitivity：

`ONE_SLOT_DELAYED_ACTUAL`

用于检验当前槽真实量可见性假设是否 materially 改变正式排序或结论。

### 4.3 known_at

所有 forecast/residual/history 都必须满足：

`known_at <= decision_time`

风险 residual 使用 strict cutoff：

`target_ts < current_day_00:00`

禁止 future actual leakage、later-vintage backfill 和隐式未来信息。

## 5. 预测层

正式 Q2 forecast family：

- Load：`LAG7`
- PV：`TRAILING7_MEAN`

Attachment1 的固定 144 槽电价曲线在 Q2 中每日重复使用。

Attachment4 动态电价不进入 Q2，它属于 Q4。

W2 forecast 层在实现时必须通过冻结的 formal causal forecast 文件消费，不在 Q2 solver 内部重新创造另一套 forecast 口径。

## 6. 日前基线与正式风险候选

### 6.1 Point Day-Ahead

`POINT_DA_LP_R1`

作用：给出点预测条件下的日前正常购电 commitment。

日前模型中不主动购买 emergency energy。

### 6.2 Risk-aware Day-Ahead

`SIGNED_RESIDUAL_Q80_MARGIN_R1`

定义 slot residual：

`e = (L_actual - PV_actual) - (L_hat - PV_hat)`

基于严格 causal expanding same-slot residual history 建立经验分位数。

primary：

`alpha = 0.80`

解析依据来自一槽无储能近似：

`J(q)=p q + 5p E[(N-q)+]`

对应临界分位约 `F(q)=0.8`。

该解析结果只作为 risk candidate 的 anchor，不构成带储能全年系统的全局最优性证明。

经验分位采用 nearest-rank：

`ceil(alpha*n)`

reserve：

`m = max(0, Q_alpha)`

并作用于 net-load forecast。

正式 sensitivity：

- alpha = 0.75
- alpha = 0.80
- alpha = 0.85

每个 alpha 必须**重新构造 causal quantile → 重新日前规划 → 全年 full replay**，禁止只对既有最优解做事后统计。

## 7. 日内控制与比较基线

### 7.1 正式因果日内控制

`Q2_RH_FIXED_Q_LP_R1`

每天每个时槽在 `q_DA` 已锁定前提下，对剩余当日时域求解储能操作。

当前槽按允许的信息集使用 actual，未来槽只使用冻结 forecast。

### 7.2 固定储能安全覆盖基线

`DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE`

用于与 causal intraday recourse 做同口径比较。

其动作只能因物理可行性被裁剪，不得借 safety override 偷偷扩大动作或改变原始方向。

每个 policy 必须传播自己的合法 SOC 路径，禁止多个 policy 共用同一 SOC 轨迹。

## 8. S1-A source-resolved 结算与能量平衡

正式 S1 模式：

`S1_A_PAID_UNUSED_NORMAL_ENERGY`

变量含义：

- `q_DA`：00:00 锁定的正常购电 commitment；
- `w`：已经付费但未物理使用的正常购电量；
- `r`：紧急购电；
- `v`：弃光；
- `c,d`：储能充/放电。

物理平衡：

`q_DA - w + r + PV + d = L + c + v`

约束：

`0 <= w <= q_DA`

`0 <= v <= PV`

正常购电费用：

`Σ p*q_DA`

紧急购电费用：

`Σ 5*p*r`

`Σ p*w` 只作为 diagnostic，不得再次计费。

无售电。

紧急购电不得用于给储能充电。

## 9. 四策略正式执行矩阵

在相同官方数据、相同 tariff、相同储能物理、相同 accounting 下至少运行：

1. `POINT_DA_LP_R1 × Q2_RH_FIXED_Q_LP_R1`
2. `POINT_DA_LP_R1 × DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE`
3. `SIGNED_RESIDUAL_Q80_MARGIN_R1 × Q2_RH_FIXED_Q_LP_R1`
4. `SIGNED_RESIDUAL_Q80_MARGIN_R1 × DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE`

该矩阵用于区分：

- 日前 risk margin 是否带来真实收益；
- 因果日内 recourse 相对固定储能基线的增益；
- 两者是否存在交互；
- 改善是否依赖 S1/w、future actual 或非法 SOC 行为。

## 10. Astra / Sol 执行分层

### 10.1 Astra High 只负责核心工程 Burst

Astra 负责：

- reusable production-grade Q2 full-year engine；
- real input → forecast → DA → recourse → SOC/accounting → validator → result2 的首次完整集成；
- 第一轮 canonical 334-day clean execution；
- primary alpha=0.80 四策略矩阵；
- canonical hard-validation；
- result2 write/readback；
- 为所有后续 sensitivity 做参数化开关。

Astra 到此停止。

### 10.2 FYQ Sol High 完成完整 evidence campaign

FYQ Sol 负责：

- 复现 Astra canonical run；
- alpha .75/.80/.85 全年 replay；
- ONE_SLOT_DELAYED_ACTUAL 全年 replay；
- S1 w/v audit；
- efficiency sensitivity；
- terminal sensitivity；
- 24h tail/day-boundary diagnostic；
- full-path validator；
- independent accounting；
- result2 readback；
- technical candidate closure。

### 10.3 XXT Sol High / Extra High 做 Mathematical Review

XXT 负责：

- formula→code mapping；
- 从 slot-level ledger 独立复算成本；
- 48096 槽全路径约束 replay；
- sensitivity interpretation；
- 按预注册客观规则选择代表/极端日独立 re-solve；
- Mathematical Verdict。

只有遇到无法由 Sol 安全闭合的高耦合独立 re-solve/debug，才建立最小 targeted Astra task。

## 11. 强制验证

正式 candidate 进入 XXT 前必须通过：

- 334×144 slot coverage；
- q_DA immutability；
- known_at / future leakage audit；
- S1 balance；
- `w<=q_DA`；
- `v<=PV`；
- no selling；
- no emergency charging；
- C/D limits；
- SOC recursion；
- SOC full-path bounds；
- cross-day continuity；
- terminal mode；
- fallback counts；
- independent total-cost recomputation；
- result2 ordinal mapping；
- saved result2 readback。

数值 tolerance：

- physics/energy：`1e-6 kWh`
- total cost：`max(1e-5 CNY, 1e-9*abs(recomputed_cost))`
- hashes/provenance/date/slot coverage：strict

## 12. 必做诊断与 sensitivity

### 12.1 Delayed Actual

完整比较：

`CURRENT_SLOT_ACTUAL` vs `ONE_SLOT_DELAYED_ACTUAL`

如果 materially 改变主策略排序，返回 XXT/FYQ，不得直接冻结。

### 12.2 S1 usage audit

至少记录：

- `sum(w)`
- `sum(p*w)` diagnostic
- `w/sum(q_DA)`
- `w>0` 的槽数和天数
- max slot/day `w`
- separate `sum(v)`
- `w` 是否 materially 驱动可行性或优势

若是，则触发 S1 counterfactual / XXT 回审。

### 12.3 Efficiency

primary：

`η_c=η_d=0.9`

替代口径：

`η_c=η_d=sqrt(0.9)`

按 current contract 做 downstream replay；只把它作为口径 sensitivity，不能无授权替代 primary semantics。

### 12.4 Terminal

比较：

- FREE_BOUNDED_YEAR_END
- EQ_INITIAL_6000
- GE_INITIAL_6000

### 12.5 24h tail / day-boundary

执行 current `Q2_24H_TAIL_DIAGNOSTIC_PROTOCOL_R1`。

如果得到：

`TAIL_CHALLENGER_REQUIRED = TRUE`

则相关 robustness claim 停止，返回 FYQ/XXT，不允许静默加长 horizon 后继续写结论。

## 13. Candidate 选择原则

选择正式 candidate 时遵循：

1. hard constraints / causal legality / provenance 先通过；
2. 只比较同口径 strategy；
3. 主目标是正式 Q2 cost；
4. baseline/challenger 需要 own-SOC-path 公平 replay；
5. sensitivity 不能 materially 推翻主策略排序；
6. 不以单个最低成本替代 Evidence Gate；
7. 不把 FEASIBLE 自动写成“全局最优”。

## 14. result2 输出

正式 writer 必须：

- 计划购电量：334 天 × 144 槽，按 frozen ordinal mapping 写入；
- 充放电量：展开模板省略号，输出完整 334 天；
- 紧急购电量：按连续事件重建；
- 保存后重新读取并独立核对；
- writer/display 不得反向改变 solver 结果。

## 15. Stop / Return 条件

出现任一情况，停止 candidate Freeze 流程并回 FYQ/XXT：

- hard/accounting/unit violation；
- future actual leakage；
- S1 w/v conflation；
- formal period unexpected n=0 risk history；
- alpha 或 delayed-actual materially 改变主策略排序；
- `TAIL_CHALLENGER_REQUIRED = TRUE`；
- S1 `w` materially 驱动可行性/优势；
- result2 readback failure；
- provenance 不完整；
- 实现对数学合同发生 material drift。

## 16. 最终 Gate 路径

`Astra core engine`
→ `FYQ Sol evidence campaign / technical review`
→ `XXT current-version Mathematical Review`
→ `Evidence Gate`
→ `Q2 Freeze decision`
→ `Paper Handoff to CYQ`

Freeze 前禁止：

- 把 candidate number 当 Paper fact；
- 宣称 `Q2_MATHEMATICAL_RESULT_PASS = TRUE`；
- 宣称 `Q2_FROZEN = TRUE`；
- 为论文叙事方便修改数学合同或结果。

## 17. 本计划冻结结论

当前冻结结论：

`Q2_MODELING_PLAN_FREEZE = PASS`

冻结内容：
- modeling family；
- authority chain；
- information set；
- strategy matrix；
- S1/accounting；
- storage dynamics；
- sensitivity/diagnostic matrix；
- Astra/Sol responsibility split；
- validation gates；
- candidate→XXT→Freeze 路径。

未冻结内容：
- 任何 Q2 最终数值；
- 最终 winning strategy；
- result2 正式文件；
- Mathematical PASS；
- Q2 Result Freeze；
- Paper-ready claim。

以上未冻结项只能由真实执行与后续 Gate 决定。

# XXT TASK｜Q2 Authority Completion + Pre-Validation R0

- `ACTIVE_ROLE = XXT_MATHEMATICAL`
- 模块：2026 CUMCM C题 Q2
- 模式：FORMAL MATHEMATICAL AUTHORITY COMPLETION / NO FULL-YEAR SOLVE
- Astra：不要求
- 禁止：正式全年求解、正式 result2、Q2 Freeze、修改 Q1 Frozen

## 0. First action

每次开始本任务前 fresh 读取 canonical：
1. `SKILL.md`
2. `skills/cumcm-rigorous-workflow/core/SHARED_CORE.md`
3. `skills/cumcm-rigorous-workflow/profiles/XXT_MATHEMATICAL.md`
4. `04_验收冻结/05_模型证据充分性Gate.md`
5. `03_建模与代码/05_参数选择协议.md`
6. 若写 GitHub：`06_协作与交接/06_三GPT协作与Skill共同维护.md`

## 1. Authority

按优先级读取：

1. 官方 2026 C题题面与附件；
2. merged PR #4：`支撑材料/03_中间结果/Q2/Q2_AUTHORITY_SUPPLEMENT_REQUEST_XXT_FYQ_R0.md`；
3. PR #5：`XXT_AUTHORITY/`；
4. PR #6：`FYQ_CONTROLLER/`；
5. 原始 XXT R1 package identity：
   - `CUMCM2026_C_XXT_Q2_FORMAL_OPT_SPEC_R1_DELIVERY.zip`
   - SHA256 `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`
   - CRC PASS，top-level checksum `23/23 PASS`
   - stable ID `CUMCM2026_C_Q2_MATH_CONTRACT_R1`
6. 原始 FYQ Controller package identity：
   - `CUMCM2026_C_CONTROLLER_Q2_FORMAL_SPEC_R1_REVIEW.zip`
   - SHA256 `d69fd9736a0a5736223e40f26211332534c31331afc834aa0e3ab5d0a325ccca`
   - CRC PASS，internal checksum `5/5 PASS`

Controller 已批准：
`normal_purchase_surplus_mode = S1_A_PAID_UNUSED_NORMAL_ENERGY`，并标记为 `MODELING_COMPLETION_ASSUMPTION`。

## 2. Task A — PR #5 mathematical source review

检查 PR #5 中直接可读的核心文件是否忠实对应 R1 authority：
- `XXT_Q2_FORMAL_OPT_SPEC_R1.md`
- `XXT_Q2_IMPLEMENTATION_HANDOFF_R1.md`
- `XXT_Q2_MATH_CONTRACT_MANIFEST_R1.json`
- `XXT_Q2_VALIDATOR_SPEC_R1.md`
- checksum/provenance material

输出：`PR5_MATH_AUTHORITY_REVIEW = PASS / FAIL`。

若不能重新计算原始 ZIP byte hash，应明确区分 `CONTENT/PROVENANCE REVIEW` 与 `BYTE_IDENTITY RECHECK`，不得伪报。

## 3. Task B — PR #6 mathematical drift review

只审查 PR #6 是否：
- 正确批准 S1-A；
- 没有改写 objective / hard constraints / units / 5× emergency accounting；
- 没有改变 known_at / terminal / efficiency / risk parameter semantics；
- 没有把 Controller 权限扩大成数学裁决。

输出：`PR6_MATH_DRIFT_REVIEW = PASS / REQUEST_CHANGES`。

## 4. Task C — 对 PR #4 的缺口逐项裁决

对以下项目逐条给出：`ALREADY_DEFINED_IN_R1 / NEED_SUPPLEMENT / HOLD_FOR_SOURCE`。

### C1 日前 point forecast

必须达到可直接实现的精度：
- `LAG7` 的精确公式；
- `TRAILING7_MEAN` 的精确公式；
- 逐 slot 还是跨 slot；
- 需要的历史天数；
- Jan 早期冷启动；
- 缺失/负值处理；
- 2 月 1 日可用历史；
- forecast `known_at`；
- 明确禁止 future actual。

若 R1 仅给 family 名称而没有完整公式，不得自行猜；必须从已存在的 W1/W2 authority 找到原定义，或标记 `HOLD_FOR_SOURCE`。

### C2 Q80 risk margin

核对并冻结：
- residual = `(L_actual-S_actual)-(Lhat-Shat)`，kWh；
- expanding same-slot history；
- strict `target_ts < T_d`；
- empirical nearest-rank `ceil(alpha*n)`；
- `m=max(0,Q_alpha)`；
- alpha primary `.80`；
- sensitivity `.75/.85` 必须重新规划 + full replay；
- Q80 只作为单槽无储能解析 anchor，不是全年最优证明。

如 R1 已完整定义，则标 `ALREADY_DEFINED_IN_R1`，不要重写另一套。

### C3 跨日 SOC / January / terminal

核对：Jan warm-up；Feb1 继承 Jan31 状态；每日跨日连续不 reset；primary `FREE_BOUNDED_YEAR_END`；T1 `EQ_INITIAL_6000`、T2 `GE_INITIAL_6000`；12/31 不允许跨 2026 补电。

### C4 Causal intraday controller

核对 same-slot actual 事件顺序、q 固定、未来只使用 00:00 frozen forecast、receding horizon 到当日 144、emergency 独立结算、solver fallback、fixed-storage baseline safety override。

### C5 `ONE_SLOT_DELAYED_ACTUAL`

R1 Controller 要求 Freeze 前做 sensitivity。给出严格时序和 validator 规则，但本任务不跑全年结果。

## 5. Task D — Adversarial validator cases

在 R1 的 18 项 validator 基础上，至少补/确认：
1. future actual 进入 00:00 commitment；
2. future actual 进入 risk calibration；
3. same-slot / delayed 时序错位；
4. 正常购电只按 `q_used` 付费；
5. `w` 被记为 PV curtailment；
6. emergency 重复计价或漏掉 5×；
7. daily SOC reset；
8. 中间 SOC 越界但终值合法；
9. terminal 不可达却标 PASS；
10. fixed baseline 动作放大/换方向；
11. Q2 注入 Attachment4 dynamic price；
12. alpha 改变后未重新规划 full replay。

每个 case 给出 minimal input、expected fail code、violated rule、validator field。

## 6. 是否需要 R2 supplement

若 C1–C5 存在任何 `NEED_SUPPLEMENT`，生成：
`CUMCM2026_C_Q2_XXT_MATH_AUTHORITY_SUPPLEMENT_R2.zip`

至少包含：
- `00_START_HERE.md`
- `Q2_AUTHORITY_COMPLETION_R2.md`
- `Q2_INFORMATION_SET_AND_FORECAST_SPEC_R2.md`
- `Q2_DELAYED_ACTUAL_SENSITIVITY_SPEC_R2.md`
- `Q2_VALIDATOR_ADVERSARIAL_CASES_R2.md`
- `Q2_MATHEMATICAL_REVIEW_VERDICT_R2.md`
- `SHA256SUMS.txt`

R2 必须写清：哪些条款只是补充 R1；哪些字段 supersede R1；不得无理由重构已通过的模型。

## 7. GitHub return path

若产生新文件，使用非 main branch，建议：`xxt/q2-authority-completion-r2-20260911`。

目标目录：`支撑材料/03_中间结果/Q2/XXT_AUTHORITY/`。

创建 PR，不自行 merge。

## 8. Exit status

只允许：
- `Q2_AUTHORITY_COMPLETION = PASS`
- `PASS_WITH_LIMITATION`
- `HOLD_FOR_SOURCE`
- `FAIL_MATHEMATICAL`

本任务不得输出 `Q2_MATHEMATICAL_RESULT_PASS = TRUE` 或 `Q2_FROZEN = TRUE`，因为正式全年结果尚未运行。
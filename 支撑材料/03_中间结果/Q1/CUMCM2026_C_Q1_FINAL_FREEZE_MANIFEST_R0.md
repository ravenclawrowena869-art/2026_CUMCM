# CUMCM 2026 C题 Q1 Final Freeze Manifest R0

- Freeze ID: `CUMCM2026_C_Q1_FREEZE_R0_20260911`
- Owner: FYQ Technical Orchestrator
- Mathematical Review: XXT / Astra current-version PASS
- Evidence Gate: `PASS_WITH_LIMITATION`
- Technical Pass: `TRUE`
- Mathematical Pass: `TRUE`
- Hard constraints zero violation: `TRUE`
- Metrics recomputed: `TRUE`
- Q1 model/result freeze: `TRUE`
- result1 freeze: `TRUE`

## 正式输入

- `source/附件1.xlsx`
- SHA256: `66b87134f5ecccd68184d3539bb1293ef039f9e0fdd955a589b9bfa7f227c377`
- 时域：144 × 10 min，`Δt=1/6 h`
- 时间合同：`C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`

## 正式模型

`TWO_STAGE_CONTINUOUS_LP`

Stage 1:

`min Σ_t p_t g_t`

Stage 2:

在 `Stage1 optimum + epsilon_cost` 内最小化 `Σ_t(c_t+d_t)`。

正式参数：

- `epsilon_cost = 1e-4 CNY`
- `eta_c = eta_d = 0.9`
- 储能容量 12000 kWh
- SOC `[1200,10800] kWh`
- `E0=E144=6000 kWh`
- 充放电功率上限 5000 kW，对应每 10 min 最大能量 `5000/6 kWh`
- 禁止售电；PV 富余这入 curtailment/spill

结构 challenger：mutex MILP，仅增加充/放电互斥二元变量。裁决：`LP_SUFFICIENT_MILP_AS_STRUCTURAL_VALIDATION`。

## 正式代码与交付

R2 delivery ZIP SHA256:

`a8acd57687c9a2380ab089e14c23bfec467dca7882b51f7777c9f97ed4977058`

ZIP CRC: PASS

内部 `SHA256SUMS.txt`: `146/146 PASS`

核心入口：

- `src/optimizer.py`
- `src/validator.py`
- `src/replay.py`
- `src/result1.py`
- `src/run_q1.py`

## 正式输出

`result1_candidate.xlsx`

SHA256:

`7aa49ebaeb506a25029c467cacd0c634138eda2f09e05e7527b287ae204cd964`

虽然文件名保留 candidate，Freeze 由本 Manifest 定义，不由文件名定义。

## 核心数字

- Stage-1 exact optimum: `35126.948589289634 CNY`
- Stage-2 exported schedule cost: `35126.948689289624 CNY`
- Stage-2 minus Stage-1: `0.0000999999901978299 CNY`
- No-storage baseline: `48052.046590846665 CNY`
- 相对 no-storage 节省: `12925.097901557041 CNY`
- 相对 no-storage 节省率: `26.89812155476249%`
- 同时充放电槽数: `0`
- SOC min/max: `1200 / 10800 kWh`
- terminal SOC residual: `0`
- primary energy-balance max residual: `1.1368683772161603e-13 kWh`
- primary SOC-recursion max residual: `9.094947017729282e-13 kWh`

## result1 4h 汇总

Charge kWh:

`[4500.000000, 833.333333, 4787.963043, 5286.035177, 0.000000, 5333.333333]`

Discharge kWh:

`[0.000000, 6365.840192, 1702.996983, 91.101383, 5780.131883, 2859.868117]`

SOC endpoints: `6000 → 6000 kWh`。

## 验收证据

- fresh pytest: `64 passed, 65 subtests passed`
- saved independent replay: primary / sqrt(0.9) sensitivity / no-storage all PASS
- result1 disk readback: PASS
- 144 purchase values present
- 6 组 4h charge/discharge aggregate: PASS
- sheet names / labels unchanged: PASS
- result1 maximum purchase readback diff: `4.547473508864641e-13 kWh`
- Blind Red Team: 12/12 claims MATCH，hard replay PASS
- LP vs MILP Stage-1 objective difference: `0`，MILP gap `0`

## epsilon confirmatory sensitivity

Fresh exact-environment solves:

`epsilon ∈ {1e-6,1e-5,1e-4,1e-3,1e-2} CNY`

5/5 HiGHS Optimal，5/5 hard replay PASS，所有点 simultaneous C/D=0。

相对 `1e-4`：

- `1e-6...1e-3` 最大 SOC 差 `0.0100847869 kWh`
- `1e-6...1e-3` 最大 4h aggregate 差 `0.0112053188 kWh`
- `1e-2` 最大 SOC 差 `0.1109326561 kWh`
- `1e-2` 最大 4h aggregate 差 `0.1232585068 kWh`
- 六个指定购电查询量最大差均为 `0`

裁决：`RETROSPECTIVE_CONFIRMATORY_SENSITIVITY PASS`。不得写成事前参数寻优，也不得声称 `1e-4` 是全局最优 epsilon 或 solver intrinsic tolerance。

## efficiency semantics sensitivity

正式口径：`eta_c=eta_d=0.9`。

替代语义：`eta_c=eta_d=sqrt(0.9)`，完整重求解成本 `33801.495642222006 CNY`，相对正式口径约 `-3.7733%`，最大 SOC 点差约 `623.1144864419075 kWh`。

该差异具有解释意义。论文必须明确 0.9/0.9 是本文采用的单程效率解释，并至少以简洁形式报告 sqrt(0.9) 替代语义敏感性；不得宣称效率语义对结果无影响。

## 非阻断限制

### L1 Cross-environment clean verifier

在当前 Linux / SciPy 1.17.0 环境重建时，正式 CSV 与核心数值复现；`verify_delivery --clean` 的 byte-identical JSON 比较会因 `solver_version`、runtime、authority tree hash 等环境/provenance 元数据变化而失败。替代环境与正式 Windows / SciPy 1.18.0 的公共 numeric 字段一致，替代效率 Stage-2 throughput 的最大数值差约 `7.28e-12 kWh`。

裁决：`ENGINEERING_P1 / NON-MATHEMATICAL / NON-BLOCKING_FOR_NUMERIC_FREEZE`。不要把跨环境 JSON 字节一致性误写成已经验证通过。

### L2 Legacy archive governance

PR #18 Review Artifact 报告三份 legacy ZIP 已在另一审查环境中取得并核验，且 `cumcm-rigorous-workflow-main (1).zip` 可锚定到 Git commit `7bb9a78f930c8b6b00c6fdcd50c72e5c3ead560b`。但当前 FYQ 窗口仍未直接取得 `write-update-math-modeling-paper-complete.zip` 与 `cumcm-rigorous-workflow-main (1).zip` 的原始 bytes，因此不声称本窗口已逐条完成 legacy paper coverage audit。

该治理缺口不改变 Q1 数值、模型或 result1 Freeze；它必须在最终 Paper Lock / Submission Gate 前闭合。

### L3 AI disclosure

AI Use Ledger 的 `human_verification / team_decision / human_changes / paper_location / artifact` 仍需由团队按真实情况补齐。它是最终提交阻断项，不改变本 Manifest 对 Q1 技术结果的 Freeze。

## 重开条件

仅在发现 P0 时重开，例如题意、hard constraints、单位、正式 accounting、result1 映射、可复现性或当前 Frozen 数字存在实质错误。普通论文措辞、PR #18 authority 迁移、AI disclosure 填写不得静默修改 Frozen Q1 数字。

# Q1 Frozen Status R1

Authority：`CUMCM2026_C_Q1_FREEZE_R0_20260911`

## Freeze state

- `Q1_FINAL_EVIDENCE_GATE = PASS_WITH_LIMITATION`
- `Q1_MATHEMATICAL_PASS = TRUE`
- `Q1_TECHNICAL_PASS = TRUE`
- `Q1_HARD_CONSTRAINT_REPLAY = PASS`
- `Q1_METRICS_RECOMPUTED = TRUE`
- `Q1_FROZEN = TRUE`
- `RESULT1_FROZEN = TRUE`
- `Q1_PAPER_LOCKED = FALSE`

## Formal model

`TWO_STAGE_CONTINUOUS_LP`

- 144 × 10 min，`Δt=1/6 h`
- time mapping：`C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`
- energy variables `g,c,d,u,E` in kWh
- balance：`g_t + PV_t + d_t = L_t + c_t + u_t`
- SOC：`E_t = E_{t-1} + 0.9*c_t - d_t/0.9`
- capacity：12000 kWh
- SOC：[1200,10800] kWh
- `E0=E144=6000 kWh`
- charge/discharge limit：`5000/6 kWh/slot`
- no selling；PV surplus may curtail/spill

Stage 1：`min Σ p_t g_t`

Stage 2：在全部 Stage-1 hard constraints 下，增加：

`Σ p_t g_t <= C* + 1e-4 CNY`

再最小化 `Σ(c_t+d_t)`。

结构验证：mutex MILP。正式裁决：`LP_SUFFICIENT_MILP_AS_STRUCTURAL_VALIDATION`。

## Frozen numbers

- no-storage：`48052.046590846665 CNY`
- Stage-1 exact：`35126.948589289634 CNY`
- Stage-2 exported：`35126.948689289624 CNY`
- savings：`12925.097901557041 CNY`
- savings rate：`26.89812155476249%`
- simultaneous C/D slots：`0`
- SOC min/max：`1200 / 10800 kWh`
- energy-balance max residual：`1.1368683772161603e-13 kWh`
- SOC-recursion max residual：`9.094947017729282e-13 kWh`
- terminal residual：`0`

4 h charge：
`[4500.000000, 833.333333, 4787.963043, 5286.035177, 0.000000, 5333.333333] kWh`

4 h discharge：
`[0.000000, 6365.840192, 1702.996983, 91.101383, 5780.131883, 2859.868117] kWh`

## Provenance

R2 delivery SHA256：
`a8acd57687c9a2380ab089e14c23bfec467dca7882b51f7777c9f97ed4977058`

R2 ZIP CRC：PASS；internal `146/146 PASS`。

Frozen result1 workbook SHA256：
`7aa49ebaeb506a25029c467cacd0c634138eda2f09e05e7527b287ae204cd964`

## Sensitivity / limitations

`epsilon_cost` 只可表述为人为设定的极小 cost-preserving tolerance。`1e-6..1e-2` confirmatory sensitivity 全部 hard replay PASS，不支持“1e-4 是全局最优 epsilon”或“solver intrinsic tolerance”的说法。

正式效率口径 `eta_c=eta_d=0.9`。替代 `sqrt(0.9)` 语义重求解费用 `33801.495642222006 CNY`，相对正式口径约 `-3.7733%`，最大 SOC 点差约 `623.1144864419075 kWh`。论文至少需要一句受限敏感性说明，不得完全隐藏。

Cross-environment Linux verifier 存在 solver/runtime/provenance metadata 的 JSON byte mismatch；核心 numeric fields 一致。不得声称跨平台所有 JSON byte-identical。

## Paper boundary

- 不得写 Stage 2 保证唯一解。
- 不得写 LP 天然禁止 simultaneous charge/discharge。
- 不得把 Stage-1 exact 与 Stage-2 exported cost 在全精度下混成一个数。
- 不得改变 slot mapping。
- 只有 P0 才允许重开 Frozen Q1。
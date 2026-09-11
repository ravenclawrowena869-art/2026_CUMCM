# Q1 result1.xlsx 复现说明

## 输入

- 官方附件：`附件1.xlsx`
- 官方结果模板：`result1.xlsx` 模板
- 数学 authority：`CUMCM2026_C_Q1_FREEZE_R0_20260911`

## 程序

`支撑材料/01_源程序/Q1/generate_result1.py`

## 输出

`支撑材料/result1.xlsx`

## 固定数学口径

- 144 个 10 min 槽，`Δt=1/6 h`
- `C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`
- `eta_c=eta_d=0.9`
- SOC `[1200,10800] kWh`
- `E0=E144=6000 kWh`
- 单槽充/放电上限 `5000/6 kWh`
- 无售电；允许必要弃光
- Stage 1 最小化 `Σ p_t g_t`
- Stage 2 在 `C*+1e-4 CNY` 内最小化 `Σ(c_t+d_t)`

## 当前复现验收值

- Stage-1 exact：`35126.948589289634 CNY`
- Stage-2 exported：`35126.948689289624 CNY`
- 全天购电量：`59482.69876179719 kWh`
- SOC：`6000 -> 6000 kWh`
- 4h charge：`[4500.000000, 833.333333, 4787.963043, 5286.035177, 0.000000, 5333.333333] kWh`
- 4h discharge：`[0.000000, 6365.840192, 1702.996983, 91.101383, 5780.131883, 2859.868117] kWh`

运行后必须通过脚本内 hard replay 与 workbook readback；否则不得替换正式 result1。

# Q1 Frozen R2 验证摘要

最终 authority：`CUMCM2026_C_Q1_FREEZE_R0_20260911`。本文件用于归档已经完成的独立复算/物理约束证据，不重开 Q1。

- Stage-1 exact optimum: `35126.948589289634 CNY`
- Stage-2 exported cost: `35126.948689289624 CNY`
- no-storage baseline: `48052.046590846665 CNY`
- savings: `26.89812155476249%`
- total purchase: `59482.69876179719 kWh`
- energy-balance max residual: `1.1368683772161603e-13 kWh`
- SOC recursion max residual: `9.094947017729282e-13 kWh`
- terminal residual: `0 kWh`
- simultaneous charge/discharge slots: `0`
- SOC range: `1200–10800 kWh`

两阶段 HiGHS 求解均为 Optimal；独立 validator 从持久化结果复算能源平衡、SOC 链、边界、终端和费用。正式结果文件见 `支撑材料/05求解结果/result1.xlsx`。

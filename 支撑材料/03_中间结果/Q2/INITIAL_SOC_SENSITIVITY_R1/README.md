# Q2 初始 SOC 敏感性验证 R1

> Status: **PASS**  
> Baseline: `Q2_FINAL_FROZEN_R1 / Q80_P2`  
> 仅改变参数：`2025-02-01 00:00 initial SOC`  
> 场景：4000 / 6000 / 8000 kWh

## 结论

初始 SOC 在 4000–8000 kWh 范围内变化时，Q2 全年主结论对该初值不敏感。

- 4000 kWh：全年总费用 `18,478,238.048302` 元，相对 6000 kWh 增加 `952.677778` 元，即 `+0.005156%`。
- 6000 kWh：全年总费用 `18,477,285.370524` 元，为 `Q2_FINAL_FROZEN_R1` primary。
- 8000 kWh：全年总费用 `18,476,335.953857` 元，相对 6000 kWh 减少 `949.416667` 元，即 `-0.005138%`。
- 4000 与 8000 两端场景全年总费用跨度仅 `1,902.094444` 元，约占 6000 kWh 基准全年费用的 `0.010294%`。
- 三组场景的紧急购电量均为 `1,063,979.277265 kWh`，紧急购电费用均为 `5,143,879.577698` 元，紧急购电槽数均为 `6,730`。
- 三组最终 SOC 均为 `1200 kWh`，SOC 全路径均满足 `[1200,10800] kWh`。

差异只发生在 2 月 1 日：

- 4000 kWh 场景在 `2025-02-01 13:50` 后与 6000 kWh 基准轨迹永久重合；
- 8000 kWh 场景在 `2025-02-01 14:30` 后与基准轨迹永久重合；
- 2 月 2 日起关键轨迹字段差异为 0。

因此，`2025-02-01 00:00 SOC = 6000 kWh` 作为 Q2–Q4 统一模型初始假设，不会实质决定 Q2 的全年费用、紧急购电风险或后续 SOC 轨迹。

## 实验控制

- Frozen input package: `Q2_FINAL_FROZEN_R1(2).zip`
- package SHA256: `d833565d01e1fd62a9014df624f3002afab5fd7b80c1bb936cb858be660a84e1`
- Frozen `run_q80_year.py` SHA256: `5a2ab76328a70a939ab9ada31bb7603ce5acb45d6a0c2d2a18783524f8bb8e47`
- 4000 场景只将源码第 20 行 `E0_YEAR=6000.0` 改为 `E0_YEAR=4000.0`；
- 8000 场景只将同一行改为 `E0_YEAR=8000.0`；
- Frozen forecast、residual、Q80 margin、附件1、附件2 的 SHA256 均保持一致；
- alpha=0.80、`eta_c=eta_d=0.9`、S1 accounting、Q80_P2 controller、`FREE_BOUNDED_YEAR_END` 均未改变；
- 4000/8000 两个场景均完整执行 334 天、48,096 个 10-min 槽；6000 使用已通过 clean replay 和 independent technical review 的 Frozen primary 输出。

## 独立验证

三组均通过：coverage、initial SOC、charge/discharge bounds、no simultaneous C/D、energy balance、SOC recursion/bounds、cross-day continuity、S1 bounds、emergency-last、cost independent recomputation、fallback=0、free-bounded terminal。

最大能量平衡残差约 `9.09e-13 kWh`，最大 SOC 递推残差约 `1.66e-11 kWh`。

## Paper Gate

Q2 可写“初始 SOC 假设具有较强稳健性”。

该证据**不能自动升级为 Q3/Q4 已完成敏感性验证**；Q3/Q4 若要写同样的定量稳健性结论，仍需对应正式模型的定点复核。

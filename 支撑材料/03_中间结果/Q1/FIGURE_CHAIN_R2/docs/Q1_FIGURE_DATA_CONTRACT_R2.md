# Q1 Figure Data Contract R2

状态：`FYQ_PARALLEL_TECHNICAL_CONTRACT`

Freeze ID：`CUMCM2026_C_Q1_FREEZE_R0_20260911`

## 1. Source of Truth

本合同只接受当前冻结技术源：

`Q1 R2 frozen source snapshot -> Q1_FIGURE_DATA_R2.csv -> candidate renderer -> DRAFT figure`

上游父交付包 SHA256：

`a8acd57687c9a2380ab089e14c23bfec467dca7882b51f7777c9f97ed4977058`

Freeze Manifest SHA256：

`058fd3f58327462f6d62a1080eb914b7bd1e4fced5e6081dd5a4ec6ba0b3ac16`

Paper Handoff SHA256：

`eb90da85ab4ff7fd1d493c742064dca2a113035ef07226cf18e78ab693940bab`

旧 Figure Bundle A R1 只做 regression/reference。生产 exporter 不读取旧 Figure CSV。

## 2. 时间合同

全时域固定为 144 个 10 min 槽，`dt_hours=1/6`。

- `slot_id=1`：raw `0:10`，物理区间 `(00:00,00:10]`；
- `slot_id=144`：raw `0:00+1`，物理区间 `(23:50,24:00]`；
- Figure Data 使用 `physical_start/physical_end` 描述真实物理区间；
- `time_hour_end=slot_id/6`，仅作为连续绘图横轴；
- 正式 result1 仍按 ordinal position 写入，禁止用官方显示标签反推 solver 时间。

Figure window 固定：`FULL_HORIZON`。本并行任务不执行事后选窗。

## 3. 字段合同

| 字段 | 单位 | 语义 | 冻结来源 / 生成规则 |
|---|---|---|---|
| `slot_id` | - | 1..144 canonical ordinal | `q1_schedule_long.csv` |
| `service_date` | date | 服务日占位日期 | frozen schedule |
| `raw_time_label` | text | 附件原始右端点标签 | `q1_input_long.csv` |
| `physical_start` | HH:MM | 物理起点 | frozen mapping A |
| `physical_end` | HH:MM | 物理终点 | frozen mapping A |
| `dt_hours` | h | 槽长度 | frozen output，必须等于 `1/6` |
| `time_hour_end` | h | 绘图横轴右端点 | `slot_id * dt_hours` |
| `price_yuan_per_kwh` | CNY/kWh | 电价 | frozen input |
| `load_kw` | kW | 小区负荷功率 | frozen input |
| `pv_kw` | kW | 光伏功率 | frozen input |
| `load_kwh` | kWh/slot | 槽负荷能量 | frozen input |
| `pv_kwh` | kWh/slot | 槽光伏能量 | frozen input |
| `grid_purchase_kwh` | kWh/slot | 正式 Stage-2 购电量 | frozen schedule `grid_kwh` |
| `grid_purchase_kw` | kW | 等效槽功率 | `grid_purchase_kwh/dt_hours` |
| `charge_kwh` | kWh/slot | 储能充电量 | frozen schedule |
| `charge_kw` | kW | 等效充电功率 | `charge_kwh/dt_hours` |
| `discharge_kwh` | kWh/slot | 储能放电量 | frozen schedule |
| `discharge_kw` | kW | 等效放电功率 | `discharge_kwh/dt_hours` |
| `storage_net_kw_positive_discharge` | kW | 正值放电、负值充电 | `(discharge-charge)/dt_hours` |
| `curtail_kwh` | kWh/slot | 光伏弃电 | frozen schedule |
| `soc_start_kwh` | kWh | 槽前 SOC | frozen schedule |
| `soc_end_kwh` | kWh | 槽后 SOC | frozen schedule |
| `baseline_grid_kwh` | kWh/slot | no-storage 基线购电量 | frozen baseline |
| `baseline_grid_kw` | kW | no-storage 等效购电功率 | `baseline_grid_kwh/dt_hours` |
| `slot_cost_yuan` | CNY | Stage-2 槽费用 | frozen schedule |
| `baseline_slot_cost_yuan` | CNY | no-storage 槽费用 | frozen baseline |

## 4. 强制一致性检查

生成 Figure Data 时逐槽验证：input / schedule / baseline 的 `slot_id`、时间标签、负荷、PV、电价一致；mapping A 的物理区间与 schedule 一致；购电、充电、放电、SOC 与 mapping A 一致。

整体检查：

- 144 行完整；
- `slot_id=1..144` 无缺失无重复；
- `dt=1/6 h`；
- 初始 SOC=6000 kWh，终端 SOC=6000 kWh；
- SOC 不越 `[1200,10800] kWh`；
- Figure Data 费用求和与 frozen metrics 的 Stage-2 / baseline 一致；
- exporter 源码中不存在旧 Figure CSV 依赖。

## 5. 图表接口

当前 renderer 使用同一 FULL_HORIZON 横轴分四个面板：

1. 电价，CNY/kWh；
2. 负荷、PV、优化购电功率，kW；
3. 充电、放电功率，kW；
4. SOC，kWh，包含 `E0` 与 `E144` 两个端点。

不同量纲分面显示，不使用未说明双轴。三角色 Merge Gate 已裁决正式论文视觉选择为 `SELECT_1_MAIN_FIGURE`。

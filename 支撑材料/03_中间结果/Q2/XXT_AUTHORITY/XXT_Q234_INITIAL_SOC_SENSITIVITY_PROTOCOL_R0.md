# Q2–Q4 初始 SOC 敏感性协议 R0

> Protocol ID: `Q234_INITIAL_SOC_SENSITIVITY_R0`  
> Date: 2026-09-13  
> Upstream assumption: `Q234_FEB1_INITIAL_SOC_ASSUMPTION_R0`  
> Status: `PROTOCOL_READY / FORMAL_RUN_PENDING`

## 1. 目的

检验人为设定的 `2025-02-01 00:00` 初始储电量是否 materially 影响 Q2–Q4 的成本、紧急购电与策略结论。

本实验只改变初始 SOC，不允许同时修改预测模型、风险参数、结算口径、效率、terminal mode、solver tolerance 或其他策略参数。

## 2. 三组正式同口径场景

| scenario_id | 2月1日初始 SOC | 角色 |
|---|---:|---|
| `SOC_INIT_4000` | 4000 kWh | lower alternative |
| `SOC_INIT_6000` | 6000 kWh | primary |
| `SOC_INIT_8000` | 8000 kWh | upper alternative |

三组均位于题目允许的 SOC 范围 `[1200,10800] kWh` 内。

## 3. 执行顺序

### Q2 主验证

优先在 Q2 当前最终 candidate/同一 solver 上执行三组 full-year replay：

1. 除 `initial_soc_kwh` 外，所有输入、预测、风险参数、控制策略、结算和 terminal mode 完全相同；
2. 从 2025-02-01 00:00 开始传播各自 SOC；
3. 禁止按日重置 SOC；
4. 保存 334×144 全路径 ledger；
5. 独立复算总费用与 SOC 递推。

### Q3 / Q4

若 Q2 sensitivity 表明初始 SOC 对全年结果或策略排序存在明显影响，则 Q3、Q4 必须分别补跑相同三场景。

若 Q2 显示影响仅集中于起始短期且不改变核心结论，Q3/Q4 仍须继承相同 primary=6000 假设，但可由 Controller 根据当前赛时决定是否做完整三场景或只做定点复核；不得未经说明直接声称“对 Q3/Q4 同样不敏感”。

## 4. 必存指标

每个 scenario 至少记录：

- `initial_soc_kwh`
- `normal_purchase_cost_cny`
- `emergency_purchase_cost_cny`
- `total_cost_cny`
- `emergency_purchase_kwh`
- `emergency_event_count`
- `pv_curtailment_kwh`
- `storage_throughput_kwh`
- `min_soc_kwh`
- `max_soc_kwh`
- `final_soc_kwh`
- `soc_max_violation_kwh`
- `soc_recursion_max_residual_kwh`
- `energy_balance_max_residual_kwh`
- `selected_strategy / strategy_id`
- `solver_status`
- `fallback_count`

另外保存相对 primary 的：

- `delta_total_cost_cny`
- `delta_total_cost_pct`
- `delta_emergency_kwh`
- `strategy_ranking_changed`
- `paper_conclusion_changed`

## 5. Gate

以下任一情况触发 `REVIEW_REQUIRED`：

- 任一场景违反 SOC、能量平衡或其他 hard constraints；
- 策略排序发生变化；
- 论文核心结论因初始 SOC 改变；
- 成本或紧急购电变化表现出明显结构性差异，不能仅解释为起始短期状态差异；
- 三组运行使用了不同预测、参数或 solver 配置。

不预先人为规定“变化小于某百分比就必然稳健”。最终稳健性措辞必须根据实际绝对变化、相对变化、策略排序与时间分布共同判断。

## 6. 推荐输出文件

正式运行后至少输出：

```text
initial_soc_sensitivity/
├── initial_soc_sensitivity_summary.csv
├── SOC_INIT_4000_metrics.json
├── SOC_INIT_6000_metrics.json
├── SOC_INIT_8000_metrics.json
├── initial_soc_daily_delta.csv
├── validator_report.json
├── provenance.json
└── README.md
```

如绘图，必须从上述正式输出生成，不得手填数字。

## 7. 当前执行限制

当前 main 中 Q2 状态仍为 `Q2_FORMAL_RESULT = NOT_RUN`，Q3/Q4 也尚未在 main 中形成正式全年求解结果。因此本协议现在可以冻结为**执行要求**，但不能在缺少 current full-year engine / current result package 的情况下伪造敏感性数字。

待 current Q2 formal engine 或已验收 full-year result package 进入可执行输入后，按本协议直接补跑，不需要重开模型设计。
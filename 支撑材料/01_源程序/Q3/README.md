# Q3 源程序

本目录对应问题 3 的最终冻结版本 `Q3_FINAL_FROZEN_R5_5`。

最终主线为 B1b：在 06:00、12:00、18:00 获得新光伏预报后，仅修改未执行时段，并根据历史 OOS 误差给新预报分配自适应权重。

## 文件

- `q3/`：冻结求解器、账本、验证器、插值和数据接口。
- `run_b1b_stream.py`：334 天 B1b 正式回放脚本。
- `generate_result3.py`：把正式 `per_slot_trace.csv` 和 `stage_ledger.csv` 写入官方 `result3.xlsx` 模板。
- `config/`：B1b 冻结 release 和 preregistration。

## result3.xlsx 口径

- `计划购电量`：00:00 阶段制定的 144 槽计划购电量；全天购电费为基础计划费用。
- `调整购电量`：各槽最终生效的调整后计划购电量；全天购电费列保存当日调整相关费用。
- `充放电量`：最终实际执行的充放电量，按 4 小时汇总，并给出 0:00、24:00 储电量。
- `紧急购电量`：按连续紧急购电槽合并时间段并汇总电量。

官方模板的 144 个购电槽按列位置与模型 `slot_id=1..144` 一一对应，不自行平移列。

## 生成 result3.xlsx

```bash
python generate_result3.py \
  --template result3_template.xlsx \
  --trace per_slot_trace.csv \
  --ledger stage_ledger.csv \
  --output result3.xlsx
```

正式冻结结果：

- B0 年费用：16,328,198.86 元
- B1a 年费用：15,234,132.83 元
- B1b 年费用：15,052,617.20 元
- B1b 紧急购电量：571,144.60 kWh
- 年末 SOC：1,349.51 kWh

正式模型结果以冻结输出为准；不要用临时 CSV 替换提交结果。

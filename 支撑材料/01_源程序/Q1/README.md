# Q1 源程序 — result1.xlsx

正式 authority：`CUMCM2026_C_Q1_FREEZE_R0_20260911`。

本目录脚本用于从官方 `附件1.xlsx` 与官方 `result1.xlsx` 模板重新生成问题一结果文件。正式模型为 `TWO_STAGE_CONTINUOUS_LP`：

1. Stage 1：最小化全天购电费用；
2. Stage 2：在 Stage-1 最优值 `+1e-4 CNY` 内最小化储能充放电总量；
3. `eta_c=eta_d=0.9`，SOC `[1200,10800] kWh`，`E0=E144=6000 kWh`；
4. 时间合同：`C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`；
5. 输出严格写入官方模板位置，不修改 worksheet 名称和时间标签。

## 入口

```bash
python generate_result1.py \
  --attachment1 /path/to/附件1.xlsx \
  --template /path/to/result1_template.xlsx \
  --output result1.xlsx \
  --report q1_result1_validation.json
```

运行依赖：Python 3、NumPy、SciPy、`artifact_tool`。

脚本包含 frozen-authority 数值 guard 与导出后 readback，若正式目标值、4h 充放电汇总、SOC 端点或硬约束发生漂移会直接报错，不生成可冒充正式结果的新版本。

> 注意：GitHub 中若重新生成 workbook，XLSX 二进制容器哈希可能因 writer 元数据/序列化而与历史 Frozen workbook SHA256 不同；正式数学身份由 Freeze Manifest + readback values/labels/constraints 确认。不得仅凭二进制哈希差异修改 Frozen Q1 数奷。

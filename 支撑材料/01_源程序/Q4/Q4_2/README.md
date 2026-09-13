# Q4-2 dynamic-price execution lane

状态：`IMPLEMENTED_PRE_FORMAL / FORMAL_RESULT_BLOCKED`

该目录实现 `Q4-2-FORMAL-R1` 在正式依赖到齐前允许完成的工程链：动态电价加载与时间归一化、`known_at` 因果审计、Q2 稳定接口适配、全路径状态/平衡/购电核验、result4-2 合同驱动 writer/readback，以及 formal orchestrator 的 fail-closed Gate。

## 关键边界

当前不得生成正式 `支撑材料/05求解结果/result4-2.xlsx`。正式全年重算只有在以下条件同时满足后才允许：

1. `Q4_COMMON_CONTRACT` 由 XXT 锁定；
2. FYQ Controller 给出最终 Q2 artifact SHA，且与输入完全匹配；
3. official result4-2 writer mapping 已锁定；
4. formal price lane `known_at <= decision_time`，future leakage count 必须为 0。

Oracle price 只允许 `DIAGNOSTIC_ONLY / FUTURE_LEAKAGE_BY_DESIGN`，formal writer 会拒绝 oracle lane。

## 结构

- `q4_2_core/contracts.py`：合同与 formal dependency Gate。
- `q4_2_core/io_adapters.py`：CSV/XLSX 动态电价 loader、右端点 slot 归一化、Q2 upstream adapter。
- `q4_2_core/validation.py`：causality、balance、SOC、跨时段连续性、功率、售电与 accounting 独立复算。
- `q4_2_core/writer.py`：合同驱动 workbook writer/readback；formal 模式 fail closed。
- `q4_2_core/orchestrator.py`：TEST_ONLY preflight 与 gated formal orchestration。
- `tests/fixtures/*TEST_ONLY*`：仅用于接口/失败路径测试，不得进入正式结果。

## 验证

```bash
cd 支撑材料/01_源程序/Q4/Q4_2
pytest -q
python tests/run_fixture_preflight.py
```

`tests/run_fixture_preflight.py` 只生成 `result4-2.TEST_ONLY_DRY_RUN.xlsx` 和 preflight JSON。其内容不代表比赛正式结果。

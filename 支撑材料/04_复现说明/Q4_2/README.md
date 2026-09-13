# Q4-2 复现说明 R1

当前只允许复现工程 preflight，不允许复现正式全年结果。

```bash
cd 支撑材料/01_源程序/Q4/Q4_2
python -m pip install -r requirements.txt
pytest -q
python tests/run_fixture_preflight.py
```

2026-09-13 对当前分支源码与测试进行 fresh reconstruction 后，`pytest -q` 实测为 `13 passed in 0.45s`。对应证据见 `支撑材料/03_中间结果/Q4/Q4_2/PREFLIGHT_R0/VERIFICATION_20260913_R1.md`。

TEST_ONLY dry-run 的当前验收条件为：`preflight_status=PASS_TEST_ONLY`、`formal_result_ready=false`、future leakage count=0、writer/readback PASS。TEST_ONLY workbook 只用于工程链复现，不属于比赛正式结果。

正式复现入口必须等 XXT-locked common contract 与 Controller-approved final Q2 SHA 到齐后，调用 `q4_2_core.orchestrator.run_formal_q4_2`。该函数会在调用 strategy runner 前校验 formal dependency Gate，并拒绝 TEST_ONLY contract。

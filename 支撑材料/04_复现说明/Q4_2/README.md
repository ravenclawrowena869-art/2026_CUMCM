# Q4-2 复现说明 R0

当前只允许复现工程 preflight，不允许复现正式全年结果。

```bash
cd 支撑材料/01_源程序/Q4/Q4_2
python -m pip install -r requirements.txt
pytest -q
python tests/run_fixture_preflight.py
```

本地 expanded regression suite 的 fresh verification 为 `17 passed`。TEST_ONLY dry-run 应满足 `preflight_status=PASS_TEST_ONLY`、`formal_result_ready=false`、future leakage count=0、writer/readback PASS。

正式复现入口必须等 XXT-locked common contract 与 Controller-approved final Q2 SHA 到齐后，调用 `q4_2_core.orchestrator.run_formal_q4_2`。该函数会在调用 strategy runner 前校验两个 Gate，并拒绝 TEST_ONLY contract。

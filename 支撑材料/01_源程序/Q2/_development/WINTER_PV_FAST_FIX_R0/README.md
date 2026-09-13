# Q2 Winter-PV Fast-Fix R0 源码快照

本目录保存 2026-09-13 Q2 Winter-PV Fast-Fix 的**源码级开发快照**。目的：把核心实现纳入 Git 版本控制，避免 104 MB Delivery ZIP 无法直接进入普通 GitHub 文件流。

## 来源与完整性

- Source Delivery: `CUMCM2026_C_Q2_FYQ_WINTER_PV_FAST_FIX_R0_DELIVERY.zip`
- Source Delivery SHA256: `011f1d0d64e4aa578a1c5f377b26ac5585d9317f807f9ffe89132b462d48ea36`
- Frozen runner SHA256: `5a2ab76328a70a939ab9ada31bb7603ce5acb45d6a0c2d2a18783524f8bb8e47`
- Selected F1 forecast SHA256: `ed198712edfbaddbd0f5d620a6f4dd5f976a49034836ad2b45bc6254a549de9a`
- XXT Phase B: `PROMOTE_P3_AMPCORR_TO_M3_REPLAY / PASS WITH LIMITATION`

## 本目录保留什么

保留正式技术链所需的源码、脚本、配置、测试、runbook、环境与 provenance。104 MB Delivery 中占绝大多数空间的年度 CSV ledger、调试输出、图和非正式历史结果不作为“源程序”重复入库。

正式 Fast-Fix 代码链以以下文件为核心：

- `frozen_runner/run_q80_year.py`
- `src/winter_fastfix.py`
- `src/exact_runner_adapter.py`
- `scripts/generate_ampcorr_candidates.py`
- `scripts/run_exact_common_worker.py`
- `scripts/run_exact_oracle_worker.py`
- `config/winter_fastfix_config.json`

其中 Oracle 仅用于诊断，禁止作为 deployable candidate。

## 当前边界

此目录是 **development source snapshot**，尚不是最终赛方提交版 Q2 源程序。最终提交版还必须合入：

1. F1_K7 的正式 M3/SP replay 实现与最终配置；
2. q 风险参数最终裁决；
3. `result2.xlsx` writer/readback；
4. 从 `submission_mirror/` 执行的 clean replay。

最终 Q2 代码闭合后，应把唯一正式版本整理到 `支撑材料/01_源程序/Q2/`，并从 Submission Mirror 复现论文与 `result2.xlsx`。本 `_development/` 目录不进入最终提交镜像。

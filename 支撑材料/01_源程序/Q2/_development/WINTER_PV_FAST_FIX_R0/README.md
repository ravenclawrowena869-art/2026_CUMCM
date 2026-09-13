# Q2 Winter-PV Fast-Fix R0 源码快照

本目录保存 2026-09-13 Q2 Winter-PV Fast-Fix 的**源码级开发快照**。目的：把核心实现纳入 Git 版本控制，避免把 104 MB Delivery ZIP 当成一个不可审阅的大文件塞进源码目录。

## 来源与完整性

- Source Delivery: `CUMCM2026_C_Q2_FYQ_WINTER_PV_FAST_FIX_R0_DELIVERY.zip`
- Source Delivery SHA256: `011f1d0d64e4aa578a1c5f377b26ac5585d9317f807f9ffe89132b462d48ea36`
- Frozen runner SHA256: `5a2ab76328a70a939ab9ada31bb7603ce5acb45d6a0c2d2a18783524f8bb8e47`
- Selected F1 forecast SHA256: `ed198712edfbaddbd0f5d620a6f4dd5f976a49034836ad2b45bc6254a549de9a`
- XXT Phase B: `PROMOTE_P3_AMPCORR_TO_M3_REPLAY / PASS WITH LIMITATION`

## 为什么不提交 104 MB Delivery ZIP

该 Delivery 的主要体积来自年度 slot-level CSV、solver/evidence ledger、图和调试历史。它们属于证据与中间结果，不等于赛方要求的“完整源程序”。源码应以普通 Git 文件形式保存，便于审阅、diff、复现和最后整理。

## 正式 Fast-Fix 源码链

- `src/winter_fastfix.py`
- `src/exact_runner_adapter.py`
- `scripts/generate_ampcorr_candidates.py`
- `scripts/run_exact_common_worker.py`
- `scripts/run_exact_oracle_worker.py`
- `config/winter_fastfix_config.json`
- `tests/`
- `provenance/CODE_CHANGE_LOG.md`
- `evidence/ENVIRONMENT.txt`

Frozen common runner 原始文件为：

`authority_snapshot/FROZEN_Q2_CURRENT/run_q80_year.py`

由于当前 ChatGPT GitHub connector 不提供本地二进制/任意 raw-file 直传能力，本分支把该 30,102-byte runner 按**原始字节**分片为 `frozen_runner_chunks/*.b64`。执行：

```bash
python rebuild_frozen_runner.py
```

会生成上述正式路径，并逐片校验 SHA256，最后强制校验整体 SHA256 必须等于：

`5a2ab76328a70a939ab9ada31bb7603ce5acb45d6a0c2d2a18783524f8bb8e47`

任何 mismatch 都会失败，不允许使用重建文件。

Oracle 代码仅用于诊断，标记 `DIAGNOSTIC_ONLY / FUTURE_LEAKAGE_BY_DESIGN`，禁止作为 deployable candidate。

## 当前边界

此目录是 **development source snapshot**，还不是最终赛方提交版 Q2 源程序。最终提交版还必须闭合：

1. F1_K7 的正式 M3/SP replay 实现与最终配置；
2. q 风险参数最终裁决；
3. `result2.xlsx` writer/readback；
4. 从 `submission_mirror/` 执行 clean replay。

Q2 技术闭合后，应把唯一正式版本整理到 `支撑材料/01_源程序/Q2/`，提供单一入口 `run_q2.py`，能够从官方附件重建正式结果、生成 `result2.xlsx` 并调用 validator。本 `_development/` 目录保留作为开发 provenance，但不进入最终提交镜像。

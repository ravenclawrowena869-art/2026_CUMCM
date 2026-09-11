# 2026 CUMCM Current Artifact Registry — 2026-09-11 R1

性质：`PROVENANCE_INDEX / CURRENT_WORKING_REGISTRY`

本表用于记录当前 FYQ 窗口能够重新核验的主要技术/任务 artifact。它不是新的数学 authority；正式结论仍以 Frozen Source、current Mathematical Review、Task/Handoff 和对应 PR 为准。

| Module | Artifact | SHA256 | Integrity / status | Repository relation |
|---|---|---|---|---|
| Q1 | `CUMCM2026_C_Q1_POST_CLOSEOUT_R2_DELIVERY(1).zip` | `a8acd57687c9a2380ab089e14c23bfec467dca7882b51f7777c9f97ed4977058` | ZIP CRC PASS；internal 146/146 PASS；Q1 Freeze evidence source | Final Freeze 已签发；ZIP 本体未在本 PR 重复入库 |
| Q1 | `CUMCM2026_C_Q1_FINAL_FREEZE_MANIFEST_R0.md` | `058fd3f58327462f6d62a1080eb914b7bd1e4fced5e6081dd5a4ec6ba0b3ac16` | exact bytes rechecked | 本 PR 直接归档到 `Q1/` |
| Q1 | `CUMCM2026_C_Q1_FINAL_PAPER_HANDOFF_R0.md` | `eb90da85ab4ff7fd1d493c742064dca2a113035ef07226cf18e78ab693940bab` | exact bytes rechecked | 本 PR 直接归档到 `Q1/` |
| Q1 | Frozen result1 workbook | `7aa49ebaeb506a25029c467cacd0c634138eda2f09e05e7527b287ae204cd964` | Frozen workbook identity from Final Freeze authority | 二进制 workbook 不在本 PR 重复上传；身份由 Freeze Manifest 固定 |
| Q2 | `CUMCM2026_C_XXT_Q2_FORMAL_OPT_SPEC_R1_DELIVERY.zip` | `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561` | ZIP CRC PASS；top-level 23/23 PASS | PR #5 归档 direct-readable core authority；原 ZIP identity 保留 |
| Q2 | `CUMCM2026_C_CONTROLLER_Q2_FORMAL_SPEC_R1_REVIEW.zip` | `d69fd9736a0a5736223e40f26211332534c31331afc834aa0e3ab5d0a325ccca` | ZIP CRC PASS；internal 5/5 PASS | PR #6 归档 Controller review / S1 authorization |
| Q2 | `CUMCM2026_C_Q2_CYQ_CODEX_BOOTSTRAP_R0.zip` | `d02da13d2c825f7d73008986c6187751faa7e6c4a45a5226e2d709615e02dabb` | bootstrap package；不等于 execution release | 当前仍等待 authority completion；不得据此 self-start full-year solve |
| Tasks | `CUMCM2026_NEXT_WAVE_TASKBOOKS_20260911.zip` | `942d2471d4ee04cf0d1702c236cdfb9d6b383b78f2e61b23e548e60fecd4e907` | historical/current task bundle | 部分旧 CYQ task wording 已被后续 authority correction supersede；不得无条件重发 |
| Tasks | `CUMCM2026_USER_ACTIONS_R0.zip` | `d12b648a6e77da8ea76ca90230b5b2bbff364b2c132dbf1d6f98bf14d7d072a6` | current human coordination task | 本 PR 同步可读 MD 版本 |
| Tasks | `CUMCM2026_XXT_NON_ASTRA_TASKS_R0.zip` | `6bc9a2ba787c16a37c32f232a5ff56271e4b743566e30f9a52fecf255447c500` | current XXT Q2/Q3 non-Astra task package | 本 PR 同步可读 MD 版本 |
| Tasks | `CUMCM2026_CURRENT_ACTION_TASKBOOKS_R1_20260911.zip` | `b3c3d2e5d1dc9c1eea6edfba29091bf0364d72546874f864d0b915216a48128d` | combined current action package | 方便人工归档；正式任务以 `TASKS/` 下 MD 为 GitHub-readable copy |

## Repository gaps still open

1. PR #5 / #6 尚未 merge，因此 Q2 原始 authority / Controller readable copies 还没有进入 `main`。
2. PR #7 尚未 merge，因此本 registry、Q1 Final Freeze/Handoff、Q1-Q4 current-state summaries 与 current Taskbooks 还没有进入 `main`。
3. PR #3 仍包含 Q1 pre-Freeze working status，不得在未 reconciliation 的情况下直接 merge。
4. 不是所有大型 ZIP、Excel、测试日志都适合或能够通过当前 connector 原样入库；对于未直接入库的 binary evidence，必须至少保留文件名、SHA256、状态和对应 Frozen/Review authority。
5. Q2/Q3/Q4 尚未产生正式全年结果，因此不存在可以归档的 Frozen result2/result3/result4。

## Rule

不得把“artifact 已索引”解释成“结果已通过 Gate”。状态升级仍需对应 Technical Review、XXT Mathematical Review、independent replay 与 Evidence Gate。
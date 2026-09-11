# CUMCM2026 C题 Q2 — Astra Core Engine Burst R1

## Purpose

This package contains **only the part of Q2 that is worth spending Astra High on**.

It intentionally removes routine sensitivity sweeps, standard evidence review, final Mathematical Gate, paper work, and routine packaging from the Astra scope.

Execution node may be physically owned by CYQ, but the execution role is:

`ACTIVE_ROLE = FYQ_TECHNICAL_ORCHESTRATOR`

CYQ Paper authority is **not** active in this task.

## Current authority

Repository:
`ravenclawrowena869-art/2026_CUMCM`

PR:
`#6`

Branch:
`fyq/q2-controller-restore-20260911`

Expected authority head at task creation:
`07413d24e290804b979188aad521809e9dcba623`

Selected mathematical chain:
- original XXT Q2 R1 package SHA256:
  `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`
- FYQ S1-A Controller authorization
- XXT R2 prevalidation SHA256:
  `63c2494eac89b164830d9e26435332f6c06afedc0234ba5a05d25468f4d0a312`
- FYQ R2 execution interfaces on PR #6

PR #8 / `d22609f9...` is not in the selected formal execution chain.

## Mandatory first action

1. Fresh-read canonical `cumcm-rigorous-workflow`:
   - `SKILL.md`
   - Shared Core
   - `FYQ_TECHNICAL_ORCHESTRATOR`
   - Evidence Gate
   - Parameter Protocol
2. Read PR #6 current FYQ Controller files, beginning with:
   `支撑材料/03_中间结果/Q2/FYQ_CONTROLLER/HANDOFF_TO_CYQ_CODEX_R2.md`
3. Verify current PR #6 head.
   - If it is exactly `07413d24e290804b979188aad521809e9dcba623`, continue.
   - If it changed, inspect the diff. If authority/interface semantics changed, stop with `HOLD_AUTHORITY_DRIFT`.
4. Bind exact input bytes before solving.

## Supersession note

This package supersedes the older broad
`CUMCM2026_CYQ_Q2_FULLYEAR_EXECUTION_R1_TASK.zip`
**only with respect to Astra workload allocation**.

If that older task is already running, do not restart from zero. Keep completed valid work, but stop the Astra phase once the stop point defined in this package is reached and return the handoff to FYQ Sol.

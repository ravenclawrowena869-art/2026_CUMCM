# Q2 Execution Release R1

`ACTIVE_ROLE = FYQ_TECHNICAL_ORCHESTRATOR`

Date: 2026-09-11

## Release

`Q2_EXECUTION_RELEASE = RELEASED`

Scope:

- formal candidate full-year replay for 2025-02-01 through 2025-12-31;
- required point / fixed-storage / Q80 candidate strategy matrix;
- alpha `.75/.80/.85` full replan + replay;
- `ONE_SLOT_DELAYED_ACTUAL` full replay;
- S1 `w/v` audit;
- terminal / efficiency checks required by the mathematical contract;
- 24-h day-boundary diagnostic;
- independent constraint/accounting replay;
- official result2 writer/readback candidate generation.

## Bound authority

Base XXT R1 math package:
`0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`

XXT R2 prevalidation package:
`63c2494eac89b164830d9e26435332f6c06afedc0234ba5a05d25468f4d0a312`

S1 mode:
`S1_A_PAID_UNUSED_NORMAL_ENERGY`

Canonical authority relation:
`ORIGINAL_R1 + FYQ_S1_A + XXT_R2_PREVALIDATION`

PR #8 `d22609f9...` is not in the execution authority chain.

## Pre-run binding

Before solver execution, record from the exact bytes used:

- W2 formal causal forecast export SHA256;
- W2 residual-history interface SHA256;
- Jan31→Feb1 SOC bridge artifact SHA256;
- code/config/solver/runtime versions.

If any required input is missing, mismatched or provenance-incompatible, stop with `HOLD_INPUT_BINDING`; do not reconstruct missing data by guess.

## Required role on CYQ-owned compute

`ACTIVE_ROLE = FYQ_TECHNICAL_ORCHESTRATOR`

Machine/API ownership does not change role authority.

## Explicit non-release

This document does **not** grant:

- `Q2_MATHEMATICAL_RESULT_PASS = TRUE`;
- `Q2_FROZEN = TRUE`;
- direct Paper use of candidate numbers;
- PR merge authority.

Candidate output returns:

`CYQ Codex/Astra -> FYQ Controller review -> XXT Mathematical Review -> Evidence Gate -> Freeze decision`.

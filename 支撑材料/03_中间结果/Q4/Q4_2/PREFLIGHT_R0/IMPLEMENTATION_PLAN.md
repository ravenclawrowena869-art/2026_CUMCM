# Q4-2 Pre-Formal Execution Implementation Plan

**Goal:** Build the Q4-2 dynamic-price execution shell that is safe to test before the XXT common contract and final Q2 artifact are locked, with formal execution failing closed until both dependencies are pinned.

**Architecture:** A small Python package under `支撑材料/01_源程序/Q4/Q4_2/` separates contracts, I/O adapters, validation/accounting, workbook writer, and orchestration. The code accepts explicit contract/upstream metadata, performs causal `known_at` audits, and labels oracle use as diagnostic-only. Formal mode rejects mock/unlocked inputs and does not emit official `result4-2.xlsx` until the contract and Q2 SHA are locked.

**Tech Stack:** Python 3.13, pandas, openpyxl, pytest, stdlib hashlib/json/dataclasses.

**Authority:** `CUMCM2026_C_Q4_2_PARALLEL_EXEC_R0_TASK`, base `704d67f84d56428eb48892784579ecba6aaeb53b`, branch `fyq/q4-2-formal-r1`.

## Global Constraints

- Write only inside the task's allowed Q4-2 paths.
- No changes to Q1/Q2/Q3/Q4-3 or paper files.
- No formal annual run until `Q4_COMMON_CONTRACT` is XXT-locked and final Q2 artifact/hash is Controller-approved.
- No future dynamic price in formal lane; oracle is `DIAGNOSTIC_ONLY / FUTURE_LEAKAGE_BY_DESIGN`.
- No official `result4-2.xlsx` in this pre-formal stage.
- TDD: every production behavior is introduced after a failing test.

### Task 1: Contract and causal boundary
- Write failing tests for unlocked contract rejection, missing `known_at`, duplicate price slots, and future-price leakage.
- Implement contract parsing, dynamic-price normalization, and causality audit.

### Task 2: Stable Q2 upstream adapter
- Test field mapping, provenance, slot coordinates, bad SHA/version handling.
- Implement adapter independent of Q2 development directories.

### Task 3: Full state and accounting validator
- Test SOC recursion/bounds/power, balance, continuity, export prohibition, and independent cost recomputation.
- Implement validator driven by explicit contract parameters.

### Task 4: Writer/readback and oracle firewall
- Test formal writer rejection for oracle/unlocked/mock authority and TEST_ONLY round-trip.
- Implement contract-driven writer/readback.

### Task 5: Orchestrator and dry-run evidence
- Test TEST_ONLY preflight and FORMAL dependency failure.
- Generate non-formal evidence only.

### Task 6: Repository handoff
- Record source, preflight evidence, blockers and XXT review request on `fyq/q4-2-formal-r1`.
- Do not claim `Q4_2_FINAL_RESULT_READY_FOR_XXT` before formal dependencies and real replay exist.

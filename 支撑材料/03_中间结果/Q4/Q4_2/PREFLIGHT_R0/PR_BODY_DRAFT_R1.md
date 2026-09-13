# Q4-2 Pre-formal Engineering Lane

## Why

Prepare the Q4-2 dynamic-price execution path so formal annual replay can start immediately after XXT locks the Q4 common contract and FYQ Controller supplies the approved final Q2 artifact/hash.

## Scope

- Dynamic-price loader, provenance and timestamp/slot validation.
- Q2 upstream adapter with SHA binding.
- `known_at` causality audit and formal/oracle separation.
- Full-path validator for balance, SOC recursion/continuity, limits, no-selling and accounting.
- Fail-closed result4-2 writer/readback path.
- TEST_ONLY fixtures, tests, preflight evidence and reproduction notes.

## Verification

Fresh reconstruction of current branch source/tests on 2026-09-13:

- Python 3.13.5
- numpy 2.3.5
- pandas 2.2.3
- openpyxl 3.1.5
- pytest 9.0.2
- `pytest -q` -> `13 passed in 0.45s`

## Status / limitations

- `Q4_2_ENGINEERING_PREFLIGHT = PASS_TEST_ONLY`
- `Q4_2_FORMAL_RESULT = BLOCKED_BY_DEPENDENCIES`
- `Q4_2_FINAL_RESULT_READY_FOR_XXT = FALSE`
- `Q4_2_FROZEN = FALSE`

No formal `result4-2.xlsx` or annual Q4-2 numbers are included. Formal execution remains blocked by the XXT-locked Q4 common contract and the Controller-approved final Q2 artifact/hash.

## Review request

FYQ engineering review: implementation/interface/fail-closed behavior.

XXT mathematical review: contract semantics, price information set, accounting, hard constraints and writer mapping authority before any formal annual execution.

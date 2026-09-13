# Q4-2 Pre-formal Review Checklist R1

Reviewer should verify:

- FORMAL_CAUSAL rejects any price row with `known_at > decision_time`.
- ORACLE_DIAGNOSTIC remains clearly non-formal.
- test-only contract cannot authorize formal orchestration or formal writer output.
- Q2 upstream SHA must equal the Controller-approved final Q2 artifact SHA before formal execution.
- dynamic price grid is complete, unique, and bound to the frozen 10-minute slot mapping.
- SOC recursion, cross-slot continuity, charge/discharge limits, balance, no-selling rule and independent accounting are replayed from the execution ledger.
- formal result writer remains blocked until official result4-2 mapping is locked.
- no formal annual numbers, result4-2 workbook, Mathematical Result PASS or Freeze are claimed by this branch.

Fresh local test evidence is recorded in `VERIFICATION_20260913_R1.md`.

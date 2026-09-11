# Astra Scope Boundary

## Astra must do

Astra High is reserved for the high-coupling engineering segment:

1. inspect the current Q2 execution interfaces and source state;
2. design / implement the reusable full-year Q2 execution engine;
3. integrate the real data → forecast → day-ahead plan → intraday recourse → SOC/accounting → validator → result2 writer path;
4. write or repair production-level tests and integration tests;
5. execute the first clean canonical 334-day full-year run;
6. run the canonical alpha=0.80 four-strategy matrix;
7. independently replay hard constraints/accounting for that canonical run;
8. verify result2 writer + saved-file readback on that canonical run;
9. return a complete code/runtime/evidence handoff that FYQ Sol can continue from without redesign.

## Astra must implement hooks for, but does NOT need to run full-year here

The engine must expose reproducible configuration switches for:

- `alpha = 0.75 / 0.80 / 0.85`;
- `CURRENT_SLOT_ACTUAL` vs `ONE_SLOT_DELAYED_ACTUAL`;
- `eta_c / eta_d`;
- year-end terminal mode:
  `FREE_BOUNDED_YEAR_END / EQ_INITIAL_6000 / GE_INITIAL_6000`;
- S1 audit reporting;
- 24-h tail/day-boundary diagnostic;
- independent accounting replay;
- known_at / leakage audit.

It is acceptable to run short pilot tests for these switches to prove that the code path exists.

## Astra must NOT spend time on

Do not run the complete final evidence campaign in this Astra burst:

- no full alpha .75 and .85 annual replay;
- no full delayed-actual annual replay;
- no full efficiency sensitivity campaign;
- no full terminal sensitivity campaign;
- no final 24-h tail decision;
- no final FYQ Controller verdict;
- no XXT Mathematical PASS;
- no Freeze;
- no Paper Handoff;
- no paper prose or figure production;
- no Git merge.

Those are handed back to FYQ/XXT Sol tasks.

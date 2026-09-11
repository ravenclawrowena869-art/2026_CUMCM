# Core Engine Implementation Task

## A. Pre-run binding

Before solve, record exact SHA256 and provenance for:

- official problem package / C题.pdf / Attachment1 / Attachment2 / result2 template;
- `FYQ_W2_FORMAL_CAUSAL_FORECAST.csv`;
- `FYQ_W2_RESIDUAL_HISTORY_INTERFACE.csv`;
- Jan31 -> Feb1 bridge artifact;
- code/config;
- solver/runtime/package versions.

Required official fixed hashes are defined by current `Q2_INPUT_BINDING_R1.json`.

If W2, residual history, or bridge bytes are unavailable or mismatched:
return `HOLD_INPUT_BINDING`.
Do not synthesize replacements.

## B. Required reusable engine components

The implementation must have explicit, testable modules or equivalent separations for:

1. official input loader + schema gate;
2. causal forecast adapter;
3. residual-history / risk-margin adapter;
4. day-ahead planner:
   - `POINT_DA_LP_R1`
   - `SIGNED_RESIDUAL_Q80_MARGIN_R1`
5. storage controllers:
   - `Q2_RH_FIXED_Q_LP_R1`
   - `DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE`
6. SOC state propagation with no daily reset;
7. S1-A source-resolved accounting:
   `q_DA - w + r + PV + d = L + c + v`
8. billing:
   `sum(p*q_DA) + sum(5*p*r)`
9. full-path validator;
10. known_at / leakage validator;
11. daily + slot-level evidence ledger;
12. result2 writer;
13. saved result2 readback checker;
14. configuration layer for later Sol-run sensitivities.

## C. Canonical Astra execution

Run the primary configuration:

- formal period: Feb 1–Dec 31, 334 days, 48096 slots;
- January only as causal warm-up / state bridge;
- alpha = 0.80;
- eta_c = eta_d = 0.9;
- primary storage timing = CURRENT_SLOT_ACTUAL;
- terminal = FREE_BOUNDED_YEAR_END;
- S1 = `S1_A_PAID_UNUSED_NORMAL_ENERGY`.

Run all four strategy combinations:

1. point DA × causal intraday recourse;
2. point DA × fixed-storage safety-override;
3. Q80 DA × causal intraday recourse;
4. Q80 DA × fixed-storage safety-override.

Each policy must advance its own SOC trajectory.

## D. Canonical-run validation

For the first full clean run, independently replay at least:

- date/slot coverage;
- q_DA immutability;
- balance;
- w<=q_DA;
- v<=PV;
- no selling;
- no emergency charging;
- charge/discharge limits;
- SOC recursion;
- full-path SOC bounds;
- cross-day continuity;
- terminal mode;
- known_at / future actual leakage;
- normal and emergency cost;
- total cost recomputation;
- result2 ordinal mapping;
- saved workbook readback.

Do not claim Mathematical PASS. This is a technical core-engine proof only.

## E. Code quality expectations

- no mock/stub/placeholder in the real execution path;
- no hard-coded formal outputs;
- deterministic config and reproducible commands;
- tests must cover normal + failure paths;
- errors must fail closed where authority requires it;
- formal code path must be traceable from config/input to saved result2.

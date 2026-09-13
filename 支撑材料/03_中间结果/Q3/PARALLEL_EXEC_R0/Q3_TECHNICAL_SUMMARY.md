# Q3-FORMAL-R1 Technical Summary — Interim Execution

## 1. Authority / state

Task base `704d67f84d56428eb48892784579ecba6aaeb53b` was verified. Canonical workflow files were fresh-read under `ACTIVE_ROLE=FYQ_TECHNICAL_ORCHESTRATOR`.

Latest visible shared Q3 state remains:

`CONTRACT_PREFLIGHT_ONLY / FORMAL_RESULT_NOT_RUN / Q3_FROZEN=FALSE`.

The latest visible XXT mathematical artifact is `XXT_Q3_MATH_CONTRACT_PREFLIGHT_R2`, status `PASS_WITH_LIMITATION / PRE-IMPLEMENTATION`. No repository artifact named/serving as `Q3_CONTRACT_LOCKED_FOR_FYQ` was found. Therefore formal annual metrics and `result3.xlsx` were intentionally not generated.

## 2. Implemented now

The contract-independent engine now contains:

- canonical 144-slot right-endpoint mapping;
- 00/06/12/18 decision-stage masks;
- causal PV hourly-to-10min adapter with linear-boundary primary and block-hold sensitivity transform;
- append-only active-commitment ledger;
- previous-active delta identities and replay audit;
- hard guards against future information and executed-slot mutation;
- battery/SOC full-path replay with energy-balance, bound and bridge diagnostics;
- isolated settlement module with formal-contract hard gate;
- result3 plan/final-active projection plus template-bound writer/readback interfaces with hard gate;
- baseline/rolling ablation schema;
- toy fixture for infrastructure tests only.

## 3. Local verification

`pytest`: **9 passed**.

Toy-fixture checks pass for ledger chronology, future leakage=0, executed-slot mutation=0, delta identity replay, physical balance, SOC bounds and bridge continuity. The toy accounting numbers are synthetic unit-test values and are explicitly tagged `NOT_A_FORMAL_Q3_METRIC`.

Formal entry points were also tested negatively: formal annual run, formal accounting and result3 writing all raise while `locked_for_fyq=false`.

## 4. What is still blocked

No claim is made that Q3 is FEASIBLE / COMPETITIVE / NEAR-OPTIMAL on official annual data. The following are still `NOT_RUN_FORMAL`:

- official Attachment 1/2/3 load;
- formal controller/optimizer run;
- annual 00-only vs 00+06+12+18 comparison;
- formal accounting recomputation;
- full-year SOC replay;
- required settlement/reference/interpolation/initial-SOC sensitivities;
- result3 projection to the official workbook and readback;
- Mathematical Result PASS / Freeze.

## 5. Exact continuation rule

Once a hash-pinned `Q3_CONTRACT_LOCKED_FOR_FYQ` is available, bind it without redesigning the model family, bind the official inputs/template, run baseline and rolling candidate under the same accounting contract, execute the full validator and sensitivities, and only then create `result3.xlsx`.

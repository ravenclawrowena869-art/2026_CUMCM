# TASK — Q4 FYQ Engineering Preflight R1

`ACTIVE_ROLE=FYQ_TECHNICAL_ORCHESTRATOR`

Recommended model: `GPT-5.6 Sol / High` for contract integration; routine coding may be delegated after XXT price semantics return.

## Allowed prework now

- parse and hash Attachment4;
- align dynamic prices to canonical 10-min slot ids;
- build `target_ts / known_at / vintage_id / source` schema;
- implement causal LAG7 price baseline adapter;
- build oracle-price adapter explicitly tagged `ORACLE_DIAGNOSTIC_ONLY`;
- build causal-vs-oracle leakage tests;
- prepare Q4-2 and Q4-3 inherited model adapters without changing Q2/Q3 mathematics;
- prepare result4-2/result4-3 writer/readback scaffolds;
- prepare Figure Data and validator schemas.

## Hard restrictions

- future Attachment4 realized price cannot enter a deployable earlier decision unless XXT/official authority explicitly permits it;
- no formal Q4 full-year solve before the price contract is accepted;
- no new complex forecasting model until LAG7 is benchmarked causally and a concrete defect is shown;
- no change to Q2/Q3 Frozen/accepted accounting just to make Q4 easier.

## Baseline evidence to reproduce

At minimum evaluate causally from Feb-Dec:
- LAG1;
- LAG7;
- trailing-7 same-slot mean;
- same-weekday recent-history mean.

Report MAE/RMSE/WAPE/Bias and downstream-ready provenance. Model selection must not use future test months to retroactively alter earlier policy families.

## Required tests

- canonical slot mapping exact;
- `known_at<=decision_time`;
- oracle rows rejected by deployable decision reader;
- future realized prices cannot leak through joins/backfill;
- Q4-2/Q4-3 inherited storage/SOC interfaces unchanged;
- result4 writers preserve template structure.

## After XXT price spec

Implement only the accepted settlement/information contract, then compare causal baseline/challenger and oracle diagnostic through full Q4-2/Q4-3 replay.

## Output

Before XXT returns:
`CUMCM2026_C_Q4_FYQ_ENGINEERING_PREFLIGHT_R1_DELIVERY.zip`

Status:
`Q4_ENGINEERING_SCAFFOLD_READY_WAITING_XXT_PRICE_SPEC`.

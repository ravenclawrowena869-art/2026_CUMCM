# Q3 Design-Stable Candidate R1

Status: `DESIGN_STABLE_CANDIDATE / FORMAL_RESULT_NOT_RUN`

This file advances Q3 architecture only. It does not grant Mathematical PASS, Evidence PASS, Freeze, or formal result authority.

## Stable contract inherited from XXT preflight

- canonical 10-min slot mapping unchanged;
- decision stages: 00:00 / 06:00 / 12:00 / 18:00;
- slots already executed at a stage are immutable;
- every forecast/action must satisfy `known_at <= decision_time`;
- primary adjustment reference: `PREVIOUS_ACTIVE_COMMITMENT`;
- primary settlement price-time assumption: `DELIVERY_SLOT_PRICE`;
- base plan cost counted once;
- adjustment settlement uses signed increase/decrease against the previous active commitment;
- emergency purchase remains a separate 5x ledger;
- result3 adjusted purchase projects the last active commitment before execution;
- all stage vintages remain internal evidence.

## Recommended controller candidate

`ROLLING_HORIZON_LP_CANDIDATE_R0`

Rationale:
- commitment delta decomposition is linear;
- battery energy balance and SOC are linear;
- only future slots are reoptimized;
- the model can reuse Q1/Q2 validator and accounting infrastructure;
- it is easier to audit than heuristic/RL alternatives;
- external microgrid literature supports day-ahead + intraday rolling/MPC architecture, but literature parameters/results are not transferred.

This controller remains a FYQ candidate until XXT formally reviews the exact objective and constraints.

## Baseline matrix

At minimum compare:
1. `00_ONLY`
2. `00_06`
3. `00_06_12`
4. `00_06_12_18`

Use identical physical/accounting semantics.

Primary outputs:
- total cost;
- normal-plan cost;
- adjustment cost;
- emergency cost/energy;
- full SOC feasibility;
- forecast error on remaining targets.

## Mandatory semantics before Freeze

1. `PREVIOUS_ACTIVE_COMMITMENT` vs coherent `FINAL_VINTAGE_VS_ORIGINAL_00` comparator;
2. `DELIVERY_SLOT_PRICE` vs `ISSUE_TIME_PRICE` sensitivity;
3. linear causal hourly-to-10min interpolation vs endpoint block hold;
4. full SOC replay and cross-day continuity;
5. no future actual leakage.

## Current evidence direction

Official-data audit already indicates 06:00 and 12:00 forecast vintages materially improve remaining-horizon PV forecast error relative to the 00:00 vintage. This supports running rolling optimization but does not yet prove downstream cost benefit. The 18:00 stage must be judged by downstream replay because absolute PV values are already small late in the day.

## Exit needed before execution Freeze

- XXT exact Mathematical Spec;
- FYQ implementation interface;
- independent validator;
- result3 writer/readback;
- all required semantic sensitivities;
- Evidence Gate.

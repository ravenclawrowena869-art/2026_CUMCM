# TASK — Q3 XXT Formal Spec R1

`ACTIVE_ROLE=XXT_MATHEMATICAL`

Recommended model: `GPT-5.6 Sol / High`. Use higher reasoning only if the adjustment-settlement wording produces an unresolved accounting contradiction.

## Goal

Convert the existing Q3 `PASS_WITH_LIMITATION / PRE-IMPLEMENTATION` contract into an exact mathematical implementation spec without producing formal results.

## Preserve current accepted preflight

- stages 00/06/12/18;
- past-slot immutability;
- `known_at<=decision_time`;
- `PREVIOUS_ACTIVE_COMMITMENT` primary reference;
- `DELIVERY_SLOT_PRICE` primary assumption;
- linear causal PV interpolation primary;
- `FINAL_ACTIVE_COMMITMENT_PER_SLOT` result3 projection;
- battery physical layer inherited from current accepted semantics.

## Decide / specify

1. exact decision variables at each stage;
2. objective and ledger accounting, including base plan, signed adjustments, emergency purchase and storage;
3. whether the rolling controller is a pure LP under the selected semantics;
4. exact stage state passed between 00/06/12/18;
5. current-slot vs future-slot information timing;
6. treatment of storage actions when forecast vintages change;
7. no-double-billing proof for repeated revisions;
8. full validator equations;
9. coherent sensitivity definitions for reference base, price-time and interpolation;
10. whether any ambiguity is P0 or can remain `PASS_WITH_LIMITATION` pending replay.

## Candidate to review

FYQ proposes:
`ROLLING_HORIZON_LP_CANDIDATE_R0`

Do not accept it because it is simple. Accept only if the objective/constraints remain linear and the information/settlement semantics are internally coherent.

## Required baseline

`00_ONLY_NO_INTRADAY_ADJUSTMENT`

Experiment family:
- 00 only;
- 00+06;
- 00+06+12;
- 00+06+12+18.

## Required output

`CUMCM2026_C_Q3_XXT_FORMAL_SPEC_R1_DELIVERY.zip`

Include:
- Mathematical Contract;
- formula-to-ledger map;
- units/time-index table;
- validator specification;
- accepted/rejected candidate-model verdict;
- mandatory sensitivity matrix;
- FYQ implementation acceptance criteria;
- paper claim boundaries.

Exit:
- `Q3_IMPLEMENTATION_SPEC_READY_FOR_FYQ`
- or `Q3_SPEC_BLOCKED_BY_MATHEMATICAL_AMBIGUITY`.

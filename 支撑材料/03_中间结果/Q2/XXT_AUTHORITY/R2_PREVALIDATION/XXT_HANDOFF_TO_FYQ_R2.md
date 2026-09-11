# XXT → FYQ Handoff R2

## Controller-facing verdict

`Q2_PREVALIDATION_SPEC = PASS`

`Q3_CONTRACT_PREFLIGHT = PASS_WITH_LIMITATION`

No Q2/Q3 result PASS and no Freeze is granted.

## Q2 implementation requirements now locked for the prevalidator

Use the approved S1-A source-resolved variables in all formal evidence:

`q_DA - w + r + PV + d = L + c + v`

with `0<=w<=q_DA`, `0<=v<=PV`.

Billing remains:

`C_total = Σp*q_DA + Σ5p*r`.

Report `Σp*w` only as the paid-but-unused part already embedded in normal commitment cost. Do not add it again. Preserve the existing q immutability, known_at, fixed Attachment1 price, SOC full-path/cross-day, terminal-mode, risk provenance and independent accounting checks.

Correct Q2 authority package identity everywhere:

`CUMCM2026_C_XXT_Q2_FORMAL_OPT_SPEC_R1_DELIVERY.zip`

SHA256 `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`.

Before Q2 Freeze, still return current-version evidence for `ONE_SLOT_DELAYED_ACTUAL`, risk-alpha full replan/replay, S1 usage audit, terminal/efficiency sensitivities required by current contract, and the 24-h tail diagnostic. If `w` is materially large or explains the strategy advantage, return to XXT for the S1-B feasible-subset/absorption counterfactual rather than hiding it.

## Q3 implementation interface

Primary stage contract:
- adjustment reference: `PREVIOUS_ACTIVE_COMMITMENT`;
- adjustment settlement price: `DELIVERY_SLOT_PRICE`;
- PV transform: `PV_HOURLY_LINEAR_CAUSAL_BOUNDARY_V1`;
- result3 adjusted purchase: `FINAL_ACTIVE_COMMITMENT_PER_SLOT`;
- time export: `C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`.

Store every stage vintage and delta even though result3 exposes only one adjusted-purchase matrix. Slots with right endpoint at or before the 06/12/18 decision time are immutable.

Before Q3 Freeze, run full downstream sensitivities for:
- coherent original-00 comparator `FINAL_VINTAGE_VS_ORIGINAL_00`;
- `ISSUE_TIME_PRICE`;
- `PV_HOURLY_ENDPOINT_BLOCK_HOLD_V1`.

Do not implement the naive “sum every stage delta relative to the 00 plan” comparator: it double counts repeatedly revised quantities and is not a valid ambiguity sensitivity.

## Integration request

Bind these R2 files to the future implementation manifest and rerun the current implementation validator. If code changes objective, hard constraints, S1 source accounting, known_at, stage ledger, settlement formula, PV transform or SOC dynamics, prior mathematical preflight is not sufficient; return the exact current-version artifacts for XXT review.

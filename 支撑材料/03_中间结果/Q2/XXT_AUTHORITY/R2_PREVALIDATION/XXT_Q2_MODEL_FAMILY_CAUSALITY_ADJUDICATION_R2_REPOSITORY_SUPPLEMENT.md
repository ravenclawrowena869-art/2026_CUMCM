# XXT Q2 Model-Family Causality Adjudication — Repository Supplement R2

`ACTIVE_ROLE=XXT_MATHEMATICAL`

Status: `SEMANTIC_REPLACEMENT_FOR_UNAVAILABLE_R1_STANDALONE_BYTES / NO_MATH_CHANGE`

Base contract: `CUMCM2026_C_Q2_MATH_CONTRACT_R1`

## 1. Provenance boundary

The historical package checksum manifest lists `XXT_Q2_MODEL_FAMILY_CAUSALITY_ADJUDICATION_R1.md` with SHA256
`543e7184fa2dd0027042e9066ff16d33cc25c428488066ee739222105790a9fc`,
but those exact standalone bytes are not available in the current repository delivery.

This R2 supplement does **not** claim byte identity with that historical file. It exposes the currently accepted causality classification already used by the base R1 formal spec and enforced by R2 prevalidator `P16`.

PR #8 remains noncanonical and is not adopted by package identity.

## 2. Formal forecast-family classification

For Q2, the retained formal causal baseline families are:

- load: `LAG7`;
- PV: `TRAILING7_MEAN`;
- Q2 tariff: fixed Attachment1 144-slot price repeated daily.

W2 dynamic-price forecast rows are **not** Q2 consumer inputs; they belong to Q4 scope.

The formal classification is:

`FORMAL_POLICY_FAMILY = PREDECLARED_BASELINE`.

Later challenger comparisons are treated as:

`CHALLENGER_COMPARISON = OFFLINE_ADEQUACY_AUDIT`.

They may support the statement that tested challengers did not justify replacing the predeclared baseline under the registered comparison rule, but they are not information that existed on earlier simulated decision dates.

## 3. Causal consumer contract

For every simulated decision date, the Q2 forecast consumer must enforce:

- all forecast rows use the approved load/PV family identifiers;
- `known_at <= decision_time`;
- history cutoffs contain no future target actuals;
- source hashes, slot mapping and contract identifiers are preserved;
- no family chosen using later-month evaluation evidence is silently backcast into earlier dates;
- no Attachment4/dynamic-price forecast is consumed by Q2.

The R2 prevalidator must return `FAIL_PROVENANCE/LEAKAGE` if family provenance or historical cutoff evidence is incomplete.

## 4. Challenger replacement rule

A future contract may replace the predeclared family only through a causal model-selection procedure. At minimum, for each decision date `d`:

1. candidate construction, fitting and comparison use only information available before `d`;
2. the family/version is frozen before reading day-`d` actuals;
3. family/version/selection cutoff is recorded in output provenance;
4. no later-selected family is backfilled to earlier dates;
5. validation uses rolling/nested time-ordered out-of-sample replay.

## 5. Claim boundary

Allowed interpretation:

“The formal forecast layer uses preregistered simple causal baselines; later challenger experiments are offline adequacy evidence and do not create future-information access for earlier decisions.”

Not allowed:

“Later evaluation months selected a model that was then causally used from February onward.”

Current gate:

- `MODEL_FAMILY_CAUSALITY = PASS_FOR_CURRENT_PREDECLARED_BASELINES`;
- `CHALLENGER_BACKCAST_PERMISSION = NOT_GRANTED`;
- full Q2 result PASS / Freeze remain ungranted.

This file is a repository-readability supplement and does not change the base mathematical objective or hard constraints.

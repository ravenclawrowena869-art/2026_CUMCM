# CUMCM 2026 C题 — Q2 Model-Family Causality Adjudication R1

**Contract:** `CUMCM2026_C_Q2_MATH_CONTRACT_R1`  
**Verdict:** `ACCEPT_WITH_PROVENANCE_RECLASSIFICATION`

## 1. Issue

W1 used Jan–Jul history/training, Aug–Oct model comparison and Nov–Dec confirmatory testing. W2 then generated Feb–Dec outputs with the retained families. If a challenger had been selected using Aug–Oct and then back-applied to Feb–Jul, the policy family itself would contain model-selection-level look-ahead even if each forecast row used past-only features.

## 2. Current factual distinction

The retained families are exactly the simple families preregistered before challenger comparison:

- load: `LAG7`;
- PV: `TRAILING7_MEAN`;
- dynamic price: `LAG7` (not a Q2 consumer input).

Independent review found no row-level future-actual leakage in the retained forecast export, and no challenger qualified under the preregistered validation rule.

## 3. Formal adjudication

Accepted classification:

`FORMAL_POLICY_FAMILY = PREDECLARED_BASELINE`

Accepted role of the later challenger experiment:

`AUG_OCT_CHALLENGER_COMPARISON = OFFLINE_ADEQUACY_AUDIT`

Meaning:

- the family used in the simulated Feb–Dec policy is the already-declared baseline family;
- Aug–Oct/Nov–Dec comparisons are evidence that no tested challenger justified replacement under the registered rule;
- those future-month comparisons are **not** claimed to be information available on Feb1 and are not the cause of the Feb–Jul family choice.

This resolves the current provenance issue without rewriting W1 numerical history.

## 4. Q2 consumer rules

The Q2 forecast consumer may read only:

- load rows compatible with `LAG7`;
- PV rows compatible with `TRAILING7_MEAN`;
- correct `known_at`, history cutoff, source hash, time mapping and current contract identifier.

The Q2 consumer must reject W2 dynamic-price forecast rows. Q2 tariff is Attachment1 fixed repeated price.

## 5. Paper wording boundary

Allowed:

> The formal forecast layer uses preregistered simple causal baselines; later-month challenger experiments serve as offline adequacy checks and did not provide sufficient evidence to replace them.

Not allowed:

> Aug–Oct data selected the model that was then causally used from February onward.

## 6. Future challenger replacement rule

If a later contract wishes to replace a predeclared family and apply it to earlier simulated dates, it must use a causal model-selection protocol. Minimum acceptable repair:

1. for each decision date `d`, construct the candidate set using only data with target timestamp `< d 00:00`;
2. fit/tune/compare only on past training/validation windows;
3. freeze the family for day `d` before reading day-`d` actuals;
4. record family/version/selection cutoff in each output row;
5. never backfill a family chosen from later months into earlier decisions;
6. validate with rolling/nested out-of-sample replay.

## 7. Gate state

`MODEL_FAMILY_CAUSALITY = PASS_FOR_CURRENT_PREDECLARED_BASELINES`  
`ROW_LEVEL_FORECAST_LEAKAGE = PREVIOUSLY_REVIEWED_PASS`  
`CHALLENGER_BACKCAST_PERMISSION = NOT_GRANTED`

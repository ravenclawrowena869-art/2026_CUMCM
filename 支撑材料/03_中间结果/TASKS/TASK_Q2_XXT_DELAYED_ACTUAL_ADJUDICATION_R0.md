# TASK — Q2 XXT Delayed-Actual Mathematical Adjudication R0

`ACTIVE_ROLE=XXT_MATHEMATICAL`

Recommended model: `GPT-5.6 Sol / High or Extra High`. Escalate to Astra only if the information-timing / source-accounting semantics cannot be decided safely from current authority.

## Scope

Adjudicate one narrow blocker only:

`ONE_SLOT_DELAYED_ACTUAL` + S1-A source-resolved accounting can produce:

`S1_A_W_EXCEEDS_Q:29.63833333333332>0.0`

on the Q80 + rolling path.

Do not redesign Q2. Do not alter CURRENT_SLOT_ACTUAL canonical results. Do not select a new main model.

## Authority

- official C question and attachments;
- `CUMCM2026_C_Q2_MATH_CONTRACT_R1`;
- FYQ S1-A controller authority;
- Q2 R2 prevalidation;
- Q2 Core Engine Fallback R1 Delivery;
- canonical Shared Core / Evidence Gate.

## Reproduced mechanism

Under delayed information, a storage action is selected from the frozen forecast before current actual load/PV is available. A planned discharge can become a realized surplus after actual revelation. Current S1-A provides only:

`q_DA - w + r + PV + d = L + c + v`

with:
- `0 <= w <= q_DA`;
- `0 <= v <= PV`;
- no selling/export.

If `q_DA=0` and realized surplus contains discharged battery energy beyond PV curtailment, the accounting requires `w>0` although `w<=q_DA=0`. Current implementation correctly fails closed.

## Questions for Mathematical verdict

1. Is the delayed sensitivity itself infeasible under the currently authorized physical/accounting model for such slots?
2. Is a safety clipping rule for an already selected delayed-information battery action mathematically legitimate, or would it reintroduce current-slot actual information into the action and defeat the sensitivity?
3. May discharged battery energy be curtailed/spilled under the official problem and selected S1-A contract? If not explicitly authorized, do not invent it.
4. Is adding export/sale forbidden under current authority? Assume yes unless official text proves otherwise.
5. Should `ONE_SLOT_DELAYED_ACTUAL` be adjudicated as:
   - a valid sensitivity that may return infeasible/fail-closed;
   - a sensitivity requiring a specifically defined physical safety override;
   - or an invalid/ill-posed timing semantics under the current model?
6. Does the answer affect the primary CURRENT_SLOT_ACTUAL model, or only the robustness/limitation claim?

## Required evidence

- reproduce or inspect the exact failing slot;
- write the slot-level source balance before and after the delayed locked action;
- identify which physical source creates the unmatched surplus;
- show whether each candidate repair preserves the information set and official energy semantics;
- explicitly reject any repair that changes objective/accounting/hard constraints without authority.

## Required output

Return:
`CUMCM2026_C_Q2_XXT_DELAYED_ACTUAL_ADJUDICATION_R0_DELIVERY.zip`

Verdict must be one of:
- `DELAYED_ACTUAL_VALID_WITH_DEFINED_SAFETY_RULE`
- `DELAYED_ACTUAL_VALID_BUT_CAN_BE_INFEASIBLE`
- `DELAYED_ACTUAL_SEMANTICS_REJECTED_AS_ILL_POSED`
- `MATHEMATICAL_P0_AFFECTS_PRIMARY_Q2`

Also state:
- whether primary CURRENT_SLOT_ACTUAL remains mathematically unaffected;
- exact implementation change, if any, that FYQ may make;
- which full replays must be rerun;
- paper claim boundary.

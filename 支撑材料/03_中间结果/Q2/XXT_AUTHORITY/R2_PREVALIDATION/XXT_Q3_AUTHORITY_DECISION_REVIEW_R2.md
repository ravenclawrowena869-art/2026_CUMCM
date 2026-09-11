# XXT Review of FYQ Q3 Authority Decisions R2

`ACTIVE_ROLE=XXT_MATHEMATICAL`  
Scope: mathematical consistency review only; no Q3 algorithm selection, no formal result, no Freeze.

## H-Q3-01 — adjustment reference base

FYQ primary: `PREVIOUS_ACTIVE_COMMITMENT`.  
XXT verdict: **ACCEPT / PASS_WITH_LIMITATION**.

For stage `s` and still-unexecuted delivery slot `t`, define

`Δ+_{s,t}=max(q^s_t-q^{s-1}_t,0)`

`Δ-_{s,t}=max(q^{s-1}_t-q^s_t,0)`.

Using the immediately previous active commitment is internally consistent and prevents charging/refunding the same quantity repeatedly when a slot is revised at multiple stages. Past/executed slots are immutable.

Required internal ledger remains:
`stage_id, decision_time, target_slot, old_active_commitment, new_commitment, delta_plus, delta_minus`.

Mandatory ambiguity sensitivity is retained. **Clarification:** an `ORIGINAL_00_PLAN` comparator must not add every stage's delta-versus-00 bill cumulatively, because that would double count repeatedly revised quantities. The coherent sensitivity comparator is `FINAL_VINTAGE_VS_ORIGINAL_00`: for each delivery slot, compare the last commitment in force before execution with the 00:00 plan and settle that reference difference once. The primary stagewise ledger remains unchanged.

## H-Q3-02 — settlement price time

FYQ primary: `DELIVERY_SLOT_PRICE`.  
XXT verdict: **ACCEPT / PASS_WITH_LIMITATION**.

For Q3, the official day tariff is a known time-of-use curve, so using delivery-slot tariff `p_t` does not create future-price leakage. With the currently accepted accounting interpretation, stage adjustment charge is

`C_adj = Σ_{s,t}[1.5 p_t Δ+_{s,t} - 0.5 p_t Δ-_{s,t}]`.

The 00:00 base normal-purchase cost is counted once. Emergency purchase remains a separate 5× shortage settlement, so adjustment and emergency ledgers must not overlap.

Mandatory sensitivity: replace `p_t` in the adjustment ledger by the tariff at stage issue time, `p(issue_s)`, while keeping quantities and all other semantics explicit. The primary choice is a modeling-completion assumption; it is not claimed to be uniquely forced by wording.

For Q4 dynamic price, ex-post settlement price and information available to a decision must be separated: a future realized delivery price may not enter an earlier decision unless it was actually known/forecast under the Q4 information contract.

## H-Q3-03 — hourly PV forecast to 10-min grid

FYQ rule: `PV_HOURLY_LINEAR_CAUSAL_BOUNDARY_V1`.  
XXT verdict: **ACCEPT / PASS_WITH_LIMITATION**.

The rule is causal if and only if:
- `F0` is the already-realized PV boundary value at issue time `tau`, not a future slot value;
- only forecast vintage with `issued_at<=decision_time` is used;
- the stage may alter only canonical slots whose right endpoint is strictly later than `tau`;
- all interpolation happens on power before multiplying by `1/6 h`;
- missing hourly anchors are hard failures, not filled using future actual.

With nonnegative adjacent hourly PV forecasts, linear interpolation preserves nonnegativity. At 00:00, `F0` is the previous boundary value already available at that instant; at 06/12/18, the slot ending exactly at the issue time is already executed and frozen.

Mandatory sensitivity is retained using explicit `PV_HOURLY_ENDPOINT_BLOCK_HOLD_V1`: for right endpoint `r` with `u=(r-tau)/1h` and `h=ceil(u)`, use `F_h` for `0<u<=24`; exact hour boundaries use their corresponding `F_h`. It uses the same forecast vintage and no future actual. Compare downstream cost/emergency/SOC and any conclusion about whether additional forecast times are useful.

Writer/validator must bind a transform implementation/config hash.

## H-Q3-04 — result3 adjusted-purchase output

FYQ primary: `FINAL_ACTIVE_COMMITMENT_PER_SLOT`.  
XXT verdict: **ACCEPT**.

The official single adjusted-purchase matrix cannot preserve all 06/12/18 vintages. Writing the last authorized commitment in force immediately before each slot executes is a coherent projection. Every stage-specific commitment/delta remains mandatory internal evidence. Export uses `C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`; human-readable template labels do not redefine physical slot identity.

## Mathematical veto check

No selected FYQ authority choice creates an unavoidable objective double count, hard-constraint contradiction, unit inconsistency or future-actual leak **when implemented with the guards above**. Therefore no targeted veto is issued.

However H-Q3-01/02/03 are not upgraded to official facts. Their required alternative-accounting / price-time / interpolation sensitivities remain hard evidence before Q3 Freeze.

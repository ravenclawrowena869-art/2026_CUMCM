# Q3 Mathematical Contract — Preflight R2

Status: `PASS_WITH_LIMITATION / PRE-IMPLEMENTATION`.  
No Q3 formal result is produced here.

## 1. Time / stage contract

Canonical 10-min slot mapping remains `C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`.

Decision stages each day:
- `s=0`: 00:00 day-ahead plan;
- `s=1`: 06:00 adjustment;
- `s=2`: 12:00 adjustment;
- `s=3`: 18:00 adjustment.

At stage time `tau_s`, every slot with right endpoint `<=tau_s` is already executed and immutable. Only slots with right endpoint `>tau_s` may receive a new active commitment. The stage uses only information with `known_at<=tau_s`; future actual load/PV is forbidden.

## 2. Commitment vintages and stage ledger

Let `q^s_t` be the active normal-purchase commitment for future slot `t` after stage `s`. Primary adjustment reference base:

`PREVIOUS_ACTIVE_COMMITMENT`.

For every adjusted future slot:

`Δ+_{s,t}=max(q^s_t-q^{s-1}_t,0)`

`Δ-_{s,t}=max(q^{s-1}_t-q^s_t,0)`.

Required internal stage ledger:

`date, stage_id, decision_time, target_slot, old_active_commitment, new_commitment, delta_plus, delta_minus, forecast_vintage_id, known_at_max, settlement_price_semantics, source_hashes`.

Past rows must never be rewritten.

## 3. Cost / settlement ledger

Base 00:00 normal purchase cost is counted once:

`C_plan = Σ_t p_t q^0_t`.

Primary price-time semantics: `DELIVERY_SLOT_PRICE`.

Primary adjustment ledger:

`C_adjust = Σ_{s=1..3} Σ_{t future at s} [1.5 p_t Δ+_{s,t} - 0.5 p_t Δ-_{s,t}]`.

A reduction therefore refunds only 50% of the canceled quantity's tariff under the accepted accounting interpretation; it does not erase the original plan cost. An increase is purchased at 1.5×. Repeated revisions are settled only against the previous active commitment.

Emergency cost is separate:

`C_emergency = Σ_t 5 p_t r_t`.

Total Q3 settlement candidate:

`C_total = C_plan + C_adjust + C_emergency`.

Validator must independently recompute all three components and prove no quantity is billed in both adjustment and emergency ledgers by construction error.

Mandatory price-time sensitivity before Freeze: recompute the adjustment ledger with `ISSUE_TIME_PRICE` while preserving all other rules.

Mandatory reference-base sensitivity before Freeze: use the coherent `FINAL_VINTAGE_VS_ORIGINAL_00` single-settlement comparator, not a cumulatively double-counted stagewise original-plan ledger.

## 4. PV forecast transform

Primary transform id: `PV_HOURLY_LINEAR_CAUSAL_BOUNDARY_V1`.

For forecast issue time `tau`:
- Attachment3 gives hourly power anchors `F_h`, `h=1..24`, at `tau+h h`;
- `F0` is the latest already-realized PV boundary at `tau`;
- for a remaining 10-min slot with right endpoint `r`, let `u=(r-tau)/1h`;
- integer `u`: use `F_u`;
- otherwise `h=floor(u)` and `P_hat(r)=F_h+(u-h)(F_{h+1}-F_h)`;
- convert after interpolation: `S_hat(r)=P_hat(r)/6` kWh.

Guards:
- `0<u<=24` only;
- forecast vintage `issued_at<=decision_time`;
- no future actual except the already-realized `F0` boundary;
- slot with right endpoint exactly `tau` is past and not adjusted;
- missing required anchor => hard input failure;
- transform implementation/config hash stored in manifest and each forecast-vintage provenance record.

Mandatory transform sensitivity: `PV_HOURLY_ENDPOINT_BLOCK_HOLD_V1` on the same forecast vintages.

## 5. Storage / physical layer

Q3 reuses the accepted battery physical constraints unless later authority explicitly changes them:
- SOC `1200..10800 kWh`;
- charge/discharge energy per 10-min slot `<=5000/6 kWh`;
- primary efficiency semantics `eta_c=eta_d=0.9`, with existing alternative sensitivity requirements preserved;
- no sale/export unless explicitly authorized;
- full SOC trajectory and cross-day continuity required;
- executed energy balance replayed independently.

The exact Q3 optimizer/controller family is **not selected in this preflight**. Any implementation must expose the stage commitment and physical actions separately so the settlement ledger is auditable.

## 6. result3 writer contract

`计划购电量`: 00:00 plan `q^0_t`.

`调整购电量`: `FINAL_ACTIVE_COMMITMENT_PER_SLOT`, i.e. the last authorized normal commitment in force immediately before the slot executes.

Internal stage vintages are never discarded merely because the official template has one adjusted-purchase matrix.

Writer uses ordinal/canonical slot mapping, not human label reinterpretation.

## 7. Validator / evidence before any Q3 result PASS

At minimum:
- stage chronology and past-slot immutability;
- `known_at` audit for every forecast/action;
- transform hash and 24-h horizon check;
- ledger delta identity and no duplicate stage billing;
- independent `C_plan/C_adjust/C_emergency/C_total` recomputation;
- energy balance, charge/discharge bounds, full SOC recurrence and cross-day continuity;
- emergency interval reconstruction;
- result3 projection back to stage ledger;
- alternative reference-base, settlement-price-time and interpolation sensitivities with full downstream replay;
- explicit test of the question's “whether additional forecast times are necessary” claim using evidence available from the permitted forecast data; unsupported hypothetical forecast accuracy may not be invented.

## 8. Exit

`Q3_CONTRACT_PREFLIGHT = PASS_WITH_LIMITATION`.

Limitations: three modeling-completion semantics require mandatory sensitivity; the formal Q3 solver and formal result have not been run or mathematically validated.

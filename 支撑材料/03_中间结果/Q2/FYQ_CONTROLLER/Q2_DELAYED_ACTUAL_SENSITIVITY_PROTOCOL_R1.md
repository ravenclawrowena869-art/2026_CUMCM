# Q2 ONE_SLOT_DELAYED_ACTUAL Sensitivity Protocol R1

Status: `FYQ_EXECUTION_PROTOCOL / REQUIRED_BEFORE_FREEZE`

This protocol implements the XXT R2 requirement for a one-slot-delayed actual-information sensitivity. It does not change the primary Q2 contract and does not grant Mathematical PASS.

## 1. Primary comparator

Primary Q2 timing keeps the accepted current-slot-actual interpretation: the current 10-min realized load/PV may affect the current-slot storage action under the disclosed modeling assumption.

Sensitivity identifier:

`ONE_SLOT_DELAYED_ACTUAL`

## 2. Exact event order

For canonical interval `I[d,t]=(tau_{t-1},tau_t]`:

1. At the storage decision for slot `t`, available actual information is limited to slots with right endpoint `<= tau_{t-1}`.
2. `q_DA[d,t]` remains the immutable 00:00 commitment and is identical to the corresponding primary-timing run.
3. Current-slot actual `L_actual[d,t]` and `PV_actual[d,t]` are **not** available when choosing `c[d,t]` / `d[d,t]`.
4. The current-slot storage action is selected using the frozen 00:00 forecast for slot `t`, current SOC and the same future 00:00 forecast horizon. No later forecast vintage is introduced.
5. After the storage action is locked, current-slot actual load/PV are revealed for physical settlement.
6. Compute actual residual using the locked storage action and source-resolved S1-A accounting:
   - `b = q_DA + PV_actual + d - L_actual - c`
   - `r = max(-b,0)`
   - `u = max(b,0)`
   - `v = min(PV_actual,u)`
   - `w = u-v`
7. Billing remains `p*q_DA + 5*p*r`; `w` is paid-unused normal commitment and `v` is PV curtailment.
8. SOC updates only from the locked storage action:
   `E_after = E_before + eta_c*c - d/eta_d`.
9. At slot `t+1`, actual information through slot `t` is available, together with `E_after`.

There is no second within-slot reoptimization after actual realization.

## 3. Slot 1 / day boundary

For `t=1`, no actual from the new day is available at the storage-decision instant. The controller uses:

- inherited cross-day SOC;
- immutable `q_DA[d,1]`;
- frozen 00:00 forecast for slot 1 and the remaining day;
- historical actuals only through the previous day's final executed slot.

No special reset or future backfill is allowed.

## 4. Replay scope

The sensitivity must be a full causal replay, not a timestamp relabel.

For every formal strategy, rerun the full Feb-Dec storage/settlement trajectory with the delayed timing while keeping fixed:

- official inputs and tariff;
- day-ahead forecasting family;
- risk-alpha definition and causal history;
- day-ahead commitment logic;
- storage parameters and efficiency mode;
- S1-A accounting;
- terminal mode;
- result mapping.

Each delayed run propagates its own SOC path.

## 5. Required evidence

At minimum compare primary timing vs delayed timing on:

- total cost;
- emergency energy/cost and slot/day count;
- normal commitment cost;
- `w` and `v` totals;
- battery throughput;
- SOC min/max/end and bound hits;
- full-path max balance/SOC residual;
- strategy ranking;
- specified-date output differences.

If the main strategy ranking or a core paper claim changes materially, stop Freeze and return current artifacts to XXT for mathematical adjudication.

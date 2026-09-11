Q2_MATH_CONTRACT_ID = CUMCM2026_C_Q2_MATH_CONTRACT_R1

# CUMCM 2026 C题 — Q2 Formal Optimization Specification R1

**ACTIVE_ROLE:** `XXT_MATHEMATICAL`  
**Contract status:** `Q2_MATH_READY_FOR_IMPLEMENTATION`  
**Purpose:** Mathematical specification / implementation release gate  
**Scope:** Q2 only. This package does **not** implement code, run the full-year optimizer, freeze Q2 results, or reopen W1.

## 0. Gate verdict

This R1 is released for implementation because the decision timing, variables, objective, storage recourse, fixed-storage baseline, risk-aware candidate, cross-day SOC, efficiency/time/terminal contracts, model-family causality and validator requirements are all specified to implementation level.

Release does **not** mean Q2 is mathematically frozen. The following remain mandatory before `FROZEN` / paper facts: full Feb–Dec causal replay, independent objective/constraint recomputation, fixed-storage baseline comparison, efficiency sensitivity, annual terminal sensitivity, risk-candidate replay and leakage audit.

No current R1 authority is silently changed. In particular:

- `time_mapping_version = C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`;
- primary efficiency `eta_c = eta_d = 0.9`;
- alternative efficiency `eta_c = eta_d = sqrt(0.9)`;
- Q2 SOC is cross-day continuous;
- primary annual terminal mode `FREE_BOUNDED_YEAR_END`;
- terminal sensitivities `E_end = 6000` and `E_end >= 6000`;
- no selling;
- emergency purchase cost is `5*c_t*r_t`;
- future actual load/PV are forbidden as decision inputs.

## 1. Time grid, units and information chronology

Let `d` denote a calendar day and `t=1,...,144` the canonical 10-minute slot. Use

\[
\Delta=\frac16\ \mathrm{h}.
\]

All optimization flow variables below are **energy per slot (kWh)**. Forecast/actual powers supplied in kW are converted by multiplying by `Delta`.

Canonical mapping is:

\[
I_{d,t}=(\tau_{t-1},\tau_t],\qquad t=1,\ldots,144,
\]

with attachment timestamp equal to the interval right endpoint. Official result-template text is display-only; solver indexing is ordinal `slot_id=1..144`.

### 1.1 Required causal sequence

```text
00:00 forecast/state known
→ normal purchase commitment q_DA[d,1:144] locked
→ each 10-min current actual load/PV realization
→ causal storage action for current slot
→ emergency purchase or spill for residual imbalance
→ SOC update
→ next slot / next day
```

### 1.2 `known_at` contract

| Stage | May use | Must not use |
|---|---|---|
| day `d` 00:00 planning | history with target time `< d 00:00`, current SOC, Attachment1 fixed tariff, day-`d` causal load/PV point forecasts, predeclared model family, past residual history | any day-`d` future actual load/PV; W2 dynamic-price forecast for Q2 |
| slot `t` recourse | all above + actual load/PV for current/past realized slots + current SOC + locked `q_DA` | actual load/PV for slots `>t`; later realized data |
| settlement / evaluation | full realized data may be read for ex-post accounting | evaluation truth may not be back-fed into earlier decisions |

The “current actual may affect current-slot storage balancing” rule is a **modeling assumption already adjudicated as reasonable**, not a claim that the problem statement explicitly says so. It must remain disclosed in the paper and controlled by the mandatory fixed-storage baseline.

Q2 settlement price is **only** Attachment1's repeated fixed tariff, known at 00:00. W2 dynamic-price forecast is `Q4_ONLY` and must be rejected by the Q2 consumer.

## 2. Constants and state

Primary constants:

- `E_cap = 12000 kWh`;
- `E_min = 1200 kWh`, `E_max = 10800 kWh`;
- `P_ch_max = P_dis_max = 5000 kW`;
- per-slot charge/discharge energy cap `X_max = 5000/6 kWh`;
- `eta_c = eta_d = 0.9` in the primary run;
- Q2 emergency multiplier `lambda_em = 5`.

State recursion for actual execution:

\[
E_{d,t}=E_{d,t-1}+\eta_c x^c_{d,t}-\frac{x^d_{d,t}}{\eta_d},
\]

\[
E_{\min}\le E_{d,t}\le E_{\max},\qquad
0\le x^c_{d,t},x^d_{d,t}\le X_{\max}.
\]

Cross-day continuity:

\[
E_{d,144}=E_{d+1,0}.
\]

For formal result2 replay, `2025-02-01 00:00` SOC is `6000 kWh`, sourced from the accepted January R14 replay bridge; it is **not** an independent February reset.

## 3. Policy P1 — point-forecast day-ahead planning baseline

Identifier:

`POINT_FORECAST_DA_PLUS_CAUSAL_INTRADAY`

At each day `d` 00:00, let `hat_l[d,t]` and `hat_s[d,t]` be the causal point forecasts of load energy and PV energy. Solve the deterministic day-ahead LP:

Decision variables for `t=1..144`:

- `q[d,t] >= 0`: normal purchase commitment (kWh), immutable after 00:00;
- `xc_ref[d,t] >= 0`, `xd_ref[d,t] >= 0`: reference storage schedule;
- `spill_ref[d,t] >= 0`;
- `E_ref[d,t]`.

Primary objective:

\[
\min \sum_{t=1}^{144} c_t q_{d,t}.
\]

Forecast balance:

\[
q_{d,t}+\hat s_{d,t}+x^{d,ref}_{d,t}
=\hat l_{d,t}+x^{c,ref}_{d,t}+spill^{ref}_{d,t}.
\]

Reference SOC:

\[
E^{ref}_{d,t}=E_{d,0}+\sum_{j=1}^{t}
\left(\eta_c x^{c,ref}_{d,j}-\frac{x^{d,ref}_{d,j}}{\eta_d}\right),
\]

subject to the same SOC and power bounds. There is **no daily terminal equality** in Q2. `E_ref[d,144]` is only bounded by `[1200,10800]`.

To remove cost-equivalent artificial charge/discharge cycles, implementation must use a lexicographic tie-break: after obtaining the minimum day-ahead purchase cost, fix that cost within numerical tolerance and minimize total reference battery throughput

\[
\sum_t(x^{c,ref}_{d,t}+x^{d,ref}_{d,t}).
\]

If the cost/throughput optimum remains non-unique, use a third lexicographic stage minimizing total absolute deviation of `q[d,t]` from the no-storage forecast purchase `max(hat_l[d,t]-hat_s[d,t],0)` (or the corresponding risk-adjusted load for P2). This is only a reproducibility tie-break and may not change the primary cost or secondary throughput optimum.

The reference trajectory is stored for audit and for the fixed-storage baseline. It is **not binding** on the causal intraday controller.

### Planning fallback

If the day-ahead LP fails technically, a safe fallback may set

\[
q_{d,t}=\max(\hat l_{d,t}-\hat s_{d,t},0),\qquad x^{c,ref}=x^{d,ref}=0.
\]

The replay may continue for diagnosis, but any use of this fallback blocks formal Q2 Freeze until the failure is resolved or separately adjudicated.

## 4. Policy P1 recourse — remaining-horizon deterministic LP

Identifier:

`CAUSAL_INTRADAY_RECEDING_HORIZON_LP`

At slot `t`, the full-day normal commitment `q[d,j]` remains fixed. For the remaining horizon `j=t,...,144`, define information-consistent load/PV energies:

\[
L^{(t)}_{d,j}=\begin{cases}
L^{act}_{d,t},&j=t,\\
\hat l_{d,j},&j>t,
\end{cases}
\qquad
S^{(t)}_{d,j}=\begin{cases}
S^{act}_{d,t},&j=t,\\
\hat s_{d,j},&j>t.
\end{cases}
\]

Q2 does **not** introduce an intraday forecast-update model. Future slots keep the day-00:00 point forecast. At the next slot the newly realized current value replaces that slot's forecast and the LP is solved again.

For each remaining slot define the pre-storage balance, which is constant inside that LP:

\[
B^{(t)}_{d,j}=q_{d,j}+S^{(t)}_{d,j}-L^{(t)}_{d,j}.
\]

Use the following direction constraints.

### Surplus slot: `B >= 0`

\[
0\le x^c_{d,j}\le \min(X_{\max},B^{(t)}_{d,j}),\qquad x^d_{d,j}=0,
\]

\[
r_{d,j}=0,\qquad spill_{d,j}=B^{(t)}_{d,j}-x^c_{d,j}\ge0.
\]

### Deficit slot: `B < 0`

\[
0\le x^d_{d,j}\le \min(X_{\max},-B^{(t)}_{d,j}),\qquad x^c_{d,j}=0,
\]

\[
spill_{d,j}=0,\qquad r_{d,j}=-B^{(t)}_{d,j}-x^d_{d,j}\ge0.
\]

Together with SOC recursion/bounds, this gives a linear remaining-horizon problem. Primary recourse objective is

\[
\min \sum_{j=t}^{144} 5c_j r_{d,j}.
\]

Among equal primary optima, minimize

\[
\sum_{j=t}^{144}(x^c_{d,j}+x^d_{d,j})
\]

as an anti-cycling tie-break. If the current-slot action is still non-unique, use a third lexicographic stage minimizing total absolute deviation from that policy's day-ahead reference storage trajectory over the remaining horizon. This is a deterministic tie-break only; it may not worsen the primary emergency-cost optimum.

Only the **current-slot** `x^c[d,t]` or `x^d[d,t]` is executed. Future LP actions are provisional and discarded at the next re-solve.

This sign-partition construction enforces by design:

- emergency is last-resort residual purchase after the allowed storage action;
- `r>0 => xc=0`;
- `r>0 => spill=0`;
- emergency energy cannot be used to charge the battery;
- no simultaneous charge/discharge;
- storage may intentionally preserve SOC instead of always maximally discharging, because the remaining-horizon emergency objective values future slots.

### Recourse solver fallback

If the remaining-horizon LP fails at slot `t`, execute a one-slot safe greedy fallback using only current information:

- if `B_t>=0`, charge `min(B_t, X_max, (E_max-E_prev)/eta_c)` and spill the rest;
- if `B_t<0`, discharge `min(-B_t, X_max, (E_prev-E_min)*eta_d)` and cover the remaining deficit with emergency purchase.

Log `fallback_used=true`. Any nonzero formal fallback count blocks Freeze unless independently shown to be mathematically equivalent to the intended policy.

## 5. Policy P2 — risk-aware candidate

Identifier:

`ANALYTIC_Q80_RESIDUAL_RESERVE_PLUS_CAUSAL_INTRADAY`

The forecast residual is defined on **net-load power**:

\[
\varepsilon_{d,t}=(L^{act}_{d,t}-S^{act}_{d,t})-(\hat L_{d,t}-\hat S_{d,t}).
\]

Positive residual means the point forecast underestimates net load.

For each decision day `d` and slot `t`, use only same-slot residuals with target timestamp strictly before `d 00:00`:

\[
\mathcal H_{d,t}=\{\varepsilon_{s,t}: target\_ts<d\ 00{:}00\}.
\]

Define the empirical nearest-rank quantile of the **full signed residual distribution**. For sorted values `e_(1)<=...<=e_(n)`,

\[
Q_\alpha(\mathcal H)=e_{(\lceil \alpha n\rceil)}.
\]

The nonnegative reserve margin in energy is

\[
m_{d,t}(\alpha)=\Delta\max(0,Q_\alpha(\mathcal H_{d,t})).
\]

### Why `alpha = 0.8` is the preregistered anchor

Ignoring storage coupling for one marginal reserve unit, normal reserve `m` costs `c*m` while uncovered positive residual costs `5c*(epsilon-m)_+`. The first-order newsvendor condition is

\[
c-5c\,P(\varepsilon>m)=0,
\]

hence

\[
F_\varepsilon(m)=1-\frac15=0.8.
\]

Therefore `alpha_star=0.80` is an **analytical economic anchor**, not a value chosen after viewing the final Q2 cost replay.

Because storage couples slots and SOC, this derivation does **not** prove that Q80 is globally optimal for the full system. It only gives a principled candidate that must pass downstream replay.

Important: W2's reported “positive-residual P80/P90/P95” are conditional quantiles **among positive residuals** and therefore are not numerically interchangeable with the full signed-distribution `Q_0.8` used here. They are tail diagnostics only.

### Risk-adjusted day-ahead LP

For P2 planning only, define

\[
\tilde l_{d,t}=\hat l_{d,t}+m_{d,t}(0.80).
\]

Use the same day-ahead LP as Section 3 with `hat_l` replaced by `tilde_l`, while PV forecast, tariff, efficiency, SOC and all other rules are unchanged. This yields risk-aware normal commitment `q_RA[d,t]` and a nonbinding reference storage trajectory.

Actual intraday execution uses **the identical** `CAUSAL_INTRADAY_RECEDING_HORIZON_LP` as P1. Future physical forecasts inside recourse remain the original point load/PV forecasts; risk protection is carried by the day-ahead commitment/state that P2 created, not by injecting future actuals.

Formal risk-parameter rules are in `XXT_Q2_RISK_PARAMETER_PROTOCOL_R1.md`.

## 6. Policy P0 — mandatory fixed-storage baseline

Identifier:

`DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE`

At 00:00 use the **same point forecast**, efficiency, terminal mode and day-ahead LP as P1, obtaining the same normal commitment `q[d,t]` and reference storage schedule `(xc_ref,xd_ref)`.

During actual execution storage is not economically reoptimized. The only permitted modification is the minimum cancellation/clipping needed for physical feasibility and for the no-emergency-charging rule.

Let

\[
B^{act}_{d,t}=q_{d,t}+S^{act}_{d,t}-L^{act}_{d,t}.
\]

If `B_act>=0`, only the originally scheduled charge may execute:

\[
x^c_{d,t}=\min\left(x^{c,ref}_{d,t},B^{act}_{d,t},X_{\max},\frac{E_{\max}-E_{d,t-1}}{\eta_c}\right),
\]

`x^d=0`, `r=0`, and `spill=B_act-xc`. Any scheduled discharge is cancelled and logged.

If `B_act<0`, only the originally scheduled discharge may execute:

\[
x^d_{d,t}=\min\left(x^{d,ref}_{d,t},-B^{act}_{d,t},X_{\max},(E_{d,t-1}-E_{\min})\eta_d\right),
\]

`x^c=0`, `spill=0`, and `r=-B_act-xd`. Any scheduled charge is cancelled and logged.

The override may **not** add a storage action, increase its magnitude above the day-ahead command, move it to a different slot, or choose a new economically preferred action.

Required clipping/cancellation evidence includes `clipped_charge_kWh`, `clipped_discharge_kWh` and `clipped_slot_count`.

## 7. Actual Q2 settlement objective

For any realized policy replay:

\[
C_{Q2}=\sum_{d,t} c_t q^{DA}_{d,t}+\sum_{d,t}5c_t r_{d,t}.
\]

Normal commitment is paid according to the planned amount even if later unused. No revenue from spill and no sale to grid are allowed.

The independent validator must recompute separately:

- normal purchase cost;
- emergency purchase cost;
- total cost;
- normal purchase kWh;
- emergency kWh;
- spill kWh;
- storage throughput;
- SOC trajectory.

## 8. Cross-day and annual terminal contract

The realized SOC after day `d` is the next day's initial state. The reference day-ahead trajectory never overwrites realized SOC.

Primary final-year condition:

\[
1200\le E_{2025-12-31,144}\le10800,
\]

with no extra year-end equality (`FREE_BOUNDED_YEAR_END`). Before Freeze, rerun at least:

- T0: `FREE_BOUNDED_YEAR_END`;
- T1: `E_end = 6000` sensitivity;
- T2: `E_end >= 6000` sensitivity.

T1/T2 are sensitivity assumptions, not official hard constraints.

## 9. Efficiency contract

Primary implementation uses

\[
\eta_c=\eta_d=0.9.
\]

Before Freeze, perform the complete Q2 replay with the alternative

\[
\eta_c=\eta_d=\sqrt{0.9}.
\]

Do not claim efficiency robustness until this comparison is actually run and checked.

## 10. Forecast family provenance adjudication

Accepted for Q2 R1:

`FORMAL_POLICY_FAMILY = PREDECLARED_BASELINE`

- load family: `LAG7`;
- PV family: `TRAILING7_MEAN`.

Accepted interpretation of the Aug–Oct challenger exercise:

`AUG_OCT_CHALLENGER_COMPARISON = OFFLINE_ADEQUACY_AUDIT`

It may support the statement that available evidence did not justify replacing the preregistered baseline, but it may **not** be described as the information used on Feb1 to choose a family from future months.

The W2 dynamic-price family is outside Q2 scope and must be consumer-filtered.

Full adjudication is in `XXT_Q2_MODEL_FAMILY_CAUSALITY_ADJUDICATION_R1.md`.

## 11. Required policy comparison before Freeze

At minimum compare under identical forecast inputs, efficiency, terminal mode, starting SOC and cost accounting:

1. P0 `DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE`;
2. P1 `POINT_FORECAST_DA_PLUS_CAUSAL_INTRADAY`;
3. P2 `ANALYTIC_Q80_RESIDUAL_RESERVE_PLUS_CAUSAL_INTRADAY`.

Minimum outputs:

- total Q2 cost;
- normal purchase kWh/cost;
- emergency kWh/cost/slot count/day count;
- P95 daily emergency cost or equivalent registered tail metric;
- spill/curtailment;
- charge/discharge throughput;
- SOC min/max/end and full trajectory;
- fixed-baseline clipping statistics;
- specified-date emergency intervals required by result2;
- constraint report;
- full-period information-leakage report.

Model ranking is invalid unless all hard validation gates pass first.

## 12. Implementation release and remaining Gate state

**Mathematical contract:** `Q2_MATH_READY_FOR_IMPLEMENTATION`  
**Q2 formal replay:** `NOT_RUN`  
**Q2 downstream Mathematical PASS:** `NOT_YET_GRANTED`  
**Q2 Freeze:** `FORBIDDEN`  
**Paper Frozen Facts:** `NOT_AVAILABLE`

The next owner is FYQ/Codex implementation. They must implement exactly this contract, seal W2 metadata with this contract ID, isolate Q4-only price forecasts, run the validator suite and return replay evidence to XXT for independent Mathematical Review.

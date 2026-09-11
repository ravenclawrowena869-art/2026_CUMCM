# XXT Q2 Validator Specification — Prevalidation R2

Contract source: `CUMCM2026_C_Q2_MATH_CONTRACT_R1`.  
This document corrects the **prevalidator** only. It does not alter the approved Q2 mathematical contract and does not validate a full-year Q2 result.

## 1. Frozen source-resolved S1-A semantics

For every 10-minute slot, all power inputs are first converted to slot energy in kWh using `Δt=1/6 h`.

- `q_DA >= 0`: 00:00 locked, paid normal commitment.
- `w`: paid-unused normal commitment, `0 <= w <= q_DA`.
- `v`: PV curtailment, `0 <= v <= PV`.
- `r >= 0`: emergency purchase.
- `c,d >= 0`: bus-side charge/discharge energy.
- optional compatibility summary only: `u_total = w + v`.

Physical balance:

`q_DA - w + r + PV + d = L + c + v`.

Equivalent interpretation: accepted normal energy is `q_DA-w`, utilized PV is `PV-v`. `w` is not PV curtailment, not sale/export, not a refund, and not a free change of `q_DA`.

Billing:

`C_normal = Σ p_t q_DA,t`

`C_emergency = Σ 5 p_t r_t`

`C_total = C_normal + C_emergency`.

`Σ p_t w_t` is an **audit decomposition of money already contained in `C_normal`**. It must never be added again to `C_total`.

## 2. Required S1 evidence fields

Each formal strategy/run must independently report:

- `sum_w_kWh = Σw`;
- `paid_unused_value_cny = Σp*w` (diagnostic subset, not extra cost);
- `w_share_of_commitment = Σw / Σq_DA` with an explicit zero-denominator rule;
- count of slots with `w>tol`;
- count of dates with any `w>tol`;
- maximum single-slot `w` and its date/slot;
- maximum daily `Σw` and its date;
- `sum_v_kWh = Σv` separately;
- optional `sum_u_total = Σ(w+v)` only as a compatibility summary;
- strategy/risk configuration so dependence of `w` on risk-aware planning can be compared.

If only a total spill field exists, or if `w` is labeled “弃光/PV curtailment”, S1 evidence is incomplete.

## 3. Prevalidation checklist

| ID | independent check | prevalidation failure |
|---|---|---|
| P01 | Q2 contract ID and original authority package SHA are exact; S1 authorization is present | `FAIL_PROVENANCE` |
| P02 | Jan–Dec / Feb–Dec time coordinates, 10-min granularity, `kW/6 -> kWh`, frozen right-endpoint mapping | `FAIL_DATA/MAPPING` |
| P03 | daily 00:00 `q_DA` vector is immutable after commitment; execution and settlement refer to the same commitment ID/hash | `FAIL_COMMITMENT` |
| P04 | every action/forecast input has `known_at <= decision_time`; no future actual is consumed | `FAIL_LEAKAGE` |
| P05 | future forecast uses the frozen daily 00:00 vintage; current actual can replace only the currently realized slot under the primary discrete-time assumption | `FAIL_LEAKAGE` |
| P06 | Q2 price source is Attachment1 fixed 144-slot tariff repeated daily; no Attachment4 dynamic price | `FAIL_PRICE_SOURCE` |
| P07 | R14 Jan bridge is the source of Feb1 SOC; full SOC recursion is independently rebuilt, including cross-day continuity | `FAIL_PHYSICS` |
| P08 | SOC bounds, charge/discharge limits, finite/nonnegative actions and no simultaneous executed charge/discharge | `FAIL_PHYSICS` |
| P09 | source-resolved S1 bounds `0<=w<=q_DA`, `0<=v<=PV`; `u_total`, if present, equals `w+v` | `FAIL_S1_BOUNDS/EVIDENCE` |
| P10 | physical balance uses `q_DA-w+r+PV+d=L+c+v`, not generic-spill replacement | `FAIL_S1_SOURCE_RESOLUTION/PHYSICS` |
| P11 | executed `r` is independently recomputed after storage action; if `r>tol`, executed charging is zero under current Q2 policy | `FAIL_SETTLEMENT/EMERGENCY_CHARGING` |
| P12 | `w` and `v` labels/provenance stay source-resolved; `w` is never reported as PV curtailment | `FAIL_S1_LABEL` |
| P13 | fixed-storage baseline safety override never increases the planned magnitude or reverses direction; every clip is auditable | `FAIL_BASELINE` |
| P14 | T0/T1/T2 terminal mode is explicit; infeasible T1/T2 is not relabeled PASS; no 2026 energy is borrowed | `FAIL_TERMINAL` |
| P15 | independent accounting recomputes `Σp*q_DA + Σ5p*r`; January excluded; `Σp*w` is not double-counted | `FAIL_ACCOUNTING` |
| P16 | forecast family / historical cutoff / baseline preregistration provenance is complete; final/evaluation data do not select the model | `FAIL_PROVENANCE/LEAKAGE` |
| P17 | risk quantile uses only signed same-slot residual history available before the planning cutoff; each alpha candidate is rebuilt from its own causal residual set | `FAIL_RISK_PROVENANCE` |
| P18 | any alpha sensitivity (`.75/.80/.85` and valid-rank neighbors) performs full replan + full downstream replay; no post-hoc reuse of a fixed path | `FAIL_RISK_PROTOCOL` |
| P19 | solver status/gap/runtime/tie-break/epsilon/fallback evidence preserved; no hidden hard-constraint relaxation | `FAIL_NUMERICAL/DEGRADED` |
| P20 | paper-specified emergency intervals and result2 writer are derived from canonical physical boundaries, not template header guesswork | `FAIL_MAPPING` |
| P21 | S1 usage audit contains all required `w` and `v` aggregates and locations | `FAIL_S1_EVIDENCE` |
| P22 | `ONE_SLOT_DELAYED_ACTUAL` counterfactual is implemented before Q2 Freeze and reruns the downstream policy, not merely relabeling timestamps | `FAIL_EVIDENCE` |
| P23 | 24-h truncation tail diagnostic reports end-of-day / next-day-start emergency and SOC behavior; material boundary artifact triggers a separate horizon challenger rather than silent model expansion | `FAIL_EVIDENCE` |

Energy tolerance for formal replay remains `1e-6 kWh`; cost tolerance remains `max(1e-5,1e-9*|C|) CNY`; hash/time/boolean provenance fields are zero-tolerance.

## 4. Hard-constraint-first rule

The validator returns feasibility/accounting/causality status **before** comparing cost. A cheaper path with any hard violation, future-information leak, incorrect S1 source accounting, or cost double counting is rejected.

For SOC/path-dependent constraints, report at least: `max_violation`, `argmax_location`, terminal violation when applicable, recursion residual, cross-day discontinuity maximum and first failure.

## 5. Sensitivity evidence still pending formal implementation

This R2 prevalidator records but does not execute full-year Q2 sensitivities. Before any Q2 Freeze, FYQ must provide current-version runs for:

- primary current-slot-actual timing vs `ONE_SLOT_DELAYED_ACTUAL`;
- risk alpha neighborhood with full replan/replay;
- FREE/T1/T2 annual terminal modes;
- primary `eta_c=eta_d=0.9` vs `sqrt(0.9)` sensitivity where required by current contract;
- 24-h truncation tail diagnostic;
- S1 usage audit and, if `w` is materially large or drives the strategy advantage, an XXT-returned S1-B feasible-subset / absorption counterfactual.

Prevalidation PASS here means the **validator specification is mathematically coherent**. It is not a Q2 result PASS.

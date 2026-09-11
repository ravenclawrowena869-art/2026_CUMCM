# CUMCM 2026 C题 — Q2 Validator Specification R1

**Contract:** `CUMCM2026_C_Q2_MATH_CONTRACT_R1`  
**Purpose:** independent mechanical + mathematical validation before XXT review.

## 0. Validation principle

Validation order is:

`feasibility → information causality → accounting semantics → policy comparison → paper eligibility`.

A lower-cost run with any hard violation is invalid.

Recommended numerical tolerance for energy equalities is `1e-7 kWh` unless solver scaling justifies a documented alternative. Bounds may use the same absolute tolerance. All tolerance changes must be versioned.

## 1. Required checks

| ID | Check | PASS condition |
|---|---|---|
| V01 | Contract identifier | every Q2 optimizer-facing row/run states `CUMCM2026_C_Q2_MATH_CONTRACT_R1` |
| V02 | Time mapping | solver uses `C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`; 144 slots/day; no template-label parsing into physics |
| V03 | Q2 price source | tariff is Attachment1 fixed repeated curve; W2 dynamic-price rows rejected as `Q4_ONLY` |
| V04 | Normal purchase immutability | execution `q_DA[d,t]` exactly matches the 00:00 committed plan for all slots |
| V05 | Day-ahead information | all forecast/model/history inputs have `known_at <= d 00:00`; no day-future actual |
| V06 | Storage information | every current storage action uses only `known_at <= decision_time`; future actual count = 0 |
| V07 | Recourse direction | if pre-storage balance `B>=0`: discharge/emergency=0; if `B<0`: charge/spill=0 |
| V08 | Emergency last / no emergency charging | `r>tol => xc<=tol and spill<=tol`; emergency equals residual deficit after allowed discharge |
| V09 | No simultaneous C/D | `min(xc,xd)<=tol` for every executed slot |
| V10 | Energy balance | max absolute residual of `q+r+PV+xd-load-xc-spill` <= tol |
| V11 | SOC recursion | max absolute SOC recursion residual <= tol |
| V12 | SOC bounds | all `E` in `[1200,10800]` within tolerance |
| V13 | Power bounds | `xc,xd <= 5000/6 kWh` within tolerance |
| V14 | Cross-day continuity | `E[d,144] == E[d+1,0]` within tolerance; no daily reset |
| V15 | Feb1 bridge | Feb1 initial SOC = accepted R14 Jan31 replay output = 6000 kWh; provenance present |
| V16 | Annual terminal primary | T0 checks bounds only; no hidden year-end equality |
| V17 | Terminal sensitivities | T1 checks `E_end=6000`; T2 checks `E_end>=6000`; both labeled sensitivity |
| V18 | Efficiency primary | eta_c=eta_d=0.9 and semantics recorded |
| V19 | Efficiency alternative | full Q2 replay exists for eta_c=eta_d=sqrt(0.9) before Freeze |
| V20 | Cost recomputation | independent `sum(c*q)+sum(5*c*r)` matches reported total within tolerance |
| V21 | Cost decomposition | normal cost and emergency cost independently reproducible; no spill revenue/sale |
| V22 | Forecast provenance | load=LAG7, PV=TRAILING7_MEAN under `PREDECLARED_BASELINE`; source/version/hash present |
| V23 | Model-family causality | Aug–Oct challenger comparison labeled `OFFLINE_ADEQUACY_AUDIT`, never a Feb decision input |
| V24 | Risk residual provenance | same-slot full signed residuals, strict `target_ts < day 00:00`, nearest-rank quantile |
| V25 | Risk alpha | primary candidate alpha=0.80 derived from 5× ratio; no post-hoc overwrite |
| V26 | Risk history completeness | each risk slot has compatible past residual history; missing history is explicit FAIL/HOLD, not silent fill |
| V27 | Fixed baseline action rule | baseline only clips/cancels original action; never adds, increases, retimes or economically reoptimizes storage |
| V28 | Fixed baseline clipping log | clipped charge/discharge energy and slot count are complete and reconcile to executed schedule |
| V29 | Fallback audit | planner/recourse fallback counts reported; any formal fallback blocks Freeze absent separate adjudication |
| V30 | Full-period leakage audit | zero decision input has `known_at > decision_time` across Feb1–Dec31 |
| V31 | Result2 coverage | 334 days × 144 planned-purchase slots; required storage and emergency outputs present |
| V32 | Emergency interval reconstruction | contiguous intervals are built from canonical slot boundaries, not display-label text |
| V33 | Specified dates | 2025-03-20, 2025-06-21, 2025-09-23, 2025-12-21 outputs are present and traceable |
| V34 | Objective/policy source hashes | run records input hash, config, solver version and policy ID |

## 2. Policy-comparison Gate

P0, P1 and P2 are comparable only if V01–V34 applicable hard checks pass under identical:

- load/PV point forecast source;
- fixed Q2 tariff;
- initial SOC provenance;
- efficiency mode;
- annual terminal mode;
- time mapping;
- actual replay period;
- accounting code.

At least report:

- total cost;
- normal purchase kWh/cost;
- emergency kWh/cost/slot/day counts;
- P95 daily emergency cost;
- spill;
- charge/discharge throughput;
- SOC min/max/end;
- fixed-baseline clipping;
- required-date emergency intervals.

## 3. Independent recomputation requirements

A validator independent of the optimization objective assembly must recompute:

1. every slot's physical balance;
2. SOC trajectory from `E0` and executed actions;
3. cross-day bridge;
4. normal and emergency costs directly from tariff and saved quantities;
5. emergency contiguous intervals from canonical `slot_id`;
6. risk-history cutoff and quantiles;
7. `known_at` leakage counts.

Do not mark the solver's own reported objective as independent evidence.

## 4. Sensitivity / materiality reports

### Storage recourse assumption

Compare P0 vs P1 under the current storage-recourse authority. Flag materiality if the accepted R1 criteria are triggered, including total-cost difference >=1%, emergency energy/cost difference >=5%, feasibility/leakage change, strategy conclusion change, or substantial fixed-baseline clipping.

### Efficiency

Apply the existing efficiency materiality criteria. Do not pre-write a robustness conclusion.

### Annual terminal

Report T0/T1/T2 and flag finite-horizon end effects under the accepted annual-terminal contract.

### Risk alpha

Run alpha `{0.75,0.80,0.85}` plus tail stress `{0.90,0.95}` as preregistered sensitivity. These runs do not authorize post-hoc causal retuning.

## 5. Validator verdict

Mechanical validator may return:

- `PASS_FOR_XXT_REVIEW`;
- `FAIL_REOPEN_IMPLEMENTATION`;
- `HOLD_MISSING_EVIDENCE`.

It may **not** grant `Q2_MATHEMATICAL_PASS`, `FROZEN`, or paper-ready status. Those remain downstream Gate decisions.

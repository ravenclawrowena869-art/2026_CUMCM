# Q2 Execution and Acceptance R1

Status: `PREPARED / EXECUTION_RELEASE_HOLD_PENDING_XXT_R2`

This document defines the engineering Gate that CYQ Codex/Astra must satisfy once FYQ explicitly releases the full-year execution. It does not itself release execution.

## 1. Required execution role

When CYQ's Codex/Astra node executes Q2, bind:

`ACTIVE_ROLE = FYQ_TECHNICAL_ORCHESTRATOR`

The machine/API owner does not change mathematical or Controller authority.

## 2. Pre-run hard gates

Do not start the formal full-year run unless all are true:

- current XXT Q2 authority version relation has been adjudicated;
- FYQ has bound the accepted current XXT package/hash in the Controller Review;
- `Q2_EXECUTION_RELEASE = RELEASED` is explicitly issued by FYQ;
- official input hashes match `Q2_INPUT_BINDING_R1.json`;
- actual W2 forecast/residual export hashes are recorded from the bytes used;
- Jan31→Feb1 bridge artifact hash is recorded;
- no unresolved objective / hard-constraint / unit / accounting / information-set ambiguity remains.

Current state at this commit:

`Q2_EXECUTION_RELEASE = HOLD_PENDING_XXT_R2`

## 3. Required formal strategy matrix

Under identical official inputs, tariff, storage physics and accounting, run at least:

1. `POINT_DA_LP_R1 × Q2_RH_FIXED_Q_LP_R1`;
2. `POINT_DA_LP_R1 × DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE`;
3. `SIGNED_RESIDUAL_Q80_MARGIN_R1 × Q2_RH_FIXED_Q_LP_R1`;
4. `SIGNED_RESIDUAL_Q80_MARGIN_R1 × DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE`.

Each strategy propagates its own SOC path from the same lawful Jan31 bridge. Do not reset SOC to force comparability.

## 4. Mandatory execution evidence

The candidate delivery must include at minimum:

- exact source code and configs;
- runtime/package versions and solver identity;
- input/provenance manifest with source hashes;
- W2 forecast/residual hashes used;
- Jan31→Feb1 bridge hash;
- slot-level result ledger;
- strategy summary;
- daily summary;
- constraint replay;
- independent accounting replay;
- S1 `w` audit separate from PV curtailment `v`;
- alpha sensitivity `0.75/0.80/0.85`, each with re-planning + full replay;
- same-slot actual vs `ONE_SLOT_DELAYED_ACTUAL` full replay;
- 24-hour truncation/day-boundary diagnostic;
- saved result2 writer/readback verification;
- fresh rerun command/log;
- handoff to XXT current-version Mathematical Review;
- outer ZIP SHA256, ZIP CRC and internal `SHA256SUMS.txt` verification.

## 5. Hard validator requirements

At minimum independently replay:

- 334 formal dates × 144 slots = 48096 formal slots;
- complete Jan warm-up and Jan31→Feb1 bridge;
- 600-second slot spacing / 10-minute indexing;
- `q_DA` commitment immutability;
- `known_at` and future-information rules;
- full physical balance with source-resolved `w` and `v`;
- SOC recursion and every intermediate SOC bound;
- charge/discharge bounds;
- no selling;
- no emergency charging;
- emergency price exactly `5*p_t` with no double charge;
- normal cost on full committed `q_DA`, not `q_DA-w`;
- year-end/terminal mode;
- solver failure/fallback logging;
- independent recomputation of total cost;
- result2 ordinal output mapping and saved-file readback.

Report for path-dependent constraints:

- `max_violation`;
- `argmax_date` / `argmax_slot`;
- violation count;
- first failure;
- terminal violation if applicable;
- max SOC recursion residual;
- max energy-balance residual.

## 6. Numerical tolerances

- energy/physics tolerance: `1e-6 kWh`;
- total cost tolerance: `max(1e-5 CNY, 1e-9*abs(recomputed_cost))`;
- metadata, hashes, date/slot coverage and information provenance: strict, no numerical waiver.

## 7. Stop conditions

Stop at candidate and return to FYQ/XXT if any occurs:

- objective/accounting differs from accepted math authority;
- future actual enters 00:00 commitment or risk calibration;
- S1 `w` and PV curtailment `v` are conflated;
- q commitment changes intraday;
- hard violation exceeds tolerance;
- emergency 5× accounting is wrong or double counted;
- day-boundary/terminal behavior is undefined or materially changes claims;
- delayed-actual sensitivity changes the main strategy ranking materially;
- alpha neighborhood changes main ranking materially without disclosure;
- baseline comparison uses unequal inputs/accounting;
- provenance is incomplete;
- saved result2 cannot be independently read back;
- current-version XXT Mathematical Review is not PASS.

## 8. Quality labels

Allowed after evidence:

- `FEASIBLE`: hard constraints + independent accounting PASS;
- `COMPETITIVE`: same-data/same-accounting comparison stably beats a reasonable baseline;
- `NEAR-OPTIMAL`: forbidden unless additional valid bound/gap/exact certificate supports that scope.

A local/daily LP optimum does not prove the full-year stochastic/causal policy globally optimal.

## 9. Freeze Gate

Q2 may enter Freeze only after all of the following on the **same current version**:

- `technical_pass = true`;
- `mathematical_pass = true` from XXT;
- `hard_constraints_zero_violation = true`;
- `metrics_recomputed = true`;
- mandatory sensitivities/diagnostics complete;
- Evidence Gate pass or explicit accepted limitation;
- current Source of Truth / commit / hashes bound;
- no unresolved Mathematical Veto.

Until then:

- `Q2_FORMAL_RESULT = NOT_RUN` or candidate-only;
- `Q2_MATHEMATICAL_RESULT_PASS = FALSE`;
- `Q2_FROZEN = FALSE`.
# Q2 Execution and Acceptance R2

Status: `RELEASED_FOR_CANDIDATE_EXECUTION / FREEZE_NOT_GRANTED`

Execution role on CYQ-owned compute:

`ACTIVE_ROLE = FYQ_TECHNICAL_ORCHESTRATOR`

## Pre-run gates

Required:

- read `Q2_AUTHORITY_CHAIN_R2.md` and `Q2_IMPLEMENTATION_INTERFACE_R2.json`;
- bind base XXT package SHA `0d17f99f...e561`;
- bind XXT R2 prevalidation SHA `63c2494e...0a312`;
- verify official input hashes from `Q2_INPUT_BINDING_R1.json`;
- record exact W2 forecast/residual and Jan31->Feb1 bridge hashes from execution bytes;
- reject PR #8 `d22609f9...` as formal authority input;
- no unresolved input/provenance mismatch.

If input bytes are missing or incompatible: `HOLD_INPUT_BINDING`.

## Formal strategy matrix

Run at least:

1. `POINT_DA_LP_R1 × Q2_RH_FIXED_Q_LP_R1`;
2. `POINT_DA_LP_R1 × DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE`;
3. `SIGNED_RESIDUAL_Q80_MARGIN_R1 × Q2_RH_FIXED_Q_LP_R1`;
4. `SIGNED_RESIDUAL_Q80_MARGIN_R1 × DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE`.

All strategies use identical tariff, official actuals, storage physics and accounting; each advances its own SOC trajectory.

## Hard validation

Independently replay:

- 334 days × 144 slots;
- q_DA immutability;
- known_at / future-actual leakage;
- S1 source-resolved balance `q_DA-w+r+PV+d=L+c+v`;
- `w<=q_DA`, `v<=PV`;
- normal cost `Σp*q_DA`;
- emergency cost `Σ5p*r`;
- no selling / no emergency charging;
- charge/discharge limits;
- SOC recursion, full-path bounds, cross-day continuity;
- terminal mode;
- fallback counts;
- independent total-cost recomputation;
- result2 ordinal mapping and saved-file readback.

Numerical tolerance:

- physics/energy: `1e-6 kWh`;
- total cost: `max(1e-5 CNY, 1e-9*abs(recomputed_cost))`;
- hashes/provenance/date/slot coverage: strict.

## Mandatory sensitivities / diagnostics

Before candidate can be sent for Freeze review:

- alpha `.75/.80/.85`: each rebuild causal quantiles, replan and full replay;
- `ONE_SLOT_DELAYED_ACTUAL`: follow `Q2_DELAYED_ACTUAL_SENSITIVITY_PROTOCOL_R1.md`;
- S1 usage audit;
- required efficiency and terminal modes;
- 24-h tail/day-boundary diagnostic per `Q2_24H_TAIL_DIAGNOSTIC_PROTOCOL_R1.md`.

Risk-history semantics follow `Q2_RISK_HISTORY_COLD_START_BINDING_R1.md`.

## Stop / return conditions

Return to FYQ/XXT if any occurs:

- hard/accounting/unit violation;
- future-information leakage;
- S1 `w/v` conflation;
- unexpected formal-period n=0 risk history;
- alpha sensitivity or delayed-actual replay changes main strategy ranking materially;
- `TAIL_CHALLENGER_REQUIRED = TRUE`;
- S1 `w` materially drives feasibility/advantage;
- saved result2 cannot be independently read back;
- provenance incomplete.

## Delivery / downstream review

Candidate delivery must contain code/config/tests, exact input hashes, runtime/solver identity, slot/daily ledgers, constraint/accounting replays, sensitivities, S1 audit, tail diagnostic, result2 candidate/readback, logs, and SHA256/CRC evidence.

Candidate then follows:

`FYQ technical review -> XXT current-version Mathematical Review -> Evidence Gate -> Freeze decision`.

Until those steps pass:

- `Q2_MATHEMATICAL_RESULT_PASS = FALSE`;
- `Q2_FROZEN = FALSE`;
- candidate numbers are not Paper facts.

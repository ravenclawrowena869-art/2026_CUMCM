# TASK — Q2 FYQ Validation R3

`ACTIVE_ROLE=FYQ_TECHNICAL_ORCHESTRATOR`

Recommended model: `GPT-5.6 Sol / High`. Escalate to Astra/highest reasoning only if a mathematical-contract conflict cannot be closed safely.

## Inputs

1. `CUMCM2026_C_Q2_CORE_ENGINE_FALLBACK_R1_DELIVERY.zip`
   - original SHA256: `0ccc3d845b0ebbb8ab440634c208ee0f40045eace7de45345b9a61b51689f132`
2. filename-normalized transport copy is allowed only to make Linux extraction deterministic; it does not replace the original delivery as authority.
3. current canonical Skill and Q2 authority embedded in the Core delivery.

## First action

Fresh-read canonical Skill:
`SKILL.md -> Shared Core -> FYQ Profile -> Evidence Gate -> Parameter Protocol`.

Then verify:
- ZIP CRC;
- internal checksums;
- `STATUS.json` says `CORE_ENGINE_READY_FOR_FYQ_VALIDATION=true`;
- code/config tree SHA;
- input hashes;
- result2 candidate hash;
- fresh tests.

Do not redesign the core engine.

## Current canonical facts

Four CURRENT_SLOT_ACTUAL strategy runs are technical PASS. Current total costs:

1. Point + fixed = `16147425.108699`
2. Point + rolling = `15520997.910296`
3. Q80 + fixed = `14660907.941256`
4. Q80 + rolling = `15787621.178991`

The existing result2 candidate uses strategy 4 only as writer evidence. Do not treat it as the final selected strategy.

## Mandatory campaign

Run with full 334-day / 48096-slot replay and independent accounting:

### V1 alpha
- `.75`
- `.80`
- `.85`

For each alpha, rerun all four policy combinations. Do not reuse alpha=.80 decisions for other alpha values.

### V2 timing
- `CURRENT_SLOT_ACTUAL`
- `ONE_SLOT_DELAYED_ACTUAL`

Known blocker: a one-day Q80 + rolling delayed pilot reproducibly throws:
`S1_A_W_EXCEEDS_Q:29.63833333333332>0.0`.

Reproduce first. If it persists, STOP the delayed campaign for the affected semantic path and bind the failure evidence to the XXT adjudication task. Do not patch S1-A, add export/spill, or silently clip the locked action.

### V3 efficiency
- primary `eta_c=eta_d=0.9`
- alternative `eta_c=eta_d=sqrt(0.9)`

Full re-solve/replay.

### V4 terminal
- `FREE_BOUNDED_YEAR_END`
- `EQ_INITIAL_6000`
- `GE_INITIAL_6000`

Full re-solve/replay. Report infeasibility/reachability explicitly if encountered.

### V5 S1-A audit
For every strategy/variant retained:
- sum(w)
- sum(p*w) diagnostic only
- w/sum(q_DA)
- slots/days with w>0
- max slot/day w
- sum(v)
- whether w materially drives candidate ranking

### V6 24h tail/day-boundary
Run the current authorized diagnostic. If it returns challenger-required, stop robustness claims and return to FYQ/XXT.

## Independent validation

For every formally compared full-year run:
- q_DA immutability
- known_at/future leakage
- S1 balance
- w<=q_DA
- v<=PV
- no selling
- no emergency charging under the authorized semantics
- C/D limits
- SOC recursion
- SOC full-path bounds
- cross-day continuity
- terminal rule
- fallback count
- independent total-cost recomputation

Record max violation and argmax location for dynamic constraints.

## Candidate selection

Pre-register:
1. hard constraints/causal legality/provenance first;
2. compare only same accounting;
3. primary objective = formal Q2 total cost;
4. use emergency energy/cost and S1 waste as diagnostics;
5. if strategy ranking changes under a required sensitivity, do not Freeze until XXT adjudicates interpretation and claim boundary.

Do not use `result2_candidate.xlsx` identity as a selection criterion.

## Required output

Return a complete ZIP:
`CUMCM2026_C_Q2_FYQ_VALIDATION_R3_DELIVERY.zip`

Must include:
- validation manifest;
- variant matrix;
- full summary tables;
- independent validator reports;
- accounting reports;
- S1 audit;
- delayed-actual blocker evidence/adjudication dependency;
- tail diagnostic;
- selected technical candidate only if selection remains valid across mandatory evidence;
- result2 candidate regenerated from the selected technical candidate only if safe;
- Figure Data draft;
- FYQ->XXT review request.

Exit status is one of:
- `Q2_TECHNICAL_CANDIDATE_READY_FOR_XXT_REVIEW`
- `Q2_VALIDATION_BLOCKED_BY_MATHEMATICAL_ADJUDICATION`
- `Q2_VALIDATION_FAIL`

Never emit Q2 Frozen or Mathematical PASS in this task.

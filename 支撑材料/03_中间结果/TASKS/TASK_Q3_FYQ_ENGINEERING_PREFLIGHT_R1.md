# TASK — Q3 FYQ Engineering Preflight R1

`ACTIVE_ROLE=FYQ_TECHNICAL_ORCHESTRATOR`

Recommended model: `GPT-5.6 Sol / High` for integration; coding may be delegated to a normal execution/Codex window after XXT spec arrives.

## Scope before XXT formal spec returns

Allowed now:
- Attachment3 parser and provenance audit;
- forecast vintage schema;
- canonical target-slot mapping;
- stage ledger schema;
- result3 template reader/writer contract scaffold;
- independent validator scaffold;
- 00-only baseline harness;
- Figure Data schema;
- tests for chronology, `known_at`, past-slot immutability and interpolation.

Not allowed now:
- silently finalize the Q3 objective if XXT has not returned it;
- produce formal result3;
- declare the rolling LP final;
- fill ambiguous adjustment accounting by intuition.

## Required interfaces

Stage ledger minimum:
`date, stage_id, decision_time, target_slot, old_active_commitment, new_commitment, delta_plus, delta_minus, forecast_vintage_id, known_at_max, settlement_price_semantics, source_hashes`.

Forecast adapter must expose:
- issue time;
- target timestamp;
- hourly source anchor(s);
- 10-min converted power/energy;
- transform id/hash;
- `known_at` proof.

## Tests to build now

- no stage changes a slot whose right endpoint `<= decision_time`;
- later vintages cannot rewrite earlier ledger rows;
- no future actual enters forecast construction;
- exact-hour and non-exact-hour interpolation cases;
- missing forecast anchor fails hard;
- writer projection preserves the last authorized commitment per slot;
- result3 template labels do not redefine canonical slot identity.

## After XXT spec arrives

Implement only the accepted mathematical contract, then run:
- 00-only baseline;
- 00+06;
- 00+06+12;
- 00+06+12+18;
- mandatory reference-base / price-time / interpolation sensitivities;
- full SOC path replay;
- independent accounting and result3 readback.

## Output

Before XXT spec:
`CUMCM2026_C_Q3_FYQ_ENGINEERING_PREFLIGHT_R1_DELIVERY.zip`

Status:
`Q3_ENGINEERING_SCAFFOLD_READY_WAITING_XXT_SPEC`.

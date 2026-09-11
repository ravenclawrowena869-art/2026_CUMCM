# Q4 Causal Dynamic-Price Pre-design R1

Status: `PREDESIGN / FORMAL_MODEL_SELECTION_PENDING / FORMAL_RESULT_NOT_RUN`

## Objective of this stage

Prepare a causal price-information layer that can be inserted into both the Q2-style and Q3-style models without leaking future realized Attachment4 prices.

## Required information fields

Every dynamic-price value entering a decision must expose:
- `target_ts`;
- `price_value`;
- `known_at`;
- `vintage_id`;
- `source` (`REALIZED_HISTORY`, `FORECAST`, or `ORACLE_DIAGNOSTIC_ONLY`).

Hard rule:
`known_at <= decision_time` for every deployable decision input.

## Recommended baseline candidate

`CAUSAL_PRICE_LAG7_R0`

For a future delivery slot, use the realized price of the same canonical slot seven days earlier. This is a simple, auditable baseline motivated by strong weekly same-slot structure in the official Attachment4 data.

This baseline is not yet a Frozen model and may be replaced only if a causal challenger demonstrates material downstream gain under the same split and accounting.

## Q4-2 inheritance

Reuse the Q2 model structure:
- 00:00 q_DA commitment;
- load/PV causal forecasts;
- risk-aware day-ahead candidate;
- storage recourse;
- S1-A accounting as adjudicated by the final Q2 mathematical contract.

Only the price-information layer changes. Future realized Attachment4 prices do not enter 00:00 decisions unless official authority explicitly says they are known.

## Q4-3 inheritance

Reuse Q3 stage decisions at 00/06/12/18. At each stage:
- historical realized prices up to the stage may enter the price forecaster;
- future target prices use a causal forecast vintage;
- future PV uses the allowed Q3 forecast vintage;
- already executed commitments/actions remain immutable.

## Oracle boundary

`ORACLE_FUTURE_PRICE_DIAGNOSTIC_ONLY`

Use complete future realized prices only to measure:
- value-of-price-information gap;
- dates/slots where causal price uncertainty matters most;
- an idealized cost lower boundary for diagnostic comparison.

Oracle results must never be written as a deployable strategy or mixed into causal model selection.

## Challenger trigger

Do not introduce a more complex price model unless LAG7 shows at least one material defect:
- large causal-vs-oracle gap;
- unstable downstream strategy ranking;
- strong systematic error under identifiable regimes;
- material emergency-cost increase;
- drift stress failure.

If triggered, compare one time-aware challenger only, under the same causal evaluation and full downstream replay.

## Open mathematical items

XXT must adjudicate before formal Q4 execution:
- whether the official wording implies any future price visibility at 00/06/12/18;
- which realized price is used for ex-post settlement when adjustment issue time and delivery time differ;
- how Q3 adjustment accounting carries into Q4 dynamic price;
- whether the oracle bound is a valid lower-bound claim or only a diagnostic comparator under the final accounting.

## Freeze boundary

No Q4 formal result, final model selection, or result4 workbook may be Frozen from this pre-design file alone.

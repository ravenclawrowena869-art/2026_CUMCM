# TASK — Q4 XXT Causal Price Mathematical Spec R1

`ACTIVE_ROLE=XXT_MATHEMATICAL`

Recommended model: `GPT-5.6 Sol / High`. Escalate only if official wording leaves a genuine unresolved information-set/accounting ambiguity.

## Goal

Freeze the mathematical information/settlement contract needed to extend Q2 and Q3 to Attachment4 dynamic prices. No formal Q4 numerical result is produced here.

## Core questions

1. At 00:00, 06:00, 12:00 and 18:00, which dynamic-price information is legally available?
2. Does the official wording provide any basis for perfect knowledge of future Attachment4 prices? If not, future realized prices are forbidden as decision inputs.
3. For Q4-2, which price enters day-ahead planning, emergency settlement and ex-post cost accounting?
4. For Q4-3, when commitment adjustment is issued at one time for later delivery, is settlement tied to issue-time price, delivery-time realized price, or another explicitly supported rule?
5. Can Q3's primary `DELIVERY_SLOT_PRICE` assumption be carried into Q4, or does dynamic pricing require a new sensitivity/contract?
6. Is `ORACLE_FUTURE_PRICE_DIAGNOSTIC_ONLY` a valid idealized lower-bound comparator under the final model, or should it be described only as a value-of-information diagnostic?
7. Which price-forecast errors require downstream replay before any robustness claim?

## Candidate structure to review

Primary deployable price baseline candidate:
`CAUSAL_PRICE_LAG7_R0`

It uses the same canonical slot's realized price seven days earlier. This is only a candidate baseline; it is not an official fact or final model.

## Required output

`CUMCM2026_C_Q4_XXT_CAUSAL_PRICE_SPEC_R1_DELIVERY.zip`

Include:
- exact information-set contract;
- price variables/units;
- settlement formulas for Q4-2 and Q4-3;
- causal-vs-oracle boundary;
- validator specification;
- accepted sensitivity matrix;
- model-selection constraints for future price challengers;
- paper claim limits.

Exit:
- `Q4_PRICE_CONTRACT_READY_FOR_FYQ`
- or `Q4_PRICE_CONTRACT_BLOCKED_BY_OFFICIAL_AMBIGUITY`.

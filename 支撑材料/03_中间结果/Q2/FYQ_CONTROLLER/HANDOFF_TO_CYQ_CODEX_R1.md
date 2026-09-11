# HANDOFF TO CYQ CODEX R1

Status: `HANDOFF_DOCUMENTED / EXECUTION_NOT_YET_RELEASED`

Consumer: CYQ-owned Codex/Astra execution node

Execution role when released:

`ACTIVE_ROLE = FYQ_TECHNICAL_ORCHESTRATOR`

This handoff exists so the CYQ execution node can locate all FYQ-side Q2 authority/interface materials in the repository. It is not a Paper Handoff and does not grant CYQ Paper authority to change mathematics.

## 1. Read order

When FYQ later releases Q2 execution, read in this order:

1. official C problem statement and official attachments;
2. accepted current-version XXT Q2 mathematical authority;
3. `CONTROLLER_Q2_CURRENT_VERSION_REVIEW_R1.md` or its later superseding version;
4. `Q2_AUTHORITY_CHAIN_R1.md`;
5. `Q2_IMPLEMENTATION_INTERFACE_R1.json`;
6. `Q2_INPUT_BINDING_R1.json`;
7. `Q2_RESULT2_WRITER_CONTRACT_R1.md`;
8. `Q2_EXECUTION_AND_ACCEPTANCE_R1.md`;
9. current canonical `cumcm-rigorous-workflow` Dispatcher → Shared Core → FYQ Profile → Evidence Gate → Parameter Protocol;
10. the explicit FYQ execution release/task for that run.

## 2. Location

All FYQ-side documents above are stored at:

`支撑材料/03_中间结果/Q2/FYQ_CONTROLLER/`

XXT mathematical materials are stored at:

`支撑材料/03_中间结果/Q2/XXT_AUTHORITY/`

Do not use PR/Issue comments as a substitute for these formal files.

## 3. Current blocker

Historical/original XXT R1 package:

`0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`

PR #8 current-version candidate package:

`d22609f9ec0368888472945f948de66fb70669a3bc89877574fd0ab8834ea54c`

These are distinct package identities. Their canonical/supersede relation is being corrected by XXT R2.

Therefore the current state is:

`Q2_EXECUTION_RELEASE = HOLD_PENDING_XXT_R2`

Do not start a formal 334-day Q2 run from this handoff alone.

## 4. Stable engineering facts available now

The following are already Controller-bound and should not be re-invented by the execution node:

- 10-minute / 144-slot daily grid;
- kW to slot-kWh conversion by `/6`;
- fixed Attachment1 tariff repeated by day for Q2;
- no Q2 dynamic-price forecast;
- no selling;
- emergency purchase at `5×` delivery-slot tariff;
- S1-A source-resolved semantics: paid-unused normal `w` separate from PV curtailment `v`;
- physical balance `q_DA - w + r + PV + d = L + c + v`;
- normal purchase cost on full `q_DA`;
- Feb1 inherits Jan31 SOC replay;
- no daily SOC reset;
- `C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT` for official writer mapping;
- point day-ahead + causal recourse + fixed-storage baseline + signed-residual Q80 candidate structure;
- full-path validator and independent accounting requirements.

If XXT R2 changes any mathematical item above, stop and use the superseding accepted authority.

## 5. Required return to FYQ after execution release

Return one candidate-delivery ZIP containing at least:

- source code / configs / tests;
- input and source-hash manifest;
- W2 forecast/residual binding;
- data audit;
- slot-level and daily results;
- strategy comparison summary;
- constraint replay;
- independent accounting replay;
- S1 audit;
- alpha 0.75/0.80/0.85 full-replay sensitivity;
- same-slot vs one-slot-delayed actual full-replay sensitivity;
- day-boundary diagnostic;
- result2 writer/readback evidence;
- implementation report;
- handoff to XXT;
- SHA256SUMS, outer ZIP SHA256 and CRC verification.

Return destination:

`FYQ Controller -> XXT current-version Mathematical Review -> Evidence Gate -> Freeze decision`

Do not send candidate numbers directly to Paper as Frozen facts.

## 6. No authority escalation

This file does not authorize:

- merging PRs;
- changing the mathematical contract;
- filling missing rules by guess;
- formal Q2 execution before FYQ release;
- Mathematical PASS;
- Q2 Freeze;
- Paper-side modification of technical facts.
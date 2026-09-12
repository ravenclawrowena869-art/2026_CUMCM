# Q2 FYQ Controller / Implementation Interface R3

Status: `XXT_R2_BOUND / CURRENT_INTERFACE_READY / Q2_CANDIDATE_EXECUTION_RELEASED / FEB1_INITIAL_SOC_ASSUMPTION_BOUND`

This directory is the FYQ-side Q2 authority/interface location required by merged PR #4:

`支撑材料/03_中间结果/Q2/FYQ_CONTROLLER/`

## 1. Historical authority retained

Historical/original XXT R1 mathematical package:

- file: `CUMCM2026_C_XXT_Q2_FORMAL_OPT_SPEC_R1_DELIVERY.zip`
- SHA256: `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`
- CRC PASS / internal checksums 23/23 PASS
- contract ID: `CUMCM2026_C_Q2_MATH_CONTRACT_R1`

Historical FYQ Controller Review package:

- file: `CUMCM2026_C_CONTROLLER_Q2_FORMAL_SPEC_R1_REVIEW.zip`
- SHA256: `d69fd9736a0a5736223e40f26211332534c31331afc834aa0e3ab5d0a325ccca`
- CRC PASS / internal checksums 5/5 PASS

S1 remains:

`S1_A_PAID_UNUSED_NORMAL_ENERGY / MODELING_COMPLETION_ASSUMPTION`.

## 2. XXT R2 return bound

Received:

`CUMCM2026_C_XXT_Q2_PREVALIDATION_Q3_PREFLIGHT_R2_20260911.zip`

FYQ fresh verification:

- SHA256: `63c2494eac89b164830d9e26435332f6c06afedc0234ba5a05d25468f4d0a312`
- ZIP CRC: PASS
- internal `SHA256SUMS.txt`: 14/14 PASS
- synthetic adversarial oracle independently rerun: 23/23 matched expected detection

XXT R2 verdict:

- `Q2_PREVALIDATION_SPEC = PASS`
- `Q3_CONTRACT_PREFLIGHT = PASS_WITH_LIMITATION`
- no Q2/Q3 formal result PASS
- no Q2/Q3 Freeze

See `XXT_R2_PREVALIDATION_BINDING_R1.md`.

## 3. Feb-1 initial SOC amendment

Controller current decision:

`E(2025-02-01 00:00) = 6000 kWh`

Classification:

`MODELING_ASSUMPTION / NOT_OFFICIAL_DIRECTLY_STATED`

Authority:

`../XXT_AUTHORITY/XXT_Q234_FEB1_INITIAL_SOC_ASSUMPTION_R0.md`

Consequences for current execution:

- January remains causal history for forecasting/residual construction;
- the primary Feb-1 SOC is not derived from a Jan31 storage replay bridge;
- the old Jan31→Feb1 bridge requirement remains preserved in historical R1 files but is superseded for current primary initialization;
- before final paper claim, run the one-factor initial-SOC sensitivity at 4000/6000/8000 kWh according to `../XXT_AUTHORITY/XXT_Q234_INITIAL_SOC_SENSITIVITY_PROTOCOL_R0.md`.

## 4. Canonical version relation

The selected current Q2 chain is:

`original XXT R1 0d17... + FYQ S1-A authorization + XXT R2 prevalidation 63c249... + Q234 Feb-1 SOC amendment + FYQ R3 implementation interface`.

PR #8 package SHA
`d22609f9ec0368888472945f948de66fb70669a3bc89877574fd0ab8834ea54c`
is classified as:

`PARALLEL_NONCANONICAL_REPACKAGE / NOT_IN_CURRENT_AUTHORITY_CHAIN`.

It is not declared corrupt, but it must not override the selected execution chain.

See `Q2_AUTHORITY_CHAIN_R2.md` and `CONTROLLER_Q2_CURRENT_VERSION_REVIEW_R2.md` for the pre-amendment chain; the Feb-1 initialization delta is governed by the current amendment above.

## 5. CYQ/Codex current read set

Use the current set:

1. `XXT_R2_PREVALIDATION_BINDING_R1.md`
2. `CONTROLLER_Q2_CURRENT_VERSION_REVIEW_R2.md`
3. `Q2_AUTHORITY_CHAIN_R2.md`
4. `Q2_IMPLEMENTATION_INTERFACE_R3.json`
5. `Q2_INPUT_BINDING_R2.json`
6. `../XXT_AUTHORITY/XXT_Q234_FEB1_INITIAL_SOC_ASSUMPTION_R0.md`
7. `../XXT_AUTHORITY/XXT_Q234_INITIAL_SOC_SENSITIVITY_PROTOCOL_R0.md`
8. `Q2_RESULT2_WRITER_CONTRACT_R1.md`
9. `Q2_DELAYED_ACTUAL_SENSITIVITY_PROTOCOL_R1.md`
10. `Q2_RISK_HISTORY_COLD_START_BINDING_R1.md`
11. `Q2_24H_TAIL_DIAGNOSTIC_PROTOCOL_R1.md`
12. `Q2_EXECUTION_AND_ACCEPTANCE_R2.md`
13. `Q2_EXECUTION_RELEASE_R1.md`
14. `HANDOFF_TO_CYQ_CODEX_R2.md`

The older `Q2_IMPLEMENTATION_INTERFACE_R2.json` and `Q2_INPUT_BINDING_R1.json` remain archival and are superseded for execution only where the current files differ.

## 6. Previously reported missing definitions now closed

- current-version Controller binding: CLOSED;
- authority chain/version relation for execution: CLOSED;
- official Attachment1/Attachment2/result2 input binding: CLOSED;
- Feb-1 primary initial SOC semantics: CLOSED as modeling assumption;
- result2 writer/readback contract: CLOSED;
- `ONE_SLOT_DELAYED_ACTUAL` strict event order: CLOSED;
- risk-history cold-start/minimum-sample semantics: CLOSED;
- 24-h day-boundary diagnostic: CLOSED;
- CYQ Codex execution handoff: CLOSED.

Still required before final paper robustness claim:

- initial-SOC 4000/6000/8000 sensitivity on the current full-year engine.

## 7. Current execution state

`Q2_EXECUTION_RELEASE = RELEASED`

Scope: candidate full-year execution + required sensitivity/validation only.

Still false/not granted:

- `Q2_MATHEMATICAL_RESULT_PASS = FALSE`
- `Q2_FROZEN = FALSE`
- candidate numbers are not Paper facts
- no PR merge authority is granted

Candidate return path:

`CYQ Codex/Astra -> FYQ Controller review -> XXT current-version Mathematical Review -> Evidence Gate -> Freeze decision`.

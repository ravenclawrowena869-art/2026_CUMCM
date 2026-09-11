# Q2 FYQ Controller / Implementation Interface R1

Status: `HISTORICAL_CONTROLLER_REVIEW_RESTORED / CURRENT_INTERFACE_DOCUMENTED / EXECUTION_HOLD_PENDING_XXT_R2`

This directory is the FYQ-side location required by merged PR #4:

`支撑材料/03_中间结果/Q2/FYQ_CONTROLLER/`

It now contains both the restored historical Controller Review and the direct-readable implementation/interface material required by the CYQ/Codex execution line.

## 1. Historical Controller Review provenance

- Original file: `CUMCM2026_C_CONTROLLER_Q2_FORMAL_SPEC_R1_REVIEW.zip`
- Original outer SHA256: `d69fd9736a0a5736223e40f26211332534c31331afc834aa0e3ab5d0a325ccca`
- Original ZIP CRC: `PASS`
- Original internal `SHA256SUMS.txt`: `5/5 PASS`
- Reviewed historical/original XXT package SHA256: `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`
- Historical contract ID: `CUMCM2026_C_Q2_MATH_CONTRACT_R1`
- Historical Controller state: `Q2_FORMAL_MATH_SPEC = PASS_WITH_LIMITATION`
- Historical implementation state: `READY_AFTER_INPUT_BINDING`
- Result/Freeze state: `Q2_FORMAL_RESULT = NOT_RUN`, `Q2_FROZEN = FALSE`

The exact original ZIP was recovered and reverified outside GitHub. The current GitHub connector cannot faithfully write the larger original binary package, so the directory retains direct-readable authority payloads plus a compact repository mirror. This transport limitation does not change the historical decision.

## 2. Current-version reconciliation

PR #8 reports a different current-version candidate package:

`d22609f9ec0368888472945f948de66fb70669a3bc89877574fd0ab8834ea54c`

This is a distinct package identity from historical/original R1. It is **not** treated as a bad hash. Its canonical/supersede relation to historical R1 is currently:

`HOLD_PENDING_XXT_R2`

FYQ therefore documents the engineering interface now, but does not grant full-year execution until XXT R2 closes that relation and FYQ binds the accepted current hash/version.

## 3. Direct-readable Controller authority

- `CONTROLLER_Q2_FORMAL_SPEC_R1_REVIEW.md`
- `Q2_S1_CONTROLLER_AUTHORIZATION_R0.md`
- `OFFICIAL_Q2_S1_WORDING_NOTE.md`
- `ORIGINAL_PACKAGE_PROVENANCE.md`
- `SHA256SUMS.txt`
- `CUMCM2026_C_Q2_FYQ_CONTROLLER_REPO_MIRROR_R1.zip`

## 4. Current implementation/interface files for CYQ/Codex

Read these files before any future released full-year execution:

1. `CONTROLLER_Q2_CURRENT_VERSION_REVIEW_R1.md`
2. `Q2_AUTHORITY_CHAIN_R1.md`
3. `Q2_IMPLEMENTATION_INTERFACE_R1.json`
4. `Q2_INPUT_BINDING_R1.json`
5. `Q2_RESULT2_WRITER_CONTRACT_R1.md`
6. `Q2_EXECUTION_AND_ACCEPTANCE_R1.md`
7. `HANDOFF_TO_CYQ_CODEX_R1.md`

These files explicitly bind:

- official problem/Attachment1/Attachment2/result2 hashes;
- 334-day × 144-slot formal output scope;
- Jan31→Feb1 bridge rule;
- Q2 fixed tariff and information-set boundary;
- S1-A source-resolved `w` vs PV-curtailment `v` accounting;
- emergency `5×` accounting;
- result2 ordinal writer/readback rules;
- mandatory full-path validation, alpha, delayed-actual and day-boundary experiments;
- CYQ Codex execution role and return contract.

## 5. Current execution state

`Q2_EXECUTION_RELEASE = HOLD_PENDING_XXT_R2`

This is **not** a missing-FYQ-document state anymore. The remaining blocker is the mathematical current-version reconciliation already sent to XXT R2.

No file in this directory authorizes:

- Q2 formal result PASS;
- Q2 Freeze;
- direct main merge;
- CYQ Paper modification of technical facts;
- formal 334-day execution before a later explicit FYQ `Q2_EXECUTION_RELEASE = RELEASED`.
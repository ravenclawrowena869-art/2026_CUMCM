# Q2 Core Engine Fallback R1 — FYQ Acceptance R1

Role: `FYQ_TECHNICAL_ORCHESTRATOR`

## Delivery identity

Original ZIP SHA256:
`0ccc3d845b0ebbb8ab440634c208ee0f40045eace7de45345b9a61b51689f132`

ZIP CRC: `PASS`.

Declared code/config tree SHA256:
`6b7a7e2e3b469ede54a80108a66f666abf9e7e6f0c5c7e38e2b37fd9ac7fd5c2`.

Declared result2 candidate SHA256:
`8dd9a501ef9a55f41bd5139404197a9d7a5593315e0559c8d4e245e6b42e5927`.

## Transport-path audit

The archive stores `C题.pdf`, `附件1.xlsx`, `附件2.xlsx` filename bytes without the UTF-8 filename flag. On Linux/Python standard extraction they decode as CP437 mojibake. The three underlying file hashes exactly match the internal `SHA256SUMS.txt` entries.

After filename-only normalization:
- internal checksums: `161/161 PASS`;
- fresh `PYTHONPATH=src pytest -q`: `25 passed, 1 skipped`.

This is classified as:
`ENGINEERING_P1 / TRANSPORT_FILENAME_ENCODING`

It does not change model bytes, numerical evidence, or mathematical authority.

## Core Gate review

Accepted technical evidence:
- F0 input/provenance binding PASS;
- F1/F2 data + causal residual adapter PASS;
- F3 day-ahead point/Q80 solvers PASS;
- F4 intraday/SOC PASS on canonical CURRENT_SLOT_ACTUAL runs;
- F5 S1-A accounting PASS;
- F6 full-path validator PASS for four canonical strategies;
- F7 result2 write/readback PASS;
- F8 Figure Data hooks PASS;
- F9 tests PASS;
- F10 four 334-day runs PASS, fallback=0;
- F11 package/manifests PASS subject to filename-transport limitation above.

## Canonical technical candidate matrix

| Strategy | Total cost CNY | Emergency kWh | w kWh | v kWh | Final SOC kWh |
|---|---:|---:|---:|---:|---:|
| Point + fixed | 16147425.108699 | 829671.645878 | 295562.304825 | 1539427.147880 | 1200.000000 |
| Point + rolling | 15520997.910296 | 738650.773616 | 258347.106361 | 1488501.637276 | 1200.000000 |
| Q80 + fixed | 14660907.941256 | 338137.680071 | 635860.674663 | 2079486.149396 | 1626.886976 |
| Q80 + rolling | 15787621.178991 | 536522.862412 | 1014568.900423 | 2070719.221461 | 1200.000000 |

Important: the currently generated `result2_candidate.xlsx` uses Q80 + rolling only as a writer/core-engine candidate. It is not the formal winner. In the canonical matrix, Q80 + fixed has the lowest current cost, so FYQ Validation must select only after all required sensitivities and XXT review.

## Reproduced blocker

FYQ independently reproduced the existing delayed-actual pilot failure on Q80 + rolling, day 0:

`S1_A_W_EXCEEDS_Q:29.63833333333332>0.0`

Interpretation at this stage:
- a storage action chosen under one-slot-delayed information can become source-infeasible when actual PV/load is later revealed;
- current S1-A only permits paid-unused normal energy `w <= q` and PV curtailment `v <= PV`;
- locally adding export/battery spill, silently re-clipping the already locked action, or changing S1-A is forbidden.

Therefore:
`DELAYED_ACTUAL_MATH_ADJUDICATION_REQUIRED = TRUE`.

## Acceptance verdict

`CORE_ENGINE_READY_FOR_FYQ_VALIDATION = ACCEPTED_WITH_ENGINEERING_LIMITATION`

Still false:
- `Q2_MATHEMATICAL_RESULT_PASS`
- `Q2_FROZEN`
- `PAPER_READY`

Next path:
`FYQ Validation -> XXT Mathematical Review -> Evidence Gate -> Freeze decision`.

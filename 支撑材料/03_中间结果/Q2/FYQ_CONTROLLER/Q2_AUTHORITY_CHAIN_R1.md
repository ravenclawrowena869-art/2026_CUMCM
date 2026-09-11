# Q2 Authority Chain R1

Status: `FYQ_CONTROLLER_BINDING / PRE-EXECUTION`

## Authority order

1. Official 2026 CUMCM C problem statement, attachments and official result2 template.
2. Q1 Frozen storage/time/unit Source of Truth.
3. XXT Q2 Mathematical Contract + current-version Mathematical Review.
4. FYQ Controller Review / S1 authorization / implementation interface.
5. Canonical `cumcm-rigorous-workflow` main.
6. Execution Task/Handoff.
7. Issue/PR comments as interaction evidence only.

## Official-source identities freshly bound

Official package:

- `CUMCM2026Problems(1).zip`
- SHA256: `a54c0e6b552d31e2dbd41aba4a07769943433cb9317927514c2d39ec6442e241`

C problem statement:

- `C题/C题.pdf`
- SHA256: `2c098f6ae9dd47ae965aebdec3b9facf3de6c173f999783c1012c08fc5fb9d2d`

Q2 official tariff / Q1-day profile source:

- `C题/附件/附件1.xlsx`
- SHA256: `66b87134f5ecccd68184d3539bb1293ef039f9e0fdd955a589b9bfa7f227c377`

Q2 actual load/PV source:

- `C题/附件/附件2.xlsx`
- SHA256: `2e95fd446bfafa0d8c59577b5c2e2ea8b3f1def20dde54a3062556f4da9b4c72`

Official Q2 output template:

- `C题/附件/附件5/result2.xlsx`
- SHA256: `1c26494cfc6d754e0bd9bff7e13e1126a73d2d2da6c5336eb251d89b9a1a1a47`

## Upstream Q1 frozen identities

- `CUMCM2026_C_Q1_FINAL_FREEZE_MANIFEST_R0.md`
- SHA256: `058fd3f58327462f6d62a1080eb914b7bd1e4fced5e6081dd5a4ec6ba0b3ac16`

- `CUMCM2026_C_Q1_FINAL_PAPER_HANDOFF_R0.md`
- SHA256: `eb90da85ab4ff7fd1d493c742064dca2a113035ef07226cf18e78ab693940bab`

Inherited implementation constants include 10-minute slots, `Δt=1/6 h`, storage capacity 12000 kWh, SOC bounds 1200–10800 kWh, charge/discharge power bound 5000 kW, no selling, and the frozen Q1 time mapping `C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`; Q2-specific cross-day and terminal rules come from Q2 authority.

## Historical mathematical authority

Historical/original XXT package:

- `CUMCM2026_C_XXT_Q2_FORMAL_OPT_SPEC_R1_DELIVERY.zip`
- SHA256: `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`
- CRC: PASS
- internal checksums: 23/23 PASS
- stable contract ID: `CUMCM2026_C_Q2_MATH_CONTRACT_R1`

Historical FYQ Controller package:

- `CUMCM2026_C_CONTROLLER_Q2_FORMAL_SPEC_R1_REVIEW.zip`
- SHA256: `d69fd9736a0a5736223e40f26211332534c31331afc834aa0e3ab5d0a325ccca`
- CRC: PASS
- internal checksums: 5/5 PASS

Controller S1 authorization:

- `normal_purchase_surplus_mode = S1_A_PAID_UNUSED_NORMAL_ENERGY`
- classification: `MODELING_COMPLETION_ASSUMPTION`

## Current-version candidate relation

PR #8 reports a different XXT package identity:

- SHA256: `d22609f9ec0368888472945f948de66fb70669a3bc89877574fd0ab8834ea54c`
- status: `CURRENT_VERSION_CANDIDATE / NOT_BYTE_IDENTICAL_TO_HISTORICAL_R1`
- canonical/supersede relation: `HOLD_PENDING_XXT_R2`

The existence of the `d226...` package does not invalidate its bytes. It is simply not yet authorized to replace the historical R1 under the same contract ID.

## Execution bootstrap identity

FYQ bootstrap previously prepared for CYQ Codex/Astra:

- `CUMCM2026_C_Q2_CYQ_CODEX_BOOTSTRAP_R0.zip`
- SHA256: `d02da13d2c825f7d73008986c6187751faa7e6c4a45a5226e2d709615e02dabb`

That bootstrap is a sealed engineering snapshot and does not replace current mathematical authority.

## Current release boundary

`Q2_EXECUTION_RELEASE = HOLD_PENDING_XXT_R2`

Reason: XXT must first close the historical-R1 vs current-version candidate relationship and the R2 corrections. After R2, FYQ updates the bound mathematical package/version and only then may issue full-year execution release.
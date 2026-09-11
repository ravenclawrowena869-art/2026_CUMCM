# Q2 Authority Chain R2

Status: `FYQ_CONTROLLER_BOUND / EXECUTION_RELEASED_FOR_CANDIDATE_RUN`

## 1. Formal authority order

1. Official 2026 CUMCM C problem statement, attachments and official result2 template.
2. Q1 Frozen storage/time/unit Source of Truth.
3. Base XXT Q2 mathematical contract package:
   `CUMCM2026_C_XXT_Q2_FORMAL_OPT_SPEC_R1_DELIVERY.zip`, SHA256
   `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`.
4. FYQ S1-A Controller authorization.
5. XXT R2 prevalidation package:
   `CUMCM2026_C_XXT_Q2_PREVALIDATION_Q3_PREFLIGHT_R2_20260911.zip`, SHA256
   `63c2494eac89b164830d9e26435332f6c06afedc0234ba5a05d25468f4d0a312`.
6. FYQ current implementation/input/writer/execution interfaces in this directory.
7. Current canonical `cumcm-rigorous-workflow` main.
8. Explicit execution task/handoff.

Issue/PR comments remain interaction evidence only.

## 2. XXT R2 integrity

FYQ fresh verification:

- ZIP CRC: PASS;
- internal checksum manifest: 14/14 PASS;
- synthetic adversarial oracle independently rerun: 23/23 matched expected detection.

XXT R2 verdicts:

- `Q2_PREVALIDATION_SPEC = PASS`;
- `Q3_CONTRACT_PREFLIGHT = PASS_WITH_LIMITATION`;
- Q2/Q3 formal results: NOT_RUN;
- Q2/Q3 Mathematical Result PASS: FALSE;
- Q2/Q3 Freeze: FALSE.

## 3. PR #8 / d226 candidate relation

PR #8 reports SHA256:

`d22609f9ec0368888472945f948de66fb70669a3bc89877574fd0ab8834ea54c`.

XXT R2 does not bind or adopt that package. Therefore FYQ selects it as:

`PARALLEL_NONCANONICAL_REPACKAGE / NOT_IN_CURRENT_AUTHORITY_CHAIN`.

It is not declared corrupt and its useful material may be consulted, but it cannot override the current mathematical chain or share canonical status merely because it uses the same R1 contract identifier.

The selected chain remains the original `0d17...` base contract plus the explicit S1-A Controller authorization and the XXT R2 prevalidation correction layer.

## 4. Source/input identities

Official bytes bound by FYQ:

- `C题.pdf`: `2c098f6ae9dd47ae965aebdec3b9facf3de6c173f999783c1012c08fc5fb9d2d`;
- `附件1.xlsx`: `66b87134f5ecccd68184d3539bb1293ef039f9e0fdd955a589b9bfa7f227c377`;
- `附件2.xlsx`: `2e95fd446bfafa0d8c59577b5c2e2ea8b3f1def20dde54a3062556f4da9b4c72`;
- `result2.xlsx`: `1c26494cfc6d754e0bd9bff7e13e1126a73d2d2da6c5336eb251d89b9a1a1a47`.

W2 forecast/residual and Jan31→Feb1 bridge hashes must be recorded from the exact execution bytes before the run proceeds beyond input binding.

## 5. Current release boundary

`Q2_EXECUTION_RELEASE = RELEASED`

Scope of release: formal **candidate** full-year execution and all mandatory validation/sensitivity runs under the authority chain above.

This release does not grant:

- Q2 Mathematical Result PASS;
- Q2 Freeze;
- paper-ready formal numbers.

The candidate delivery must return to FYQ and then XXT current-version Mathematical Review before any Freeze decision.

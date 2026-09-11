# Q2 XXT Mathematical Authority Archive

Status: `ORIGINAL_R1_AUTHORITY_RESTORED / R2_PREVALIDATION_REPOSITORY_MIRRORED`

This directory is the XXT-side Q2 mathematical authority location required by `Q2_AUTHORITY_SUPPLEMENT_REQUEST_XXT_FYQ_R0.md`.

## 1. Base mathematical authority — original R1

- Original file: `CUMCM2026_C_XXT_Q2_FORMAL_OPT_SPEC_R1_DELIVERY.zip`
- Original outer SHA256: `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`
- Original ZIP CRC: `PASS`
- Original top-level internal `SHA256SUMS.txt`: `23/23 PASS`
- Stable contract ID: `CUMCM2026_C_Q2_MATH_CONTRACT_R1`
- Authority relation: base Q2 mathematical contract; not superseded by the R2 prevalidation layer.

The exact original ZIP was recovered from the project Library and reverified against the historical SHA256 above. The current GitHub connector cannot preserve larger binary ZIP bytes directly, so the directly readable core MD/JSON payloads are stored in this directory together with provenance/checksum material.

### Direct-readable R1 authority/interface files

- `XXT_Q2_FORMAL_OPT_SPEC_R1.md`
- `XXT_Q2_IMPLEMENTATION_HANDOFF_R1.md`
- `XXT_Q2_MATH_CONTRACT_MANIFEST_R1.json`
- `XXT_Q2_VALIDATOR_SPEC_R1.md`
- `SHA256SUMS.txt` (original package checksum manifest)

### Repository transport supplement R1

- File: `CUMCM2026_C_Q2_XXT_AUTHORITY_REPO_SUPPLEMENT_R1.zip`
- SHA256: `7b3e7dfe73eb3877be19302bcb9080f1ec4cd293722a30da6fc0a7cfc3213ea5`
- ZIP CRC: `PASS`
- Purpose: transport/provenance supplement only; it does **not** supersede or reinterpret the original R1 delivery.

## 2. Current XXT correction layer — R2 prevalidation

Package identity:

`CUMCM2026_C_XXT_Q2_PREVALIDATION_Q3_PREFLIGHT_R2_20260911.zip`

Outer SHA256:

`63c2494eac89b164830d9e26435332f6c06afedc0234ba5a05d25468f4d0a312`

Local integrity before repository write:

- ZIP CRC / compressed-data test: `PASS`
- internal `SHA256SUMS.txt`: package manifest present
- synthetic adversarial oracle: `23/23 PASS`

Repository mirror path:

`支撑材料/03_中间结果/Q2/XXT_AUTHORITY/R2_PREVALIDATION/`

The R2 directory contains the package's directly readable source files, original internal checksum manifest, validator/oracle evidence, Q3 preflight files and `REPOSITORY_BINDING_R2.md`.

Important authority relation:

- R2 does **not** replace `CUMCM2026_C_Q2_MATH_CONTRACT_R1`;
- R2 corrects/locks the prevalidator and supplies the current Q2/Q3 preflight evidence layer;
- current selected execution chain is:
  `original XXT R1 0d17... + FYQ S1-A authorization + XXT R2 63c249... + FYQ R2 implementation interfaces`;
- PR #8 package `d22609f9...` is not adopted by this R2 return as canonical execution authority.

Current R2 mathematical state:

- `Q2_PREVALIDATION_SPEC = PASS`
- `Q3_CONTRACT_PREFLIGHT = PASS_WITH_LIMITATION`
- `Q2_FORMAL_RESULT = NOT_RUN`
- `Q2_MATHEMATICAL_RESULT_PASS = FALSE`
- `Q2_FROZEN = FALSE`
- `Q3_FORMAL_RESULT = NOT_RUN`
- `Q3_MATHEMATICAL_RESULT_PASS = FALSE`
- `Q3_FROZEN = FALSE`

## 3. Binary transport limitation

The currently available GitHub connector supports UTF-8 text writes but not a byte-preserving binary ZIP upload. XXT therefore does **not** fabricate or reconstruct a replacement archive and claim byte identity. The exact outer ZIP filename/SHA256 and all directly readable package constituents/checksums are preserved in `R2_PREVALIDATION/`.

A later binary-capable Git path may add the original ZIP bytes without changing mathematical authority or version identity.

## 4. Downstream use

FYQ should bind the repository path above together with the R2 outer SHA256 in `Q2_AUTHORITY_CHAIN_R2.md` / current execution provenance before declaring repository-level input binding closed.

No file in this directory grants Q2 or Q3 result PASS, Freeze, or Paper-ready formal numbers by itself. Candidate results must still pass FYQ technical review, XXT current-version Mathematical Review and the Evidence Gate.

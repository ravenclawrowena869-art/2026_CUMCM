# Q2 XXT Mathematical Authority Archive

Status: `R2_PREVALIDATION_PASS / XXT_REPOSITORY_DELIVERY_PASS_WITH_PROVENANCE_LIMITATION`

This directory is the XXT-side Q2 mathematical authority location required by `Q2_AUTHORITY_SUPPLEMENT_REQUEST_XXT_FYQ_R0.md`.

## 1. Base mathematical authority — R1

Historical package identity:

- file: `CUMCM2026_C_XXT_Q2_FORMAL_OPT_SPEC_R1_DELIVERY.zip`
- historical outer SHA256: `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`
- stable contract ID: `CUMCM2026_C_Q2_MATH_CONTRACT_R1`
- historical validation record: ZIP CRC PASS / top-level internal `SHA256SUMS.txt` 23/23 PASS
- authority relation: base Q2 mathematical contract; not superseded by the R2 prevalidation layer.

### Repository provenance limitation

The exact historical `0d17...` ZIP bytes are **not currently stored as a certified byte-identical repository blob**. The directly readable R1 core files below and the historical checksum manifest are stored in GitHub. A previously attempted binary transport blob was independently checked and was not byte-identical to `0d17...`; it was therefore removed rather than mislabeled as the original archive.

The current Project/Library file carrying the same historical filename is also not used to repair this gap because its byte identity does not match the selected historical package identity. PR #8 package `d22609f9...` remains `PARALLEL_NONCANONICAL_REPACKAGE / NOT_IN_CURRENT_AUTHORITY_CHAIN` and is not silently substituted for the selected R1 package.

### Direct-readable R1 core files

- `XXT_Q2_FORMAL_OPT_SPEC_R1.md`
- `XXT_Q2_IMPLEMENTATION_HANDOFF_R1.md`
- `XXT_Q2_MATH_CONTRACT_MANIFEST_R1.json`
- `XXT_Q2_VALIDATOR_SPEC_R1.md`
- `SHA256SUMS.txt` — historical package checksum manifest retained as provenance evidence

### Repository transport supplement R1

- file: `CUMCM2026_C_Q2_XXT_AUTHORITY_REPO_SUPPLEMENT_R1.zip`
- SHA256: `7b3e7dfe73eb3877be19302bcb9080f1ec4cd293722a30da6fc0a7cfc3213ea5`
- purpose: repository transport/provenance supplement only; it does **not** claim byte identity with or supersede the historical `0d17...` package.

## 2. Closure of the two unavailable R1 standalone files

The historical `SHA256SUMS.txt` lists two additional R1 authority files that are not available in this branch as verified historical standalone bytes:

1. `XXT_Q2_RISK_PARAMETER_PROTOCOL_R1.md`  
   historical expected SHA256: `53b0a88bcf2f9742f28d58cb42b7eb46ec23822d681489e49e3dfd9535b951b3`
2. `XXT_Q2_MODEL_FAMILY_CAUSALITY_ADJUDICATION_R1.md`  
   historical expected SHA256: `543e7184fa2dd0027042e9066ff16d33cc25c428488066ee739222105790a9fc`

XXT does **not** import the same-named PR #8 files to fill this gap, because their byte hashes differ and PR #8 is outside the selected authority chain.

For repository-readability, the current accepted semantics are instead made explicit by two R2 supplements. These are semantic replacements, **not byte-identical reconstructions**:

| Historical unavailable R1 file | Current repository-readable replacement | Replacement SHA256 |
|---|---|---|
| `XXT_Q2_RISK_PARAMETER_PROTOCOL_R1.md` | `R2_PREVALIDATION/XXT_Q2_RISK_PARAMETER_PROTOCOL_R2_REPOSITORY_SUPPLEMENT.md` | `66ed21e35eadab74fc0ba9fc956b9a90207442c856b292cd6119092d50b2482f` |
| `XXT_Q2_MODEL_FAMILY_CAUSALITY_ADJUDICATION_R1.md` | `R2_PREVALIDATION/XXT_Q2_MODEL_FAMILY_CAUSALITY_ADJUDICATION_R2_REPOSITORY_SUPPLEMENT.md` | `6c9b3885da634f5278ca1dc2f29ac6a7669178ad36155f3f82cd4f1f23c16a22` |

Their hashes are recorded separately in:

`R2_PREVALIDATION/REPOSITORY_SUPPLEMENT_SHA256SUMS_R2.txt`.

Authority interpretation for these two topics is therefore:

`base R1 formal spec + R2 repository supplement + R2 prevalidator`

with the provenance limitation above explicitly retained. No claim is made that the replacement files reproduce the missing historical bytes word-for-word.

## 3. Current XXT correction layer — R2 prevalidation

Package identity:

`CUMCM2026_C_XXT_Q2_PREVALIDATION_Q3_PREFLIGHT_R2_20260911.zip`

Historical/current selected outer SHA256:

`63c2494eac89b164830d9e26435332f6c06afedc0234ba5a05d25468f4d0a312`

Prior XXT/FYQ validation record for this package:

- ZIP CRC / compressed-data check: PASS
- internal package checksum manifest: present and preserved
- synthetic adversarial oracle: `23/23 PASS`

Repository mirror path:

`支撑材料/03_中间结果/Q2/XXT_AUTHORITY/R2_PREVALIDATION/`

The R2 directory contains the directly readable package constituents, original internal `SHA256SUMS.txt`, validator/oracle evidence, Q3 preflight files, `REPOSITORY_BINDING_R2.md`, and the two repository-only supplements listed above.

Important authority relation:

- R2 does **not** replace `CUMCM2026_C_Q2_MATH_CONTRACT_R1`;
- R2 corrects/locks the prevalidator and supplies the current Q2/Q3 preflight evidence layer;
- current selected chain remains:
  `original XXT R1 0d17... + FYQ S1-A authorization + XXT R2 63c249... + FYQ R2 implementation interfaces`;
- PR #8 `d22609f9...` is not canonical execution authority.

Current mathematical state:

- `Q2_PREVALIDATION_SPEC = PASS`
- `Q3_CONTRACT_PREFLIGHT = PASS_WITH_LIMITATION`
- `Q2_FORMAL_RESULT = NOT_RUN`
- `Q2_MATHEMATICAL_RESULT_PASS = FALSE`
- `Q2_FROZEN = FALSE`
- `Q3_FORMAL_RESULT = NOT_RUN`
- `Q3_MATHEMATICAL_RESULT_PASS = FALSE`
- `Q3_FROZEN = FALSE`

## 4. Binary-package boundary

Neither the historical R1 `0d17...` ZIP nor the selected R2 `63c249...` ZIP is currently certified as an exact byte-identical binary blob in this GitHub authority directory. GitHub therefore uses directly readable constituents plus explicit filename/SHA provenance; no reconstructed archive is presented as the original bytes.

If a binary-capable trusted path later supplies an archive, its SHA256 must match the recorded outer identity before it is labeled as that original package.

## 5. Downstream use and current hold

XXT repository delivery is now:

`XXT_REPOSITORY_DELIVERY = PASS_WITH_PROVENANCE_LIMITATION`.

This closes the two missing standalone-file **semantic/readability** requirements without fabricating historical bytes.

However Q2 annual execution must **not** start yet. FYQ still needs to close the PR #6 repository-level binding tasks, including binding this PR #5 path/version into `Q2_AUTHORITY_CHAIN_R2.md`, updating its current checksum manifest, and fixing the R2 handoff read-order version. Until those are closed and PR #5 then PR #6 are reviewed/merged in order, use:

`Q2_EXECUTION_NODE = HOLD_INPUT_BINDING`.

No file in this directory grants Q2 or Q3 result PASS, Freeze, or Paper-ready formal numbers. Candidate results must still pass FYQ technical review, XXT current-version Mathematical Review and the Evidence Gate.

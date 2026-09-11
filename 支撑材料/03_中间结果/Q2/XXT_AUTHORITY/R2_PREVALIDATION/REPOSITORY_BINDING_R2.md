# XXT R2 Repository Binding

Status: `REPOSITORY_MIRROR_CREATED / BINARY_ZIP_NOT_CERTIFIED_IN_REPOSITORY`

## Package identity

Selected source package identity:

`CUMCM2026_C_XXT_Q2_PREVALIDATION_Q3_PREFLIGHT_R2_20260911.zip`

Recorded outer SHA256:

`63c2494eac89b164830d9e26435332f6c06afedc0234ba5a05d25468f4d0a312`

Prior XXT/FYQ validation evidence records CRC PASS, internal checksum PASS and 23/23 adversarial-oracle PASS for that selected package.

## Repository path

The directly readable extracted package is mirrored under:

`支撑材料/03_中间结果/Q2/XXT_AUTHORITY/R2_PREVALIDATION/`

The selected package's original internal `SHA256SUMS.txt` is preserved in this directory for its package constituents.

Two additional repository-only semantic supplements are tracked separately in:

`REPOSITORY_SUPPLEMENT_SHA256SUMS_R2.txt`.

## Transport / provenance limitation

The selected outer ZIP bytes are not currently certified as a byte-identical binary blob in this GitHub authority directory. Therefore this repository binding does **not** claim that a reconstructed archive is identical to the recorded `63c249...` package.

The repository instead preserves:

- the selected outer package filename and SHA256 as provenance identity;
- directly readable R2 constituent files;
- the selected package's internal checksum manifest;
- explicit repository-only supplements where historical standalone R1 bytes are unavailable.

A future binary-capable trusted path may add an archive only after its SHA256 matches the recorded outer identity.

## Authority relation

R2 does **not** replace the base Q2 mathematical contract. Current chain remains:

`original XXT R1 0d17f99f... + FYQ S1-A authorization + XXT R2 63c2494e... + FYQ R2 implementation interfaces`.

R2 status remains:

- `Q2_PREVALIDATION_SPEC = PASS`
- `Q2_FORMAL_RESULT = NOT_RUN`
- `Q2_MATHEMATICAL_RESULT_PASS = FALSE`
- `Q2_FROZEN = FALSE`

Repository delivery status after the standalone-file closure is:

`XXT_REPOSITORY_DELIVERY = PASS_WITH_PROVENANCE_LIMITATION`.

FYQ should bind this repository path plus the recorded R2 outer SHA256 into the current R2 authority chain before treating repository-level input binding as closed. Until then the execution node remains `HOLD_INPUT_BINDING`.

# XXT R2 Repository Binding

Status: `REPOSITORY_MIRROR_CREATED / BINARY_ZIP_NOT_DIRECTLY_WRITTEN_BY_CONNECTOR`

## Package identity

Source package:

`CUMCM2026_C_XXT_Q2_PREVALIDATION_Q3_PREFLIGHT_R2_20260911.zip`

Outer SHA256:

`63c2494eac89b164830d9e26435332f6c06afedc0234ba5a05d25468f4d0a312`

Local ZIP integrity check before repository write: `CRC PASS` / no compressed-data errors.

## Repository path

The directly readable extracted package is mirrored under:

`支撑材料/03_中间结果/Q2/XXT_AUTHORITY/R2_PREVALIDATION/`

The original package's own `SHA256SUMS.txt` is preserved in this directory and identifies every package constituent.

## Transport limitation

The currently available GitHub connector only supports UTF-8 text-file create/update operations and does not provide a byte-preserving binary ZIP upload action. Therefore the outer ZIP itself is not represented as a GitHub binary blob by this write operation.

To avoid pretending that a reconstructed archive is byte-identical, XXT uploads the complete directly readable text payload set, the original internal checksum manifest, the exact outer ZIP filename/hash, and this provenance note. A later binary-capable Git path may add the original ZIP bytes without changing the mathematical authority.

## Authority relation

This R2 package does **not** replace the base Q2 mathematical contract. Current chain remains:

`original XXT R1 0d17f99f... + FYQ S1-A authorization + XXT R2 63c2494e... + FYQ R2 implementation interfaces`.

R2 status remains:

- `Q2_PREVALIDATION_SPEC = PASS`
- `Q2_FORMAL_RESULT = NOT_RUN`
- `Q2_MATHEMATICAL_RESULT_PASS = FALSE`
- `Q2_FROZEN = FALSE`

FYQ should bind the repository path above plus outer package SHA256 in the current R2 authority chain before treating the execution node's repository-level input binding as closed.

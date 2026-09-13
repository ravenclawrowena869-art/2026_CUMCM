# FYQ Full Delivery Validation — Winter-PV Fast-Fix R0

Validation date: 2026-09-13

## Source

- File: `CUMCM2026_C_Q2_FYQ_WINTER_PV_FAST_FIX_R0_DELIVERY.zip`
- Exact size: `104106491 bytes`
- SHA256: `011f1d0d64e4aa578a1c5f377b26ac5585d9317f807f9ffe89132b462d48ea36`
- Project/Library exact filename: `CUMCM2026_C_Q2_FYQ_WINTER_PV_FAST_FIX_R0_DELIVERY.zip`

The 104 MB archive is intentionally not duplicated as a normal Git blob because it is near GitHub's single-file size ceiling. The repository stores the complete verification record, compact source snapshot, and Phase-B handoff instead.

## Fresh byte-level validation

A fresh local verification against the exact Project/Library bytes returned:

- ZIP CRC: `PASS`
- ZIP entry count: `368`
- internal `SHA256SUMS.txt`: `367/367 PASS`
- internal hash mismatches: `0`
- missing files referenced by internal SHA256SUMS: `0`

Therefore the complete FYQ Delivery used for the XXT Phase-B review is byte-integrity verified by FYQ Controller.

## Technical identity pins

- Selected forecast layer: `L2 + P3_AMPCORR_K7`
- Selected K: `7`
- selected F1 forecast SHA256: `ed198712edfbaddbd0f5d620a6f4dd5f976a49034836ad2b45bc6254a549de9a`
- frozen Q2 runner SHA256: `5a2ab76328a70a939ab9ada31bb7603ce5acb45d6a0c2d2a18783524f8bb8e47`
- source Delivery SHA256: `011f1d0d64e4aa578a1c5f377b26ac5585d9317f807f9ffe89132b462d48ea36`

## Scope boundary

This validation closes the source-integrity question only. It does not itself authorize:

- `Q2_FREEZE`;
- final q-level selection;
- claiming q=0.80 was revalidated;
- final `result2.xlsx`;
- skipping the authorized M3/SP replay and independent full-path validator.

The controlling mathematical verdict is recorded separately in `XXT_PHASE_B_HANDOFF.md` and the original XXT return ZIP in this directory.

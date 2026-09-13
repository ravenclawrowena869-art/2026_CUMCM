# XXT Phase B Handoff — Winter-PV Fast-Fix R0

## Source review package

- XXT return ZIP: `CUMCM2026_C_Q2_XXT_WINTER_PV_PHASE_B_RETURN_R0.zip`
- SHA256: `be31c7b03f1c65c2a837363b5ebcbf3a1e2d6a03046a9ddfb5e9c9f3070c453d`
- ZIP CRC: `PASS`
- internal SHA256SUMS: `PASS`

The original XXT return ZIP is stored in this same GitHub handoff directory.

## Mathematical / causal verdict

- Controller verdict: `PROMOTE_P3_AMPCORR_TO_M3_REPLAY`
- Mathematical Review: `PASS WITH LIMITATION`
- promoted forecast candidate: `L2 + P3_AMPCORR_K7`
- selected K: `7`

## What is authorized

FYQ may promote the strictly causal `F1_K7` forecast layer into the existing M3/SP formal replay path and perform the required downstream validation.

## What is not authorized

This verdict does not authorize:

- `Q2_FREEZE`;
- declaring q=0.80 mathematically revalidated;
- replacing the final q-level without a separate Parameter Evidence closure;
- treating Oracle diagnostics as deployable;
- skipping the 334-day / 48,096-slot full-path replay and independent accounting/constraint validation.

## Remaining limitation

The exact-runner re-adjudication was a runner-fidelity repair after an earlier non-authoritative winter replica had been observed. Candidate set and selection rule were not changed, and K=7 remained selected. XXT therefore accepted the forecast-layer promotion with limitation rather than treating Nov–Dec as a pristine untouched holdout.

## Controller next action

For speed, use the existing code and evidence chain. Do not reopen K-selection or invent a new forecast family.

1. Run the minimal F1 q-level Parameter Evidence closure using the already-defined same-accounting cheap replay path.
2. Send the q decision to XXT for a fast mathematical check.
3. Run only the selected `F1_K7 + q*` through one formal M3/SP annual replay.
4. Run independent full-path validator and same-accounting comparison.
5. Only after current-version Mathematical PASS may Q2 enter Freeze and produce final `result2.xlsx`.

# Q2 Winter-PV Fast-Fix Handoff — 2026-09-13

## Full FYQ Delivery byte source

File name:
`CUMCM2026_C_Q2_FYQ_WINTER_PV_FAST_FIX_R0_DELIVERY.zip`

SHA256:
`011f1d0d64e4aa578a1c5f377b26ac5585d9317f807f9ffe89132b462d48ea36`

Size:
`104106491 bytes`

The exact full Delivery is stored in the shared ChatGPT Project/Library under `/数模/CUMCM2026_C_Q2_FYQ_WINTER_PV_FAST_FIX_R0_DELIVERY.zip` and can be retrieved in another Project window by exact filename through Project Files.

The 104 MB byte archive itself is intentionally not committed as a normal Git blob in this handoff branch. It sits very close to GitHub's single-file hard limit and the current GitHub connector has no direct local-file upload parameter for a binary of this size. Do not substitute another archive: verify the SHA above.

## XXT Phase B result archived in this branch

`CUMCM2026_C_Q2_XXT_WINTER_PV_PHASE_B_RETURN_R0.zip`

Outer SHA256:
`be31c7b03f1c65c2a837363b5ebcbf3a1e2d6a03046a9ddfb5e9c9f3070c453d`

Internal SHA256SUMS: PASS (7/7 payloads)
ZIP CRC: PASS

Controller verdict:
`PROMOTE_P3_AMPCORR_TO_M3_REPLAY`

Mathematical Review:
`PASS WITH LIMITATION`

Selected forecast layer:
`L2 + P3_AMPCORR_K7`

Selected K:
`7`

## Scope boundary

This verdict authorizes one formal M3/SP replay with only the forecast layer replaced by F1_K7. It does not authorize Q2 Freeze, does not revalidate q=0.80, and does not make Oracle deployable.

## Next action

1. Freeze F1_K7 artifact and SHA `ed198712edfbaddbd0f5d620a6f4dd5f976a49034836ad2b45bc6254a549de9a`.
2. Run one M3/SP replay with all other contracts unchanged.
3. Run the independent full validator and same-accounting F0/F1 comparison.
4. Return to Controller/XXT before Q2 re-freeze.

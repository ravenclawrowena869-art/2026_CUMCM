# Q1 Figure Chain Merge Decision R2

Freeze ID: `CUMCM2026_C_Q1_FREEZE_R0_20260911`

- CYQ: `SELECT_1_MAIN_FIGURE`; M1 PASS.
- FYQ: reproducible Frozen-output → Figure Data/table/script chain VERIFIED.
- XXT: `PASS_FOR_MERGE_GATE_WITH_NON_MODEL_FIGURE_PATCHES`; no Mathematical P0.

## Final
`SELECT_1_MAIN_FIGURE`

Four panels: price; load/PV forecast/optimized grid; discharge positive & charge negative; 145-state SOC with bounds/endpoints.
No-storage vs optimized economics is a compact table.

## Merge Gate
- M1 Paper relevance: PASS
- M2 Technical reproducibility: PASS
- M3 Mathematical validity: PASS after non-model patches
- M4 Final selection: PASS

`Q1_MODEL_RESULT_FREEZE = PRESERVED`

Forbidden: actual-PV wording; peak-shaving claim; inferring 26.90% from curve area; mixing Stage-1 exact with Stage-2 exported cost.

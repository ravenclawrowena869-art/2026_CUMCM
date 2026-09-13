# Code change / authority map

## Authoritative final path

Formal final claims use the byte-pinned Frozen common runner snapshot:

`authority_snapshot/FROZEN_Q2_CURRENT/run_q80_year.py`

SHA256: `5a2ab76328a70a939ab9ada31bb7603ce5acb45d6a0c2d2a18783524f8bb8e47`

The fast-fix implementation is layered around that runner through new modules/scripts:
- `src/winter_fastfix.py`: causal amplitude correction and K selection helpers;
- `src/exact_runner_adapter.py`: forecast/margin adapter into the frozen Q2 runner plus independent trace validation;
- `scripts/generate_ampcorr_candidates.py`: A1–A4-compliant F1 construction and provenance logs;
- `scripts/run_exact_common_worker.py`: exact M1/M2 runner wrapper;
- `scripts/run_exact_oracle_worker.py`: explicitly non-deployable O1/O2 diagnostics.

## Non-authoritative local replica

`src/q2fyq/*`, legacy `outputs/tuning/*`, and legacy `outputs/winter_eval/*` were used during implementation/debugging before the exact frozen runner was recovered. Their numerical cost claims are superseded by `outputs/exact_*`. `provenance/planner_vs_R2.patch` records the numerical-portability retry made to that local replica; it is **not used** to support the final Promotion or full-year claims.

No Q2 Frozen source file is overwritten by this delivery.

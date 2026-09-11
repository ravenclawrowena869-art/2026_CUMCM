# Astra Stop Point

The Astra burst is complete when all of the following are true:

- exact pre-run input provenance is bound;
- reusable Q2 engine is implemented;
- canonical alpha=0.80 four-strategy full-year execution finishes;
- canonical full-path validator passes or returns explicit technical failure evidence;
- canonical result2 candidate is written and read back;
- sensitivity switches are implemented and pilot-tested;
- a clean continuation handoff exists for FYQ Sol.

At that moment STOP.

Do not continue burning Astra on routine sweeps.

Allowed final status:

- `ASTRA_CORE_ENGINE_READY_FOR_SOL_CONTINUATION`
- `HOLD_INPUT_BINDING`
- `HOLD_AUTHORITY_DRIFT`
- `RETURN_CONTRACT_OR_MATH`
- `ASTRA_CORE_ENGINE_FAIL_TECHNICAL`

Forbidden:

- `Q2_MATHEMATICAL_RESULT_PASS = TRUE`
- `Q2_FROZEN = TRUE`
- `PAPER_READY = TRUE`

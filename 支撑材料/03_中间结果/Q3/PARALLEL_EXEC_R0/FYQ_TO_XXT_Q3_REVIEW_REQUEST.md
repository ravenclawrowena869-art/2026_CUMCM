# FYQ → XXT Q3 Mathematical Review / Contract-Lock Request

Module: `Q3-FORMAL-R1`  
FYQ execution branch: `fyq/q3-formal-r1`  
Frozen task base: `704d67f84d56428eb48892784579ecba6aaeb53b`  
Current status requested after review: `Q3_CONTRACT_LOCKED_FOR_FYQ` (or an explicit mathematical blocker)

## Implemented mapping

1. Canonical slots use `C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`.
2. Stage `s=0/1/2/3` maps to `00/06/12/18`; right endpoint `<=tau_s` is immutable.
3. Active commitment ledger is append-only. Preflight primary adjustment reference is `PREVIOUS_ACTIVE_COMMITMENT`.
4. PV adapter implements `PV_HOURLY_LINEAR_CAUSAL_BOUNDARY_V1` and the required block-hold sensitivity transform.
5. Physical validator replays the complete SOC trajectory and balance, not only terminal SOC.
6. Settlement accounting and result3 writing are isolated and hard-blocked until a locked contract is supplied.
7. Initial SOC binding is 6000 kWh as `REASONABLE_MODELING_ASSUMPTION`, not an official direct fact.

## Constraint / causality audit on toy fixture

- stage chronology: PASS;
- future leakage: 0;
- executed-slot mutation: 0;
- previous-active replay residual: 0;
- delta identity residual: 0;
- energy-balance residual: 0;
- SOC bound violation: 0;
- bridge mismatch: 0.

These are infrastructure tests only; no official-data mathematical PASS is claimed.

## Items requiring XXT lock before FYQ formal run

Please issue one hash-pinned contract (or veto) that resolves/authorizes at least:

1. whether the R2 preflight settlement identity is now the formal primary accounting contract;
2. whether `PREVIOUS_ACTIVE_COMMITMENT` + `DELIVERY_SLOT_PRICE` is the formal primary pair, with the stated mandatory comparators retained only as sensitivities;
3. whether `PV_HOURLY_LINEAR_CAUSAL_BOUNDARY_V1` is formally authorized as the primary 10-min transform;
4. the exact formal controller/optimizer semantics at each 00/06/12/18 stage, including what future load information is legally available and whether the Q2 formal engine is to be reused stagewise;
5. all hard physical constraints that must be inherited from Q2, including any constraint not listed in the current Q3 preflight;
6. whether result3 `调整购电量 = FINAL_ACTIVE_COMMITMENT_PER_SLOT` is locked for export;
7. exact formal validator requirements and whether any additional sensitivity is a pre-Freeze hard gate.

## Required response fields

- contract ID + source hash;
- variables/units/objective/hard constraints;
- information set and forecast-vintage rules;
- settlement/accounting formula;
- validator specification;
- mandatory sensitivities;
- `mathematical_pass` for the contract itself (not for annual results);
- explicit `Q3_CONTRACT_LOCKED_FOR_FYQ=true`, or a blocker/P0 statement.

Until this arrives, FYQ will not generate annual Q3 metrics or `result3.xlsx`.

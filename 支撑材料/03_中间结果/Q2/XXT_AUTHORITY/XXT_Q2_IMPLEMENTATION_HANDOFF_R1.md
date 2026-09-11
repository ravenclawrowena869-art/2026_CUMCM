# CUMCM 2026 C题 — Q2 Implementation Handoff R1

`Q2_MATH_CONTRACT_ID = CUMCM2026_C_Q2_MATH_CONTRACT_R1`

**From:** XXT Mathematical  
**To:** FYQ / Codex implementation  
**Release:** `Q2_MATH_READY_FOR_IMPLEMENTATION`  
**Freeze:** `FORBIDDEN`

## 1. Implement exactly these three policies

1. `DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE` (mandatory assumption baseline);
2. `POINT_FORECAST_DA_PLUS_CAUSAL_INTRADAY` (point-forecast main baseline);
3. `ANALYTIC_Q80_RESIDUAL_RESERVE_PLUS_CAUSAL_INTRADAY` (risk-aware candidate).

Do not add a fourth model unless a concrete implementation failure/gap is returned to XXT.

## 2. Inputs

Required:

- W2 formal causal load forecast (`LAG7`);
- W2 formal causal PV forecast (`TRAILING7_MEAN`);
- W2 past-only residual-history interface;
- Attachment1 fixed tariff for Q2;
- actual Attachment2 load/PV only as time-progressive realizations/evaluation truth;
- Feb1 SOC bridge from accepted R14 January replay;
- `time_mapping_version=C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`.

Explicitly reject W2 dynamic-price forecast for Q2.

Before optimizer execution, patch/seal W2 metadata with exact contract ID:

`CUMCM2026_C_Q2_MATH_CONTRACT_R1`.

## 3. Required 00:00 planning output per day

Persist before any day-actual is consumed:

- `q_DA[1:144]`;
- reference `xc_ref`, `xd_ref`, `E_ref`;
- policy ID;
- current actual SOC `E0`;
- forecast source/version/hash;
- contract ID;
- efficiency mode;
- terminal mode;
- planning timestamp and all input `known_at` values.

For the risk policy also persist per slot:

- residual history count;
- latest residual target timestamp;
- empirical quantile rank/value;
- `alpha=0.80`;
- reserve margin kWh.

## 4. Causal recourse pseudocode

```text
for day d in 2025-02-01..2025-12-31:
    E = previous realized day-end SOC
    read only data known by d 00:00
    solve day-ahead LP and LOCK q_DA[1:144]

    for t in 1..144:
        reveal current actual load/PV only
        build remaining horizon:
            current t = actual
            future t+1..144 = day-00:00 point forecasts
        keep q_DA immutable
        solve remaining-horizon LP with SOC starting at current E
        execute only current storage action
        emergency fills residual deficit last
        spill absorbs residual surplus
        update E
        log known_at / actions / balance / SOC
```

Q2 has no authorized intraday forecast re-estimation step in this contract.

## 5. Fixed-storage baseline pseudocode

```text
use same point-forecast day-ahead q_DA and reference storage schedule
for each actual slot:
    do not reoptimize storage
    if actual pre-storage balance is surplus:
        only scheduled charge may survive, clipped by surplus/power/SOC
        cancel scheduled discharge
    else:
        only scheduled discharge may survive, clipped by deficit/power/SOC
        cancel scheduled charge
    emergency covers remaining deficit
    spill covers remaining surplus
    record every clipped/cancelled amount
```

Never add/retime/increase a storage action in this baseline.

## 6. Risk policy implementation

At day 00:00, for each slot `t`:

1. select past residuals with same canonical slot and `target_ts < decision_time`;
2. use full signed residuals;
3. sort and take nearest-rank `ceil(0.80*n)`;
4. `margin_kWh = max(0,quantile_kW)/6`;
5. `risk_load_kWh = point_load_kWh + margin_kWh`;
6. solve the same day-ahead LP using risk load;
7. execute the same causal recourse algorithm as the point policy.

Do not use W2's conditional positive-residual P80 number directly as the Q80 margin.

## 7. Required full replay matrix

Primary comparison:

- P0 fixed storage, eta `0.9/0.9`, terminal T0;
- P1 point + causal, eta `0.9/0.9`, terminal T0;
- P2 Q80 + causal, eta `0.9/0.9`, terminal T0.

Mandatory additional runs before Freeze:

- efficiency alternative `sqrt(0.9)/sqrt(0.9)` for current formal Q2 policies as required by existing authority;
- terminal T1 `E_end=6000` and T2 `E_end>=6000`;
- risk alpha sensitivity `{0.75,0.80,0.85,0.90,0.95}`.

Do not collapse these into a single tuned run.

## 8. Required outputs back to XXT

Return at least:

- source/input manifest and hashes;
- solver/config versions;
- immutable day-ahead plan file;
- executed slot-level replay file;
- daily metrics and annual metrics;
- result2 workbook candidate;
- fixed-baseline clipping report;
- risk-quantile provenance report;
- terminal/efficiency/risk sensitivity summaries;
- full validator report per `XXT_Q2_VALIDATOR_SPEC_R1.md`;
- leakage audit;
- clean replay command/log;
- SHA256SUMS.

## 9. Stop / escalation rules

Stop and return to XXT rather than silently patching mathematics if any occurs:

- contract equation cannot be implemented without changing semantics;
- Q2 consumer cannot isolate dynamic-price rows;
- required residual history is unavailable/incompatible;
- frequent planner/recourse fallback occurs;
- hard constraints conflict;
- output mapping needs a new physical-time assumption;
- efficiency/terminal interpretation needs reopening.

Engineering-only path/format fixes may proceed if they do not change the math contract.

## 10. Next Gate

FYQ implementation/technical checks do not grant mathematical acceptance. After fresh replay and validator PASS, return to XXT for independent recomputation and only then consider downstream `Q2_MATHEMATICAL_PASS` / Freeze.

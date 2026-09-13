# Reproduction runbook

All commands assume execution from this delivery root.

## 1. Tests

```bash
PYTHONPATH=.:src python -m pytest -q tests
```

## 2. Exact candidate replay

Example K=7 M1 Feb-Oct prefix:

```bash
PYTHONPATH=.:src python scripts/run_exact_common_worker.py \
  --root . \
  --forecast inputs/F1_K7_through_oct31.csv \
  --model M1 \
  --start-date 2025-02-01 --end-date 2025-10-31 \
  --initial-soc-kwh 6000 \
  --output-dir /tmp/K7_M1 \
  --label K7_M1
```

For M2 change `--model M2`. For K=14/28 change the forecast path. K selection is scored only on Sep-Oct after each path has been carried causally from Feb-01 SOC=6000.

## 3. Exact winter continuation

Use the selected `inputs/F1_K7_annual_forecast.csv`, initial SOC equal to that policy/model's own Oct-31 terminal state, and run 2025-11-01 through 2025-12-31. Formal recorded outputs are under `outputs/exact_winter_eval/`.

## 4. Oracle diagnostics

```bash
PYTHONPATH=.:src python scripts/run_exact_oracle_worker.py \
  --root . --oracle O1 --model M1 \
  --output-dir /tmp/O1_M1
```

Repeat for O1/M2, O2/M1, O2/M2. These runs intentionally use future actuals and are diagnostic only.

## 5. Formal evidence namespaces

Use these for review:
- `outputs/exact_tuning/`
- `outputs/exact_winter_eval/`
- `outputs/exact_full_year/`
- `outputs/exact_oracle/`
- `evidence/FINAL_INDEPENDENT_VERIFICATION.json`

Legacy `outputs/tuning/` and `outputs/winter_eval/` are non-authoritative implementation history.

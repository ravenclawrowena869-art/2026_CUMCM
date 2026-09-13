# Q3-FORMAL-R1 interim reproduction

## Authority state

- Frozen base requested by task: `704d67f84d56428eb48892784579ecba6aaeb53b`.
- Latest visible Q3 state: `CONTRACT_PREFLIGHT_ONLY / FORMAL_RESULT_NOT_RUN`.
- Latest visible XXT mathematical artifact: `XXT_Q3_MATH_CONTRACT_PREFLIGHT_R2`, not `Q3_CONTRACT_LOCKED_FOR_FYQ`.
- Primary Q2-Q4 initial SOC assumption for the formal interval: `6000 kWh`, explicitly a modeling assumption rather than an official direct fact.

## Reproduce infrastructure validation

The supplied interim execution package contains the executable source and tests. Run:

```bash
cd 支撑材料/01_源程序/Q3
python -m pytest -q
python generate_interim_evidence.py
```

Expected behavior: all toy-fixture tests pass, while every formal-run/accounting/result3 entry point remains blocked.

## Formal continuation trigger

Only after a hash-pinned `Q3_CONTRACT_LOCKED_FOR_FYQ` arrives:

1. bind the locked contract instead of the preflight contract;
2. bind official Attachment 1/2/3 loaders and the official result3 workbook layout;
3. execute 00-only baseline and 00+06+12+18 rolling policy using the same accounting contract;
4. independently replay commitment ledger, accounting, energy balance and full SOC path;
5. run mandatory sensitivities: reference base, settlement price time, interpolation transform and initial SOC 4000/6000/8000;
6. only after formal validator PASS write `result3.xlsx`, read it back and hash all artifacts.

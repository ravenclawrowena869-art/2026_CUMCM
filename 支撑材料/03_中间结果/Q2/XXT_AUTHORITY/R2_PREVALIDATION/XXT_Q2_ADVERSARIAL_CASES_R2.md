# Q2 Adversarial / Negative-Oracle Cases R2

Purpose: verify that the corrected prevalidator catches semantic, accounting, causality, SOC and evidence failures before FYQ runs formal Q2. These are synthetic unit-style checks only; they do not use full-year competition outputs.

## R2 changes

The suite was rebuilt around the approved S1-A source-resolved balance. It explicitly distinguishes `w` (paid-unused normal commitment) from `v` (PV curtailment), checks that `Σp*w` is not added twice to total cost, and retains the accepted R1 causality/SOC/accounting failure families.

Input table: `XXT_Q2_ADVERSARIAL_CASES_R2.csv`.  
Executable oracle: `run_q2_adversarial_oracle_r2.py`.  
Observed results: `XXT_Q2_ADVERSARIAL_RESULTS_R2.csv`.

The executed local result is:

`23 / 23 cases matched expected detection`.

This means the synthetic oracle behaves as specified. It does **not** establish that FYQ's future full-year implementation passes these checks; the same checks must be run against current implementation artifacts.

## Covered failure classes

- old generic-spill S1 semantics;
- `w>q_DA`, `v>PV`, `w` mislabeled as PV curtailment;
- normal cost computed from accepted rather than committed normal energy;
- `Σp*w` double counted as a new fee;
- emergency multiplier error;
- post-00:00 `q_DA` mutation;
- future-actual leakage;
- Attachment4 dynamic price injected into Q2;
- emergency purchase while charging;
- simultaneous charge/discharge and SOC-path failure;
- daily SOC reset;
- terminal mismatch hidden as PASS;
- risk-alpha change without full replan/replay;
- fixed-storage safety override amplifying an action;
- missing `ONE_SLOT_DELAYED_ACTUAL` evidence;
- missing or source-collapsed S1 audit;
- time-mapping mismatch.

The two positive controls confirm that valid source-resolved S1-A and an optional `u_total=w+v` compatibility field pass when `w` and `v` remain separately evidenced.

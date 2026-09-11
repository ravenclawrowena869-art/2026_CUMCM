# Q2 Adversarial Oracle Execution Report R2

Run type: synthetic prevalidation / negative oracle.  
Formal Q2 result: `NOT_RUN`.

Command:

`python run_q2_adversarial_oracle_r2.py`

Observed stdout:

`adversarial_oracle: 23/23 cases matched expected detection`

All case-level outputs are in `XXT_Q2_ADVERSARIAL_RESULTS_R2.csv`.

## Adjudication

`Q2_ADVERSARIAL_PREVALIDATION_R2 = PASS`

Scope of PASS: the R2 checker catches the predefined synthetic violations under the corrected S1-A semantics. This is evidence for the validator contract only. FYQ's current-version implementation still requires full formal replay, independent accounting recomputation, leakage audit, S1 usage audit and required sensitivities before any mathematical result PASS or Freeze.

# Q2 PR #5 / PR #8 Repository Reconciliation R1

Date: 2026-09-11

`ACTIVE_ROLE = FYQ_TECHNICAL_ORCHESTRATOR`

Status: `REPOSITORY_RECONCILIATION_ONLY / NO_MATH_AUTHORITY_CHANGE`

## 1. Why this reconciliation exists

PR #8 has already been merged to `main`, while PR #5 was created earlier from an older base and now conflicts on several files under:

`支撑材料/03_中间结果/Q2/XXT_AUTHORITY/`

The conflict is a repository-history/integration problem. It is not evidence that the Q2 mathematical contract changed.

## 2. Conflict policy

This reconciliation deliberately does **not** overwrite the R1-named files already merged by PR #8.

The following overlapping paths from old PR #5 are therefore not replayed onto current `main`:

- `README.md`
- `SHA256SUMS.txt`
- `XXT_Q2_FORMAL_OPT_SPEC_R1.md`
- `XXT_Q2_IMPLEMENTATION_HANDOFF_R1.md`
- `XXT_Q2_MATH_CONTRACT_MANIFEST_R1.json`
- `XXT_Q2_VALIDATOR_SPEC_R1.md`

PR #8 remains the repository copy for those current-version filenames.

## 3. Material retained from PR #5

Only the non-overlapping repository-readable material that remains useful is brought forward:

- `XXT_AUTHORITY/R2_PREVALIDATION/` in full;
- `CUMCM2026_C_Q2_XXT_AUTHORITY_REPO_SUPPLEMENT_R1.zip` as a small repository supplement archive.

The R2 directory contains the selected XXT R2 prevalidation evidence and repository-only semantic supplements, including the explicit replacements for historical standalone files whose verified historical bytes were unavailable.

## 4. Formal authority boundary

This repository reconciliation does not alter the FYQ-selected formal execution chain:

1. original XXT Q2 R1 package provenance identity:
   `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`;
2. FYQ S1-A Controller authorization;
3. XXT R2 prevalidation package:
   `63c2494eac89b164830d9e26435332f6c06afedc0234ba5a05d25468f4d0a312`;
4. FYQ current implementation/input/writer/execution interfaces.

The package merged through PR #8 with SHA prefix `d22609f9...` remains a current repository copy / parallel repackage. Its presence in `main` does not by itself replace the selected execution authority chain.

Any future change to that mathematical authority relation requires XXT Mathematical Review plus FYQ integration. This reconciliation cannot make that decision.

## 5. Result / Freeze boundary

Unchanged:

- `Q2_PREVALIDATION_SPEC = PASS`;
- `Q2_FORMAL_RESULT = NOT_RUN`;
- `Q2_MATHEMATICAL_RESULT_PASS = FALSE`;
- `Q2_FROZEN = FALSE`.

## 6. PR migration

After this reconciliation PR is reviewed/merged:

- old PR #5 should be treated as `SUPERSEDED_BY_RECONCILIATION` and closed rather than force-merged;
- PR #6 remains the FYQ Controller/interface integration PR and may proceed through normal review;
- later Q2 plan/Astra PRs must not be used to bypass the current mathematical/controller review chain.

This file is a repository integration record, not a Mathematical PASS or Freeze record.

# HANDOFF TO CYQ CODEX R2

Status: `Q2_CANDIDATE_EXECUTION_RELEASED`

Consumer: CYQ-owned Codex/Astra execution node

Execution role:

`ACTIVE_ROLE = FYQ_TECHNICAL_ORCHESTRATOR`

This handoff supersedes `HANDOFF_TO_CYQ_CODEX_R1.md` for Q2 execution.

## 1. Read order

Read before implementation/run:

1. official C problem statement and attachments;
2. original XXT Q2 mathematical package identity `0d17f99f...e561`;
3. `XXT_R2_PREVALIDATION_BINDING_R1.md`;
4. `CONTROLLER_Q2_CURRENT_VERSION_REVIEW_R2.md`;
5. `Q2_AUTHORITY_CHAIN_R2.md`;
6. `Q2_IMPLEMENTATION_INTERFACE_R2.json`;
7. `Q2_INPUT_BINDING_R1.json`;
8. `Q2_RESULT2_WRITER_CONTRACT_R1.md`;
9. `Q2_DELAYED_ACTUAL_SENSITIVITY_PROTOCOL_R1.md`;
10. `Q2_RISK_HISTORY_COLD_START_BINDING_R1.md`;
11. `Q2_24H_TAIL_DIAGNOSTIC_PROTOCOL_R1.md`;
12. `Q2_EXECUTION_AND_ACCEPTANCE_R1.md`;
13. `Q2_EXECUTION_RELEASE_R1.md`;
14. current canonical workflow: Dispatcher -> Shared Core -> FYQ Profile -> Evidence Gate -> Parameter Protocol.

## 2. Canonical authority identity

Use:

- base math package SHA256:
  `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`;
- XXT R2 prevalidation package SHA256:
  `63c2494eac89b164830d9e26435332f6c06afedc0234ba5a05d25468f4d0a312`;
- S1 mode: `S1_A_PAID_UNUSED_NORMAL_ENERGY`.

Do not bind formal execution to PR #8 package SHA `d22609f9...`; it is not in the selected current authority chain.

## 3. Pre-run action

From the exact bytes used by the execution environment, record:

- `FYQ_W2_FORMAL_CAUSAL_FORECAST.csv` SHA256;
- `FYQ_W2_RESIDUAL_HISTORY_INTERFACE.csv` SHA256;
- Jan31->Feb1 bridge artifact SHA256;
- source-code/config hash;
- solver/runtime/package versions.

If any expected artifact is unavailable, stop with `HOLD_INPUT_BINDING` and report the exact missing path/artifact. Do not synthesize replacements.

## 4. Required execution matrix

At minimum run on identical official data/accounting:

1. point DA + causal intraday recourse;
2. point DA + fixed-storage safety-override baseline;
3. signed-residual Q80 DA + causal intraday recourse;
4. signed-residual Q80 DA + fixed-storage safety-override baseline.

Each policy advances its own lawful SOC path.

## 5. Required sensitivity/evidence

Mandatory before returning the candidate delivery:

- alpha `.75/.80/.85`, each replan + full replay;
- primary same-slot actual vs `ONE_SLOT_DELAYED_ACTUAL` full replay;
- S1 `w` audit separate from PV curtailment `v`;
- required efficiency and annual-terminal sensitivities;
- 24-h tail/day-boundary diagnostic;
- independent full-path balance/SOC/accounting replay;
- leakage/known_at audit;
- saved result2 writer/readback verification.

If `w` materially explains feasibility/advantage, mark `RETURN_TO_XXT_S1_COUNTERFACTUAL` rather than hiding it.

If tail diagnostic returns `TAIL_CHALLENGER_REQUIRED`, stop the affected robustness claim and return to FYQ/XXT; do not silently extend the horizon.

## 6. Required delivery

Return one candidate ZIP containing at least:

- source/config/tests;
- input/provenance manifest;
- solver/runtime manifest;
- slot-level ledger;
- daily/strategy summaries;
- constraint replay;
- independent accounting replay;
- S1 audit;
- sensitivity outputs;
- day-boundary diagnostic;
- result2 candidate workbook + readback evidence;
- execution report;
- handoff to XXT Mathematical Review;
- internal `SHA256SUMS.txt`, outer SHA256 and CRC result.

## 7. Status boundary

`Q2_EXECUTION_RELEASE = RELEASED`

But still:

- `Q2_FORMAL_RESULT = NOT_RUN` until this execution completes;
- `Q2_MATHEMATICAL_RESULT_PASS = FALSE`;
- `Q2_FROZEN = FALSE`;
- candidate numbers are not Paper facts.

Return path:

`CYQ Codex/Astra -> FYQ Controller -> XXT current-version Mathematical Review -> Evidence Gate -> Freeze`.

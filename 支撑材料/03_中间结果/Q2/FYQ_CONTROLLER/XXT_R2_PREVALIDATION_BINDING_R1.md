# XXT R2 Prevalidation Binding R1

`ACTIVE_ROLE = FYQ_TECHNICAL_ORCHESTRATOR`

Date: 2026-09-11

## Received package

File:
`CUMCM2026_C_XXT_Q2_PREVALIDATION_Q3_PREFLIGHT_R2_20260911.zip`

FYQ fresh verification:

- outer SHA256: `63c2494eac89b164830d9e26435332f6c06afedc0234ba5a05d25468f4d0a312`
- ZIP CRC: `PASS`
- internal `SHA256SUMS.txt`: `14/14 PASS`
- included synthetic oracle rerun by FYQ: `23/23 cases matched expected detection`

The independent rerun returned process code 0. A sandbox spreadsheet-runtime warmup warning occurred outside the oracle logic and did not alter the oracle result.

## Mathematical status accepted from XXT R2

- `Q2_PREVALIDATION_SPEC = PASS`
- `Q3_CONTRACT_PREFLIGHT = PASS_WITH_LIMITATION`
- `Q2_FORMAL_RESULT = NOT_RUN`
- `Q2_MATHEMATICAL_RESULT_PASS = FALSE`
- `Q2_FROZEN = FALSE`
- `Q3_FORMAL_RESULT = NOT_RUN`
- `Q3_MATHEMATICAL_RESULT_PASS = FALSE`
- `Q3_FROZEN = FALSE`

Q2 S1-A is corrected to the source-resolved form:

`q_DA - w + r + PV + d = L + c + v`

with `0<=w<=q_DA`, `0<=v<=PV`.

Billing remains:

`C_total = Σ p*q_DA + Σ 5*p*r`.

`Σp*w` is diagnostic only and must not be added a second time.

## Canonical Q2 mathematical chain selected by FYQ

The current implementation chain is:

1. base XXT mathematical contract package:
   `CUMCM2026_C_XXT_Q2_FORMAL_OPT_SPEC_R1_DELIVERY.zip`
   SHA256 `0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`;
2. FYQ S1-A Controller authorization;
3. this XXT R2 prevalidation return, outer SHA256
   `63c2494eac89b164830d9e26435332f6c06afedc0234ba5a05d25468f4d0a312`;
4. FYQ current implementation/input/writer/execution interfaces in this directory.

The PR #8 package with SHA256
`d22609f9ec0368888472945f948de66fb70669a3bc89877574fd0ab8834ea54c`
is **not selected as canonical mathematical authority**. It remains a parallel repository candidate/repackage and may not override the chain above unless a later XXT review explicitly adopts it.

This resolves the FYQ version-integration blocker without pretending the two ZIPs are byte-identical.

## Remaining evidence boundary

XXT R2 explicitly requires before Q2 Freeze:

- `ONE_SLOT_DELAYED_ACTUAL` full downstream replay;
- alpha sensitivity with replan + full replay;
- S1 usage audit;
- terminal/efficiency sensitivities required by the contract;
- 24-h tail/day-boundary diagnostic;
- current implementation validator + independent accounting replay.

These are execution/validation requirements, not a reason to keep the first formal candidate run blocked once the execution interface is fully specified.

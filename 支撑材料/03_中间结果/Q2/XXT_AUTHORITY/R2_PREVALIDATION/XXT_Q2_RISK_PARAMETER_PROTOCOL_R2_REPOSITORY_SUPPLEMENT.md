# XXT Q2 Risk Parameter Protocol — Repository Supplement R2

`ACTIVE_ROLE=XXT_MATHEMATICAL`

Status: `SEMANTIC_REPLACEMENT_FOR_UNAVAILABLE_R1_STANDALONE_BYTES / NO_MATH_CHANGE`

Base contract: `CUMCM2026_C_Q2_MATH_CONTRACT_R1`

## 1. Provenance boundary

The historical package checksum manifest lists `XXT_Q2_RISK_PARAMETER_PROTOCOL_R1.md` with SHA256
`53b0a88bcf2f9742f28d58cb42b7eb46ec23822d681489e49e3dfd9535b951b3`,
but those exact standalone bytes are not available in the current repository delivery.

This R2 supplement does **not** claim byte identity with that historical file. It makes the currently accepted risk semantics directly readable from the selected authority chain:

- base R1 formal spec, especially §7 Risk-aware candidate;
- FYQ Controller acceptance of the analytic `alpha=0.80` anchor;
- R2 prevalidator `P17/P18` and its sensitivity requirements.

PR #8 remains noncanonical and is not adopted by package identity.

## 2. Residual definition and causal history

For canonical slot `t`, define net-load residual

`epsilon = (L_actual - PV_actual) - (L_hat - PV_hat)`.

For decision day `d`, the calibration history for slot `t` contains only residuals whose target timestamp is **strictly earlier** than `d 00:00`.

Hard rules:

- same canonical slot;
- full **signed** residual sample, not positive residuals only;
- no current/future-day actuals;
- compatible frozen time mapping and formal load/PV forecast families;
- all source timestamps and `known_at` fields must be auditable;
- missing or provenance-incompatible history is never silently backfilled with future data.

## 3. Analytic candidate anchor

Ignoring inter-slot storage coupling, the isolated reserve problem is

`J(m) = p*m + 5*p*E[(epsilon-m)_+]`.

For a continuous residual distribution,

`J'(m)=p-5*p*P(epsilon>m)`,

so the isolated critical fractile satisfies

`P(epsilon <= m)=0.80`.

Therefore the formal candidate anchor remains:

`RISK_ALPHA_PRIMARY = 0.80`.

This is an **analytic candidate anchor**, not a proof of the globally optimal alpha for the full storage-coupled annual control problem.

## 4. Reserve construction

For each decision day/slot, compute the deterministic empirical quantile from the causal signed-residual history using nearest rank `ceil(alpha*n)`.

The nonnegative reserve energy is

`m_(d,t)(alpha) = (1/6) * max(0, Q_alpha(H_(d,t)))  [kWh]`.

Apply this reserve to the point net-load planning input and rerun the same day-ahead optimization and downstream causal controller. A change in `alpha` requires rebuilding the causal quantiles, **replanning**, and performing a full downstream replay.

## 5. Required neighborhood and evidence

Before any risk-related Freeze claim:

- run `alpha in {0.75, 0.80, 0.85}` as mandatory local sensitivity;
- each alpha must use its own causal history/quantiles and full replan + replay;
- compare total purchase cost, emergency energy/cost, tail emergency behavior, `w/v`, battery throughput and SOC-path behavior;
- hard feasibility, leakage, commitment immutability and independent accounting are checked before cost ranking;
- no post-hoc reuse of one fixed trajectory is allowed.

Stronger tail values may be used only as explicit stress tests; they must not be selected retrospectively from Feb–Dec actual outcomes and then described as causal historical policy choices.

## 6. Freeze boundary

`RISK_PARAMETER_FROZEN = FORBIDDEN` until current-version execution provides causal quantile provenance, the registered alpha replays, downstream full-path validation, and independent cost/accounting checks.

This file is a repository-readability supplement. It does not grant Q2 result PASS or Freeze.

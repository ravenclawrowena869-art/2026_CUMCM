# CUMCM 2026 C题 — Q2 Risk Parameter Protocol R1

**Contract:** `CUMCM2026_C_Q2_MATH_CONTRACT_R1`  
**Risk policy:** `ANALYTIC_Q80_RESIDUAL_RESERVE_PLUS_CAUSAL_INTRADAY`  
**Status:** `IMPLEMENTATION_SPEC / NOT_FROZEN_RESULT`

## 1. Risk source

Q2 under-purchase is asymmetric: normal planned purchase costs `c_t`, while residual emergency purchase costs `5*c_t`. Therefore forecast error must be evaluated through downstream cost/risk, not only MAE/WAPE.

W2 evidence reports net-load residual diagnostics, including an underforecast rate near 49% and conditional positive-tail P80/P90/P95 values. Those values establish that material positive residuals exist, but they do **not** select the formal reserve parameter.

## 2. Residual definition and provenance

Use net-load power residual

\[
\varepsilon=(L^{act}-PV^{act})-(\hat L-\hat{PV}).
\]

For decision day `d` and canonical slot `t`, the calibration set is

\[
\mathcal H_{d,t}=\{\varepsilon_{s,t}: target\_ts<d\ 00{:}00\}.
\]

Hard rules:

- same canonical `slot_id`;
- only historical target timestamps strictly before the current 00:00 decision;
- no current/future day actuals;
- residuals must correspond to the formal predeclared load/PV families and compatible time mapping;
- quantile is computed from the **full signed residual sample**, not only positive residuals;
- deterministic nearest-rank empirical quantile: rank `ceil(alpha*n)`.

If the required historical set is missing or provenance-incompatible, the risk candidate for that slot is not silently imputed. Flag the slot and fail the risk-policy provenance gate; the point policy may still be run separately.

## 3. Primary analytical anchor

For one marginal reserve decision `m`, ignoring inter-slot storage coupling,

\[
J(m)=c m+5c\,\mathbb E[(\varepsilon-m)_+].
\]

For a continuous residual distribution,

\[
J'(m)=c-5c\,P(\varepsilon>m).
\]

Setting `J'(m)=0` gives

\[
P(\varepsilon\le m)=0.8.
\]

Thus:

`RISK_ALPHA_PRIMARY = 0.80`

This is frozen as the **candidate definition**, not as a proven globally optimal system parameter.

Because the 5× multiplier is proportional to the same `c_t`, the isolated critical fractile remains 0.8 across tariff slots. Storage coupling, SOC scarcity and spill can move the system-level optimum, so the full replay remains mandatory.

## 4. Reserve construction

For each day/slot:

\[
m_{d,t}(\alpha)=\frac16\max(0,Q_\alpha(\mathcal H_{d,t}))\quad\text{kWh}.
\]

The risk-adjusted planning load is

\[
\tilde l_{d,t}=\hat l_{d,t}+m_{d,t}(\alpha).
\]

Run the same day-ahead LP and the same causal intraday recourse as the point policy.

## 5. Pre-registered neighborhood / stress set

These runs are **sensitivity**, not retrospective tuning:

- local neighborhood: `alpha in {0.75, 0.80, 0.85}`;
- stronger tail stress: `alpha in {0.90, 0.95}`.

Rationale:

- 0.80 is the cost-ratio analytical anchor;
- 0.75/0.85 test nearby conservatism without changing model identity;
- 0.90/0.95 probe the positive tail already shown by W2 diagnostics.

Do not select 0.90/0.95 merely because they look best after seeing all Feb–Dec actual results and then claim that the earlier dates used that data. If a different alpha is to become a future formal policy parameter, open a new contract version and use a causal/nested calibration rule based only on information available before each decision.

## 6. Acceptance / comparison criterion

All policies are replayed over the same formal period and first must pass:

- zero hard-constraint violations;
- zero future-information leakage;
- immutable normal commitments;
- emergency/no-charge rule;
- objective independent recomputation.

Then compare:

1. total Q2 purchase cost (primary economic metric);
2. emergency purchase energy and cost;
3. P95 daily emergency cost (tail-risk metric);
4. spill/curtailment;
5. battery throughput and SOC boundary behavior;
6. specified-date outputs;
7. terminal sensitivity and efficiency sensitivity.

No arbitrary “must improve by X%” threshold is preregistered. A cost improvement may be reported only if independently reproduced; a robustness claim requires the neighborhood/stress runs to preserve the substantive conclusion.

If Q80 does not improve the relevant cost/risk tradeoff, retain P1 and report P2 as a rejected candidate. Do not retune on the final replay until a preferred number appears.

## 7. W2 positive-tail statistic warning

W2 currently reports quantiles conditioned on `residual > 0`:

- positive residual P80 ≈ 446.8982 kW;
- P90 ≈ 662.2788 kW;
- P95 ≈ 863.8899 kW.

These are **not** `Q_0.80`, `Q_0.90`, `Q_0.95` of the full signed residual distribution. They may be used to describe tail scale and to motivate stress checks, but implementation must recompute the contract-defined full-distribution quantiles from the causal residual-history interface.

## 8. Freeze condition for risk claims

`RISK_PARAMETER_FROZEN = FORBIDDEN` until the current implementation provides:

- causal per-day/per-slot quantile provenance;
- full-period replay for P1/P2;
- registered alpha sensitivity runs;
- efficiency and terminal cross-checks where required;
- independent cost/constraint/leakage validation.

# Q2 Risk-History / Cold-Start Binding R1

Status: `SOURCE_BACKED_IMPLEMENTATION_BINDING`

This file closes the risk-history/cold-start ambiguity reported in the PR discussion. It does not retune alpha and does not modify the base mathematical contract.

## 1. Source-backed rule

The authoritative original XXT R1 risk protocol states:

- residual: `e[h,t]=(Lact-Sact)-(Lhat-Shat)` in kWh;
- keep the full signed residual distribution;
- use expanding same-slot history;
- strict cutoff `target_ts < T_d` and all dependencies `known_at <= T_d`;
- earliest calibration date: `2025-01-08`;
- nearest-rank empirical quantile at rank `ceil(alpha*n)`;
- primary `alpha=0.80`;
- if `n=0`, set reserve to 0 and record `INSUFFICIENT_HISTORY_POINT_FALLBACK`; do not backfill from full-year statistics.

The original W2 Controller Handoff additionally reports:

- formal output period starts `2025-02-01`;
- Feb1 residual-history observations: `3455`;
- latest included residual target: `2025-01-31T23:50:00`;
- Jan31 slot-144 target at Feb1 00:00 is excluded by the strict cutoff.

Therefore the formal Feb-Dec run begins after a real January calibration warm-up. The `n=0` rule is a genuine early-history fallback, not permission to ignore missing formal-period provenance.

## 2. Minimum sample rule

No arbitrary extra `n_min` threshold is introduced.

For the nearest-rank empirical quantile, the mathematical minimum is `n>=1`. Every run must record per day/slot:

- `sample_count`;
- `latest_history_target_ts`;
- residual-history hash;
- alpha;
- selected rank;
- quantile value;
- fallback flag.

For the formal period, an unexpected `n=0` or provenance-incompatible history is treated as `FAIL_RISK_PROVENANCE`, because the accepted W2 warm-up establishes non-empty history before Feb1. The early-history `n=0` fallback is retained only where it is legitimately reached during warm-up construction.

## 3. Causal guard

Changing alpha from `.80` to `.75` or `.85` requires rebuilding each day's quantile from that day's lawful history and rerunning the downstream policy. Reusing a fixed full-year quantile or a previously solved path is forbidden.

W2 conditional positive-residual P80/P90/P95 diagnostics are not the same as the full signed-distribution quantiles used by the contract and may not be substituted.

## 4. Acceptance

Before Freeze, the validator must confirm:

- no `target_ts >= decision_time` in risk calibration;
- no future actual backfill;
- per-slot history provenance is complete;
- nearest-rank rule is exact;
- every alpha sensitivity is a full replan + replay;
- formal-period `n=0` count is zero unless explicitly returned to XXT as a provenance failure.

# Q2 24-hour Tail / Day-Boundary Diagnostic Protocol R1

Status: `FYQ_EVIDENCE_PROTOCOL / REQUIRED_BEFORE_FREEZE`

Purpose: satisfy the XXT R2 requirement that daily-horizon truncation be checked explicitly instead of silently assuming the midnight boundary is harmless.

## 1. Boundary windows

For every adjacent day pair `(d,d+1)` define:

- end window: day `d`, slots `139..144` (last 60 minutes);
- start window: day `d+1`, slots `1..6` (first 60 minutes).

Do not reinterpret slot labels; use canonical ordinal mapping.

## 2. Required per-boundary evidence

Record for each strategy and boundary:

- `E[d,138]`, `E[d,144]`, `E[d+1,6]`;
- min/max SOC within both windows;
- lower/upper SOC bound-hit flags;
- charge/discharge throughput in both windows;
- emergency kWh and CNY in both windows;
- `w` and `v` in both windows;
- planner/recourse fallback flags;
- energy-balance and SOC-recursion max residuals;
- day-end and next-day-start forecast/provenance hashes.

Aggregate across all 333 internal Feb-Dec day boundaries plus the Jan31→Feb1 bridge separately.

## 3. Boundary-dependence diagnostics

For every candidate-vs-baseline comparison compute:

- full-period cost gap `Delta_full`;
- cost gap after removing all boundary windows, `Delta_interior`;
- total candidate-vs-baseline cost-gap contribution from the boundary windows,
  `Delta_boundary = Delta_full - Delta_interior`;
- emergency-energy gap analogues;
- boundary SOC-bound-hit counts.

Flag `TAIL_CHALLENGER_REQUIRED` if any of the following holds:

1. any hard violation, provenance failure or unexplained solver fallback occurs in a boundary window;
2. `sign(Delta_full) != sign(Delta_interior)` for the main candidate-vs-baseline comparison;
3. `abs(Delta_boundary) >= abs(Delta_full)` when `Delta_full != 0`, meaning the claimed advantage is entirely boundary-dependent or can be neutralized by the boundary contribution;
4. delayed-actual or terminal-mode sensitivity changes the main ranking and the change is concentrated at day boundaries;
5. repeated day-end SOC depletion plus next-day emergency behavior is large enough to alter the paper's qualitative scheduling claim.

Items 2 and 3 avoid an arbitrary percentage threshold: the trigger is tied directly to whether the main ranking/claim depends on the horizon boundary.

## 4. Challenger behavior

If `TAIL_CHALLENGER_REQUIRED = TRUE`, do **not** silently extend the formal controller horizon or introduce tomorrow's unavailable information.

Return the current evidence to XXT/FYQ and open a separately specified horizon/continuation-value challenger with its own causal information contract. Until that challenger is adjudicated, the affected robustness claim is `HOLD`.

If the flag is false and all hard replay checks pass, report the boundary diagnostic as supporting evidence only; it does not by itself prove global optimality.

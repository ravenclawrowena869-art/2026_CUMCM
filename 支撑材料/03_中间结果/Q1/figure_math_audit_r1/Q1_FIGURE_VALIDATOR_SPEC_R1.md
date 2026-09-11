# Q1 Figure Validator Specification R1

Role: `XXT_MATHEMATICAL`

## 1. Source-of-Truth

Every final candidate records `freeze_id=CUMCM2026_C_Q1_FREEZE_R0_20260911`, schedule/baseline/metrics source, `time_contract=C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`, figure script and Figure Data hash. Reject screenshot/chat/manual-copy sources.

## 2. Time mapping

Power data: exactly 144 unique slots, physical boundaries `0,1/6,...,24h`; raw `0:10` corresponds to `(00:00,00:10]`, raw `0:00+1` to `(23:50,24:00]`. SOC, if shown, must contain 145 endpoint states including E0 and E144.

## 3. Units

With `Δt=1/6h`: `grid_kw=grid_kwh/Δt`, charge/discharge likewise. Cost is `Σ price_yuan_per_kwh*grid_kwh`. Hard fail on kW/kWh confusion.

## 4. Frozen-field reconciliation

Independently compare all used fields with Frozen output: load, PV forecast, grid, charge, discharge, SOC, price. Recommended pre-round tolerance `1e-9`.

## 5. Baseline

If no-storage baseline appears: `grid_base_kw=max(load_kw-pv_kw,0)`, `curtail_base_kw=max(pv_kw-load_kw,0)`, storage=0. Recompute baseline purchase/cost, Stage-2 cost, savings. Required unrounded savings anchor: `26.89812155476249%`.

## 6. Stage-1 vs Stage-2

Formal optimized schedule figures must use Stage-2 Frozen schedule. “optimized/final/exported schedule cost” = `35126.948689289624 CNY`. Stage-1 exact, if shown, must be explicitly labeled `35126.948589289634 CNY`. They may round to the same 2-decimal value but cannot be merged at full precision.

## 7. Storage sign

Separate charge/discharge are nonnegative magnitudes. Signed net is `discharge-charge`; legend must state positive=discharge, negative=charge. Net curve alone cannot prove zero simultaneous charge/discharge.

## 8. SOC

If shown, independently check `[1200,10800] kWh`, E0=E144=6000, and 145-state alignment. Bound lines must be exactly 1200 and 10800 kWh.

## 9. Price / dual axis

Preferred encoding is separate aligned panel. If dual axis is used, units must be explicit, scales not post-hoc tuned, caption must forbid cross-axis magnitude comparison, and no quantitative claim may derive from visual similarity. Otherwise reject as `MISLEADING_ENCODING`.

## 10. Slot encoding

10-min power variables should use step/stairs for final mainline plots. Ordinary line connectors are allowed only if registry marks them trend-only and no within-slot/inter-slot ramp claim is made.

## 11. Normalization

Normalized curves are `SHAPE_ONLY` and cannot support power limits, SOC bounds, peak power, energy totals, cost, or absolute baseline differences.

## 12. Window audit

Any non-full-horizon figure must record window start/end, rule, reason, and whether selection was predeclared or post-hoc. Post-hoc diagnostic windows cannot support full-day claims.

## 13. Labels

Use “光伏预测功率” for Q1 Attachment1 PV; distinguish 购电功率/kW from 购电量/kWh; SOC uses kWh; price uses 元/kWh.

## 14. Claim checks

- “节省26.90%”: independently recompute baseline and Stage-2 cost.
- “SOC安全”: check full 145-state trajectory.
- “无同时充放电”: check Frozen schedule, not only net curve.
- “削峰”: compare max grid power. Current evidence has optimized peak > baseline, so reject this claim.

## 15. Export

If selected as final paper figure: PNG>=300dpi, PDF/SVG retained, Figure Data retained, script retained, registry row retained, paper-scale labels readable, provenance/hash recorded.

## PASS

`SOURCE PASS + TIME PASS + UNIT PASS + CLAIM PASS + ENCODING PASS + PROVENANCE PASS`.

Mathematical PASS does not itself select the figure for the paper.
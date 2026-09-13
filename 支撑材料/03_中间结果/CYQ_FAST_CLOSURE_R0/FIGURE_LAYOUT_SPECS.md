# FIGURE LAYOUT SPECS R0

All figures remain specification-only until their registry row reaches `DATA_LOCKED`; no placeholder values are drawn.

## Q2-F01 Emergency-purchase heatmap
- x: time-of-day slot; y: evaluation date; fill: frozen emergency-purchase metric.
- Full horizon only. If page density forces aggregation, register the exact aggregation before drawing.
- Caption must state unit, evaluation horizon, final q and freeze version after available.

## Q2-F02 PV-bias heatmap
- x: time-of-day; y: date; fill: one signed error definition fixed by the data contract.
- Caption must explicitly state `forecast-actual` or `actual-forecast`.

## Q3-F01 Multi-vintage forecast / commitment evolution
- Use vertically aligned panels on one objectively selected day.
- Forecast vintages and commitment trajectories share the x-axis; mark 00/06/12/18 boundaries.
- Curves before a stage boundary must not be redrawn using future vintages.
- Default selection rule: day with maximum total absolute plan adjustment in the Frozen annual ledger.

## Q3-F02 Stage ablation
- Compare 00-only, 00/06, 00/06/12, 00/06/12/18 on the same annual horizon and accounting contract.
- Separate cost and emergency/risk metrics into aligned panels rather than forcing different units onto a dual axis.
- Do not call the best observed category “optimal” without matching evidence.

## Q4-F01 Dynamic-price heatmap
- x: time-of-day; y: date; fill: price.
- Caption must distinguish actual realized price used for descriptive plotting from causal price information available to the decision rule.

## Q4-F02 Aligned price–purchase–SOC mechanism panel
- Three vertical panels sharing x: formal causal price input; purchase/emergency purchase; SOC.
- If realized/oracle price is displayed, show it only as a separately labelled `oracle diagnostic` reference.
- No dual y-axis.
- Default selection rule: day with maximum emergency-purchase cost under the frozen formal causal strategy.

## Final export contract
After `DATA_LOCKED`, retain editable script + Figure Data CSV + 300 dpi PNG + PDF/SVG + registry row containing source file, freeze version, time scope and selection rule.

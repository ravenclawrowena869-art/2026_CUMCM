# Q1 Legacy Figure Package Audit R1

Audited package: `CUMCM2026_C_Q1_FIGURES_A_R1.zip`  
Status of package: `DRAFT_REFERENCE_ONLY`  
XXT verdict on provenance: **SUFFICIENT FOR MATHEMATICAL AUDIT, NOT FINAL FIGURE AUTHORITY**

## 1. Data provenance reconciliation

Legacy `Q1_FROZEN_FIGURE_DATA_R1.csv` was independently compared with R2 Frozen schedule/baseline.

All 144 rows match Frozen evidence within floating-point noise:

- load max abs diff: `0 kW`;
- PV max abs diff: `0 kW`;
- optimized grid power max abs diff: `9.095e-13 kW`;
- charge/discharge/net-storage max abs diff: `<=4.547e-13 kW`;
- no-storage baseline grid max abs diff: `9.095e-13 kW`;
- price max abs diff: `0`;
- raw time-label mismatch count: `0`;
- `time_hour = slot_id/6` max abs diff: `3.553e-15 h`。

Legacy metric JSON exactly matches Frozen Stage-2/baseline cost anchors. Therefore the old package is not `INSUFFICIENT_PROVENANCE`.

## 2. Figure 01 — 购电与储能联合调度结果

**Status: `MATHEMATICALLY_VALID`**

The load, PV, grid purchase and storage-net series all trace to the Frozen Stage-2 schedule and are consistently expressed in kW. Storage net is `P_discharge-P_charge`, so positive means discharge and negative means charge.

Required non-model patches before final paper use:

1. 图例“光伏发电”必须改成 **“光伏预测功率”**，因为Q1 Attachment1是预测功率，不是actual PV；
2. 10 min功率量建议用step/stairs而非普通线性插值；
3. caption需说明storage net正放电、负充电；
4. 当前图没有SOC，不能单独支持“SOC满足上下界/首末状态”Claim；
5. 当前图没有price，不能单独支持“低价充电、高价放电”Claim。

It may support the statement that load, PV forecast, grid purchase and storage action are temporally coordinated, but not by itself prove SOC feasibility, zero simultaneous C/D, the 26.90% saving, or price-arbitrage timing.

## 3. Figure 02 — 储能优化前后购电曲线对比

**Status: `MATHEMATICALLY_VALID`**

- baseline is the Frozen no-storage replay;
- optimized curve is the Frozen Stage-2 schedule;
- both are kW;
- full 24h is shown;
- the annotation `48052.05 / 35126.95 / 12925.10 / 26.90%` matches Frozen metrics;
- the optimized cost annotation uses Stage-2 exported cost, not Stage-1 exact cost.

Important limitations:

1. **Do not call this a peak-shaving figure.** The no-storage maximum grid power is about `4956.50 kW`, while Stage-2 reaches about `8458.83 kW`; low-price charging increases instantaneous grid draw.
2. Cost is not the simple area under the power curve because price varies by slot. The 26.90% saving must be backed by `Σ p_t g_t` recomputation.
3. The curve is useful for showing temporal restructuring; precise cost comparison is usually better shown in a table.
4. Final rendering should preferably use step/stairs for 10 min slot power.

Whether the figure belongs in the paper is a CYQ Paper Relevance decision, not an XXT decision.

## 4. Overall verdict

`LEGACY_PACKAGE_MATH_STATUS = VALID_REFERENCE_NOT_FINAL`

No mathematical P0 requiring Q1 Frozen reopen was found. The legacy figures remain references only; final selection and final Figure Data/script must pass the new Merge Gate.
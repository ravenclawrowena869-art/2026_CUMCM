# XXT Q1 Figure Mathematical Review R1

ACTIVE_ROLE = `XXT_MATHEMATICAL`  
PARALLEL_MODE = `TRUE`  
FREEZE_ID = `CUMCM2026_C_Q1_FREEZE_R0_20260911`

## 0. Review result

**STATUS = PASS_FOR_MERGE_GATE_WITH_NON_MODEL_FIGURE_PATCHES**

No mathematical P0 was found. Q1 Frozen model/result remains closed.

This review does **not** freeze figure selection.

## 1. Inputs / integrity

Shared input SHA256 checks: PASS. Legacy figure ZIP internal checksum: PASS. R2 delivery is used as technical evidence source, and the formal numeric anchors agree with Freeze Manifest / Paper Handoff.

Three mandatory project workflows were read again before this audit. Applied rules: Frozen data only, independent source reconciliation, Claim-matched validation, paper figures as evidence rather than decoration, and no change to the frozen model/result.

## 2. Legacy audit verdict

| legacy figure | verdict | mathematical conclusion |
|---|---|---|
| Q1_FIG_01 购电与储能联合调度结果 | `MATHEMATICALLY_VALID` | source data correct; label “光伏发电” must become “光伏预测功率”; final power encoding should preferably be step/stairs; current figure alone cannot support SOC or price-arbitrage Claim |
| Q1_FIG_02 储能优化前后购电曲线对比 | `MATHEMATICALLY_VALID` | baseline/Stage-2 data and 26.90% annotation correct; cannot be described as peak shaving because optimized max grid power is higher than baseline; precise savings better represented by table |

Legacy package overall: `VALID_REFERENCE_NOT_FINAL`.

## 3. Key mathematical corrections for Figure Merge

1. Q1 Attachment1 contains **PV forecast power**. Final figure legend/caption must not call it actual PV generation.
2. 144 power observations represent 10 min intervals under the right-endpoint contract. Final mechanism/result chart should use interval-aware step encoding or mark ordinary line connectors as trend-only.
3. Stage-1 exact = `35126.948589289634 CNY`; Stage-2 formal exported schedule = `35126.948689289624 CNY`. Final schedule figures use Stage-2 data/cost.
4. No-storage maximum grid power = `4956.4995 kW`; Stage-2 maximum grid power = `8458.8273 kW`. Therefore Q1 does **not** support “外网购电峰值下降/削峰”. Supported wording is temporal restructuring / low-price charging / high-price discharging / PV utilization improvement under the frozen objective.
5. The 26.90% cost saving cannot be inferred from area between power curves because price varies over time. It must be backed by independent `Σ p_t g_t` metrics.

## 4. Evidence routing

Mechanism figure candidates: load / PV forecast / Stage-2 grid purchase; charge/discharge or signed storage net; SOC 145-state trajectory; optional price in a separate aligned panel.

Better as table/text: baseline vs Stage-2 cost and 26.90%; Stage-1 vs Stage-2 exact distinction; 6×4h charge/discharge aggregate; SOC endpoints; constraint residuals; epsilon / efficiency sensitivity.

XXT makes no final paper-layout choice.

## 5. FYQ integration requirements

Parallel FYQ figure exporter/script should satisfy `Q1_FIGURE_VALIDATOR_SPEC_R1.md`.

Minimum Figure Data fields if a mechanism figure is selected:

```text
slot_id
physical_start
physical_end
load_kw
pv_forecast_kw
price_yuan_per_kwh
grid_stage2_kw
charge_kw
discharge_kw
storage_net_kw_positive_discharge
soc_start_kwh
soc_end_kwh
```

No additional targeted solve is required: all needed mathematical data already exist in Frozen R2 evidence.

`TARGETED_FIGURE_EXECUTION_REQUEST = NOT_REQUIRED`

## 6. Merge Gate handoff

For M3 Mathematical Validity: unit/time/SOC/sign/baseline contracts are specified; claim matrix supplied; legacy figures audited; misleading encodings/overclaims identified; no frozen model/result changes requested.

### STATUS

`PASS_FOR_MERGE_GATE_WITH_NON_MODEL_FIGURE_PATCHES`

### NEXT_ACTION

FYQ merges CYQ relevance brief + FYQ reproducible Figure Data/script + this XXT math domain into `Q1_FIGURE_REGISTRY_R2`, then clean-replays only the selected final figure/table candidates.

### DO_NOT_CHANGE

Q1 Frozen optimization, Stage-1/Stage-2 costs, result1, time mapping, efficiency primary semantics, baseline definition.

### SOURCE_OF_TRUTH

`CUMCM2026_C_Q1_FINAL_FREEZE_MANIFEST_R0.md` + R2 Frozen outputs.
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _as_float(value: object) -> float:
    return float(value)


def _validate_144(rows: list[dict[str, str]], name: str) -> None:
    if len(rows) != 144:
        raise ValueError(f"{name}: expected 144 rows, got {len(rows)}")
    slots = [int(row["slot_id"]) for row in rows]
    if slots != list(range(1, 145)):
        raise ValueError(f"{name}: slot_id must be exactly 1..144")


def _assert_close(a: float, b: float, label: str, atol: float = 1e-9) -> None:
    if not math.isclose(a, b, rel_tol=0.0, abs_tol=atol):
        raise ValueError(f"semantic mismatch for {label}: {a} vs {b}")


def export_figure_data(snapshot_dir: Path | str, output_csv: Path | str) -> dict[str, object]:
    snapshot = Path(snapshot_dir)
    output = Path(output_csv)
    inputs = _read_csv(snapshot / "q1_input_long.csv")
    schedule = _read_csv(snapshot / "q1_schedule_long.csv")
    baseline = _read_csv(snapshot / "q1_baseline_no_storage_long.csv")
    mapping = _read_csv(snapshot / "q1_mapping_144_slots.csv")

    for rows, name in ((inputs, "input"), (schedule, "schedule"), (baseline, "baseline"), (mapping, "mapping")):
        _validate_144(rows, name)

    out_rows: list[dict[str, object]] = []
    for idx, (irow, srow, brow, mrow) in enumerate(zip(inputs, schedule, baseline, mapping), start=1):
        if not all(int(r["slot_id"]) == idx for r in (irow, srow, brow, mrow)):
            raise ValueError(f"slot alignment mismatch at ordinal {idx}")
        if irow["raw_time_label"] != srow["raw_time_label"] or irow["raw_time_label"] != mrow["raw_time_label"]:
            raise ValueError(f"time label mismatch at slot {idx}")
        if irow["physical_start"] != srow["physical_start"] or irow["physical_end"] != srow["physical_end"]:
            raise ValueError(f"physical interval mismatch at slot {idx}")
        if irow["physical_start"] != mrow["a_start"] or irow["physical_end"] != mrow["a_end"]:
            raise ValueError(f"mapping A interval mismatch at slot {idx}")

        dt = _as_float(srow["dt_hours"])
        _assert_close(dt, 1.0 / 6.0, f"dt_hours slot {idx}", atol=1e-15)
        for key in ("price_yuan_per_kwh", "load_kw", "pv_kw", "load_kwh", "pv_kwh"):
            _assert_close(_as_float(irow[key]), _as_float(srow[key]), f"{key} input/schedule slot {idx}", atol=1e-9)
            _assert_close(_as_float(irow[key]), _as_float(brow[key]), f"{key} input/baseline slot {idx}", atol=1e-9)

        grid_kwh = _as_float(srow["grid_kwh"])
        charge_kwh = _as_float(srow["charge_kwh"])
        discharge_kwh = _as_float(srow["discharge_kwh"])
        baseline_grid_kwh = _as_float(brow["grid_kwh"])
        _assert_close(grid_kwh, _as_float(mrow["a_grid_kwh"]), f"grid mapping slot {idx}", atol=1e-9)
        _assert_close(charge_kwh, _as_float(mrow["a_charge_kwh"]), f"charge mapping slot {idx}", atol=1e-9)
        _assert_close(discharge_kwh, _as_float(mrow["a_discharge_kwh"]), f"discharge mapping slot {idx}", atol=1e-9)
        _assert_close(_as_float(srow["soc_start_kwh"]), _as_float(mrow["a_soc_start_kwh"]), f"soc start slot {idx}", atol=1e-9)
        _assert_close(_as_float(srow["soc_end_kwh"]), _as_float(mrow["a_soc_end_kwh"]), f"soc end slot {idx}", atol=1e-9)

        out_rows.append({
            "slot_id": idx,
            "service_date": srow["service_date"],
            "raw_time_label": srow["raw_time_label"],
            "physical_start": srow["physical_start"],
            "physical_end": srow["physical_end"],
            "dt_hours": format(dt, ".17g"),
            "time_hour_end": format(idx * dt, ".17g"),
            "price_yuan_per_kwh": srow["price_yuan_per_kwh"],
            "load_kw": srow["load_kw"],
            "pv_kw": srow["pv_kw"],
            "load_kwh": srow["load_kwh"],
            "pv_kwh": srow["pv_kwh"],
            "grid_purchase_kwh": srow["grid_kwh"],
            "grid_purchase_kw": format(grid_kwh / dt, ".17g"),
            "charge_kwh": srow["charge_kwh"],
            "charge_kw": format(charge_kwh / dt, ".17g"),
            "discharge_kwh": srow["discharge_kwh"],
            "discharge_kw": format(discharge_kwh / dt, ".17g"),
            "storage_net_kw_positive_discharge": format((discharge_kwh - charge_kwh) / dt, ".17g"),
            "curtail_kwh": srow["curtail_kwh"],
            "soc_start_kwh": srow["soc_start_kwh"],
            "soc_end_kwh": srow["soc_end_kwh"],
            "baseline_grid_kwh": brow["grid_kwh"],
            "baseline_grid_kw": format(baseline_grid_kwh / dt, ".17g"),
            "slot_cost_yuan": srow["cost_yuan"],
            "baseline_slot_cost_yuan": brow["cost_yuan"],
        })

    _write_csv(output, list(out_rows[0].keys()), out_rows)
    return {"row_count": len(out_rows), "output": str(output)}


def _official_schema(snapshot: Path) -> dict[tuple[str, str], str]:
    rows = _read_csv(snapshot / "result1_official_schema_r1.csv")
    return {(r["sheet"], r["cell"]): r["value"] for r in rows}


def export_paper_tables(snapshot_dir: Path | str, output_dir: Path | str) -> dict[str, object]:
    snapshot = Path(snapshot_dir)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    schema = _official_schema(snapshot)
    audit = _read_csv(snapshot / "RESULT1_MAPPING_AUDIT.csv")
    mapping = _read_csv(snapshot / "q1_mapping_144_slots.csv")

    slot_audit = [r for r in audit if r["record_type"] == "slot_grid"]
    block_charge = [r for r in audit if r["record_type"] == "4h_charge_kwh"]
    block_discharge = [r for r in audit if r["record_type"] == "4h_discharge_kwh"]
    soc = [r for r in audit if r["record_type"] == "soc_endpoint"]
    if len(slot_audit) != 144 or len(block_charge) != 6 or len(block_discharge) != 6 or len(soc) != 2:
        raise ValueError("unexpected RESULT1 mapping audit cardinality")
    if any(r["status"] != "PASS" for r in audit):
        raise ValueError("RESULT1 mapping audit contains FAIL")

    purchase_rows = []
    lineage_rows = []
    for ordinal, (a, m) in enumerate(zip(slot_audit, mapping), start=1):
        official_cell = a["target_cell"]
        label_cell = f"A{ordinal + 1}"
        official_label = schema.get(("计划购电量", label_cell))
        if official_label is None:
            raise ValueError(f"official purchase label missing for {label_cell}")
        purchase_rows.append({"时间段": official_label, "购电量": a["actual"]})
        lineage_rows.append({"record_type":"slot_grid","ordinal":ordinal,"official_sheet":"计划购电量","official_label":official_label,"official_target_cell":official_cell,"unit":"kWh/10min-slot","source_slot_start":ordinal,"source_slot_end":ordinal,"source_raw_time_label":m["raw_time_label"],"physical_start":m["a_start"],"physical_end":m["a_end"],"value":a["actual"],"status":a["status"]})

    storage_rows = []
    for block in range(1, 7):
        row_num = block + 1
        label = schema.get(("充放电量", f"A{row_num}"))
        moment = schema.get(("充放电量", f"D{row_num}"), "")
        charge = block_charge[block - 1]
        discharge = block_discharge[block - 1]
        soc_value = ""
        if block == 1:
            soc_value = next(r for r in soc if r["target_cell"] == "E2")["actual"]
        elif block == 2:
            soc_value = next(r for r in soc if r["target_cell"] == "E3")["actual"]
        storage_rows.append({"时间段":label,"充电量":charge["actual"],"放电量":discharge["actual"],"时刻":moment,"储电量":soc_value})
        for a, typ in ((charge, "4h_charge_kwh"), (discharge, "4h_discharge_kwh")):
            lineage_rows.append({"record_type":typ,"ordinal":block,"official_sheet":"充放电量","official_label":label,"official_target_cell":a["target_cell"],"unit":"kWh/4h-block","source_slot_start":24*(block-1)+1,"source_slot_end":24*block,"source_raw_time_label":"","physical_start":f"{4*(block-1):02d}:00","physical_end":f"{4*block:02d}:00" if block<6 else "24:00","value":a["actual"],"status":a["status"]})
    for a in soc:
        target = a["target_cell"]
        moment = schema.get(("充放电量", "D2" if target == "E2" else "D3"), "")
        lineage_rows.append({"record_type":"soc_endpoint","ordinal":a["ordinal"],"official_sheet":"充放电量","official_label":moment,"official_target_cell":target,"unit":"kWh","source_slot_start":0 if target=="E2" else 144,"source_slot_end":0 if target=="E2" else 144,"source_raw_time_label":"","physical_start":moment,"physical_end":moment,"value":a["actual"],"status":a["status"]})

    _write_csv(output / "Q1_PAPER_TABLE_01_RESULT1_PURCHASE_R1.csv", ["时间段", "购电量"], purchase_rows)
    _write_csv(output / "Q1_PAPER_TABLE_02_RESULT1_STORAGE_R1.csv", ["时间段", "充电量", "放电量", "时刻", "储电量"], storage_rows)
    _write_csv(output / "Q1_PAPER_TABLE_LINEAGE_R1.csv", ["record_type","ordinal","official_sheet","official_label","official_target_cell","unit","source_slot_start","source_slot_end","source_raw_time_label","physical_start","physical_end","value","status"], lineage_rows)
    return {"purchase_rows": len(purchase_rows), "storage_rows": len(storage_rows), "lineage_rows": len(lineage_rows)}


def export_cost_comparison_table(snapshot_dir: Path | str, output_csv: Path | str) -> dict[str, object]:
    snapshot = Path(snapshot_dir)
    output = Path(output_csv)
    metrics = json.loads((snapshot / "q1_metrics.json").read_text(encoding="utf-8"))
    baseline = float(metrics["baseline_total_cost_cny"])
    optimized = float(metrics["stage2_cost"])
    savings = baseline - optimized
    rate = savings / baseline * 100.0
    _assert_close(savings, float(metrics["savings_absolute_cny"]), "savings_absolute", atol=1e-8)
    _assert_close(rate, float(metrics["savings_percent"]), "savings_percent", atol=1e-10)
    rows = [
        {"方案":"无储能基线","总购电成本_元":format(baseline,".15g"),"相对基线节省额_元":"0","相对基线节省率_百分比":"0"},
        {"方案":"两阶段LP储能调度","总购电成本_元":format(optimized,".15g"),"相对基线节省额_元":format(savings,".15g"),"相对基线节省率_百分比":format(rate,".15g")},
    ]
    _write_csv(output, list(rows[0].keys()), rows)
    return {"row_count": 2, "output": str(output)}


def file_sha256(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

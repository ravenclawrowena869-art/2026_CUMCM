from __future__ import annotations

import argparse
import csv
from datetime import datetime, timedelta
from pathlib import Path

from artifact_tool import Blob, SpreadsheetFile

DATE_START = "2025-02-01"
DATE_END = "2025-12-31"
SLOTS = 144


def read_rows(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def date_list():
    start = datetime.fromisoformat(DATE_START)
    end = datetime.fromisoformat(DATE_END)
    out = []
    d = start
    while d <= end:
        out.append(d.strftime("%Y-%m-%d"))
        d += timedelta(days=1)
    return out


def group_inputs(trace_rows, ledger_rows):
    dates = date_list()
    trace_by_date = {d: [] for d in dates}
    stage0_by_date = {d: [] for d in dates}
    base_fee = {d: 0.0 for d in dates}
    adjustment_fee = {d: 0.0 for d in dates}

    for row in trace_rows:
        trace_by_date[row["date"]].append(row)

    for row in ledger_rows:
        d = row["date"]
        stage = int(row["stage"])
        if stage == 0:
            stage0_by_date[d].append(row)
            base_fee[d] += float(row["fee_delta"])
        else:
            adjustment_fee[d] += float(row["fee_delta"])

    for d in dates:
        trace_by_date[d].sort(key=lambda r: int(r["slot_id"]))
        stage0_by_date[d].sort(key=lambda r: int(r["slot_id"]))
        if len(trace_by_date[d]) != SLOTS or len(stage0_by_date[d]) != SLOTS:
            raise RuntimeError(f"{d}: slot count mismatch")

    return dates, trace_by_date, stage0_by_date, base_fee, adjustment_fee


def interval_label(headers, first_slot, last_slot):
    first = str(headers[first_slot - 1]).split("-", 1)[0]
    last = str(headers[last_slot - 1]).split("-", 1)[1]
    return f"{first}-{last}"


def emergency_groups(rows, tol=1e-9):
    groups = []
    start_slot = None
    prev_slot = None
    total = 0.0

    for row in rows:
        slot = int(row["slot_id"])
        amount = float(row["r"])
        if amount > tol:
            if start_slot is None:
                start_slot = slot
                total = amount
            elif prev_slot == slot - 1:
                total += amount
            else:
                groups.append((start_slot, prev_slot, total))
                start_slot = slot
                total = amount
            prev_slot = slot
        elif start_slot is not None:
            groups.append((start_slot, prev_slot, total))
            start_slot = None
            prev_slot = None
            total = 0.0

    if start_slot is not None:
        groups.append((start_slot, prev_slot, total))
    return groups


def write_result3(template, trace_csv, ledger_csv, output):
    trace_rows = read_rows(trace_csv)
    ledger_rows = read_rows(ledger_csv)
    dates, trace, stage0, base_fee, adjustment_fee = group_inputs(trace_rows, ledger_rows)

    wb = SpreadsheetFile.import_xlsx(Blob.load(str(template)))
    expected = ["计划购电量", "调整购电量", "充放电量", "紧急购电量"]
    if [ws.name for ws in wb.worksheets.items] != expected:
        raise ValueError("result3 template sheets changed")

    plan = wb.worksheets.get_item("计划购电量")
    adjusted = wb.worksheets.get_item("调整购电量")
    storage = wb.worksheets.get_item("充放电量")
    emergency = wb.worksheets.get_item("紧急购电量")
    headers = plan.get_range("B1:EO1").values[0]
    if len(headers) != SLOTS:
        raise ValueError("result3 template slot columns changed")

    date_cells = [[datetime.fromisoformat(d)] for d in dates]
    plan_values = []
    adjusted_values = []

    for d in dates:
        p = [float(r["new_active_q"]) for r in stage0[d]]
        q = [float(r["q"]) for r in trace[d]]
        plan_values.append(p + [sum(p), base_fee[d]])
        adjusted_values.append(q + [sum(q), adjustment_fee[d]])

    plan.get_range("A2:A335").values = date_cells
    adjusted.get_range("A2:A335").values = date_cells
    plan.get_range("B2:EQ335").values = plan_values
    adjusted.get_range("B2:EQ335").values = adjusted_values
    plan.get_range("A2:A335").format.number_format = "yyyy/m/d"
    adjusted.get_range("A2:A335").format.number_format = "yyyy/m/d"
    plan.get_range("B2:EQ335").format.number_format = "0.000000"
    adjusted.get_range("B2:EQ335").format.number_format = "0.000000"

    blocks = [
        ("0:00-4:00", 1, 24),
        ("4:00-8:00", 25, 48),
        ("8:00-12:00", 49, 72),
        ("12:00-16:00", 73, 96),
        ("16:00-20:00", 97, 120),
        ("20:00-24:00", 121, 144),
    ]
    storage_values = []
    for d in dates:
        rows = trace[d]
        for i, (label, lo, hi) in enumerate(blocks):
            block = rows[lo - 1:hi]
            storage_values.append([
                datetime.fromisoformat(d) if i == 0 else None,
                label,
                sum(float(r["c"]) for r in block),
                sum(float(r["d"]) for r in block),
                "0:00" if i == 0 else ("24:00" if i == 1 else None),
                float(rows[0]["e_before"]) if i == 0 else (float(rows[-1]["e_after"]) if i == 1 else None),
            ])

    storage_end = 1 + len(storage_values)
    storage.get_range(f"A2:F{storage_end}").values = storage_values
    storage.get_range(f"A2:A{storage_end}").format.number_format = "yyyy/m/d"
    storage.get_range(f"C2:D{storage_end}").format.number_format = "0.000000"
    storage.get_range(f"F2:F{storage_end}").format.number_format = "0.000000"

    emergency_values = []
    for d in dates:
        groups = emergency_groups(trace[d])
        if not groups:
            emergency_values.append([datetime.fromisoformat(d), None, None])
            continue
        for i, (lo, hi, total) in enumerate(groups):
            emergency_values.append([
                datetime.fromisoformat(d) if i == 0 else None,
                interval_label(headers, lo, hi),
                total,
            ])

    emergency_end = 1 + len(emergency_values)
    emergency.get_range(f"A2:C{emergency_end}").values = emergency_values
    emergency.get_range(f"A2:A{emergency_end}").format.number_format = "yyyy/m/d"
    emergency.get_range(f"C2:C{emergency_end}").format.number_format = "0.000000"

    SpreadsheetFile.export_xlsx(wb).save(str(output))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--trace", required=True, type=Path)
    parser.add_argument("--ledger", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    write_result3(args.template, args.trace, args.ledger, args.output)


if __name__ == "__main__":
    main()

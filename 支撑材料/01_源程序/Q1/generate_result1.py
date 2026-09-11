#!/usr/bin/env python3
"""Generate the frozen Q1 result1.xlsx from official Attachment1 and template.

Mathematical authority: CUMCM2026_C_Q1_FREEZE_R0_20260911
Model: two-stage continuous LP, epsilon_cost=1e-4 CNY,
eta_c=eta_d=0.9, right-endpoint canonical slots + ordinal export.

This script intentionally writes into the official result1 template without
changing worksheet names or time-label cells.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from artifact_tool import Blob, SpreadsheetFile

T = 144
DT_H = 1.0 / 6.0
ETA_C = 0.9
ETA_D = 0.9
E0 = 6000.0
E_MIN = 1200.0
E_MAX = 10800.0
SLOT_LIMIT = 5000.0 * DT_H
EPSILON_COST = 1e-4

# Frozen current-version authority, used only as a guard against silent drift.
FROZEN_STAGE1_COST = 35126.948589289634
FROZEN_STAGE2_COST = 35126.948689289624
FROZEN_CHARGE_4H = np.array([
    4500.000000,
    833.3333333333334,
    4787.963043030471,
    5286.035176954732,
    0.0,
    5333.333333333334,
])
FROZEN_DISCHARGE_4H = np.array([
    0.0,
    6365.840191521346,
    1702.9969833333334,
    91.10138333333339,
    5780.1318833333335,
    2859.868116666667,
])


def load_attachment1(path: Path):
    wb = SpreadsheetFile.import_xlsx(Blob.load(str(path)))
    ws = wb.worksheets.get_item("Sheet1")
    rows = ws.get_range("A2:D145").values
    if len(rows) != T:
        raise ValueError(f"Attachment1 must contain {T} data rows, got {len(rows)}")
    price = np.array([float(r[1]) for r in rows], dtype=float)
    load_kwh = np.array([float(r[2]) * DT_H for r in rows], dtype=float)
    pv_kwh = np.array([float(r[3]) * DT_H for r in rows], dtype=float)
    return price, load_kwh, pv_kwh


def solve_q1(price: np.ndarray, load: np.ndarray, pv: np.ndarray):
    # x = [g, charge, discharge, curtail, E_after]
    n = 5 * T
    G = slice(0, T)
    C = slice(T, 2 * T)
    D = slice(2 * T, 3 * T)
    U = slice(3 * T, 4 * T)
    E = slice(4 * T, 5 * T)

    c1 = np.zeros(n)
    c1[G] = price

    aeq = []
    beq = []

    # g + pv - u + d = load + c
    for t in range(T):
        row = np.zeros(n)
        row[t] = 1.0
        row[T + t] = -1.0
        row[2 * T + t] = 1.0
        row[3 * T + t] = -1.0
        aeq.append(row)
        beq.append(load[t] - pv[t])

    # E_t = E_{t-1} + eta_c*c_t - d_t/eta_d
    for t in range(T):
        row = np.zeros(n)
        row[4 * T + t] = 1.0
        row[T + t] = -ETA_C
        row[2 * T + t] = 1.0 / ETA_D
        if t > 0:
            row[4 * T + t - 1] = -1.0
            rhs = 0.0
        else:
            rhs = E0
        aeq.append(row)
        beq.append(rhs)

    # Q1 terminal SOC equality.
    row = np.zeros(n)
    row[4 * T + T - 1] = 1.0
    aeq.append(row)
    beq.append(E0)

    aeq = np.asarray(aeq)
    beq = np.asarray(beq)

    bounds = []
    bounds.extend([(0.0, None)] * T)                  # g
    bounds.extend([(0.0, SLOT_LIMIT)] * T)            # charge
    bounds.extend([(0.0, SLOT_LIMIT)] * T)            # discharge
    bounds.extend([(0.0, float(pv[t])) for t in range(T)])  # curtail
    bounds.extend([(E_MIN, E_MAX)] * T)                # SOC

    # Stage 1: exact minimum purchase cost.
    r1 = linprog(c1, A_eq=aeq, b_eq=beq, bounds=bounds, method="highs")
    if not r1.success:
        raise RuntimeError(f"Stage 1 failed: {r1.message}")

    # Stage 2: within C* + 1e-4 CNY, minimize storage throughput.
    c2 = np.zeros(n)
    c2[C] = 1.0
    c2[D] = 1.0
    r2 = linprog(
        c2,
        A_ub=np.asarray([c1]),
        b_ub=np.asarray([float(r1.fun) + EPSILON_COST]),
        A_eq=aeq,
        b_eq=beq,
        bounds=bounds,
        method="highs",
    )
    if not r2.success:
        raise RuntimeError(f"Stage 2 failed: {r2.message}")

    x = r2.x
    g = x[G]
    charge = x[C]
    discharge = x[D]
    curtail = x[U]
    soc = x[E]

    balance_residual = g + pv - curtail + discharge - load - charge
    soc_residual = np.empty(T)
    soc_residual[0] = soc[0] - E0 - ETA_C * charge[0] + discharge[0] / ETA_D
    soc_residual[1:] = soc[1:] - soc[:-1] - ETA_C * charge[1:] + discharge[1:] / ETA_D

    charge_4h = np.array([charge[i * 24:(i + 1) * 24].sum() for i in range(6)])
    discharge_4h = np.array([discharge[i * 24:(i + 1) * 24].sum() for i in range(6)])
    stage2_cost = float(np.dot(price, g))

    report = {
        "stage1_cost_CNY": float(r1.fun),
        "stage2_cost_CNY": stage2_cost,
        "total_purchase_kWh": float(g.sum()),
        "max_energy_balance_residual_kWh": float(np.max(np.abs(balance_residual))),
        "max_soc_recursion_residual_kWh": float(np.max(np.abs(soc_residual))),
        "soc_min_kWh": float(soc.min()),
        "soc_max_kWh": float(soc.max()),
        "terminal_soc_kWh": float(soc[-1]),
        "simultaneous_charge_discharge_slots": int(np.sum((charge > 1e-7) & (discharge > 1e-7))),
        "charge_4h_kWh": charge_4h.tolist(),
        "discharge_4h_kWh": discharge_4h.tolist(),
    }

    # Hard guards: if any of these fire, do not write a result workbook.
    if np.max(np.abs(balance_residual)) > 1e-6:
        raise AssertionError("energy-balance replay failed")
    if np.max(np.abs(soc_residual)) > 1e-6:
        raise AssertionError("SOC recursion replay failed")
    if abs(soc[-1] - E0) > 1e-6:
        raise AssertionError("terminal SOC failed")
    if report["simultaneous_charge_discharge_slots"] != 0:
        raise AssertionError("simultaneous charge/discharge detected")
    if abs(float(r1.fun) - FROZEN_STAGE1_COST) > 1e-6:
        raise AssertionError("Stage-1 frozen authority drift")
    if abs(stage2_cost - FROZEN_STAGE2_COST) > 1e-6:
        raise AssertionError("Stage-2 frozen authority drift")
    if np.max(np.abs(charge_4h - FROZEN_CHARGE_4H)) > 1e-6:
        raise AssertionError("4h charge aggregate drift")
    if np.max(np.abs(discharge_4h - FROZEN_DISCHARGE_4H)) > 1e-6:
        raise AssertionError("4h discharge aggregate drift")

    return g, charge_4h, discharge_4h, report


def write_result1(template: Path, output: Path, g, charge_4h, discharge_4h):
    wb = SpreadsheetFile.import_xlsx(Blob.load(str(template)))
    if [ws.name for ws in wb.worksheets.items] != ["计划购电量", "充放电量"]:
        raise ValueError("official template sheet names changed")

    plan = wb.worksheets.get_item("计划购电量")
    storage = wb.worksheets.get_item("充放电量")

    # Official writer contract: canonical slot t -> official template position t.
    plan.get_range("B2:B145").values = [[float(v)] for v in g]
    storage.get_range("B2:B7").values = [[float(v)] for v in charge_4h]
    storage.get_range("C2:C7").values = [[float(v)] for v in discharge_4h]
    storage.get_range("E2:E3").values = [[E0], [E0]]

    SpreadsheetFile.export_xlsx(wb).save(str(output))


def readback_validate(output: Path, attachment1: Path):
    result = SpreadsheetFile.import_xlsx(Blob.load(str(output)))
    source = SpreadsheetFile.import_xlsx(Blob.load(str(attachment1)))
    prices = np.array([float(r[1]) for r in source.worksheets.get_item("Sheet1").get_range("A2:D145").values])
    grid = np.array([float(r[0]) for r in result.worksheets.get_item("计划购电量").get_range("B2:B145").values])
    charge = np.array([float(r[0]) for r in result.worksheets.get_item("充放电量").get_range("B2:B7").values])
    discharge = np.array([float(r[0]) for r in result.worksheets.get_item("充放电量").get_range("C2:C7").values])
    soc = [float(r[0]) for r in result.worksheets.get_item("充放电量").get_range("E2:E3").values]

    cost = float(np.dot(prices, grid))
    if abs(cost - FROZEN_STAGE2_COST) > 1e-6:
        raise AssertionError("result1 readback cost mismatch")
    if np.max(np.abs(charge - FROZEN_CHARGE_4H)) > 1e-6:
        raise AssertionError("result1 readback charge mismatch")
    if np.max(np.abs(discharge - FROZEN_DISCHARGE_4H)) > 1e-6:
        raise AssertionError("result1 readback discharge mismatch")
    if soc != [E0, E0]:
        raise AssertionError("result1 SOC endpoint mismatch")
    return {"readback_cost_CNY": cost, "readback_total_purchase_kWh": float(grid.sum())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--attachment1", required=True, type=Path)
    ap.add_argument("--template", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()

    price, load, pv = load_attachment1(args.attachment1)
    g, charge_4h, discharge_4h, report = solve_q1(price, load, pv)
    write_result1(args.template, args.output, g, charge_4h, discharge_4h)
    report.update(readback_validate(args.output, args.attachment1))
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

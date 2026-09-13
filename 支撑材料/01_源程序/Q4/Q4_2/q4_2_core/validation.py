from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from .contracts import Q4Contract
from .io_adapters import DataContractError, validate_slot_grid


class FutureLeakageError(RuntimeError):
    """Raised when formal execution consumes price information unavailable at decision time."""


def audit_price_causality(
    prices: pd.DataFrame,
    upstream: pd.DataFrame,
    *,
    lane: str,
) -> dict[str, Any]:
    merged = upstream[["date", "slot", "decision_time"]].merge(
        prices[["date", "slot", "known_at", "price_yuan_per_kWh"]],
        on=["date", "slot"],
        how="left",
        validate="one_to_one",
    )
    if merged["known_at"].isna().any():
        raise DataContractError("dynamic price mapping is incomplete for upstream schedule")
    future = merged["known_at"] > merged["decision_time"]
    count = int(future.sum())
    first = None
    if count:
        row = merged.loc[future].iloc[0]
        first = {"date": str(row["date"]), "slot": int(row["slot"])}
    if lane == "FORMAL_CAUSAL":
        if count:
            raise FutureLeakageError(
                f"formal lane has {count} future-price rows; first={first}"
            )
        status = "PASS_CAUSAL"
    elif lane == "ORACLE_DIAGNOSTIC":
        status = "DIAGNOSTIC_ONLY / FUTURE_LEAKAGE_BY_DESIGN" if count else "DIAGNOSTIC_ONLY"
    else:
        raise ValueError(f"unsupported lane: {lane}")
    return {
        "lane": lane,
        "status": status,
        "future_leakage_count": count,
        "first_future_leakage": first,
        "rows": int(len(merged)),
    }


def _linear_sum(frame: pd.DataFrame, terms: list[list[Any]]) -> np.ndarray:
    total = np.zeros(len(frame), dtype=float)
    for col, coeff in terms:
        if col not in frame.columns:
            raise DataContractError(f"validator ledger missing contract term: {col}")
        total += pd.to_numeric(frame[col], errors="raise").to_numpy(dtype=float) * float(coeff)
    return total


def validate_execution_ledger(
    ledger: pd.DataFrame,
    contract: Q4Contract,
    *,
    energy_tolerance_kWh: float = 1e-6,
) -> dict[str, Any]:
    raw = contract.raw
    required = {
        "date",
        "slot",
        "charge_kWh",
        "discharge_kWh",
        "soc_start_kWh",
        "soc_end_kWh",
        "q_active_kWh",
        "emergency_kWh",
        "price_yuan_per_kWh",
    }
    missing = sorted(required - set(ledger.columns))
    if missing:
        raise DataContractError(f"validator ledger missing fields: {', '.join(missing)}")
    if ledger.empty:
        raise DataContractError("validator ledger is empty")

    f = ledger.copy().reset_index(drop=True)
    f["date"] = pd.to_datetime(f["date"], errors="raise").dt.strftime("%Y-%m-%d")
    f["slot"] = pd.to_numeric(f["slot"], errors="raise").astype(int)
    validate_slot_grid(
        f,
        slots_per_day=contract.slots_per_day,
        date_col="date",
        slot_col="slot",
    )
    f = f.sort_values(["date", "slot"]).reset_index(drop=True)
    for col in required - {"date"}:
        f[col] = pd.to_numeric(f[col], errors="raise")

    lhs = _linear_sum(f, raw["balance"]["lhs"])
    rhs = _linear_sum(f, raw["balance"]["rhs"])
    balance_residual = np.abs(lhs - rhs)

    storage = raw["storage"]
    if storage.get("recursion") != "Q2_BUS_SIDE_R1":
        raise DataContractError("unsupported or unresolved SOC recursion; formal validation fails closed")
    eta_c = float(storage["eta_c"])
    eta_d = float(storage["eta_d"])
    expected_end = (
        f["soc_start_kWh"].to_numpy(dtype=float)
        + eta_c * f["charge_kWh"].to_numpy(dtype=float)
        - f["discharge_kWh"].to_numpy(dtype=float) / eta_d
    )
    soc_recursion_residual = np.abs(f["soc_end_kWh"].to_numpy(dtype=float) - expected_end)

    soc_min = float(storage["soc_min_kWh"])
    soc_max = float(storage["soc_max_kWh"])
    emax = float(storage["slot_energy_max_kWh"])
    soc_bound_violation = np.maximum.reduce(
        [
            np.maximum(soc_min - f["soc_start_kWh"].to_numpy(dtype=float), 0.0),
            np.maximum(f["soc_start_kWh"].to_numpy(dtype=float) - soc_max, 0.0),
            np.maximum(soc_min - f["soc_end_kWh"].to_numpy(dtype=float), 0.0),
            np.maximum(f["soc_end_kWh"].to_numpy(dtype=float) - soc_max, 0.0),
        ]
    )
    power_violation = np.maximum(
        np.maximum(f["charge_kWh"].to_numpy(dtype=float) - emax, 0.0),
        np.maximum(f["discharge_kWh"].to_numpy(dtype=float) - emax, 0.0),
    )
    negative_action_violation = np.maximum.reduce(
        [
            np.maximum(-f["charge_kWh"].to_numpy(dtype=float), 0.0),
            np.maximum(-f["discharge_kWh"].to_numpy(dtype=float), 0.0),
            np.maximum(-f["q_active_kWh"].to_numpy(dtype=float), 0.0),
            np.maximum(-f["emergency_kWh"].to_numpy(dtype=float), 0.0),
        ]
    )

    continuity = np.zeros(len(f), dtype=float)
    if storage.get("cross_day") == "NO_DAILY_RESET" and len(f) > 1:
        continuity[1:] = np.abs(
            f["soc_start_kWh"].to_numpy(dtype=float)[1:]
            - f["soc_end_kWh"].to_numpy(dtype=float)[:-1]
        )

    selling_allowed = bool(raw["settlement"].get("selling_allowed", False))
    export = (
        pd.to_numeric(f["export_kWh"], errors="raise").to_numpy(dtype=float)
        if "export_kWh" in f.columns
        else np.zeros(len(f), dtype=float)
    )
    export_violation = np.zeros(len(f), dtype=float) if selling_allowed else np.maximum(export, 0.0)

    simultaneous = np.minimum(
        np.maximum(f["charge_kWh"].to_numpy(dtype=float), 0.0),
        np.maximum(f["discharge_kWh"].to_numpy(dtype=float), 0.0),
    )

    components = {
        "balance": balance_residual,
        "soc_recursion": soc_recursion_residual,
        "soc_bounds": soc_bound_violation,
        "power": power_violation,
        "negative_action": negative_action_violation,
        "soc_continuity": continuity,
        "export": export_violation,
        "simultaneous_charge_discharge": simultaneous,
    }
    per_row_max = np.maximum.reduce(list(components.values()))
    arg = int(np.argmax(per_row_max))
    max_violation = float(per_row_max[arg])

    settlement = raw["settlement"]
    normal_multiplier = float(settlement["normal_multiplier"])
    emergency_multiplier = float(settlement["emergency_multiplier"])
    p = f["price_yuan_per_kWh"].to_numpy(dtype=float)
    q = f["q_active_kWh"].to_numpy(dtype=float)
    r = f["emergency_kWh"].to_numpy(dtype=float)
    normal_cost = float(np.sum(normal_multiplier * p * q))
    emergency_cost = float(np.sum(emergency_multiplier * p * r))

    return {
        "pass": bool(max_violation <= energy_tolerance_kWh),
        "energy_tolerance_kWh": energy_tolerance_kWh,
        "max_violation": max_violation,
        "argmax_location": {"date": str(f.loc[arg, "date"]), "slot": int(f.loc[arg, "slot"])},
        "max_balance_violation_kWh": float(np.max(balance_residual)),
        "max_soc_recursion_violation_kWh": float(np.max(soc_recursion_residual)),
        "cross_slot_soc_discontinuity_max_kWh": float(np.max(continuity)),
        "soc_bound_violation_max_kWh": float(np.max(soc_bound_violation)),
        "power_violation_max_kWh": float(np.max(power_violation)),
        "export_violation_max_kWh": float(np.max(export_violation)),
        "simultaneous_charge_discharge_max_kWh": float(np.max(simultaneous)),
        "normal_cost_cny": normal_cost,
        "emergency_cost_cny": emergency_cost,
        "total_cost_cny": normal_cost + emergency_cost,
        "rows": int(len(f)),
    }

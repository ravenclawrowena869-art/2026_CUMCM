from __future__ import annotations

from dataclasses import dataclass

from q3_contract import Q3Contract


@dataclass(frozen=True)
class StorageReplay:
    soc: list[float]
    max_bound_violation_kwh: float
    max_power_violation_kwh: float
    max_recursion_residual_kwh: float
    simultaneous_charge_discharge_count: int


def replay_storage(
    contract: Q3Contract,
    initial_soc_kwh: float,
    charge_kwh: list[float],
    discharge_kwh: list[float],
    reported_soc_end_kwh: list[float] | None = None,
) -> StorageReplay:
    if len(charge_kwh) != len(discharge_kwh):
        raise ValueError("charge/discharge length mismatch")
    if reported_soc_end_kwh is not None and len(reported_soc_end_kwh) != len(charge_kwh):
        raise ValueError("reported SOC length mismatch")

    soc = []
    prev = float(initial_soc_kwh)
    max_bound = 0.0
    max_power = 0.0
    max_residual = 0.0
    simultaneous = 0

    for i, (c, d) in enumerate(zip(charge_kwh, discharge_kwh)):
        c = float(c)
        d = float(d)
        if c < -1e-12 or d < -1e-12:
            raise ValueError("negative charge/discharge")
        if c > 1e-12 and d > 1e-12:
            simultaneous += 1
        max_power = max(
            max_power,
            max(c - contract.power_limit_kwh_per_slot, 0.0),
            max(d - contract.power_limit_kwh_per_slot, 0.0),
        )
        nxt = prev + contract.eta_c * c - d / contract.eta_d
        max_bound = max(
            max_bound,
            max(contract.soc_min_kwh - nxt, 0.0),
            max(nxt - contract.soc_max_kwh, 0.0),
        )
        if reported_soc_end_kwh is not None:
            max_residual = max(max_residual, abs(nxt - float(reported_soc_end_kwh[i])))
        soc.append(nxt)
        prev = nxt

    return StorageReplay(
        soc=soc,
        max_bound_violation_kwh=max_bound,
        max_power_violation_kwh=max_power,
        max_recursion_residual_kwh=max_residual,
        simultaneous_charge_discharge_count=simultaneous,
    )

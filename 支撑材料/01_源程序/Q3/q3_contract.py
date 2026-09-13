from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


class ContractNotLocked(RuntimeError):
    pass


@dataclass(frozen=True)
class Q3Contract:
    status: Literal["mock", "preflight", "locked"]
    reference_base: str
    settlement_price_time: str
    pv_transform: str
    increase_factor: float
    decrease_refund_factor: float
    emergency_factor: float
    eta_c: float
    eta_d: float
    soc_min_kwh: float
    soc_max_kwh: float
    power_limit_kwh_per_slot: float
    no_export: bool = True
    no_emergency_charging: bool = True

    def require_formal_lock(self) -> None:
        if self.status != "locked":
            raise ContractNotLocked(
                "formal Q3 run requires Q3_CONTRACT_LOCKED_FOR_FYQ"
            )


def mock_preflight_contract() -> Q3Contract:
    return Q3Contract(
        status="mock",
        reference_base="PREVIOUS_ACTIVE_COMMITMENT",
        settlement_price_time="DELIVERY_SLOT_PRICE",
        pv_transform="PV_HOURLY_LINEAR_CAUSAL_BOUNDARY_V1",
        increase_factor=1.5,
        decrease_refund_factor=0.5,
        emergency_factor=5.0,
        eta_c=0.9,
        eta_d=0.9,
        soc_min_kwh=1200.0,
        soc_max_kwh=10800.0,
        power_limit_kwh_per_slot=5000.0 / 6.0,
    )

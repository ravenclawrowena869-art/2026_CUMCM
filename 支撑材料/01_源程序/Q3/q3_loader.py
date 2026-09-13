from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class DailyActuals:
    date: str
    price: list[float]
    load_kwh: list[float]
    pv_kwh: list[float]


def load_daily_actuals(
    date: str,
    price: Sequence[float],
    load_kwh: Sequence[float],
    pv_kwh: Sequence[float],
) -> DailyActuals:
    vectors = [price, load_kwh, pv_kwh]
    if any(len(v) != 144 for v in vectors):
        raise ValueError("daily price/load/PV vectors must have 144 slots")
    if any(float(x) < 0 for v in vectors for x in v):
        raise ValueError("negative daily input")
    return DailyActuals(
        date=date,
        price=list(map(float, price)),
        load_kwh=list(map(float, load_kwh)),
        pv_kwh=list(map(float, pv_kwh)),
    )


def require_forecast_vintages(vintages: Mapping[str, Sequence[float]]) -> None:
    required = ("00:00", "06:00", "12:00", "18:00")
    missing = [key for key in required if key not in vintages]
    if missing:
        raise ValueError(f"missing Q3 forecast vintages: {missing}")
    for key in required:
        if len(vintages[key]) != 24:
            raise ValueError(f"{key} forecast must have 24 hourly anchors")

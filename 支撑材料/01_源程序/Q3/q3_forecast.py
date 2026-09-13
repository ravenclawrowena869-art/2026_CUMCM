from __future__ import annotations

from collections.abc import Sequence

from q3_time import future_slots, slot_right_endpoint_minute


class ForecastInputError(ValueError):
    pass


def linear_hourly_to_10min_energy(
    stage_minute: int,
    realized_boundary_kw: float,
    hourly_forecast_kw: Sequence[float],
) -> dict[int, float]:
    if len(hourly_forecast_kw) != 24:
        raise ForecastInputError("24 hourly forecast anchors are required")
    if realized_boundary_kw < 0 or any(x < 0 for x in hourly_forecast_kw):
        raise ForecastInputError("PV forecast must be nonnegative")

    anchors = [float(realized_boundary_kw), *map(float, hourly_forecast_kw)]
    result: dict[int, float] = {}
    for slot in future_slots(stage_minute):
        endpoint = slot_right_endpoint_minute(slot)
        u = (endpoint - stage_minute) / 60.0
        if not 0 < u <= 24:
            continue
        lo = int(u)
        if u == lo:
            power_kw = anchors[lo]
        else:
            hi = lo + 1
            frac = u - lo
            power_kw = anchors[lo] + frac * (anchors[hi] - anchors[lo])
        result[slot] = power_kw / 6.0
    return result


def endpoint_hold_to_10min_energy(
    stage_minute: int,
    hourly_forecast_kw: Sequence[float],
) -> dict[int, float]:
    if len(hourly_forecast_kw) != 24:
        raise ForecastInputError("24 hourly forecast anchors are required")
    if any(x < 0 for x in hourly_forecast_kw):
        raise ForecastInputError("PV forecast must be nonnegative")

    result: dict[int, float] = {}
    for slot in future_slots(stage_minute):
        endpoint = slot_right_endpoint_minute(slot)
        u = (endpoint - stage_minute) / 60.0
        if not 0 < u <= 24:
            continue
        h = int(-(-u // 1))
        result[slot] = float(hourly_forecast_kw[h - 1]) / 6.0
    return result

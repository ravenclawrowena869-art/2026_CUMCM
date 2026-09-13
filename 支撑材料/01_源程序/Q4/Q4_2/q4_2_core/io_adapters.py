from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Mapping

import pandas as pd

from .contracts import Q4Contract


class DataContractError(ValueError):
    """Raised when an input violates a declared data/interface contract."""


_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_PRICE_REQUIRED = (
    "target_ts",
    "slot",
    "price_yuan_per_kWh",
    "known_at",
    "source",
    "provenance_sha256",
)
_UPSTREAM_CANONICAL = (
    "date",
    "slot",
    "decision_time",
    "q_active_kWh",
    "charge_ref_kWh",
    "discharge_ref_kWh",
    "SOC_start_kWh",
    "SOC_end_kWh",
    "emergency_kWh",
)


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_slot_grid(frame: pd.DataFrame, *, slots_per_day: int, date_col: str, slot_col: str) -> None:
    if frame.empty:
        raise DataContractError("input is empty")
    if not pd.api.types.is_integer_dtype(frame[slot_col]):
        try:
            frame[slot_col] = frame[slot_col].astype(int)
        except Exception as exc:  # pragma: no cover - defensive
            raise DataContractError("slot must be integer-like") from exc
    if ((frame[slot_col] < 1) | (frame[slot_col] > slots_per_day)).any():
        raise DataContractError(f"slot must be within 1..{slots_per_day}")
    if frame.duplicated([date_col, slot_col]).any():
        raise DataContractError("duplicate date/slot rows are forbidden")
    expected = list(range(1, slots_per_day + 1))
    for day, g in frame.groupby(date_col, sort=False):
        slots = sorted(int(v) for v in g[slot_col].tolist())
        if len(slots) != slots_per_day:
            raise DataContractError(
                f"slot count for {day} is {len(slots)}; expected exactly {slots_per_day}"
            )
        if slots != expected:
            raise DataContractError(f"slot grid for {day} must be exactly 1..{slots_per_day}")


def normalize_dynamic_price(
    frame: pd.DataFrame,
    *,
    slots_per_day: int,
    slot_minutes: int,
    time_mapping: str,
) -> pd.DataFrame:
    missing = [c for c in _PRICE_REQUIRED if c not in frame.columns]
    if missing:
        raise DataContractError(f"dynamic price missing required fields: {', '.join(missing)}")
    if time_mapping != "C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT":
        raise DataContractError(
            "dynamic-price time mapping is unresolved or unsupported; require explicit locked mapping"
        )
    if slot_minutes <= 0:
        raise DataContractError("slot_minutes must be positive")

    out = frame.loc[:, _PRICE_REQUIRED].copy()
    out["target_ts"] = pd.to_datetime(out["target_ts"], errors="raise")
    out["known_at"] = pd.to_datetime(out["known_at"], errors="raise")
    out["slot"] = pd.to_numeric(out["slot"], errors="raise").astype(int)
    out["price_yuan_per_kWh"] = pd.to_numeric(out["price_yuan_per_kWh"], errors="raise")
    if not pd.Series(out["price_yuan_per_kWh"]).map(pd.notna).all() or (out["price_yuan_per_kWh"] < 0).any():
        raise DataContractError("price_yuan_per_kWh must be finite and nonnegative")
    if out["provenance_sha256"].isna().any():
        raise DataContractError("provenance_sha256 is required for every dynamic-price row")
    if not out["provenance_sha256"].astype(str).map(lambda x: bool(_SHA256_RE.fullmatch(x))).all():
        raise DataContractError("provenance_sha256 must be a 64-hex sha256 for every row")
    if out.duplicated(["target_ts", "slot"]).any():
        raise DataContractError("duplicate target_ts/slot dynamic-price rows are forbidden")

    delta = pd.to_timedelta(slot_minutes, unit="m")
    operating_start = out["target_ts"] - delta
    out["date"] = operating_start.dt.strftime("%Y-%m-%d")
    expected_target = pd.to_datetime(out["date"]) + out["slot"] * delta
    mismatch = out["target_ts"] != expected_target
    if mismatch.any():
        first = int(mismatch[mismatch].index[0])
        raise DataContractError(
            f"timestamp/slot mapping mismatch at row {first}: "
            f"target_ts={out.loc[first, 'target_ts']}, slot={out.loc[first, 'slot']}"
        )
    validate_slot_grid(out, slots_per_day=slots_per_day, date_col="date", slot_col="slot")
    return out.reset_index(drop=True)


def load_dynamic_price_attachment(
    path: str | Path,
    *,
    column_mapping: Mapping[str, str],
    contract: Q4Contract,
) -> pd.DataFrame:
    required_bindings = {"target_ts", "slot", "price_yuan_per_kWh", "known_at"}
    missing_bindings = sorted(required_bindings - set(column_mapping))
    if missing_bindings:
        raise DataContractError(
            f"dynamic-price attachment binding missing: {', '.join(missing_bindings)}"
        )
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        raw = pd.read_csv(path)
    elif suffix in {".xlsx", ".xlsm"}:
        raw = pd.read_excel(path, engine="openpyxl")
    else:
        raise DataContractError(f"unsupported dynamic-price attachment type: {suffix}")
    missing_source = [src for src in column_mapping.values() if src not in raw.columns]
    if missing_source:
        raise DataContractError(f"attachment missing mapped fields: {', '.join(missing_source)}")
    canonical = pd.DataFrame({dst: raw[src] for dst, src in column_mapping.items()})
    canonical["source"] = path.name
    canonical["provenance_sha256"] = sha256_file(path)
    return normalize_dynamic_price(
        canonical,
        slots_per_day=contract.slots_per_day,
        slot_minutes=contract.slot_minutes,
        time_mapping=str(contract.raw.get("time", {}).get("time_mapping", "")),
    )


def adapt_q2_upstream(
    frame: pd.DataFrame,
    *,
    mapping: Mapping[str, str],
    upstream_version: str,
    upstream_sha256: str,
    slots_per_day: int,
) -> pd.DataFrame:
    missing_map = [c for c in _UPSTREAM_CANONICAL if c not in mapping]
    if missing_map:
        raise DataContractError(f"upstream mapping missing canonical fields: {', '.join(missing_map)}")
    missing_src = [mapping[c] for c in _UPSTREAM_CANONICAL if mapping[c] not in frame.columns]
    if missing_src:
        raise DataContractError(f"upstream source missing fields: {', '.join(missing_src)}")
    if not upstream_version:
        raise DataContractError("upstream_version is required")
    if not _SHA256_RE.fullmatch(str(upstream_sha256)):
        raise DataContractError("upstream_sha256 must be a 64-hex sha256")

    out = pd.DataFrame({canonical: frame[source] for canonical, source in mapping.items() if canonical in _UPSTREAM_CANONICAL})
    out = out.loc[:, _UPSTREAM_CANONICAL]
    out["date"] = pd.to_datetime(out["date"], errors="raise").dt.strftime("%Y-%m-%d")
    out["decision_time"] = pd.to_datetime(out["decision_time"], errors="raise")
    out["slot"] = pd.to_numeric(out["slot"], errors="raise").astype(int)
    numeric_cols = [
        "q_active_kWh",
        "charge_ref_kWh",
        "discharge_ref_kWh",
        "SOC_start_kWh",
        "SOC_end_kWh",
        "emergency_kWh",
    ]
    for col in numeric_cols:
        out[col] = pd.to_numeric(out[col], errors="raise")
        if not pd.Series(out[col]).map(pd.notna).all():
            raise DataContractError(f"{col} contains non-finite values")
    if (out[["q_active_kWh", "charge_ref_kWh", "discharge_ref_kWh", "emergency_kWh"]] < 0).any().any():
        raise DataContractError("upstream energy actions must be nonnegative")
    validate_slot_grid(out, slots_per_day=slots_per_day, date_col="date", slot_col="slot")
    out["upstream_version"] = upstream_version
    out["upstream_sha256"] = upstream_sha256.lower()
    return out.reset_index(drop=True)

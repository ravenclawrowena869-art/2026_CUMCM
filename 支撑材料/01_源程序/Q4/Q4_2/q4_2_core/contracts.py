from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping
import re


class ContractNotLockedError(RuntimeError):
    """Raised when formal execution is attempted before required authority is locked."""


_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


@dataclass(frozen=True)
class Q4Contract:
    raw: dict[str, Any]

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Q4Contract":
        if not isinstance(payload, Mapping):
            raise TypeError("contract must be a mapping")
        raw = dict(payload)
        if not raw.get("contract_id"):
            raise ValueError("contract_id is required")
        if not raw.get("status"):
            raise ValueError("contract status is required")
        return cls(raw=raw)

    @property
    def contract_id(self) -> str:
        return str(self.raw["contract_id"])

    @property
    def status(self) -> str:
        return str(self.raw["status"])

    @property
    def is_locked_by_xxt(self) -> bool:
        return self.status == "LOCKED_BY_XXT"

    @property
    def slot_minutes(self) -> int:
        return int(self.raw["time"]["slot_minutes"])

    @property
    def slots_per_day(self) -> int:
        return int(self.raw["time"]["slots_per_day"])

    @property
    def writer_mapping_locked(self) -> bool:
        return bool(self.raw.get("writer", {}).get("official_mapping_locked", False))


def valid_sha256(value: str) -> bool:
    return bool(_SHA256_RE.fullmatch(str(value)))


def require_formal_dependencies(
    contract: Q4Contract,
    *,
    q2_upstream_sha: str,
    controller_approved_q2_sha: str,
) -> None:
    if bool(contract.raw.get("test_only", False)):
        raise ContractNotLockedError("test-only contract cannot authorize formal execution")
    if not contract.is_locked_by_xxt:
        raise ContractNotLockedError(
            f"Q4 common contract is {contract.status!r}; formal execution requires LOCKED_BY_XXT"
        )
    if not valid_sha256(q2_upstream_sha) or not valid_sha256(controller_approved_q2_sha):
        raise ContractNotLockedError("formal Q2 provenance requires two valid SHA256 values")
    if q2_upstream_sha.lower() != controller_approved_q2_sha.lower():
        raise ContractNotLockedError(
            "Q2 upstream SHA does not match Controller-approved final Q2 artifact"
        )

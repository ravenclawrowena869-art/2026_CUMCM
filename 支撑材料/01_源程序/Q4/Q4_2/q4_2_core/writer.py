from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from .contracts import Q4Contract


class OutputMappingError(RuntimeError):
    """Raised when result4-2 output authority/mapping is insufficient."""


def write_result_workbook(
    ledger: pd.DataFrame,
    path: str | Path,
    *,
    contract: Q4Contract,
    lane: str,
    formal: bool,
) -> dict[str, Any]:
    if formal:
        if not contract.is_locked_by_xxt:
            raise OutputMappingError("formal writer requires XXT-locked Q4 common contract")
        if not contract.writer_mapping_locked:
            raise OutputMappingError("formal writer requires locked official result4-2 mapping")
        if lane != "FORMAL_CAUSAL":
            raise OutputMappingError("oracle/diagnostic data are forbidden from formal result4-2")

    sheets = contract.raw.get("writer", {}).get("sheets")
    if not sheets:
        raise OutputMappingError("writer sheet mapping is unresolved")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as xw:
        for sheet_name, columns in sheets.items():
            missing = [c for c in columns if c not in ledger.columns]
            if missing:
                raise OutputMappingError(
                    f"writer mapping for {sheet_name} references missing columns: {missing}"
                )
            ledger.loc[:, columns].to_excel(xw, sheet_name=sheet_name, index=False)
    return {
        "path": str(path),
        "formal": formal,
        "lane": lane,
        "status": "FORMAL_WRITTEN" if formal else "TEST_ONLY_DRY_RUN",
        "sheet_names": list(sheets.keys()),
    }


def readback_workbook(path: str | Path, contract: Q4Contract) -> dict[str, Any]:
    sheets = contract.raw.get("writer", {}).get("sheets") or {}
    book = pd.ExcelFile(path, engine="openpyxl")
    expected = list(sheets.keys())
    actual = list(book.sheet_names)
    rows: dict[str, int] = {}
    columns_ok = True
    for sheet, columns in sheets.items():
        if sheet not in actual:
            columns_ok = False
            continue
        frame = pd.read_excel(path, sheet_name=sheet, engine="openpyxl")
        rows[sheet] = int(len(frame))
        if list(frame.columns) != list(columns):
            columns_ok = False
    return {
        "pass": actual == expected and columns_ok,
        "sheet_names": actual,
        "row_counts": rows,
        "columns_ok": columns_ok,
    }

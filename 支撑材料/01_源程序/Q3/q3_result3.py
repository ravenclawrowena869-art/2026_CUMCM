from __future__ import annotations

from pathlib import Path

from q3_contract import Q3Contract


def write_result3(
    contract: Q3Contract,
    template_path: Path,
    output_path: Path,
    day_ahead_rows: list[list[object]],
    final_commitment_rows: list[list[object]],
) -> None:
    contract.require_formal_lock()
    if not template_path.exists():
        raise FileNotFoundError(template_path)

    from artifact_tool import Blob, SpreadsheetFile

    wb = SpreadsheetFile.import_xlsx(Blob.load(str(template_path)))
    plan_sheet = wb.worksheets.get_item("计划购电量")
    adjust_sheet = wb.worksheets.get_item("调整购电量")

    plan_sheet.get_range_by_indexes(
        0, 0, len(day_ahead_rows), len(day_ahead_rows[0])
    ).values = day_ahead_rows
    adjust_sheet.get_range_by_indexes(
        0, 0, len(final_commitment_rows), len(final_commitment_rows[0])
    ).values = final_commitment_rows
    SpreadsheetFile.export_xlsx(wb).save(str(output_path))

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Mapping

import pandas as pd

from .contracts import Q4Contract, require_formal_dependencies
from .io_adapters import adapt_q2_upstream, normalize_dynamic_price
from .validation import audit_price_causality, validate_execution_ledger
from .writer import readback_workbook, write_result_workbook


def _normalize_inputs(
    *,
    price_frame: pd.DataFrame,
    upstream_frame: pd.DataFrame,
    upstream_mapping: Mapping[str, str],
    upstream_version: str,
    upstream_sha256: str,
    contract: Q4Contract,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    prices = normalize_dynamic_price(
        price_frame,
        slots_per_day=contract.slots_per_day,
        slot_minutes=contract.slot_minutes,
        time_mapping=str(contract.raw.get("time", {}).get("time_mapping", "")),
    )
    upstream = adapt_q2_upstream(
        upstream_frame,
        mapping=upstream_mapping,
        upstream_version=upstream_version,
        upstream_sha256=upstream_sha256,
        slots_per_day=contract.slots_per_day,
    )
    return prices, upstream


def run_preflight(
    *,
    price_frame: pd.DataFrame,
    upstream_frame: pd.DataFrame,
    upstream_mapping: Mapping[str, str],
    upstream_version: str,
    upstream_sha256: str,
    contract: Q4Contract,
    output_dir: str | Path,
) -> dict[str, Any]:
    """Run structural/dry-run checks only. Never represents a formal annual Q4-2 result."""
    prices, upstream = _normalize_inputs(
        price_frame=price_frame,
        upstream_frame=upstream_frame,
        upstream_mapping=upstream_mapping,
        upstream_version=upstream_version,
        upstream_sha256=upstream_sha256,
        contract=contract,
    )
    causality = audit_price_causality(prices, upstream, lane="FORMAL_CAUSAL")
    merged = upstream.merge(
        prices[["date", "slot", "price_yuan_per_kWh"]],
        on=["date", "slot"],
        how="left",
        validate="one_to_one",
    )
    dry = merged.assign(
        charge_kWh=merged["charge_ref_kWh"],
        discharge_kWh=merged["discharge_ref_kWh"],
        soc_start_kWh=merged["SOC_start_kWh"],
        soc_end_kWh=merged["SOC_end_kWh"],
    )
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    workbook = outdir / "result4-2.TEST_ONLY_DRY_RUN.xlsx"
    writer = write_result_workbook(
        dry,
        workbook,
        contract=contract,
        lane="FORMAL_CAUSAL",
        formal=False,
    )
    readback = readback_workbook(workbook, contract)
    if not readback["pass"]:
        raise RuntimeError("dry-run result4-2 writer/readback failed")
    return {
        "preflight_status": "PASS_TEST_ONLY",
        "formal_result_ready": False,
        "formal_blockers": [
            "Q4_COMMON_CONTRACT_PENDING_XXT_LOCK",
            "FINAL_Q2_ARTIFACT_HASH_PENDING_CONTROLLER_APPROVAL",
        ],
        "future_leakage_count": causality["future_leakage_count"],
        "price_rows": int(len(prices)),
        "upstream_rows": int(len(upstream)),
        "dry_run_workbook": writer["path"],
        "readback": readback,
    }


def run_formal_q4_2(
    *,
    price_frame: pd.DataFrame,
    upstream_frame: pd.DataFrame,
    upstream_mapping: Mapping[str, str],
    upstream_version: str,
    upstream_sha256: str,
    controller_approved_q2_sha: str,
    contract: Q4Contract,
    strategy_runner: Callable[..., pd.DataFrame],
    output_path: str | Path,
) -> dict[str, Any]:
    """Execute the formal orchestration chain after all external gates are locked."""
    require_formal_dependencies(
        contract,
        q2_upstream_sha=upstream_sha256,
        controller_approved_q2_sha=controller_approved_q2_sha,
    )
    if not contract.writer_mapping_locked:
        from .writer import OutputMappingError
        raise OutputMappingError("formal execution requires locked official result4-2 mapping")

    prices, upstream = _normalize_inputs(
        price_frame=price_frame,
        upstream_frame=upstream_frame,
        upstream_mapping=upstream_mapping,
        upstream_version=upstream_version,
        upstream_sha256=upstream_sha256,
        contract=contract,
    )
    causality = audit_price_causality(prices, upstream, lane="FORMAL_CAUSAL")
    execution = strategy_runner(upstream=upstream.copy(), prices=prices.copy(), contract=contract)
    if not isinstance(execution, pd.DataFrame):
        raise TypeError("strategy_runner must return a pandas DataFrame execution ledger")
    if "price_yuan_per_kWh" not in execution.columns:
        execution = execution.merge(
            prices[["date", "slot", "price_yuan_per_kWh"]],
            on=["date", "slot"],
            how="left",
            validate="one_to_one",
        )
    validator = validate_execution_ledger(execution, contract)
    if not validator["pass"]:
        raise RuntimeError(
            f"formal Q4-2 execution violates hard constraints: max={validator['max_violation']} "
            f"at {validator['argmax_location']}"
        )
    writer = write_result_workbook(
        execution,
        output_path,
        contract=contract,
        lane="FORMAL_CAUSAL",
        formal=True,
    )
    readback = readback_workbook(output_path, contract)
    if not readback["pass"]:
        raise RuntimeError("formal result4-2 readback failed")
    return {
        "formal_result_ready_for_xxt_review": True,
        "contract_id": contract.contract_id,
        "q2_upstream_sha256": upstream_sha256.lower(),
        "causality": causality,
        "validator": validator,
        "writer": writer,
        "readback": readback,
    }

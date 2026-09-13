from __future__ import annotations

import json
from pathlib import Path

from q3_contract import ContractNotLocked, mock_preflight_contract
from q3_forecast import linear_hourly_to_10min_energy
from q3_settlement import settle_day
from q3_state import ActiveCommitmentBook
from q3_validator import validate_day


def build_mock_case() -> dict:
    contract = mock_preflight_contract()
    prices = [1.0] * 144
    q0 = [100.0] * 144
    book = ActiveCommitmentBook("2025-02-01")
    book.set_day_ahead(q0)
    book.adjust(
        stage_id=1,
        decision_minute=360,
        updates={37: 110.0, 38: 90.0},
        forecast_vintage_id="mock-0600",
        known_at_max="2025-02-01T06:00:00",
    )

    final_q = list(book.active)
    emergency = [0.0] * 144
    charge = [0.0] * 144
    discharge = [0.0] * 144
    pv = [20.0] * 144
    load = [final_q[i] + pv[i] for i in range(144)]
    soc = [6000.0] * 144
    settlement = settle_day(contract, prices, q0, book.stage_ledger, emergency)
    validation = validate_day(
        contract=contract,
        prices=prices,
        q0_kwh=q0,
        ledger=book.stage_ledger,
        final_commitment_kwh=final_q,
        normal_received_kwh=final_q,
        emergency_kwh=emergency,
        actual_load_kwh=load,
        actual_pv_kwh=pv,
        charge_kwh=charge,
        discharge_kwh=discharge,
        initial_soc_kwh=6000.0,
        reported_soc_end_kwh=soc,
        claimed_total_cost_yuan=settlement.total_cost_yuan,
    )
    forecast = linear_hourly_to_10min_energy(360, 60.0, [60.0] * 24)

    formal_guard = "FAIL"
    try:
        contract.require_formal_lock()
    except ContractNotLocked:
        formal_guard = "PASS"

    return {
        "mode": "MOCK_DRY_RUN_ONLY",
        "formal_guard": formal_guard,
        "validator": validation.to_dict(),
        "stage_ledger_rows": len(book.stage_ledger),
        "forecast_slots_after_0600": len(forecast),
        "formal_metrics_generated": False,
        "result3_generated": False,
    }


if __name__ == "__main__":
    result = build_mock_case()
    out = (
        Path(__file__).resolve().parents[2]
        / "03_中间结果"
        / "Q3"
        / "PARALLEL_EXEC_R0"
        / "DRY_RUN_VALIDATOR.json"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))

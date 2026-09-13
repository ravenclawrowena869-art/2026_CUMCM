from __future__ import annotations

import sys
from pathlib import Path

import pytest

Q3_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Q3_DIR))

from q3_contract import ContractNotLocked, mock_preflight_contract
from q3_forecast import linear_hourly_to_10min_energy
from q3_loader import load_daily_actuals, require_forecast_vintages
from q3_pipeline import FormalQ3Runner
from q3_settlement import adjustment_cost
from q3_state import ActiveCommitmentBook
from q3_time import future_slots


def test_right_endpoint_future_slots() -> None:
    assert future_slots(0)[0] == 1
    assert future_slots(360)[0] == 37
    assert future_slots(720)[0] == 73
    assert future_slots(1080)[0] == 109


def test_executed_slot_is_immutable() -> None:
    book = ActiveCommitmentBook("2025-02-01")
    book.set_day_ahead([100.0] * 144)
    with pytest.raises(RuntimeError):
        book.adjust(1, 360, {36: 120.0}, "v0600", "06:00")


def test_previous_active_commitment_delta() -> None:
    contract = mock_preflight_contract()
    book = ActiveCommitmentBook("2025-02-01")
    book.set_day_ahead([100.0] * 144)
    book.adjust(1, 360, {37: 120.0}, "v0600", "06:00")
    book.adjust(2, 720, {73: 80.0}, "v1200", "12:00")
    prices = [1.0] * 144
    assert adjustment_cost(contract, prices, book.stage_ledger) == pytest.approx(20.0)


def test_linear_forecast_uses_realized_boundary() -> None:
    result = linear_hourly_to_10min_energy(360, 60.0, [120.0] * 24)
    assert result[37] == pytest.approx(70.0 / 6.0)
    assert result[42] == pytest.approx(120.0 / 6.0)


def test_formal_run_is_fail_closed() -> None:
    with pytest.raises(ContractNotLocked):
        mock_preflight_contract().require_formal_lock()


def test_loader_rejects_incomplete_vintages() -> None:
    with pytest.raises(ValueError):
        require_forecast_vintages({"00:00": [0.0] * 24})


def test_daily_loader_requires_144_slots() -> None:
    with pytest.raises(ValueError):
        load_daily_actuals("2025-02-01", [1.0] * 143, [1.0] * 144, [0.0] * 144)


def test_formal_pipeline_is_fail_closed() -> None:
    class DummyController:
        def run_year(self, contract, stage_minutes):
            return {"unexpected": True}

    runner = FormalQ3Runner(mock_preflight_contract(), DummyController())
    with pytest.raises(ContractNotLocked):
        runner.run("S0_00_ONLY")


def test_issue_time_price_sensitivity_is_explicit() -> None:
    contract = mock_preflight_contract()
    contract = type(contract)(**{**contract.__dict__, "settlement_price_time": "ISSUE_TIME_PRICE"})
    book = ActiveCommitmentBook("2025-02-01")
    book.set_day_ahead([100.0] * 144)
    book.adjust(1, 360, {37: 110.0}, "v0600", "06:00")
    prices = [1.0] * 144
    assert adjustment_cost(contract, prices, book.stage_ledger, {1: 2.0}) == pytest.approx(30.0)

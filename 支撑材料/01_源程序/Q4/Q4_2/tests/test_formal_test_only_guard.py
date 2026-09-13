from __future__ import annotations

import pandas as pd
import pytest

from q4_2_core.contracts import Q4Contract
from q4_2_core.writer import OutputMappingError, write_result_workbook


def test_direct_formal_writer_rejects_test_only_contract(tmp_path):
    contract = Q4Contract.from_dict({
        "contract_id": "Q4_COMMON_CONTRACT_TEST_ONLY",
        "test_only": True,
        "status": "LOCKED_BY_XXT",
        "time": {"slot_minutes": 10, "slots_per_day": 1},
        "writer": {
            "official_mapping_locked": True,
            "sheets": {"计划购电量": ["date", "slot", "q_active_kWh", "price_yuan_per_kWh"]}
        }
    })
    ledger = pd.DataFrame({
        "date": ["2025-02-01"],
        "slot": [1],
        "q_active_kWh": [1.0],
        "price_yuan_per_kWh": [0.5]
    })
    with pytest.raises(OutputMappingError, match="test-only"):
        write_result_workbook(
            ledger,
            tmp_path / "result4-2.xlsx",
            contract=contract,
            lane="FORMAL_CAUSAL",
            formal=True,
        )

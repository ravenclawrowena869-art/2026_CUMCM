from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from q4_2_core.contracts import Q4Contract
from q4_2_core.orchestrator import run_preflight

FIX = Path(__file__).resolve().parent / "fixtures"
OUT = Path(__file__).resolve().parents[4] / "03_中间结果" / "Q4" / "Q4_2" / "PREFLIGHT_R0"

contract = Q4Contract.from_dict(json.loads((FIX / "q4_common_contract.TEST_ONLY.json").read_text(encoding="utf-8")))
prices = pd.read_csv(FIX / "dynamic_price.TEST_ONLY.csv")
upstream = pd.read_csv(FIX / "q2_upstream.TEST_ONLY.csv")
summary = run_preflight(
    price_frame=prices,
    upstream_frame=upstream,
    upstream_mapping={
        "date": "day",
        "slot": "slot_id",
        "decision_time": "decision_ts",
        "q_active_kWh": "q",
        "charge_ref_kWh": "c",
        "discharge_ref_kWh": "d",
        "SOC_start_kWh": "soc0",
        "SOC_end_kWh": "soc1",
        "emergency_kWh": "r"
    },
    upstream_version="Q2_TEST_ONLY",
    upstream_sha256="b" * 64,
    contract=contract,
    output_dir=OUT,
)
(OUT / "DRY_RUN_SUMMARY.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))

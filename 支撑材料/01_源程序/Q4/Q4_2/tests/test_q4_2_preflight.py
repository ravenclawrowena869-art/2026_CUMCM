from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from q4_2_core.contracts import ContractNotLockedError, Q4Contract, require_formal_dependencies
from q4_2_core.io_adapters import DataContractError, adapt_q2_upstream, load_dynamic_price_attachment, normalize_dynamic_price
from q4_2_core.validation import FutureLeakageError, audit_price_causality, validate_execution_ledger
from q4_2_core.writer import OutputMappingError, readback_workbook, write_result_workbook
from q4_2_core.orchestrator import run_formal_q4_2, run_preflight


def mock_contract(*, locked: bool = False, official_writer: bool = False) -> Q4Contract:
    return Q4Contract.from_dict({
        "contract_id": "Q4_COMMON_CONTRACT_TEST_ONLY", "test_only": True,
        "status": "LOCKED_BY_XXT" if locked else "TEST_ONLY_MOCK",
        "time": {"slot_minutes": 10, "slots_per_day": 2, "time_mapping": "C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT"},
        "storage": {"soc_min_kWh": 1.0, "soc_max_kWh": 10.0, "slot_energy_max_kWh": 3.0, "eta_c": 0.9, "eta_d": 0.9, "recursion": "Q2_BUS_SIDE_R1", "cross_day": "NO_DAILY_RESET"},
        "balance": {"lhs": [["q_active_kWh",1.0],["emergency_kWh",1.0],["pv_kWh",1.0],["discharge_kWh",1.0]], "rhs": [["paid_unused_kWh",1.0],["load_kWh",1.0],["charge_kWh",1.0],["pv_curtail_kWh",1.0]]},
        "settlement": {"normal_multiplier":1.0,"emergency_multiplier":5.0,"selling_allowed":False},
        "writer": {"official_mapping_locked": official_writer, "sheets": {"计划购电量":["date","slot","q_active_kWh","price_yuan_per_kWh"], "执行明细":["date","slot","charge_kWh","discharge_kWh","soc_start_kWh","soc_end_kWh","emergency_kWh"]}}
    })


def price_df(*, future: bool=False) -> pd.DataFrame:
    return pd.DataFrame({"target_ts":["2025-02-01 00:10:00","2025-02-01 00:20:00"],"slot":[1,2],"price_yuan_per_kWh":[0.5,0.6],"known_at":["2025-02-01 00:20:00" if future else "2025-02-01 00:00:00","2025-02-01 00:00:00"],"source":["mock","mock"],"provenance_sha256":["a"*64,"a"*64]})


def upstream_df() -> pd.DataFrame:
    return pd.DataFrame({"day":["2025-02-01"]*2,"slot_id":[1,2],"decision_ts":["2025-02-01 00:00:00"]*2,"q":[3.0,2.0],"c":[1.0,0.0],"d":[0.0,1.0],"soc0":[5.0,5.9],"soc1":[5.9,4.788888888888889],"r":[0.0,0.5]})


def mapping():
    return {"date":"day","slot":"slot_id","decision_time":"decision_ts","q_active_kWh":"q","charge_ref_kWh":"c","discharge_ref_kWh":"d","SOC_start_kWh":"soc0","SOC_end_kWh":"soc1","emergency_kWh":"r"}


def canonical_upstream():
    return adapt_q2_upstream(upstream_df(),mapping=mapping(),upstream_version="Q2_TEST",upstream_sha256="b"*64,slots_per_day=2)


def execution_ledger():
    return pd.DataFrame({"date":["2025-02-01"]*2,"slot":[1,2],"q_active_kWh":[3.0,2.0],"emergency_kWh":[0.0,0.5],"pv_kWh":[1.0,0.0],"discharge_kWh":[0.0,1.0],"paid_unused_kWh":[1.0,0.0],"load_kWh":[2.0,3.5],"charge_kWh":[1.0,0.0],"pv_curtail_kWh":[0.0,0.0],"soc_start_kWh":[5.0,5.9],"soc_end_kWh":[5.9,4.788888888888889],"export_kWh":[0.0,0.0],"price_yuan_per_kWh":[0.5,0.6]})


def norm(frame):
    return normalize_dynamic_price(frame,slots_per_day=2,slot_minutes=10,time_mapping="C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT")


def test_dependencies_fail_closed():
    with pytest.raises(ContractNotLockedError): require_formal_dependencies(mock_contract(),q2_upstream_sha="b"*64,controller_approved_q2_sha="b"*64)
    with pytest.raises(ContractNotLockedError): require_formal_dependencies(mock_contract(locked=True),q2_upstream_sha="b"*64,controller_approved_q2_sha="c"*64)


def test_price_contract_and_causality():
    with pytest.raises(DataContractError,match="known_at"): norm(price_df().drop(columns=["known_at"]))
    with pytest.raises(DataContractError,match="duplicate"): norm(pd.concat([price_df(),price_df().iloc[[0]]],ignore_index=True))
    with pytest.raises(FutureLeakageError): audit_price_causality(norm(price_df(future=True)),canonical_upstream(),lane="FORMAL_CAUSAL")
    r=audit_price_causality(norm(price_df(future=True)),canonical_upstream(),lane="ORACLE_DIAGNOSTIC")
    assert r["future_leakage_count"]==1 and r["status"]=="DIAGNOSTIC_ONLY / FUTURE_LEAKAGE_BY_DESIGN"


def test_q2_adapter_and_sha():
    out=canonical_upstream(); assert out["upstream_sha256"].nunique()==1
    with pytest.raises(DataContractError,match="sha256"): adapt_q2_upstream(upstream_df(),mapping=mapping(),upstream_version="Q2_TEST",upstream_sha256="bad",slots_per_day=2)
    bad=upstream_df(); bad.loc[1,"slot_id"]=3
    with pytest.raises(DataContractError,match="slot"): adapt_q2_upstream(bad,mapping=mapping(),upstream_version="Q2_TEST",upstream_sha256="b"*64,slots_per_day=2)


def test_validator_and_accounting():
    r=validate_execution_ledger(execution_ledger(),mock_contract())
    assert r["pass"] and r["max_balance_violation_kWh"]<=1e-9 and r["max_soc_recursion_violation_kWh"]<=1e-9
    assert r["normal_cost_cny"]==pytest.approx(2.7) and r["emergency_cost_cny"]==pytest.approx(1.5) and r["total_cost_cny"]==pytest.approx(4.2)


def test_validator_reports_failure_location():
    bad=execution_ledger(); bad.loc[1,"soc_end_kWh"]=12.0; bad.loc[1,"export_kWh"]=0.25
    r=validate_execution_ledger(bad,mock_contract()); assert not r["pass"] and r["argmax_location"]=={"date":"2025-02-01","slot":2} and r["export_violation_max_kWh"]==pytest.approx(0.25)


def test_writer_gates_and_readback(tmp_path:Path):
    for contract,lane in [(mock_contract(official_writer=True),"FORMAL_CAUSAL"),(mock_contract(locked=True),"FORMAL_CAUSAL"),(mock_contract(locked=True,official_writer=True),"ORACLE_DIAGNOSTIC")]:
        with pytest.raises(OutputMappingError): write_result_workbook(execution_ledger(),tmp_path/"formal.xlsx",contract=contract,lane=lane,formal=True)
    path=tmp_path/"dry.xlsx"; m=write_result_workbook(execution_ledger(),path,contract=mock_contract(),lane="FORMAL_CAUSAL",formal=False); rb=readback_workbook(path,mock_contract())
    assert m["status"]=="TEST_ONLY_DRY_RUN" and rb["pass"] and rb["row_counts"]=={"计划购电量":2,"执行明细":2}


def test_preflight_stays_nonformal(tmp_path:Path):
    s=run_preflight(price_frame=price_df(),upstream_frame=upstream_df(),upstream_mapping=mapping(),upstream_version="Q2_TEST",upstream_sha256="b"*64,contract=mock_contract(),output_dir=tmp_path)
    assert s["preflight_status"]=="PASS_TEST_ONLY" and not s["formal_result_ready"] and s["future_leakage_count"]==0 and Path(s["dry_run_workbook"]).exists()


def test_slot_count_timestamp_and_provenance():
    with pytest.raises(DataContractError,match="slot count"): norm(price_df().iloc[[0]])
    shifted=price_df(); shifted.loc[1,"target_ts"]="2025-02-01 00:30:00"
    with pytest.raises(DataContractError,match="timestamp/slot"): norm(shifted)
    bad=price_df(); bad["provenance_sha256"]="not-a-sha"
    with pytest.raises(DataContractError,match="provenance_sha256"): norm(bad)


def test_attachment_loader_csv_xlsx_and_known_at_gate(tmp_path:Path):
    raw=price_df().drop(columns=["source","provenance_sha256"]); bind={"target_ts":"target_ts","slot":"slot","price_yuan_per_kWh":"price_yuan_per_kWh","known_at":"known_at"}
    for ext in ("csv","xlsx"):
        p=tmp_path/f"attachment4.{ext}"; raw.to_csv(p,index=False) if ext=="csv" else raw.to_excel(p,index=False)
        out=load_dynamic_price_attachment(p,column_mapping=bind,contract=mock_contract()); assert len(out)==2 and out["provenance_sha256"].str.fullmatch(r"[0-9a-f]{64}").all()
    p=tmp_path/"missing.csv"; raw.drop(columns=["known_at"]).to_csv(p,index=False)
    with pytest.raises(DataContractError,match="known_at"): load_dynamic_price_attachment(p,column_mapping={"target_ts":"target_ts","slot":"slot","price_yuan_per_kWh":"price_yuan_per_kWh"},contract=mock_contract())


def test_formal_orchestrator_checks_authority_before_strategy(tmp_path:Path):
    called=False
    def runner(*args,**kwargs):
        nonlocal called; called=True; return execution_ledger()
    with pytest.raises(ContractNotLockedError): run_formal_q4_2(price_frame=price_df(),upstream_frame=upstream_df(),upstream_mapping=mapping(),upstream_version="Q2_TEST",upstream_sha256="b"*64,controller_approved_q2_sha="b"*64,contract=mock_contract(),strategy_runner=runner,output_path=tmp_path/"result4-2.xlsx")
    assert not called


def test_mock_contract_cannot_authorize_formal():
    with pytest.raises(ContractNotLockedError,match="test-only"): require_formal_dependencies(mock_contract(locked=True,official_writer=True),q2_upstream_sha="b"*64,controller_approved_q2_sha="b"*64)


def test_validator_requires_complete_grid():
    with pytest.raises(DataContractError,match="slot count"): validate_execution_ledger(execution_ledger().iloc[[0]].copy(),mock_contract())

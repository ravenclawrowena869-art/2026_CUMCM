#!/usr/bin/env python3
"""Synthetic negative-oracle suite for Q2 pre-validation R2.

This is NOT a Q2 optimizer and produces no competition result. It checks that a
validator implementation would reject known semantic/accounting/causality errors.
Stdlib only, deterministic.
"""
from __future__ import annotations
import csv, math, sys
from pathlib import Path

TOL = 1e-9


def base_case():
    # A physically consistent S1-A slot: q-w+r+PV+d = L+c+v = 100 kWh.
    return {
        "s1_semantics": "S1_A_PAID_UNUSED_NORMAL_ENERGY",
        "q": 100.0, "q_locked": 100.0, "w": 20.0, "v": 10.0,
        "pv": 20.0, "load": 80.0, "c": 10.0, "d": 0.0, "r": 0.0,
        "p": 1.0, "normal_cost": 100.0, "emergency_cost": 0.0,
        "w_label": "paid_unused_normal", "v_label": "pv_curtailment",
        "known_at": 100.0, "decision_time": 100.0,
        "price_source": "ATTACHMENT1_FIXED_REPEATED_TARIFF",
        "E_before": 6000.0, "E_after": 6009.0, "eta_c": 0.9, "eta_d": 0.9,
        "soc_min": 1200.0, "soc_max": 10800.0,
        "prev_day_end": 6000.0, "next_day_start": 6000.0,
        "terminal_mode": "FREE_BOUNDED_YEAR_END", "terminal_report_status": "PASS", "E_end": 6000.0,
        "risk_alpha_changed": False, "full_replan": True,
        "baseline_ref_c": 10.0, "baseline_ref_d": 0.0,
        "delayed_actual_sensitivity_planned": True,
        "w_evidence_complete": True, "v_evidence_separate": True,
        "time_mapping": "C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT",
        "u_total": 30.0, "total_cost": 100.0,
    }


def apply_mutation(x, m):
    if m in ("valid_source_resolved", "valid_utotal_compat"):
        return
    if m == "old_generic_spill":
        x["s1_semantics"] = "GENERIC_SPILL"
        x["generic_u"] = 30.0
    elif m == "w_gt_q":
        x["w"] = 110.0
    elif m == "v_gt_pv":
        x["v"] = 25.0
    elif m == "w_relabel_pv":
        x["w_label"] = "pv_curtailment"
    elif m == "normal_cost_received":
        x["normal_cost"] = x["p"] * (x["q"] - x["w"])
    elif m == "emergency_multiplier_1x":
        x.update({"load": 190.0, "c": 0.0, "w": 0.0, "v": 0.0, "r": 70.0, "emergency_cost": 70.0})
        x["E_after"] = x["E_before"]
        x["u_total"] = 0.0
    elif m == "q_mutated_after_0000":
        x["q"] = 101.0
        # Keep the physical slot consistent so commitment immutability is isolated.
        x["w"] = 21.0
        x["normal_cost"] = 101.0
        x["u_total"] = 31.0
    elif m == "future_actual_known_at":
        x["known_at"] = 101.0
    elif m == "dynamic_price_in_q2":
        x["price_source"] = "ATTACHMENT4_DYNAMIC_PRICE"
    elif m == "emergency_and_charge":
        x.update({"load": 200.0, "c": 10.0, "d": 0.0, "w": 0.0, "v": 0.0, "r": 90.0})
        x["E_after"] = x["E_before"] + 9.0
        x["emergency_cost"] = 450.0
        x["u_total"] = 0.0
    elif m == "simultaneous_charge_discharge":
        x["d"] = 5.0
        # adjust v to keep slot balance, and recurrence to isolate simultaneity
        x["v"] = 15.0
        x["E_after"] = x["E_before"] + 0.9*10.0 - 5.0/0.9
        x["u_total"] = x["w"] + x["v"]
    elif m == "soc_below_bound":
        x["E_after"] = 1000.0
    elif m == "daily_soc_reset":
        x["prev_day_end"] = 5500.0
        x["next_day_start"] = 6000.0
    elif m == "t1_mismatch_marked_pass":
        x["terminal_mode"] = "EQ_INITIAL_6000"
        x["E_end"] = 5900.0
        x["terminal_report_status"] = "PASS"
    elif m == "alpha_change_no_replan":
        x["risk_alpha_changed"] = True
        x["full_replan"] = False
    elif m == "fixed_action_amplified":
        x["baseline_ref_c"] = 5.0
        x["c"] = 10.0
    elif m == "missing_delayed_actual_sensitivity":
        x["delayed_actual_sensitivity_planned"] = False
    elif m == "missing_w_audit":
        x["w_evidence_complete"] = False
    elif m == "total_spill_only":
        x["v_evidence_separate"] = False
    elif m == "wrong_time_mapping":
        x["time_mapping"] = "TEMPLATE_HEADER_AS_PHYSICAL_INTERVAL"
    elif m == "total_cost_adds_w_again":
        x["total_cost"] = x["normal_cost"] + x["emergency_cost"] + x["p"]*x["w"]
    else:
        raise ValueError(f"unknown mutation {m}")


def validate(x):
    e = set()
    if x.get("s1_semantics") != "S1_A_PAID_UNUSED_NORMAL_ENERGY":
        e.add("FAIL_S1_SOURCE_RESOLUTION")
    q,w,v,pv = x["q"], x["w"], x["v"], x["pv"]
    if w < -TOL or w > q + TOL or v < -TOL or v > pv + TOL:
        e.add("FAIL_S1_BOUNDS")
    if x.get("w_label") != "paid_unused_normal" or x.get("v_label") != "pv_curtailment":
        e.add("FAIL_S1_LABEL")
    # Physical balance uses source-resolved semantics, never generic u as a replacement.
    resid = q - w + x["r"] + pv + x["d"] - x["load"] - x["c"] - v
    if abs(resid) > 1e-7:
        e.add("FAIL_PHYSICS")
    if abs(x["normal_cost"] - x["p"]*q) > 1e-7 or abs(x["emergency_cost"] - 5*x["p"]*x["r"]) > 1e-7:
        e.add("FAIL_ACCOUNTING")
    expected_total = x["normal_cost"] + x["emergency_cost"]
    if abs(x.get("total_cost", expected_total) - expected_total) > 1e-7:
        e.add("FAIL_ACCOUNTING")
    if abs(q - x["q_locked"]) > TOL:
        e.add("FAIL_COMMITMENT")
    if x["known_at"] > x["decision_time"] + TOL:
        e.add("FAIL_LEAKAGE")
    if x["price_source"] != "ATTACHMENT1_FIXED_REPEATED_TARIFF":
        e.add("FAIL_PRICE_SOURCE")
    if x["r"] > TOL and x["c"] > TOL:
        e.add("FAIL_EMERGENCY_CHARGING")
    if x["c"] > TOL and x["d"] > TOL:
        e.add("FAIL_PHYSICS")
    expected_E = x["E_before"] + x["eta_c"]*x["c"] - x["d"]/x["eta_d"]
    if abs(expected_E - x["E_after"]) > 1e-7 or not (x["soc_min"]-TOL <= x["E_after"] <= x["soc_max"]+TOL):
        e.add("FAIL_PHYSICS")
    if abs(x["prev_day_end"] - x["next_day_start"]) > 1e-7:
        e.add("FAIL_CROSS_DAY_SOC")
    if x["terminal_mode"] == "EQ_INITIAL_6000" and abs(x["E_end"]-6000.0) > 1e-7 and x["terminal_report_status"] == "PASS":
        e.add("FAIL_TERMINAL")
    if x["risk_alpha_changed"] and not x["full_replan"]:
        e.add("FAIL_RISK_PROTOCOL")
    if x["c"] > x["baseline_ref_c"] + TOL or x["d"] > x["baseline_ref_d"] + TOL:
        # This check is only meaningful for the synthetic fixed-storage baseline case;
        # baseline_ref values equal action in positive controls.
        e.add("FAIL_BASELINE")
    if not x["delayed_actual_sensitivity_planned"]:
        e.add("FAIL_EVIDENCE")
    if not x["w_evidence_complete"] or not x["v_evidence_separate"]:
        e.add("FAIL_S1_EVIDENCE")
    if x["time_mapping"] != "C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT":
        e.add("FAIL_MAPPING")
    if abs(x.get("u_total", w+v) - (w+v)) > 1e-7:
        e.add("FAIL_S1_EVIDENCE")
    return e


def main():
    here = Path(__file__).resolve().parent
    cases_path = here / "XXT_Q2_ADVERSARIAL_CASES_R2.csv"
    out_path = here / "XXT_Q2_ADVERSARIAL_RESULTS_R2.csv"
    rows = list(csv.DictReader(cases_path.open(encoding="utf-8")))
    results=[]
    ok=0
    for row in rows:
        x=base_case(); apply_mutation(x,row["mutation"])
        errors=validate(x)
        observed="PASS" if not errors else ";".join(sorted(errors))
        expected=row["expected_code"]
        passed = (expected == "PASS" and not errors) or (expected in errors)
        ok += int(passed)
        results.append({**row,"observed_codes":observed,"oracle_pass":"PASS" if passed else "FAIL"})
    with out_path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(results[0].keys())); w.writeheader(); w.writerows(results)
    print(f"adversarial_oracle: {ok}/{len(rows)} cases matched expected detection")
    if ok != len(rows):
        for r in results:
            if r["oracle_pass"] != "PASS": print(r)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

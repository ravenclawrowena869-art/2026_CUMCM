from __future__ import annotations
import hashlib,json
from pathlib import Path
from src.q1_figure_chain import export_cost_comparison_table,export_figure_data,export_paper_tables
from src.q1_figure_merge_r2 import export_final_interfaces
from plots.make_q1_main_figure_r2 import render_q1_main_figure
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    root=Path(__file__).resolve().parent; snap=root/"frozen_source_snapshot"; gen=root/"generated"; tab=gen/"tables"; fig=gen/"figures"
    gen.mkdir(parents=True,exist_ok=True); tab.mkdir(parents=True,exist_ok=True); fig.mkdir(parents=True,exist_ok=True)
    fd=gen/"Q1_FIGURE_DATA_R2.csv"; export_figure_data(snap,fd); export_paper_tables(snap,tab)
    c=tab/"Q1_PAPER_TABLE_03_COST_COMPARISON_R1.csv"; export_cost_comparison_table(snap,c)
    export_final_interfaces(fd,c,gen); render_q1_main_figure(fd,fig)
    fs=[p for p in gen.rglob("*") if p.is_file() and not p.name.startswith("GENERATION_MANIFEST_")]
    m={"status":"Q1_FIGURE_CHAIN_MERGE_READY","freeze_id":"CUMCM2026_C_Q1_FREEZE_R0_20260911","selection":"SELECT_1_MAIN_FIGURE","window_rule":"FULL_HORIZON","model_result_freeze_preserved":True,"files":{str(p.relative_to(root)):sha(p) for p in sorted(fs)}}
    for name in ["GENERATION_MANIFEST_R2.json"]:
        (gen/name).write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(m,ensure_ascii=False,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())

# SUBMISSION MIRROR PLAN R0

Status: `SUBMISSION_MIRROR_STRUCTURE_READY` — structure only, **not a submission candidate**.

```text
submission_mirror/
├─ paper/
│  └─ FINAL_PAPER.pdf                 # insert only after PAPER_LOCKED
└─ support-material/
   ├─ AI 工具使用详情.pdf
   ├─ result1.xlsx
   ├─ result2.xlsx
   ├─ result3.xlsx
   ├─ result4-2.xlsx
   ├─ result4-3.xlsx
   ├─ 01_源程序/
   │  ├─ Q1/
   │  ├─ Q2/
   │  ├─ Q3/
   │  └─ Q4/
   ├─ 03_中间结果/                    # only evidence necessary for paper conclusions
   ├─ 04_复现说明/
   └─ README                          # if retained by final package policy
```

Do not copy `_development/`, Task ZIPs, debug logs, caches, superseded FINAL files, personal notes, obsolete result workbooks or GitHub download wrappers.

## Freeze-bound insertions
- `result1.xlsx`: only the verified Q1 frozen official workbook.
- `result2.xlsx`: only after current Q2 Mathematical PASS/Freeze.
- `result3.xlsx`: only after current Q3 Mathematical PASS/Freeze.
- `result4-2.xlsx` / `result4-3.xlsx`: only after current Q4 Mathematical PASS/Freeze.
- source directories: consolidate only the runnable final versions; development snapshots stay outside the mirror.
- AI disclosure: generate the final PDF only after the full ledger is team-verified.

## Identity lint
Run on final PDF, support tree, code, README, tables, figures and document metadata:

- [ ] no participant names, student IDs, team IDs, school/college names or competition region;
- [ ] no personal email, phone, account handle or profile text;
- [ ] no local usernames or absolute paths such as `C:\\Users\\...`, `/Users/...`, `/home/...`;
- [ ] no member-name/initial filenames or directories in the submission version;
- [ ] no GitHub owner/repository URL or private-project link if it identifies the team;
- [ ] no author/company/last-saved-by identity in PDF/DOCX/XLSX metadata;
- [ ] no comments, tracked changes, hidden sheets, notes, alt text or image metadata carrying identity;
- [ ] no screenshots containing account names, desktop paths, browser profile or chat identity;
- [ ] no code headers/debug logs identifying members or machines;
- [ ] after any hit is fixed, rebuild mirror and rerun clean replay + identity lint.

Suggested generic automated text patterns (extend with the team’s actual identifiers before final run):
`姓名|学号|队伍|学校|学院|赛区|C:\\Users\\|/Users/|/home/|github.com/`

## Candidate gate
A mirror can become a submission candidate only after: all Q1–Q4 frozen sources are identified; five official result workbooks are inserted; source directories are consolidated; paper/Figure Registry/AI provenance is complete; clean replay passes; identity lint passes; final PDF is manually inspected. MD5 sealing happens only after that.

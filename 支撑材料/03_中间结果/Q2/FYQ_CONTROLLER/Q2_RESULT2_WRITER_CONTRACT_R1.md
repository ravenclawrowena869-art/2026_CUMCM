# Q2 result2 Writer Contract R1

Status: `FYQ_OUTPUT_BINDING / PRE-EXECUTION`

Official template:

- `C题/附件/附件5/result2.xlsx`
- SHA256: `1c26494cfc6d754e0bd9bff7e13e1126a73d2d2da6c5336eb251d89b9a1a1a47`

This writer contract defines output mapping only. It must not drive solver time semantics.

## 1. Global time rule

Use `C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`.

Canonical physical slot `slot_id = 1..144` is determined by the model/source time axis. Export it **positionally** to the 144 template slot columns. The official human-readable interval text is `DISPLAY_LABEL_ONLY` and must never be parsed back into solver time.

For `计划购电量`:

- date rows: 2025-02-01 through 2025-12-31, 334 rows;
- slot columns: `B:EO`, exactly 144 columns;
- `slot_id=1 -> B`, ..., `slot_id=144 -> EO`;
- `EP = 全天购电量`;
- `EQ = 全天购电费`.

The template's first displayed interval is `0:10-0:20` and its final interval is `0:00-0:10+1`. These labels are not allowed to shift the physical 00:00–24:00 model horizon.

## 2. 计划购电量 sheet

For every date d and slot t:

- write locked day-ahead normal commitment `q_DA[d,t]` in kWh;
- do not write used-normal energy `q_DA-w`;
- do not add emergency purchase into the slot cells.

Daily summary columns:

- `EP[d] = sum_t q_DA[d,t]`, kWh;
- `EQ[d] = sum_t p[t] * q_DA[d,t]`, CNY, i.e. the normal planned-purchase cost represented by this sheet.

Emergency purchase cost remains separately reproducible from the emergency ledger as `sum_t 5*p[t]*r[d,t]`. Formal Q2 total cost is the sum of normal planned-purchase cost and emergency purchase cost; it is recorded in evidence/reporting and must not be silently substituted into `EQ`.

## 3. 充放电量 sheet

The official template shows Feb 1, Feb 2, an ellipsis, and Dec 31. The writer must expand the ellipsis to **all 334 dates**.

For each date create six rows in this exact block order:

1. `0:00-4:00`
2. `4:00-8:00`
3. `8:00-12:00`
4. `12:00-16:00`
5. `16:00-20:00`
6. `20:00-24:00`

For each 4-hour block:

- `充电量 = sum(c_t)` over its 24 canonical 10-minute slots;
- `放电量 = sum(d_t)` over its 24 canonical 10-minute slots;
- units are kWh.

Date-cell convention:

- write the date only on the first row of each six-row daily block;
- leave the following five date cells blank, matching the template grouping style.

SOC cells:

- first row of the daily block: `时刻 = 0:00`, `储电量 = E[d,0]`;
- second row: `时刻 = 24:00`, `储电量 = E[d,144]`;
- remaining four `时刻/储电量` cells remain blank.

`E[d,0]` must equal the previous day's final SOC. Feb 1 must inherit the Jan 31 replay state; no independent Feb 1 reset is allowed.

## 4. 紧急购电量 sheet

The official template contains ellipsis/example rows. The writer must generate the complete Feb 1–Dec 31 event ledger from canonical physical slots.

For each date:

1. identify slots with independently recomputed `r_t > 1e-6 kWh`;
2. merge only **physically consecutive canonical slots** into one emergency interval;
3. interval start/end must come from canonical physical slot boundaries, not the shifted display labels in the plan sheet;
4. `购电量 = sum(r_t)` over the merged interval, kWh;
5. if a day has multiple disjoint intervals, write multiple rows and place the date only on the first row for that date;
6. if a day has no emergency event, retain one dated row with blank interval and `购电量 = 0` so that absence is explicit and readback is deterministic.

No interval may cross a non-emergency gap. A midnight-adjacent event is split by natural-day output ownership unless the official writer/readback explicitly supports a cross-date interval; the underlying slot ledger remains authoritative.

## 5. Paper date set

The official problem's Table 3 date set is:

- 2025-03-20
- 2025-06-21
- 2025-09-23
- 2025-12-21

Paper tables for Q2 must be regenerated from the same saved slot/event ledger used for result2, not manually copied from another run.

## 6. Save/readback acceptance

After writing and saving result2.xlsx, reopen the saved file and independently verify:

- workbook contains exactly the three required sheets;
- `计划购电量` covers all 334 dates and 144 positional slots/day;
- all exported q values match the locked commitment ledger;
- EP and EQ recompute exactly within cost tolerance;
- every 4-hour charge/discharge aggregation recomputes from slot-level c/d;
- every 0:00/24:00 SOC value matches the full SOC replay;
- emergency intervals reproduce the slot-level emergency ledger without gaps/overlaps/double counting;
- the four official Table-3 dates can be reconstructed from the saved workbook;
- no formula/display label is used as a substitute for canonical slot IDs.

Any readback mismatch is `FAIL_OUTPUT_MAPPING`; it cannot be waived by a solver PASS.
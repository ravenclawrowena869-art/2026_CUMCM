# TASK — CYQ Paper Acceleration R1

`ACTIVE_ROLE=CYQ_PAPER`

Recommended model: `GPT-5.6 Sol / Medium or High`.

## Purpose

Advance the full Q1-Q4 paper framework in parallel with Q2 validation and Q3/Q4 technical design. Do not wait for every result to Freeze before writing stable framework prose.

## First action

Fresh-read canonical Skill:
`SKILL.md -> Shared Core -> CYQ Profile -> Paper Pipeline -> Per-question Writing Gate -> Paper Handoff`.

## Technical sources

Read-only:
- Q1 Frozen Status / Final Freeze Manifest / final Figure chain;
- Q2 Model Plan Freeze + current Core acceptance;
- Q3 XXT preflight + `Q3_DESIGN_STABLE_R1.md`;
- `Q4_CAUSAL_PRICE_PREDESIGN_R1.md`;
- literature-to-model evidence matrix supplied by FYQ;
- current Figure Registry / source provenance.

## Status tags

Use explicitly in working draft metadata:
- `FROZEN_FACT`
- `DESIGN_STABLE`
- `OPEN_INTERFACE`
- `OPEN_PARAMETER`
- `PENDING_EVIDENCE`

Do not leave these tags in final polished prose if the corresponding item later freezes; they are authoring controls.

## Q1

May advance close to final prose using Frozen facts.

Do not write:
- “削峰” as a proved result;
- Stage-2 exported cost as the exact Stage-1 optimum at full precision;
- LP naturally forbids simultaneous charge/discharge;
- epsilon=1e-4 is globally optimal or an intrinsic solver tolerance;
- efficiency semantics are irrelevant.

## Q2

May write:
- causal 00:00 commitment problem;
- Load LAG7 / PV trailing-7 baseline rationale;
- 5x emergency penalty and q80 risk anchor;
- S1-A accounting definition;
- rolling/fixed storage comparison design;
- full validation plan.

Must leave `PENDING_EVIDENCE` for:
- formal winning strategy;
- formal total cost;
- result2 identity;
- alpha/delayed/terminal/efficiency conclusions;
- Mathematical PASS.

Core candidate costs may be kept in an internal evidence table, but must not be written as final ranking because the mandatory sensitivity campaign and delayed-actual adjudication are open.

## Q3

May write framework prose for:
- 0/6/12/18 forecast vintages;
- rolling/receding-horizon architecture;
- previous-active-commitment ledger;
- adjustment/emergency cost decomposition;
- hourly-to-10min forecast transform;
- 00-only vs multi-stage experiment logic;
- literature rationale.

Do not call `ROLLING_HORIZON_LP_CANDIDATE_R0` the final model until XXT/FYQ complete model selection.

## Q4

May write framework prose for:
- causal dynamic-price information set;
- Q2-style and Q3-style inherited models;
- causal LAG7 price baseline candidate;
- oracle future-price diagnostic boundary;
- experiment/validator design.

Do not assume future realized Attachment4 prices are known at earlier decision times.

## Literature use

Use literature to support mechanisms/model families, not to import parameters or results. At minimum maintain citations for:
- forecast update + re-planning;
- day-ahead + intraday MPC/rolling optimization;
- risk-aware day-ahead microgrid scheduling;
- forecast quality -> dispatch cost relationship.

## Required output

Return:
`CUMCM2026_C_CYQ_PAPER_ACCELERATION_R1_DELIVERY.zip`

Include:
- updated paper draft;
- claim-status matrix;
- citation registry;
- Figure Registry update;
- Evidence Gap Return for FYQ/XXT;
- list of every placeholder still blocking final prose.

Do not modify technical Frozen facts.

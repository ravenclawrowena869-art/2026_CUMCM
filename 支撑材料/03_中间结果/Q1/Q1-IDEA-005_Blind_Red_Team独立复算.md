# Q1-IDEA-005 Blind Red Team 独立复算

- `IDEA_ID`: `Q1-IDEA-005`
- `STATUS`: `UNDER_REVIEW`
- `AUTHORITY`: `WORKING_IDEA_ONLY`
- `OWNER`: `FYQ / XXT`
- `CREATED_AT`: `2026-09-11`
- `LAST_UPDATED`: `2026-09-11`

## 目的

Q1 主模型形成 current-version mathematical candidate 后，引入独立 Blind Red Team，从官方题面、附件1和数学合同重新实现 LP/MILP 并独立复算，不读取正式 solver 源码或原 results，以降低同源验证偏差。

## 独立复算结果

FYQ Controller fresh 验收后接受：

`Q1_BLIND_RED_TEAM_NUMERIC = PASS`

主要独立结果：

- Stage-1 cost ≈ `35126.94858928963 CNY`；
- Stage-2 exported schedule cost ≈ `35126.948689289624 CNY`；
- NO_STORAGE ≈ `48052.04659084666 CNY`；
- `eta_c=eta_d=sqrt(0.9)` sensitivity ≈ `33801.495642222 CNY`；
- max SOC sensitivity difference ≈ `623.114486442 kWh`；
- LP vs mutex-MILP Stage-1 objective 一致；
- MILP gap = 0；
- simultaneous C/D = 0；
- balance / SOC recursion residual 处于 `1e-13 kWh` 数量级。

Red Team Claim Comparison 中 12/12 待核验 Claim 均 MATCH。

FYQ 还把 Red Team primary schedule 与 Engineering Closeout schedule 做了逐列数值对照，grid / charge / discharge / SOC 最大差仅处于约 `1e-10 kWh` 或更小的浮点量级。

## Independence 边界

Red Team 的求解代码没有把正式 candidate 目标值写进求解器。正式数字仅在 solve 后 comparison layer 中用于比对。

因此本轮可作为有效 independent shadow recomputation evidence。

## 来源限制

Red Team 与 FYQ 当前都无法定位项目最初指定的两个 exact legacy ZIP：

- `write-update-math-modeling-paper-complete.zip`
- `cumcm-rigorous-workflow-main (1).zip`

该限制已显式记录，不影响 Red Team 数值独立性结论，但在项目当前规则下不能被描述为“三个 exact ZIP 已联合复读”。

对应 replacement-authority 方案正在 workflow Proposal PR 中审查。

## 当前决定

Blind Red Team 数值层已经退出 Q1 blocker；Q1 不因本轮触发 Mathematical P0，也不需要重开模型。

最终是否 Freeze 仍由 FYQ Final Evidence Gate 结合 R2、来源、AI/human adoption 与最终 provenance 共同裁决。

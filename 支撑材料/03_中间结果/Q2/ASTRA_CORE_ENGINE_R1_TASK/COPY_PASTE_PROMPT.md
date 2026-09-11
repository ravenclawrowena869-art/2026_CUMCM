# COPY-PASTE PROMPT — CYQ ASTRA HIGH

任务：
`CUMCM2026-C-Q2-ASTRA-CORE-ENGINE-R1`

这是一个 **Astra High 限定执行 Burst**。

物理执行节点可以在 CYQ 账户，但：

`ACTIVE_ROLE = FYQ_TECHNICAL_ORCHESTRATOR`

不要切换成 `CYQ_PAPER`。

先读取本包：

1. `00_START_HERE.md`
2. `ASTRA_SCOPE_BOUNDARY.md`
3. `CORE_ENGINE_IMPLEMENTATION_TASK.md`
4. `ASTRA_STOP_POINT.md`
5. `REQUIRED_DELIVERY.md`

然后 fresh-read canonical `cumcm-rigorous-workflow`，并读取：

repo:
`ravenclawrowena869-art/2026_CUMCM`

PR #6 / branch:
`fyq/q2-controller-restore-20260911`

task creation authority head:
`07413d24e290804b979188aad521809e9dcba623`

入口：
`支撑材料/03_中间结果/Q2/FYQ_CONTROLLER/HANDOFF_TO_CYQ_CODEX_R2.md`

selected math authority:

base XXT R1:
`0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`

XXT R2 prevalidation:
`63c2494eac89b164830d9e26435332f6c06afedc0234ba5a05d25468f4d0a312`

本任务只负责最值得 Astra 的部分：

**生产级 reusable Q2 engine + 集成 + 第一次 canonical 334-day clean full-year execution + alpha=0.80 四策略矩阵 + canonical hard validation + result2 write/readback。**

必须把后续 sensitivity/config hooks 实现好，但不要继续用 Astra 批量跑完整：

- alpha .75/.85 annual replay；
- ONE_SLOT_DELAYED_ACTUAL annual replay；
- efficiency annual sensitivity；
- terminal annual sensitivity；
- final tail diagnostic campaign。

这些回交 FYQ Sol High。

如果旧的 broad CYQ full-year task 已经执行了一部分，不要从头重来。保留有效工作，按本任务的新 stop point 收口。

最终交付：
`CUMCM2026_C_Q2_ASTRA_CORE_ENGINE_R1_DELIVERY.zip`

最终状态只能是：
`ASTRA_CORE_ENGINE_READY_FOR_SOL_CONTINUATION`
或本包规定的 HOLD/FAIL 状态。

不要 Freeze。
不要 Mathematical PASS。
不要生成 Paper 正式数字结论。
不要自行 merge GitHub PR。

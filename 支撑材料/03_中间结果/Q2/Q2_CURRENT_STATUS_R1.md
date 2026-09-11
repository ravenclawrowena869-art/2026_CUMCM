# Q2 Current Status R1

## Formal state

- `Q2_MATH_CONTRACT_ID = CUMCM2026_C_Q2_MATH_CONTRACT_R1`
- `Q2_FORMAL_MATH_SPEC = PASS_WITH_LIMITATION`
- `S1 = S1_A_PAID_UNUSED_NORMAL_ENERGY`
- `S1_CONTROLLER_AUTHORIZATION = PASS_WITH_LIMITATION`
- `Q2_IMPLEMENTATION_RELEASE = READY_AFTER_INPUT_BINDING`
- `Q2_FORMAL_RESULT = NOT_RUN`
- `Q2_MATHEMATICAL_RESULT_PASS = FALSE`
- `Q2_FROZEN = FALSE`

## Original authority identities

XXT R1 delivery：

`CUMCM2026_C_XXT_Q2_FORMAL_OPT_SPEC_R1_DELIVERY.zip`

SHA256：`0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`

CRC PASS；top-level checksum `23/23 PASS`。

FYQ Controller review：

`CUMCM2026_C_CONTROLLER_Q2_FORMAL_SPEC_R1_REVIEW.zip`

SHA256：`d69fd9736a0a5736223e40f26211332534c31331afc834aa0e3ab5d0a325ccca`

CRC PASS；internal checksum `5/5 PASS`。

## Core model family

- `POINT_DA_LP_R1`：每天 00:00 锁定 normal purchase commitment。
- `Q2_RH_FIXED_Q_LP_R1`：每 10 min 使用因果可得信息，对固定 q 做 storage recourse。
- baseline：`DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE`。
- risk candidate：`SIGNED_RESIDUAL_Q80_MARGIN_R1`。

正常购电全部按 commitment 收费。S1 中 `w` 表示已付费但未使用的 normal energy；无退款、无售电收入，与 PV curtailment 分开。

## Mandatory evidence before Freeze

1. `ONE_SLOT_DELAYED_ACTUAL` full sensitivity / counterfactual；
2. 每日 24 h truncation tail diagnostic；
3. S1 `w` 全量 audit；
4. `alpha=.75/.80/.85` 重新规划 + full replay；
5. full input/provenance binding；
6. independent objective/accounting + full SOC path replay；
7. current-version XXT Mathematical Review。

## Repository status

Merged PR #4：authority supplement request。

PR #5：XXT authority restoration，Draft，未 merge。

PR #6：FYQ Controller restoration，Draft，未 merge。

当前执行窗口仍不得把 stable contract ID 当作 full-year execution license。先完成 authority completion、input binding 和 FYQ execution release。
# Q4-2 Technical Summary R0

Block: `Q4-2-FORMAL-R1`  
Base: `704d67f84d56428eb48892784579ecba6aaeb53b`  
Branch: `fyq/q4-2-formal-r1`  
Current state: `IMPLEMENTED_PRE_FORMAL / FORMAL_RESULT_BLOCKED`

## 本轮已经实现并真实验证

1. 动态电价 CSV/XLSX loader，实际文件 SHA-256 自动绑定；`known_at` 缺失时 fail closed。
2. 右端点 ordinal 的 timestamp/slot 归一化、逐日精确 slot count、重复 slot 和错位 timestamp 拦截。
3. Q2 稳定 upstream adapter。Q4-2 不直接 import Q2 开发目录，最终只需要替换 Controller-approved artifact 与字段 mapping。
4. `known_at <= decision_time` 因果审计。formal lane 发现未来价格立即失败；oracle lane 强制标记 `DIAGNOSTIC_ONLY / FUTURE_LEAKAGE_BY_DESIGN`。
5. 全路径 validator：平衡式、SOC 递推、SOC 上下界、充放电槽能量限制、跨时段/跨日连续性、非负动作、禁止售电、同时充放电、max violation + argmax。
6. 独立 accounting recompute 接口。结算倍率只从显式 contract 读取，当前 formal settlement 仍未锁定。
7. 合同驱动 workbook writer/readback。formal writer 会拒绝 TEST_ONLY contract、未锁 common contract、未锁 official mapping、oracle lane。
8. Q4-2 orchestrator 的 formal dependency Gate 在调用 strategy runner 之前执行，避免 mock/未批准 Q2 进入正式链路。
9. TEST_ONLY 接口 fixtures 与 dry-run workbook/readback 已执行。

## 真实验证证据

- 本地 expanded regression suite：`17 passed`。
- TEST_ONLY dry-run：`PASS_TEST_ONLY`。
- dry-run future leakage count：`0`。
- dry-run writer/readback：PASS，两个测试 sheet 均 2 行。
- synthetic validator：balance/SOC recursion/continuity 最大违反量均在 `1e-6 kWh` Gate 内。
- failure-path tests 覆盖：缺 `known_at`、重复/缺失 slot、timestamp/slot 错位、bad SHA、future leakage、SOC/export violation、oracle formal write、unlocked contract、mock contract formal leakage。

## 当前明确未做

- 未运行 334-day 正式 Q4-2 annual replay。
- 未生成正式 `支撑材料/05求解结果/result4-2.xlsx`。
- 未声明 Q4-2 Mathematical PASS / Evidence PASS / Freeze。
- 未填写任何 formal Q4-2 成本数字。

## Formal blockers

1. `Q4_COMMON_CONTRACT` 仍需 XXT lock，尤其 price information set、settlement、Q2 inheritance、export、terminal SOC、official writer mapping。
2. 最终 Q2 artifact/hash 仍需 FYQ Controller 在 q closure + current Mathematical PASS 后批准。
3. 上述两项完成后，替换 TEST_ONLY fixtures，执行一次 canonical 334-day formal replay，随后跑 independent objective/accounting + full SOC replay + readback，再提交 XXT review。

当前最高状态：

`Q4_2_ENGINEERING_PREFLIGHT = PASS_TEST_ONLY`

`Q4_2_FINAL_RESULT_READY_FOR_XXT = FALSE`

## 证据等级

- `SOFTWARE_CONTRACT_VERIFIED`：是，限本轮 pre-formal 工程合同与 TEST_ONLY failure paths。
- `INTEGRATION_NOT_VERIFIED`：是，尚未绑定 XXT-locked Q4 common contract 与 Controller-approved final Q2 artifact。
- `REAL_DATA_NOT_VERIFIED`：是，未进行正式 Attachment 4 全年 Q4-2 replay。
- `PRODUCTION_NOT_VERIFIED`：是，Q4-2 formal result 尚未生成。

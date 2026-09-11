Q2_MATH_CONTRACT_ID = CUMCM2026_C_Q2_MATH_CONTRACT_R1

# XXT → FYQ / Codex implementation handoff

退出 `HOLD_FOR_EVIDENCE`。六件所需合同交付齐备，实施规则已写明；未运行Q2正式优化，未给予任何结果Freeze。

## 唯一物理 release blocker

S1：明确正常计划q全额收费后，未使用电量是否允许不接收/丢弃。R0允许spill；R1禁止general dump且称PV弃光。请求Controller审批规范第1节S1-A（q-w实际接收、q照计费），或坚持S1-B并补充吸收保证。请在独立授权载体记录 `normal_purchase_surplus_mode` 与authority hash；不覆盖本包既有hash文件。审批后发下一版release状态。本ID可引用，但不是绕过阻断的license。

## 已确定的开发输入

point日前144槽LP、固定q剩余日LP、互斥动作的模式界、零storage故障fallback、fixed baseline最小clip、有符号残差解析80%reserve、January bridge/annual SOC、两种效率、三个terminal、固定Attachment1 tariff、严格known_at均已给出完整公式。

标准枚举：storage=`CAUSAL_INTRADAY` 或 `DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE`；policy=`POINT_DA_LP_R1` 或 `SIGNED_RESIDUAL_Q80_MARGIN_R1`；time mapping=`C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`；forecast update=`FROZEN_DAILY_0000`；normal surplus=S1待批。

日初步骤：核验W2 adapter与R14 bridge → 构造point或past-only margin → 解日前LP及throughput阶段 → 锁定q/reference/hash。逐槽：放出当前actual → 读取SOC和锁定q → 解剩余LP或fixed clip → 独立计算emergency/余量 → 更新SOC并记录provenance。跨日直接传E，禁止重置。T1/T2不可达则记录失败，不借紧急电充电完成末端。

## 开发前输入清单

当前包只有W2摘要和指标，未提供全部forecast/source bytes。正式run前需接入既有W2 144288行导出，筛选load/PV为96192行（48096槽×2），其truth保留独立评价访问器；metadata用本exact ID、price scope修复及family重分类。接入Attachment1固定tariff原始hash、R14 bridge输出hash、模型预注册证据；题面指定表3日期与官方模板另读原件。缺项阻断formal replay但不要求重做W1。

## 先测后跑顺序（后续实现轮）

1. 实施规范中的手算anchor和validator负例，先RED后GREEN。
2. 单日、跨午夜、Jan31→Feb1、Dec31目标不可达边界测试。
3. point/risk × causal/fixed完整回放，各自产生全轨迹；另做共享commitment受控比较。
4. 两个causal政策分别做效率、terminal单因素敏感性；参数邻域重新规划全回放。
5. 独立费用与全路径SOC复算、完整信息访问审计、hash/CRC、指定日期/模板输出回读。
6. Controller+XXT current implementation review之后才讨论Freeze；Q2全期policy最优不由局部LP optimal状态证明。

## 限制与历史结论

W1基线family条件接受为预声明政策，Aug-Oct离线adequacy；动态price Q4_ONLY。当前slot actual用于本槽是R1离散假设。每日24h规划无延续价值，须报告短视和末端效应。1%、5%及480kWh等authority screening只作提示，不替代对策略排序/可行性的数学裁决。S1未决是release HOLD而非已证明的current-result P0。

本轮AI参与为数学合同设计与文档编制；human_verification/team_decision/adoption均PENDING，不冒填人工采纳。

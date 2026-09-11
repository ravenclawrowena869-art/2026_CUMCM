# Q2 XXT Authority 补件索引

- 模块：2026 CUMCM C 题问题二
- 角色：`XXT_MATHEMATICAL`
- 当前合同 ID：`CUMCM2026_C_Q2_MATH_CONTRACT_R1`
- 当前状态：`Q2_MATH_READY_FOR_IMPLEMENTATION`
- 正式全年 replay：`NOT_RUN`
- Q2 Freeze：`FORBIDDEN`

## 1. Authority 身份

PR #4 任务书记录的历史 XXT 原始 ZIP SHA256 为：

`0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`

当前会话可取得的是重新生成并完成 Gate 自检的 current-version 数学 authority 包：

`CUMCM2026_C_XXT_Q2_FORMAL_OPT_SPEC_R1_DELIVERY.zip`

其外层 SHA256 为：

`d22609f9ec0368888472945f948de66fb70669a3bc89877574fd0ab8834ea54c`

两者哈希不一致，因此**当前包不得冒充历史 byte-identical 原始 ZIP**。本目录将当前包视为用于继续 FYQ Controller Review / implementation binding 的 current-version authority snapshot；历史 ZIP 若日后找回，应重新核验并记录差异，不得静默覆盖本目录 current authority。

## 2. 已直接入库的关键文件

- `XXT_Q2_FORMAL_OPT_SPEC_R1.md`：正式数学合同与 P0/P1/P2 优化定义；
- `XXT_Q2_MATH_CONTRACT_MANIFEST_R1.json`：机器可读合同、来源与 canonical 参数；
- `XXT_Q2_RISK_PARAMETER_PROTOCOL_R1.md`：SIGNED residual / Q80 风险参数协议；
- `XXT_Q2_VALIDATOR_SPEC_R1.md`：独立 replay 与 Mathematical Gate validator contract；
- `XXT_Q2_MODEL_FAMILY_CAUSALITY_ADJUDICATION_R1.md`：预测模型族因果性与 provenance 裁决；
- `XXT_Q2_IMPLEMENTATION_HANDOFF_R1.md`：交给 FYQ/Codex 的实现接口；
- `SHA256SUMS.txt`：上述包内文件 checksum。

## 3. ZIP 状态

完整 ZIP 大小约 44 KB，当前聊天工作区可读取并通过内部 checksum。当前 GitHub 连接器只支持 UTF-8 文本内容写入，不能保真写入二进制 ZIP，因此本次先按 PR #4 的回退要求将承担 authority / interface / review 作用的 MD、JSON 与 checksum 全部入库。

完整 ZIP 当前外层 SHA256：

`d22609f9ec0368888472945f948de66fb70669a3bc89877574fd0ab8834ea54c`

当前没有可由本连接器写入的持久二进制下载位置，故不能伪造 ZIP 已入库状态。若后续使用本地 Git/GitHub Web/支持二进制文件参数的连接器补传 ZIP，应保持同一 SHA256 并在此 README 更新其仓库路径。

## 4. Supersede / Gate 边界

- 当前文件用于解除“执行者缺少数学定义”的 authority blocker；
- 不代表 FYQ Controller Review 已完成；
- 不代表全年优化已运行；
- 不授予 `Q2_MATHEMATICAL_PASS`；
- 不授予 `Q2_FROZEN`；
- FYQ 应在核验本目录 current-version authority 后，按 PR #4 要求将 Controller/interface 补件提交到 `../FYQ_CONTROLLER/`。

## 5. 下一步

按 PR #4 提交顺序：

1. XXT authority 文件入库（本目录）；
2. FYQ 核验当前合同与 checksum；
3. FYQ 生成并上传 Controller Review / implementation interface；
4. Codex/Astra 执行窗口核验两侧 authority 后，才恢复 Q2 全年实现与验证。

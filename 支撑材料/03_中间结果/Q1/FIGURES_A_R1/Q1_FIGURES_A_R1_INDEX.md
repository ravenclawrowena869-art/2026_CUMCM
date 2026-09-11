# Q1 Figures A R1 仓库索引

完整本地图表包：
`CUMCM2026_C_Q1_FIGURES_A_R1.zip`

SHA256：
`a1f29b70f3ee16be9fe0f9c7ab6b3e4359c74c70e0aeba351d7bdf5755af1d59`

GitHub repository-native 可下载包：
`CUMCM2026_C_Q1_FIGURES_A_R1_REPO_NATIVE.zip`

SHA256：
`a40c07460e1bd607cbf8e3b6f64aea3505f2e2fa90727564f0a1add7f81cb7b2`

Freeze：
`CUMCM2026_C_Q1_FREEZE_R0_20260911`

图表：
1. `Q1_FIG_01_购电与储能联合调度结果`
2. `Q1_FIG_02_储能优化前后购电曲线对比`

完整本地 ZIP 中含：
- 300 dpi PNG
- PDF
- SVG
- `Q1_FROZEN_FIGURE_DATA_R1.csv`
- `make_q1_figures.py`
- `Q1_FIGURE_REGISTRY_R1.csv`
- metrics/provenance/README/checksums

GitHub repository-native ZIP 与解压目录保留：
- 完整 144 槽 Frozen Figure Data；
- frozen metrics；
- Figure Registry；
- 可编辑绘图脚本；
- provenance / checksum。

CYQ 可直接从 GitHub 下载 repository-native ZIP，或读取解压文件核对数据和复现。运行 `make_q1_figures.py` 会从冻结 Figure Data 重新导出同规格 PNG/PDF/SVG；正式论文图不得从截图或聊天数字反推。

用途：供 CYQ Paper 选择、排版与 Figure Review。技术数据来自 Q1 Frozen Output，版式可调整，但 Frozen 数值和技术含义只读。

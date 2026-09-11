# Q1 正式绘图链 R2

Authority: `CUMCM2026_C_Q1_FREEZE_R0_20260911`.

本目录保存 Q1 的可编辑、可 clean replay 绘图链。正式 Source of Truth 路径：

`Frozen Output -> Figure Data -> Figure Script -> PDF/SVG/PNG -> Paper`

当前论文视觉裁决：`SELECT_1_MAIN_FIGURE`。主图为 FULL_HORIZON 四联图：电价、负荷/PV预测/优化购电、充放电、SOC。

运行：
```bash
cd 支撑材料/01_源程序/Q1/figure_chain_r2
python run_all.py
python -m pytest -q tests
```

目录内 `frozen_source_snapshot/` 是本轮绘图链 clean replay 的冻结技术输入，不是第二套模型。R2 仅补全绘图/表格 provenance，不修改 Q1 Frozen 模型、result1 或正式数字。

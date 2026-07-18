# -*- coding: utf-8 -*-
"""Append textflow audit and refreshed package note to project memory."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"
ENTRY = """

## 2026-07-06 用户样本文本流复核与新交付包

- 针对用户贴出的“地质表/构造段后接方言声韵调段”样本，复跑 `audit_mojibake_and_sample_continuity_20260705.py` 与 `audit_final_reader_textflow_risk_20260705.py`；当前主交付 `output/final_reader/连云港市志_全书.html` 中两类锚点不相邻，地质构造锚点与方言声韵调锚点相距约 259 万字符，不能证明当前主交付存在该连续拼接错误。
- 审计确认：当前主交付超长段落 0、疑似表格压扁段落 0；旧 `output/final_reader/连云港市志_最终阅读版.html` 及部分旧分册 HTML 仍有表格压扁/旧转换残留，若误打开旧文件会看到类似问题。报告：`output/reports/progress/20260705_阅读版文本流风险审计.md`、`output/reports/progress/20260705_正文错乱样本与乱码副产物审计.md`。
- 同轮复跑：`audit_delivery_quality.py issues=0`；`audit_full_reader.py` Missing anchors `[]`、Placeholders `0`、TOC links `65`；`audit_table_delivery_readiness.py tables=305/problem_tables=0/issues=0`；`build_table_source_verification_queue.py queued=0`。
- 已基于当前主交付重打包：`output/package/连云港市志_交付包_20260706_145418`，包内 HTML 路径 `output/package/连云港市志_交付包_20260706_145418/连云港市志_最终阅读版.html`，PDF 路径 `output/package/连云港市志_交付包_20260706_145418/连云港市志_最终阅读版.pdf`。本轮未展示、未嵌入任何图片。
""".strip()

text = MEMORY.read_text(encoding="utf-8")
if ENTRY not in text:
    MEMORY.write_text(text.rstrip() + "\n\n" + ENTRY + "\n", encoding="utf-8")
print("memory_appended")

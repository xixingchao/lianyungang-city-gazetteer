# -*- coding: utf-8 -*-
"""Repair source-backed post-liberation item headings in volume 2."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume2_postliberation_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume2_postliberation_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第二卷解放以后条目边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>一、新海连特区</p>": "<h5>一、新海连特区</h5>",
    "<p>二、新海连市</p>": "<h5>二、新海连市</h5>",
    "<p>三、新海县</p>": "<h5>三、新海县</h5>",
    "<p>四、连云港市</p>": "<h5>四、连云港市</h5>",
}

SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第二卷_建置区划.md:852-854",
    "workbench/body_chapters/paddle_上/第二卷_建置区划.md:867-868",
    "workbench/body_chapters/paddle_上/第二卷_建置区划.md:874-875",
    "workbench/body_chapters/paddle_上/第二卷_建置区划.md:1021-1022",
]

TABLE_RESIDUE = [
    "output/final_reader/连云港市志_全书.html:2857",
    "output/final_reader/连云港市志_全书.html:2864",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> int:
    text = HTML.read_text(encoding="utf-8")
    changed = 0
    for old, new in REPLACEMENTS.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected one match for {old!r}, got {count}")
        text = text.replace(old, new, 1)
        changed += 1
    HTML.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第二卷建置区划：第二章第二节解放以后条目标题",
        "html_boundaries_fixed": changed,
        "source_evidence": SOURCE_LINES,
        "known_residual_table_text": TABLE_RESIDUE,
        "notes": [
            "仅按 PaddleOCR 源文独立行恢复条目标题边界，不改正文文字。",
            "表2-6的线性 OCR 残文仍保留为后续表格恢复对象，本批不反推表格数值。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第二卷解放以后条目边界修复

- 时间：{now}
- 范围：第二卷建置区划，第二章建置沿革，第二节解放以后。
- 本次修复边界：{changed} 处。

## 修复

- 将 `一、新海连特区`、`二、新海连市`、`三、新海县`、`四、连云港市` 从普通段落恢复为条目标题。
- 仅恢复源文可证明的版式边界，不改正文文字。
- `表2-6 1956年新海连市行政区划表` 当前在最终阅读版中仍有线性 OCR 残文；本批不反推表格数值，留给后续表格恢复。

## 依据

"""
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    md += "\n## 保留风险\n\n"
    md += "".join(f"- `{line}`：表2-6线性 OCR 残文。\n" for line in TABLE_RESIDUE)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第二卷解放以后条目边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第二卷建置区划 `第二节解放以后` 4 处条目标题边界：`一、新海连特区`、`二、新海连市`、`三、新海县`、`四、连云港市`。
- 依据 `workbench/body_chapters/paddle_上/第二卷_建置区划.md` 中的独立行，只恢复标题语义，不改正文文字。
- `表2-6 1956年新海连市行政区划表` 的线性 OCR 残文暂不反推数值，另列为后续表格恢复对象。
- 报告：`output/reports/reader_readability_volume2_postliberation_boundaries_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

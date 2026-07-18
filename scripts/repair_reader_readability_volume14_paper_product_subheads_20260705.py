# -*- coding: utf-8 -*-
"""Repair source-backed paper product subheading boundaries in volume 14."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume14_paper_product_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume14_paper_product_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第十四卷造纸产品分项标题边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>一、草浆卫生纸民国20年（1931年），板浦普益南纸坊": "<h5>一、草浆卫生纸</h5>\n<p>民国20年（1931年），板浦普益南纸坊",
    "<p>二、棉浆卫生纸1962年，新浦造纸厂因草浆纸滞销": "<h5>二、棉浆卫生纸</h5>\n<p>1962年，新浦造纸厂因草浆纸滞销",
}

SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:10583-10584",
    "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:10617-10618",
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
        "scope": "第十四卷轻（手）工业：造纸章生活用纸产品分项标题",
        "html_boundaries_fixed": changed,
        "source_evidence": SOURCE_LINES,
        "notes": ["仅按 PaddleOCR 源文独立行恢复标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第十四卷造纸产品分项标题边界修复

- 时间：{now}
- 范围：第十四卷轻（手）工业，第一章造纸，第一节生活用纸。
- 本次修复边界：{changed} 处。

## 修复

- 恢复 `一、草浆卫生纸`、`二、棉浆卫生纸` 两处产品分项标题。
- 仅恢复源文可证明的版式边界，不改正文文字。

## 依据

"""
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第十四卷造纸产品分项标题边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第十四卷轻（手）工业造纸章 2 处产品分项标题粘正文问题：`一、草浆卫生纸`、`二、棉浆卫生纸`。
- 依据 `workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md` 中独立行，只恢复标题边界，不改正文文字。
- 报告：`output/reports/reader_readability_volume14_paper_product_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Split volume 1 mineral-resource headings in final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_mineral_resource_headings_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_mineral_resource_headings_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷矿产资源标题版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>第四节矿产资源一、金属矿黑色金属": "<h4>第四节 矿产资源</h4>\n<h5>一、金属矿</h5>\n<p><strong>黑色金属</strong>",
    "<p>有色金属 锦屏山": "<p><strong>有色金属</strong> 锦屏山",
    "<p>贵金属境内金矿矿点": "<p><strong>贵金属</strong>境内金矿矿点",
    "<p>稀土金属赣榆县": "<p><strong>稀土金属</strong>赣榆县",
    "<p>二、非金属矿磷 境内磷矿资源丰富": "<h5>二、非金属矿</h5>\n<p><strong>磷</strong> 境内磷矿资源丰富",
}


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
    for residue in REPLACEMENTS:
        if residue in text:
            raise RuntimeError(f"mineral-resource residue remains: {residue}")
    HTML.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第一卷自然环境：第四节矿产资源",
        "html_boundaries_split": changed,
        "source_evidence": ["workbench/body_chapters/paddle_上/第一卷_自然环境.md:5924-5948"],
        "notes": ["仅拆最终 HTML 标题和段首小类边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷矿产资源标题版式修复

- 时间：{now}
- 范围：第一卷自然环境，第四节矿产资源。
- 本次拆分边界：{changed} 处。

## 修复

- 将 `第四节矿产资源`、`一、金属矿`、`二、非金属矿` 从段首粘连中恢复为独立标题。
- 将 `黑色金属`、`有色金属`、`贵金属`、`稀土金属`、`磷` 恢复为段首小类标识。
- 仅恢复版式边界，不改正文文字。

## 依据

- `workbench/body_chapters/paddle_上/第一卷_自然环境.md:5924-5948`
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第一卷矿产资源标题版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第一卷自然环境 `第四节矿产资源` 在最终阅读版中节标题、矿类标题和段首小类名粘正文的问题。
- 按 PaddleOCR 源文边界恢复 `一、金属矿`、`二、非金属矿` 及 `黑色金属`、`有色金属`、`贵金属`、`稀土金属`、`磷` 的版式边界。
- 仅恢复版式边界，不改正文文字。
- 报告：`output/reports/reader_readability_mineral_resource_headings_20260705.md`。
""",
    )
    print(f"html_boundaries_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

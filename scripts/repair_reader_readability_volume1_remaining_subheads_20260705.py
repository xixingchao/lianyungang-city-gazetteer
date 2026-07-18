# -*- coding: utf-8 -*-
"""Repair a small source-backed batch of remaining volume 1 subheadings."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume1_remaining_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume1_remaining_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷残留小标题边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>二、墟沟南山又称南固山": "<h5>二、墟沟南山</h5>\n<p>又称南固山",
    "<p>六、北崮山北崮山为北云台山": "<h5>六、北崮山</h5>\n<p>北崮山为北云台山",
    "<p>三、气压连云港市气压变化特点": "<h5>三、气压</h5>\n<p>连云港市气压变化特点",
    "<p>六、风连云港市由于海陆的共同作用": "<h5>六、风</h5>\n<p>连云港市由于海陆的共同作用",
    "<p>二、冻土连云港市土壤冻结的平均初日": "<h5>二、冻土</h5>\n<p>连云港市土壤冻结的平均初日",
    "<p>三、地热水和矿泉水地热水 东海县温泉镇热矿泉": "<h5>三、地热水和矿泉水</h5>\n<p>地热水 东海县温泉镇热矿泉",
}

SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:848-850",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:872-874",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1367-1369",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1899-1901",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:2372-2374",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:6069-6071",
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
        "scope": "第一卷自然环境：残留目级小标题边界",
        "html_boundaries_fixed": changed,
        "source_evidence": SOURCE_LINES,
        "notes": ["仅按 PaddleOCR 源文独立行恢复标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷残留小标题边界修复

- 时间：{now}
- 范围：第一卷自然环境，山体、气候、水文地质等残留目级小标题。
- 本次修复边界：{changed} 处。

## 修复

- 恢复 `二、墟沟南山`、`六、北崮山` 两处山体条目标题。
- 恢复 `三、气压`、`六、风`、`二、冻土` 三处气候/水文小标题。
- 恢复 `三、地热水和矿泉水` 小标题。
- 仅恢复源文可证明的版式边界，不改正文文字。

## 依据

"""
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第一卷残留小标题边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第一卷自然环境 6 处残留小标题粘正文问题：`二、墟沟南山`、`六、北崮山`、`三、气压`、`六、风`、`二、冻土`、`三、地热水和矿泉水`。
- 依据 `workbench/body_chapters/paddle_上/第一卷_自然环境.md` 中独立行，只恢复标题边界，不改正文文字。
- 报告：`output/reports/reader_readability_volume1_remaining_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

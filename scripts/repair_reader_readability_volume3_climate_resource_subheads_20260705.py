# -*- coding: utf-8 -*-
"""Repair source-backed climate/resource subheadings in volume 3."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume3_climate_resource_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume3_climate_resource_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第三卷气候资源小标题边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>二、气候境内属暖温带季风性气候": "<h5>二、气候</h5>\n<p>境内属暖温带季风性气候",
    "<p>三、资源境内水资源丰富，但时控分布不平衡": "<h5>三、资源</h5>\n<p>境内水资源丰富，但时控分布不平衡",
    "<p>二、气候云台地处暖温带和北亚热带过渡区域": "<h5>二、气候</h5>\n<p>云台地处暖温带和北亚热带过渡区域",
    "<p>三、资源境内水资源主要来自大气降水": "<h5>三、资源</h5>\n<p>境内水资源主要来自大气降水",
    "<p>三、气候地处暖温带的南缘": "<h5>三、气候</h5>\n<p>地处暖温带的南缘",
    "<p>四、资源境濒海州湾渔场": "<h5>四、资源</h5>\n<p>境濒海州湾渔场",
    "<p>二、气候赣榆县属暖温带季风气候": "<h5>二、气候</h5>\n<p>赣榆县属暖温带季风气候",
    "<p>三、资源境内有高等植物种类169科657属1062种": "<h5>三、资源</h5>\n<p>境内有高等植物种类169科657属1062种",
    "<p>二、气候县属北亚热带和暖温带过渡性气候": "<h5>二、气候</h5>\n<p>县属北亚热带和暖温带过渡性气候",
    "<p>三、资源境内26个乡（镇）蕴藏着丰富的矿产资源": "<h5>三、资源</h5>\n<p>境内26个乡（镇）蕴藏着丰富的矿产资源",
    "<p>二、气候灌云属暖温带海洋季风性气候": "<h5>二、气候</h5>\n<p>灌云属暖温带海洋季风性气候",
    "<p>三、资源境内地处冲积平原": "<h5>三、资源</h5>\n<p>境内地处冲积平原",
}

SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第三卷_区县概况.md:269-274",
    "workbench/body_chapters/paddle_上/第三卷_区县概况.md:466-472",
    "workbench/body_chapters/paddle_上/第三卷_区县概况.md:629-635",
    "workbench/body_chapters/paddle_上/第三卷_区县概况.md:809-815",
    "workbench/body_chapters/paddle_上/第三卷_区县概况.md:1150-1156",
    "workbench/body_chapters/paddle_上/第三卷_区县概况.md:1484-1489",
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
        "scope": "第三卷区县概况：各区县气候/资源小标题",
        "html_boundaries_fixed": changed,
        "source_evidence": SOURCE_LINES,
        "notes": ["仅按 PaddleOCR 源文独立行恢复小标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第三卷气候资源小标题边界修复

- 时间：{now}
- 范围：第三卷区县概况，各区县 `气候`、`资源` 小标题。
- 本次修复边界：{changed} 处。

## 修复

- 将海州区、云台区、连云区、赣榆县、东海县、灌云县等条目中的 `气候`、`资源` 小标题从段首粘连中恢复。
- 仅恢复源文可证明的版式边界，不改正文文字。

## 依据

"""
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第三卷气候资源小标题边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第三卷区县概况 12 处 `气候`、`资源` 小标题粘正文问题。
- 覆盖海州区、云台区、连云区、赣榆县、东海县、灌云县等同型结构。
- 仅按 PaddleOCR 源文独立行恢复版式边界，不改正文文字。
- 报告：`output/reports/reader_readability_volume3_climate_resource_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

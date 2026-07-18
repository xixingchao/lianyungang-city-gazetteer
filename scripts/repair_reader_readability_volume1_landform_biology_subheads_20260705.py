# -*- coding: utf-8 -*-
"""Split source-backed first-volume landform and biology subheads."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume1_landform_biology_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume1_landform_biology_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷地貌植被生物条目标题版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>一、低山丘陵连云港市境内低山丘陵地貌": "<h5>一、低山丘陵</h5>\n<p>连云港市境内低山丘陵地貌",
    "<p>二、岗地境内岗地面积": "<h5>二、岗地</h5>\n<p>境内岗地面积",
    "<p>三、平原境内地貌以平原为主": "<h5>三、平原</h5>\n<p>境内地貌以平原为主",
    "<p>一、花果山花果山是南云台山": "<h5>一、花果山</h5>\n<p>花果山是南云台山",
    "<p>二、巨平山位于花果山玉女峰之右": "<h5>二、巨平山</h5>\n<p>位于花果山玉女峰之右",
    "<p>三、九层顶位于花果山玉女峰西侧": "<h5>三、九层顶</h5>\n<p>位于花果山玉女峰西侧",
    "<p>二、针阔混交林在北云台山南坡": "<h5>二、针阔混交林</h5>\n<p>在北云台山南坡",
    "<p>三、栽培植被境内农垦历史久远": "<h5>三、栽培植被</h5>\n<p>境内农垦历史久远",
    "<p>四、天然植被境内天然植被除云台山": "<h5>四、天然植被</h5>\n<p>境内天然植被除云台山",
    "<p>二、野生动物境内野生动物种类繁多": "<h5>二、野生动物</h5>\n<p>境内野生动物种类繁多",
}

SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:513",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:541",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:553",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:673",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:689",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:695",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5402",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5415",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5422",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5684",
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
    for residue in REPLACEMENTS:
        if residue in text:
            raise RuntimeError(f"residue remains: {residue}")
    HTML.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第一卷自然环境：地貌、南云台山、植被、野生动物条目标题",
        "html_boundaries_split": changed,
        "source_evidence": SOURCE_LINES,
        "notes": ["仅拆最终 HTML 条目标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷地貌植被生物条目标题版式修复

- 时间：{now}
- 范围：第一卷自然环境，地貌、南云台山、植被、野生动物相关条目标题。
- 本次拆分边界：{changed} 处。

## 修复

- 将 `一、低山丘陵`、`二、岗地`、`三、平原` 从段首粘连中恢复为独立条目标题。
- 将南云台山下 `一、花果山`、`二、巨平山`、`三、九层顶` 恢复为独立条目标题。
- 将植被和野生生物资源中的 `二、针阔混交林`、`三、栽培植被`、`四、天然植被`、`二、野生动物` 恢复为独立条目标题。
- 仅恢复版式边界，不改正文文字。

## 依据

"""
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第一卷地貌植被生物条目标题版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第一卷自然环境 10 处地貌、南云台山、植被、野生动物条目标题粘正文问题。
- 仅按 PaddleOCR 源文独立行恢复版式边界，不改正文文字。
- 报告：`output/reports/reader_readability_volume1_landform_biology_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Repair source-backed military section/subheading boundaries in volume 45."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume45_military_section_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume45_military_section_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四十五卷军事节标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"

REPAIRS = [
    {
        "old": "<p>第三节战‧勤一、支前参战抗日战争时期，民国28年（1939年）3月",
        "new": '<h4 id="第四十五卷-第四章民兵-第三节战勤">第三节战勤</h4>\n<h5>一、支前参战</h5>\n<p>抗日战争时期，民国28年（1939年）3月',
        "remove": '<h4 id="第四十五卷-第四章民兵-第三节战勤">第三节战勤</h4>\n',
        "heading": "第三节战勤 / 一、支前参战",
        "source": f"{SOURCE}:9768-9769",
    },
    {
        "old": "<p>第二节纟组织指挥一、防空袭预案1956年6月开始至年底",
        "new": '<h4 id="第四十五卷-第五章人民防空-第二节组织指挥">第二节组织指挥</h4>\n<h5>一、防空袭预案</h5>\n<p>1956年6月开始至年底',
        "remove": '<h4 id="第四十五卷-第五章人民防空-第二节组织指挥">第二节组织指挥</h4>\n',
        "heading": "第二节组织指挥 / 一、防空袭预案",
        "source": f"{SOURCE}:9906-9907",
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> list[dict[str, str]]:
    text = HTML.read_text(encoding="utf-8")
    fixed = []
    for item in REPAIRS:
        old_count = text.count(item["old"])
        if old_count != 1:
            raise RuntimeError(f"expected one old match for {item['heading']}, got {old_count}")
        remove_count = text.count(item["remove"])
        if remove_count != 1:
            raise RuntimeError(f"expected one duplicate heading for {item['heading']}, got {remove_count}")
        text = text.replace(item["old"], item["new"], 1)
        text = text.replace(item["remove"], "", 1)
        fixed.append({"heading": item["heading"], "source": item["source"]})
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十五卷军事：民兵战勤、人民防空组织指挥节标题边界",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": ["移动已存在节标题到正确位置，删除后置重复节标题；不改正文内容。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四十五卷军事节标题边界补修

- 时间：{now}
- 范围：第四十五卷军事，第四章民兵、第五章人民防空。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['heading']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 仅恢复源文可证明的节标题和子目标题位置，删除后置重复节标题，不改正文内容。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四十五卷军事节标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四十五卷军事 2 处节标题/子目标题粘正文问题：`第三节战勤 / 一、支前参战`、`第二节组织指挥 / 一、防空袭预案`。
- 依据 `{SOURCE}` 源文独立标题行，移动既有节标题到正确位置并删除后置重复标题，不改正文内容。
- 报告：`output/reports/reader_readability_volume45_military_section_boundaries_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

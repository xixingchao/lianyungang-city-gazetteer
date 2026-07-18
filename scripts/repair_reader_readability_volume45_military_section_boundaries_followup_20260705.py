# -*- coding: utf-8 -*-
"""Fix ordering left by the volume 45 military heading repair."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume45_military_section_boundaries_followup_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume45_military_section_boundaries_followup_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四十五卷军事节标题顺序补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"

FIXES = [
    {
        "h4": '<h4 id="第四十五卷-第四章民兵-第三节战勤">第三节战勤</h4>\n',
        "h5": "<h5>一、支前参战</h5>\n",
        "heading": "第三节战勤 / 一、支前参战",
        "source": f"{SOURCE}:9768-9769",
    },
    {
        "h4": '<h4 id="第四十五卷-第五章人民防空-第二节组织指挥">第二节组织指挥</h4>\n',
        "h5": "<h5>一、防空袭预案</h5>\n",
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
    fixed: list[dict[str, str]] = []
    for item in FIXES:
        h4 = item["h4"]
        h5 = item["h5"]
        if text.count(h4) != 1 or text.count(h5) != 1:
            raise RuntimeError(f"expected one h4/h5 match for {item['heading']}")
        h4_pos = text.index(h4)
        h5_pos = text.index(h5)
        if h4_pos < h5_pos:
            continue
        text = text[:h4_pos] + text[h4_pos + len(h4):]
        h5_pos = text.index(h5)
        text = text[:h5_pos] + h4 + text[h5_pos:]
        fixed.append({"heading": item["heading"], "source": item["source"]})
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十五卷军事：修正两处节标题与子目标题顺序",
        "html_order_fixed": len(fixed),
        "fixed": fixed,
        "notes": ["只移动既有 h4 标题到对应 h5 前，不改正文。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四十五卷军事节标题顺序补修

- 时间：{now}
- 范围：第四十五卷军事，第四章民兵、第五章人民防空。
- 本次修正标题顺序：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['heading']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 仅修正上一轮补修遗留的 h4/h5 顺序，不改正文内容。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四十五卷军事节标题顺序补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修正第四十五卷军事 2 处上一轮补修遗留的标题顺序：`第三节战勤 / 一、支前参战`、`第二节组织指挥 / 一、防空袭预案`。
- 仅移动既有 h4 到对应 h5 前，不改正文；依据 `{SOURCE}` 源文独立标题行。
- 报告：`output/reports/reader_readability_volume45_military_section_boundaries_followup_20260705.md`。
""",
    )
    print(f"html_order_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

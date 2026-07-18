# -*- coding: utf-8 -*-
"""Repair source-backed mosque subhead boundaries in volume 57."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume57_mosque_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume57_mosque_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第五十七卷清真寺标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md"

REPAIRS = [
    {
        "old": "<p>一、连云港市清真寺坐落在新浦解放西路，1985年10月兴建，",
        "new": "<h5>一、连云港市清真寺</h5>\n<p>坐落在新浦解放西路，1985年10月兴建，",
        "heading": "一、连云港市清真寺",
        "source": f"{SOURCE}:12029",
    },
    {
        "old": "<p>二、东海县桃林清真寺1956年，有3间房屋作为穆斯林活动场所。",
        "new": "<h5>二、东海县桃林清真寺</h5>\n<p>1956年，有3间房屋作为穆斯林活动场所。",
        "heading": "二、东海县桃林清真寺",
        "source": f"{SOURCE}:12034",
    },
    {
        "old": "<p>三、灌云县四队镇二队村清真寺清光绪十二年（1886年），为许氏穆斯林所建，",
        "new": "<h5>三、灌云县四队镇二队村清真寺</h5>\n<p>清光绪十二年（1886年），为许氏穆斯林所建，",
        "heading": "三、灌云县四队镇二队村清真寺",
        "source": f"{SOURCE}:12037",
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> list[dict[str, str]]:
    text = HTML.read_text(encoding="utf-8")
    fixed: list[dict[str, str]] = []
    for item in REPAIRS:
        count = text.count(item["old"])
        if count == 0 and item["new"] in text:
            continue
        if count != 1:
            raise RuntimeError(f"expected one match for {item['heading']}, got {count}")
        text = text.replace(item["old"], item["new"], 1)
        fixed.append({"heading": item["heading"], "source": item["source"]})
    for item in REPAIRS:
        marker = f"<h5>{item['heading']}</h5>"
        if text.count(marker) != 1:
            raise RuntimeError(f"expected one marker after repair: {marker}")
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十七卷宗教：第三章伊斯兰教第二节清真寺",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": ["依据源 MD 独立标题行拆出 h5；不改正文数字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十七卷清真寺标题边界补修

- 时间：{now}
- 范围：第五十七卷宗教，第三章伊斯兰教第二节清真寺。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['heading']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 拆出源文独立编号子目标题，恢复为 h5。\n- 不重写清真寺正文，不猜改 OCR 数字。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第五十七卷清真寺标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第五十七卷宗教第三章伊斯兰教第二节清真寺 3 处编号子目标题边界：`一、连云港市清真寺`、`二、东海县桃林清真寺`、`三、灌云县四队镇二队村清真寺`。
- 依据 `{SOURCE}:12029-12037` 源文独立标题行；仅拆出 h5，不改正文数字。
- 报告：`output/reports/reader_readability_volume57_mosque_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Repair source-backed militia and air-defense subhead boundaries in volume 45."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume45_military_militia_airdefense_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume45_military_militia_airdefense_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四十五卷军事民兵人防标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"

REPAIRS = [
    {
        "old": "<p>二、治安执勤解放初期，民兵配合中国人民解放军开展剿匪反特斗争。",
        "new": "<h5>二、治安执勤</h5>\n<p>解放初期，民兵配合中国人民解放军开展剿匪反特斗争。",
        "heading": "二、治安执勤",
        "source": f"{SOURCE}:9812",
    },
    {
        "old": "<p>三、参加社会主义建设社会主义建设时期，全市民兵继续保持和发扬战争年代的光荣传统，",
        "new": "<h5>三、参加社会主义建设</h5>\n<p>社会主义建设时期，全市民兵继续保持和发扬战争年代的光荣传统，",
        "heading": "三、参加社会主义建设",
        "source": f"{SOURCE}:9837",
    },
    {
        "old": "<p>二、防空专业队伍1953年4月，江苏省按照网式、群众性的要求，建立防空监视哨。",
        "new": "<h5>二、防空专业队伍</h5>\n<p>1953年4月，江苏省按照网式、群众性的要求，建立防空监视哨。",
        "heading": "二、防空专业队伍",
        "source": f"{SOURCE}:9930",
    },
    {
        "old": "<p>：三、防空演练防空训练1953年5月，华东军区司令部要求各地开展对空监视哨的训练工作，",
        "new": "<h5>三、防空演练</h5>\n<p>防空训练1953年5月，华东军区司令部要求各地开展对空监视哨的训练工作，",
        "heading": "三、防空演练",
        "source": f"{SOURCE}:9967-9968",
    },
]

CHECKS = [
    "<h5>一、支前参战</h5>",
    "<h5>二、治安执勤</h5>",
    "<h5>三、参加社会主义建设</h5>",
    "<h5>一、防空袭预案</h5>",
    "<h5>二、防空专业队伍</h5>",
    "<h5>三、防空演练</h5>",
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
    for marker in CHECKS:
        if text.count(marker) != 1:
            raise RuntimeError(f"expected one marker after repair: {marker}")
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十五卷军事：第四章民兵第三节、第五章人民防空第二节",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": ["依据源 MD 独立标题行拆出 h5；不改正文数字；防空训练/防空演习保留为段首文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四十五卷军事民兵人防标题边界补修

- 时间：{now}
- 范围：第四十五卷军事，第四章民兵第三节、第五章人民防空第二节。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['heading']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 拆出源文独立编号子目标题，恢复为 h5。\n- `防空训练`、`防空演习` 源文未带编号，本轮保留为段首文字。\n- 不重写民兵战勤、人防训练正文，不猜改 OCR 数字。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四十五卷军事民兵人防标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四十五卷军事 4 处编号子目标题边界：`二、治安执勤`、`三、参加社会主义建设`、`二、防空专业队伍`、`三、防空演练`。
- 依据 `{SOURCE}:9812`、`:9837`、`:9930`、`:9967-9968` 源文独立标题行；仅拆出 h5，不改正文数字。
- `防空训练`、`防空演习` 源文未带编号，本轮保留为段首文字。
- 报告：`output/reports/reader_readability_volume45_military_militia_airdefense_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

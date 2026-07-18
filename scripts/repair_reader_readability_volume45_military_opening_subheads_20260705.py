# -*- coding: utf-8 -*-
"""Repair source-backed volume 45 military opening subhead boundaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume45_military_opening_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume45_military_opening_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四十五卷军事开篇标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"

REPAIRS = [
    {
        "label": "一、民国前起义、起事",
        "source": f"{SOURCE}:8689",
        "old": "<p>一、民国前起义、起事徐宣、谢禄、杨音、逢安起义新天凤五年（18年），",
        "new": "<h5>一、民国前起义、起事</h5>\n<p>徐宣、谢禄、杨音、逢安起义新天凤五年（18年），",
    },
    {
        "label": "二、民国时期起义暴动",
        "source": f"{SOURCE}:8765",
        "old": "<p>二、民国时期起义暴动吴山起义民国元年（1912年）2月8日，",
        "new": "<h5>二、民国时期起义暴动</h5>\n<p>吴山起义民国元年（1912年）2月8日，",
    },
    {
        "label": "二、海州光复与北伐军攻占海州",
        "source": f"{SOURCE}:8903",
        "old": "<p>二、海州光复与北伐军攻占海州海州光复清宣统三年（1911年），",
        "new": "<h5>二、海州光复与北伐军攻占海州</h5>\n<p>海州光复清宣统三年（1911年），",
    },
    {
        "label": "三、抗日战争战事",
        "source": f"{SOURCE}:8966",
        "old": "<p>三、抗日战争战事连云港保卫战台儿庄战役之后，",
        "new": "<h5>三、抗日战争战事</h5>\n<p>连云港保卫战台儿庄战役之后，",
    },
    {
        "label": "四、解放战争战事",
        "source": f"{SOURCE}:9038",
        "old": "<p>四、解放战争战事在台儿庄前线宣布起义。",
        "new": "<h5>四、解放战争战事</h5>\n<p>在台儿庄前线宣布起义。",
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
        if count != 1:
            raise RuntimeError(f"expected one match for {item['label']}, got {count}")
        text = text.replace(item["old"], item["new"], 1)
        fixed.append({"label": item["label"], "source": item["source"]})
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十五卷军事开篇：起义起事、战事小标题边界",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": ["仅拆分源文独立行可证明的小标题。", "不改概述断句和无源证据正文。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四十五卷军事开篇标题边界补修

- 时间：{now}
- 范围：第四十五卷军事开篇。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['label']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 拆出第一章内起义起事、战事相关小标题。\n- 不重建表格，不改缺少源证的 OCR 正文。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四十五卷军事开篇标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四十五卷军事开篇 5 处小标题边界，覆盖 `一、民国前起义、起事`、`二、民国时期起义暴动`、`二、海州光复与北伐军攻占海州`、`三、抗日战争战事`、`四、解放战争战事`。
- 不处理概述末尾疑似断句，不改缺少源证的 OCR 正文。
- 报告：`output/reports/reader_readability_volume45_military_opening_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

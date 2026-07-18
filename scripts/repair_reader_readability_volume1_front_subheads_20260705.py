# -*- coding: utf-8 -*-
"""Split source-backed first-volume front subsection headings in final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume1_front_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume1_front_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷前段条目标题版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>二、地层市境所处地层属": "<h5>二、地层</h5>\n<p>市境所处地层属",
    "<p>三、构造市境所处大地构造位置": "<h5>三、构造</h5>\n<p>市境所处大地构造位置",
    "<p>二、海岸类型砂质后退型海岸": "<h5>二、海岸类型</h5>\n<p>砂质后退型海岸",
    "<p>三、海岸变迁连云港市海岸经历": "<h5>三、海岸变迁</h5>\n<p>连云港市海岸经历",
    "<p>四、滩涂市境北自绣针河口": "<h5>四、滩涂</h5>\n<p>市境北自绣针河口",
    "<p>二、波浪连云港波浪观测始于": "<h5>二、波浪</h5>\n<p>连云港波浪观测始于",
    "<p>二、夏季连云港市夏季起讫时间": "<h5>二、夏季</h5>\n<p>连云港市夏季起讫时间",
    "<p>三、秋季连云港市秋季起讫时间": "<h5>三、秋季</h5>\n<p>连云港市秋季起讫时间",
    "<p>四、冬季连云港市冬季起讫时间": "<h5>四、冬季</h5>\n<p>连云港市冬季起讫时间",
    "<p>二、日照连云港市年平均日照时数": "<h5>二、日照</h5>\n<p>连云港市年平均日照时数",
    "<p>二、利用据1990年统计资料": "<h5>二、利用</h5>\n<p>据1990年统计资料",
    "<p>三、保护建国后，随着经济建设": "<h5>三、保护</h5>\n<p>建国后，随着经济建设",
    "<p>二、过境水市域过境水主要包括": "<h5>二、过境水</h5>\n<p>市域过境水主要包括",
    "<p>三、调引江淮沭水以及回归水连云港市": "<h5>三、调引江淮沭水以及回归水</h5>\n<p>连云港市",
    "<p>四、地下水市境地下水分为": "<h5>四、地下水</h5>\n<p>市境地下水分为",
}

SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:96",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:420",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:904",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:963",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:993",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1251",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1278",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1285",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1290",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1330",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5456",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5467",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5494",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5500",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5505",
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
        "scope": "第一卷自然环境前段：已核源文的后续条目标题",
        "html_boundaries_split": changed,
        "source_evidence": SOURCE_LINES,
        "notes": ["仅拆最终 HTML 条目标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷前段条目标题版式修复

- 时间：{now}
- 范围：第一卷自然环境前段，地质、海岸、潮汐波浪、气候、土地资源、水资源后续条目标题。
- 本次拆分边界：{changed} 处。

## 修复

- 将 `二、地层`、`三、构造`、`二、海岸类型`、`三、海岸变迁`、`四、滩涂`、`二、波浪` 等条目标题从段首粘连中恢复。
- 将四季和气候要素中的 `二、夏季`、`三、秋季`、`四、冬季`、`二、日照` 恢复为独立条目标题。
- 将土地资源、水资源中的 `二、利用`、`三、保护`、`二、过境水`、`三、调引江淮沭水以及回归水`、`四、地下水` 恢复为独立条目标题。
- 仅恢复版式边界，不改正文文字。

## 依据

"""
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第一卷前段条目标题版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第一卷自然环境前段 15 处后续条目标题粘正文问题。
- 覆盖地质、海岸、潮汐波浪、气候、土地资源、水资源内部条目标题。
- 仅按 PaddleOCR 源文独立行恢复版式边界，不改正文文字。
- 报告：`output/reports/reader_readability_volume1_front_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

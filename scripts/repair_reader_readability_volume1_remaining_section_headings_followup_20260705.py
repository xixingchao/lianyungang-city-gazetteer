# -*- coding: utf-8 -*-
"""Repair source-backed remaining section heading boundaries in volume 1."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume1_remaining_section_headings_followup_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume1_remaining_section_headings_followup_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷残留节标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>第二节地市境位于鲁中南丘陵和淮北平原结合部": "<h4>第二节 地貌</h4>\n<p>市境位于鲁中南丘陵和淮北平原结合部",
    "<p>第一节锦屏山锦屏山古称朐山": "<h4>第一节锦屏山</h4>\n<p>锦屏山古称朐山",
    "<p>第二节南云台山南云台山是云台山最大的一条山脉": "<h4>第二节南云台山</h4>\n<p>南云台山是云台山最大的一条山脉",
    "<p>第五节鹰游山鹰游山亦称东西连岛，详见《海域》章。</p>": "<h4>第五节鹰游山</h4>\n<p>鹰游山亦称东西连岛，详见《海域》章。</p>",
    "<p>第一节 水涝连云港市地处沂、沭河尾间。": "<h4>第一节 水涝</h4>\n<p>连云港市地处沂、沭河尾间。",
    "<p>第二节干旱建国前，境内旱灾与水灾交替发生": "<h4>第二节 干旱</h4>\n<p>建国前，境内旱灾与水灾交替发生",
    "<p>第四节 风暴潮 海啸历史上境内风暴潮、海啸灾害主要有：</p>": "<h4>第四节 风暴潮 海啸</h4>\n<p>历史上境内风暴潮、海啸灾害主要有：</p>",
    "<p>第五节 霜 冻市境3月份极端最低气温低于-7℃": "<h4>第五节 霜冻</h4>\n<p>市境3月份极端最低气温低于-7℃",
    "<p>第六节 冰雹市境春夏之交和夏末秋初，易发生雹灾。": "<h4>第六节 冰雹</h4>\n<p>市境春夏之交和夏末秋初，易发生雹灾。",
    "<p>第七节 虫害建国前，市境蝗虫肆虐，危害甚烈，史籍多有记载。</p>": "<h4>第七节 虫害</h4>\n<p>建国前，市境蝗虫肆虐，危害甚烈，史籍多有记载。</p>",
}

TABLE_RESIDUE = "<p>每年平均伸展宽度（米）</p>\n<p>绣针河口一柘汪2200～2600约50～60海头一兴庄河口约32青口北侧一临洪河口北侧2200～3200约50～75临洪河口南侧—西墅2200～2800约50～65第二节 岛连云港市沿海有大小岛屿9座，即：东西连岛、秦山岛、平山岛、达山岛、车牛山岛、竹岛、开山岛、羊山岛、鸽岛。</p>"
TABLE_REPLACEMENT = "<h4>第二节 岛礁</h4>\n<p>连云港市沿海有大小岛屿9座，即：东西连岛、秦山岛、平山岛、达山岛、车牛山岛、竹岛、开山岛、羊山岛、鸽岛。</p>"

SOURCE_LINES = [
    "workbench/indexes/连云港市志_全书_章节骨架.md:37",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:508-512",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:595-598",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:670-672",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:881",
    "workbench/indexes/连云港市志_全书_章节骨架.md:46",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1018-1021",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:6123-6127",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:6149-6151",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:6164-6166",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:6195-6197",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:6205-6208",
    "workbench/indexes/连云港市志_全书_章节骨架.md:64-70",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> tuple[int, int]:
    text = HTML.read_text(encoding="utf-8")
    changed = 0
    for old, new in REPLACEMENTS.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected one match for {old!r}, got {count}")
        text = text.replace(old, new, 1)
        changed += 1

    residue_count = text.count(TABLE_RESIDUE)
    if residue_count != 1:
        raise RuntimeError(f"expected one table residue match, got {residue_count}")
    text = text.replace(TABLE_RESIDUE, TABLE_REPLACEMENT, 1)

    for old in REPLACEMENTS:
        if old in text:
            raise RuntimeError(f"residue remains: {old}")
    if TABLE_RESIDUE in text:
        raise RuntimeError("table residue remains")

    HTML.write_text(text, encoding="utf-8")
    return changed, residue_count


def main() -> None:
    changed, removed_residue = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第一卷自然环境残留节标题边界",
        "section_boundaries_fixed": changed,
        "linearized_table_residue_removed": removed_residue,
        "source_evidence": SOURCE_LINES,
        "notes": [
            "按目录骨架补足 OCR 丢字标题：第二节 地貌、第二节 岛礁。",
            "表1-3已有结构化表，删除岛礁标题前重复线性表格残留。",
            "仅恢复标题边界和移除重复表格残留，不改正文事实。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷残留节标题边界补修

- 时间：{now}
- 范围：第一卷自然环境，地貌、云台山、海域岛礁、自然灾害残留节标题。
- 本次恢复节标题边界：{changed} 处。
- 移除重复线性表格残留：{removed_residue} 处。

## 修复

- 恢复 `第二节 地貌`、`第一节锦屏山`、`第二节南云台山`、`第五节鹰游山` 为独立节标题。
- 将表1-3后残留的线性表格文本移除，并按目录恢复 `第二节 岛礁`。
- 恢复自然灾害章 `第一节 水涝`、`第二节 干旱`、`第四节 风暴潮 海啸`、`第五节 霜冻`、`第六节 冰雹`、`第七节 虫害`。
- 不处理正常数字密集正文，不为降低风险数而拆自然段。

## 依据

"""
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第一卷残留节标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第一卷自然环境 10 处残留节标题粘正文问题，覆盖地貌、云台山、海域岛礁、自然灾害章。
- 依据目录骨架确认 `第二节 地貌`、`第二节 岛礁`，并移除表1-3之后重复的线性表格残留 1 处；结构化表本体保留。
- 仅恢复标题边界和删除重复表格残留，不改正文事实，不拆正常数字密集自然段。
- 报告：`output/reports/reader_readability_volume1_remaining_section_headings_followup_20260705.md`。
""",
    )
    print(f"section_boundaries_fixed={changed}")
    print(f"linearized_table_residue_removed={removed_residue}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

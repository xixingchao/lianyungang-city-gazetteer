# -*- coding: utf-8 -*-
"""Repair source-backed remaining embedded section heading residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_remaining_embedded_section_headings_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_remaining_embedded_section_headings_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_残留嵌入节标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REMOVE_RESIDUES = [
    ("<p>第三节印</p>\n", "第十五卷第二章 `第三节印染` 前重复残段"),
    ("<p>第二节</p>\n", "第十七卷第二章 `第二节玩具` 前重复残段"),
    ("<p>主要企业简介第四节</p>\n", "第十七卷第二章 `第四节主要企业简介` 前倒序重复残段"),
    ("<p>第四节柳•编</p>\n", "第十七卷第三章 `第四节柳编` 前重复残段"),
]

REPLACEMENTS = [
    (
        "<p>第二节内联企业优惠待遇根据《连云港市人民政府关于连云港经济技术开发区内联企业优惠待遇的暂行规定》，对国内企、事业单位到开发区联合或独立兴办、经营的企业（即内联企业）提供税收、费用和其他方面的优惠。</p>",
        "<p>根据《连云港市人民政府关于连云港经济技术开发区内联企业优惠待遇的暂行规定》，对国内企、事业单位到开发区联合或独立兴办、经营的企业（即内联企业）提供税收、费用和其他方面的优惠。</p>",
        "第二十八卷第三章已存在 `第二节内联企业优惠待遇` h4，清除段首重复标题词",
    ),
    (
        "<p>云台区人民政府第三节民国37年（1948年）12月，新海连特区专员公署云台办事处在新县建立。1949年8月，云台办事处与其所属的区公所奉命撤销。</p>",
        "<h4 id=\"第四十二卷-第七章区、县人民政府-第三节云台区人民政府\">第三节云台区人民政府</h4>\n<p>民国37年（1948年）12月，新海连特区专员公署云台办事处在新县建立。1949年8月，云台办事处与其所属的区公所奉命撤销。</p>",
        "第四十二卷第七章 `第三节云台区人民政府` 标题前移",
    ),
    (
        "<h4 id=\"第四十二卷-第七章区、县人民政府-第三节云台区人民政府\">第三节云台区人民政府</h4>\n<p>1983年4月，成立南城区筹备组。1983年7月，组建云台区人民政府。</p>",
        "<p>1983年4月，成立南城区筹备组。1983年7月，组建云台区人民政府。</p>",
        "删除第四十二卷第七章后置重复 `第三节云台区人民政府` h4",
    ),
    (
        "<p>第五节章赣榆县人民政府1949年10月，县政权仍称竹庭县政府，设1名县长（1952年1月始增设副县长）。</p>",
        "<h4 id=\"第四十二卷-第七章区、县人民政府-第五节赣榆县人民政府\">第五节赣榆县人民政府</h4>\n<p>1949年10月，县政权仍称竹庭县政府，设1名县长（1952年1月始增设副县长）。</p>",
        "第四十二卷第七章 `第五节赣榆县人民政府` 标题前移并去除 OCR 残字 `章`",
    ),
    (
        "<h4 id=\"第四十二卷-第七章区、县人民政府-第五节赣榆县人民政府\">第五节赣榆县人民政府</h4>\n<p>1952～1990年，每逢突击性工作，县政府多成立临时性机构专门负责，任务完成后自行撤销。</p>",
        "<p>1952～1990年，每逢突击性工作，县政府多成立临时性机构专门负责，任务完成后自行撤销。</p>",
        "删除第四十二卷第七章后置重复 `第五节赣榆县人民政府` h4",
    ),
]

SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:13387",
    "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:1123",
    "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:24005",
    "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:32398-32400",
    "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:32461-32463",
    "workbench/indexes/连云港市志_全书_章节骨架.md:1069-1071",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> tuple[list[str], list[str]]:
    text = HTML.read_text(encoding="utf-8")
    removed = []
    fixed = []

    for residue, label in REMOVE_RESIDUES:
        count = text.count(residue)
        if count != 1:
            raise RuntimeError(f"expected one residue for {label}, got {count}")
        text = text.replace(residue, "", 1)
        removed.append(label)

    for old, new, label in REPLACEMENTS:
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected one match for {label}, got {count}")
        text = text.replace(old, new, 1)
        fixed.append(label)

    HTML.write_text(text, encoding="utf-8")
    return removed, fixed


def main() -> None:
    removed, fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "残留嵌入节标题和重复标题残段",
        "residue_paragraphs_removed": len(removed),
        "boundaries_or_order_fixed": len(fixed),
        "removed": removed,
        "fixed": fixed,
        "source_evidence": SOURCE_LINES,
        "notes": ["仅处理源文和既有 h4 可证明的残留项；不改正文事实。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 残留嵌入节标题边界补修

- 时间：{now}
- 范围：第十五卷、第十七卷、第二十八卷、第四十二卷中可证实的残留嵌入节标题。
- 删除重复标题残段：{len(removed)} 处。
- 修复标题边界/顺序：{len(fixed)} 处。

## 删除残段

"""
    md += "".join(f"- {item}\n" for item in removed)
    md += "\n## 修复\n\n"
    md += "".join(f"- {item}\n" for item in fixed)
    md += "\n## 依据\n\n"
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 残留嵌入节标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 删除第十五卷、第十七卷中 4 处重复标题残段：`第三节印`、`第二节`、`主要企业简介第四节`、`第四节柳•编`。
- 清理第二十八卷第三章 `第二节内联企业优惠待遇` 段首重复标题词，保留既有 h4。
- 前移第四十二卷第七章 `第三节云台区人民政府`、`第五节赣榆县人民政府` 标题，并删除后置重复 h4。
- 报告：`output/reports/reader_readability_remaining_embedded_section_headings_20260705.md`。
""",
    )
    print(f"residue_paragraphs_removed={len(removed)}")
    print(f"boundaries_or_order_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

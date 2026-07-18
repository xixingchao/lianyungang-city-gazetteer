# -*- coding: utf-8 -*-
"""Split source-backed first-volume front section headings in final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume1_front_section_headings_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume1_front_section_headings_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷前段节标题版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>第一节 地一、地质演变": "<h4>第一节 地质</h4>\n<h5>一、地质演变</h5>\n<p>",
    "<p>第一节 海 岸一、岸线长度": "<h4>第一节 海岸</h4>\n<h5>一、岸线长度</h5>\n<p>",
    "<p>第三节潮汐波浪一、潮流": "<h4>第三节 潮汐波浪</h4>\n<h5>一、潮流</h5>\n<p>",
    "<p>第一节四季特征一、春季": "<h4>第一节 四季特征</h4>\n<h5>一、春季</h5>\n<p>",
    "<p>第二节气候要素一、太阳总辐射": "<h4>第二节 气候要素</h4>\n<h5>一、太阳总辐射</h5>\n<p>",
    "<p>第一节水系一、河流": "<h4>第一节 水系</h4>\n<h5>一、河流</h5>\n<p>",
    "<p>第一节 土壤一、棕壤类": "<h4>第一节 土壤</h4>\n<h5>一、棕壤类</h5>\n<p>",
    "<p>第二节植一、针叶林系": "<h4>第二节 植被</h4>\n<h5>一、针叶林系</h5>\n<p>",
    "<p>第一节土地资源一、特点": "<h4>第一节 土地资源</h4>\n<h5>一、特点</h5>\n<p>",
    "<p>第二节水资源一、当地径流": "<h4>第二节 水资源</h4>\n<h5>一、当地径流</h5>\n<p>",
    "<p>第三节野生生物资源一、野生植物": "<h4>第三节 野生生物资源</h4>\n<h5>一、野生植物</h5>\n<p>",
}

SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:76-77",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:930-931",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1190-1191",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1261-1262",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1297-1298",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:3848-3849",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5207-5208",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5399-5400",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5466-5467",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5492-5493",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5517-5518",
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
        "scope": "第一卷自然环境前段：地质、海、气候、水系、土壤、植被、自然资源节标题",
        "html_boundaries_split": changed,
        "source_evidence": SOURCE_LINES,
        "notes": ["仅拆最终 HTML 节标题和首个条目标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷前段节标题版式修复

- 时间：{now}
- 范围：第一卷自然环境前段，地质、海、气候、水系、土壤、植被、自然资源相关节标题。
- 本次拆分边界：{changed} 处。

## 修复

- 将 `第一节 地质`、`第一节 海岸`、`第三节 潮汐波浪`、`第一节 四季特征`、`第二节 气候要素` 等节标题从正文段首粘连中恢复为独立标题。
- 同步恢复各节首个条目标题，如 `一、地质演变`、`一、岸线长度`、`一、潮流`、`一、春季`、`一、太阳总辐射` 等。
- 仅恢复版式边界，不改正文文字；其它二级条目和表格残文另批回源处理。

## 依据

"""
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第一卷前段节标题版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第一卷自然环境前段 11 处节标题/首个条目标题在最终阅读版中粘正文的问题。
- 覆盖地质、海岸、潮汐波浪、四季特征、气候要素、水系、土壤、植被、土地资源、水资源、野生生物资源等入口。
- 仅按 PaddleOCR 源文独立行恢复版式边界，不改正文文字；其它二级条目和表格残文另批处理。
- 报告：`output/reports/reader_readability_volume1_front_section_headings_20260705.md`。
""",
    )
    print(f"html_boundaries_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

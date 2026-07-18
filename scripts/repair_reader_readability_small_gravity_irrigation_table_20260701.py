# -*- coding: utf-8 -*-
"""Add verified table 10-17 source rows and remove flattened irrigation residue."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T049.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_small_gravity_irrigation_table_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_small_gravity_irrigation_table_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第十卷小型自流灌区基本情况表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_PAGES = [34, 35, 36, 37, 38]
SOURCE_PATHS = [ROOT / "workbench" / "ocr" / "raw" / "上" / "part03" / f"page_{page:04d}.txt" for page in SOURCE_PAGES]
COLUMNS = ["源页", "页内范围", "源页可见文本序列", "说明"]

HEADER_TOKENS = {
    "续上表",
    "受益范围",
    "灌溉涵洞",
    "灌溉面积",
    "建成",
    "水库灌区",
    "断面尺寸",
    "设计",
    "实灌",
    "兴利库容",
    "兴利水位",
    "进口高程",
    "县区乡镇",
    "(高×宽)",
    "年份",
    "名称",
    "（万立方米）",
    "(万立方米）",
    "(米)",
    "(亩)",
    "水 ",
}


def table_text_for_page(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    body: list[str] = []
    started = False
    for line in lines:
        s = line.strip()
        if not s or s.startswith("#") or "连云港市志" in s or "第四章灌溉" in s:
            continue
        if "1990年连云港市小型自流灌区基本情况表" in s:
            started = True
            continue
        if s.startswith("表 10"):
            started = True
            continue
        if s == "续上表":
            started = True
            continue
        if "第二节" in s or "提水灌溉" in s:
            break
        if not started and path.name != "page_0034.txt":
            started = True
        if not started:
            continue
        if s in HEADER_TOKENS:
            continue
        body.append(s)
    return " ".join(body)


def build_rows() -> list[list[str]]:
    rows = []
    for page, path in zip(SOURCE_PAGES, SOURCE_PATHS):
        visible = table_text_for_page(path)
        rows.append([
            str(557 + page - 34),
            f"workbench/ocr/raw/上/part03/page_{page:04d}.txt",
            visible,
            "按源页 OCR 可见序列保留；此表横向错位严重，本轮不据版面残文强拆列位。",
        ])
    return rows


def build_entry(rows: list[list[str]]) -> dict:
    return {
        "table_id": "LYG-上-T049",
        "title": "1990年连云港市小型自流灌区基本情况表",
        "table_number": "表10-17",
        "page": 557,
        "pages": [557, 558, 559, 560, 561],
        "part": "part03",
        "vol": "上",
        "columns": COLUMNS,
        "rows": rows,
        "row_count": len(rows),
        "col_count": len(COLUMNS),
        "status": "verified",
        "notes": "已据 raw OCR 回源核录：workbench/ocr/raw/上/part03/page_0034.txt 至 page_0038.txt。表10-17位于第十卷第四章灌溉第一节小型灌区后、第二节提水灌溉前。源页为长跨页宽表，OCR横向错位明显，本条先按源页保留可见文本序列，避免将残文误拆为伪精确列。",
        "volume": "上",
    }


def render_table(entry: dict) -> str:
    thead = "".join(f"<th>{html.escape(col)}</th>" for col in COLUMNS)
    body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>"
        for row in entry["rows"]
    )
    return (
        '<section class="verified-table-block" id="table-LYG-上-T049"><div class="structured-table-meta">'
        '表ID：LYG-上-T049；源页：557-561</div>'
        '<table class="structured-table"><caption>表10-17 1990年连云港市小型自流灌区基本情况表</caption>'
        f"<thead><tr>{thead}</tr></thead><tbody>{body}</tbody></table></section>"
    )


def write_json(entry: dict) -> bool:
    old = DATA.read_text(encoding="utf-8") if DATA.exists() else ""
    new = json.dumps(entry, ensure_ascii=False, indent=2) + "\n"
    if old != new:
        DATA.write_text(new, encoding="utf-8")
        return True
    return False


def patch_site(entry: dict) -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise RuntimeError("TABLES payload not found")
    tables = json.loads(match.group(1))
    changed = False
    for idx, table in enumerate(tables):
        if table.get("table_id") == entry["table_id"]:
            if table != entry:
                tables[idx] = entry
                changed = True
            break
    else:
        tables.append(entry)
        changed = True
    if changed:
        tables.sort(
            key=lambda t: (
                str(t.get("vol") or t.get("volume") or ""),
                int((t.get("pages") or [t.get("page") or 999999])[0]),
                str(t.get("table_id") or ""),
            )
        )
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
        return 1
    return 0


RESIDUE_RE = re.compile(
    r"\n?<p>县区乡镇（万立方米）</p>\s*<p>（米）</p>\s*<p>（米）</p>\s*<p>（米）</p>\s*<p>（亩）</p>\s*<p>（米）</p>\s*<p>芦窝67\.560\.01\.0×0\.8.*?</p>\s*(?=<h4 id=\"第十卷-第四章灌溉-第二节提水灌溉\">)",
    re.S,
)


def patch_reader(entry: dict) -> int:
    text = HTML.read_text(encoding="utf-8")
    table = render_table(entry)
    if 'id="table-LYG-上-T049"' in text:
        new, count = RESIDUE_RE.subn("\n", text, count=1)
    else:
        new, count = RESIDUE_RE.subn("\n" + table + "\n", text, count=1)
    if count != 1 and 'id="table-LYG-上-T049"' not in text:
        raise RuntimeError(f"expected to replace 1 flattened irrigation block, replaced {count}")
    if new != text:
        HTML.write_text(new, encoding="utf-8")
    return count


def write_reports(entry: dict, json_changed: bool, site_changed: int, replaced: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    result = {
        "time": now,
        "table_id": entry["table_id"],
        "table_number": entry["table_number"],
        "title": entry["title"],
        "source_pages": entry["pages"],
        "json_changed": json_changed,
        "site_changed": site_changed,
        "reader_flattened_blocks_replaced": replaced,
        "rows": entry["row_count"],
        "columns": entry["col_count"],
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第十卷小型自流灌区基本情况表残文修复

- 时间：{now}
- 表ID：`LYG-上-T049`
- 表题：表10-17 `1990年连云港市小型自流灌区基本情况表`
- 源页：`workbench/ocr/raw/上/part03/page_0034.txt` 至 `workbench/ocr/raw/上/part03/page_0038.txt`

## 修复动作

- 新增 verified 回源核录表：`workbench/table_entries/上/data/LYG-上-T049.json`，按 5 个源页保留可见文本序列。
- 同步结构化表格站：`output/structured_tables/index.html`。
- 将最终阅读版中 `芦窝67.560.01.0×0.8...大庄3号41.336.20.8×0.8` 的压平残文替换为 verified 表块：{replaced} 组。

## 核对说明

- 表10-17位于第十卷第四章灌溉第一节小型灌区后、第二节提水灌溉前。
- 源表横跨 5 页，OCR 横向错位明显；本轮按源页可见序列保守核录，不把残文强拆为伪精确列。
- 后续如需精细拆列，应基于源页坐标或人工校读继续从 `LYG-上-T049` 细化。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(replaced: int) -> None:
    marker = "## 2026-07-01 第十卷小型自流灌区基本情况表残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第十卷水利 `芦窝67.560.01.0×0.8`、`77.00.5×0.7官庄前`、`石门沟82.878.30.5×0.5` 等摊平残文回源处理。
- 据 `workbench/ocr/raw/上/part03/page_0034.txt` 至 `page_0038.txt` 新增 `workbench/table_entries/上/data/LYG-上-T049.json`：表10-17《1990年连云港市小型自流灌区基本情况表》，按源页可见文本序列保守核录。
- 阅读版中表10-17压平残文已替换为 verified 表块 {replaced} 组；未将横向错位 OCR 强拆为伪精确列。
- 报告：`output/reports/reader_readability_small_gravity_irrigation_table_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    rows = build_rows()
    entry = build_entry(rows)
    json_changed = write_json(entry)
    site_changed = patch_site(entry)
    replaced = patch_reader(entry)
    write_reports(entry, json_changed, site_changed, replaced)
    update_memory(replaced)
    print(f"json_changed={int(json_changed)}")
    print(f"site_changed={site_changed}")
    print(f"reader_flattened_blocks_replaced={replaced}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

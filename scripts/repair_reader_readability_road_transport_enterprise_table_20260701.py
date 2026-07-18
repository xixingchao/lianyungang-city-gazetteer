# -*- coding: utf-8 -*-
"""Add table 30-9 head page and move continuation table to reader location."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T135.json"
CONT_DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T062.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_road_transport_enterprise_table_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_road_transport_enterprise_table_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第三十卷公路运输企业基本情况表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

COLUMNS = [
    "区域",
    "企业名称",
    "经济性质",
    "地址",
    "成立年份",
    "年末职工数(人)",
    "货车(辆/吨)",
    "挂车(辆/吨)",
    "半挂车(辆/吨)",
]

ROWS = [
    ["市内", "省汽车连云港分公司", "全民", "新浦通灌路34号", "1954", "2652", "80/733", "18/72", "59/590"],
    ["", "市港务管理处", "全民代集体", "海连中路49号", "1960", "508", "35/198", "2/10", "8/82"],
    ["", "市运输公司", "集体", "新浦海连路24号", "1949", "1240", "20/321", "7/32", "105/1050"],
    ["", "市第二运输公司", "集体", "猴嘴镇", "1949", "203", "7/35", "7/35", "30/292"],
    ["", "市第三运输公司", "集体", "板桥镇", "1953", "102", "5/25", "5/25", "11/108"],
    ["", "市第四运输公司", "集体", "墟沟镇", "1949", "171", "3/15", "3/15", "27/295"],
    ["", "市第五运输公司", "集体", "连云港镇", "1957", "150", "1/5", "1/5", "36/395"],
    ["", "市第六运输公司", "集体", "南城镇", "1949", "110", "4/20", "4/20", "11/110"],
    ["", "联运公司", "全民", "新浦区海连路9号", "1982", "120", "9/38", "", ""],
]

ENTRY = {
    "table_id": "LYG-中-T135",
    "title": "1990年连云港市公路运输企业基本情况表",
    "table_number": "表30-9",
    "page": 1456,
    "pages": [1456],
    "part": "part02",
    "vol": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0036.txt；并参考 raw OCR：workbench/ocr/raw/中/part02/page_0036.txt 和 page_0036.json。源页为表30-9首页；续页另见 LYG-中-T062。OCR 将市港务管理处经济性质、成立年份纵向拆行为“全民代/全民 1960/集体/集体 1949”，按版面与下一行关系核为市港务管理处“全民代集体、1960”，市运输公司“集体、1949”。联运公司挂车、半挂车栏源页未见数值，保留空值。",
    "volume": "中",
}

TABLE_RE_T062 = re.compile(
    r"\n?<section class=\"verified-table-block\" id=\"table-LYG-中-T062\">.*?</section>\s*",
    re.S,
)

RESIDUE_RE = re.compile(
    r"\n?<p>（辆/吨）</p>\s*"
    r"<p>\(辆/吨\)省汽车连云港分全民新浦通灌路34号1954265218/7280/73359/590公司.*?12085/6·1339</p>\s*",
    re.S,
)

NOTE = "注：赣榆、东海、灌云三县客运站属市汽车分公司，三县本身没有客运实体。"


def render_table(entry: dict) -> str:
    columns = entry["columns"]
    rows = entry["rows"]
    thead = "".join(f"<th>{html.escape(str(col))}</th>" for col in columns)
    body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    source_pages = "、".join(str(page) for page in entry.get("pages") or [entry.get("page")])
    return (
        f'<section class="verified-table-block" id="table-{entry["table_id"]}"><div class="structured-table-meta">'
        f'表ID：{entry["table_id"]}；源页：{html.escape(source_pages)}</div>'
        f'<table class="structured-table"><caption>{html.escape(entry["table_number"])} {html.escape(entry["title"])}</caption>'
        f"<thead><tr>{thead}</tr></thead><tbody>{body}</tbody></table></section>"
    )


def write_json() -> bool:
    old = DATA.read_text(encoding="utf-8") if DATA.exists() else ""
    new = json.dumps(ENTRY, ensure_ascii=False, indent=2) + "\n"
    if old != new:
        DATA.write_text(new, encoding="utf-8")
        return True
    return False


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise RuntimeError("TABLES payload not found")
    tables = json.loads(match.group(1))
    changed = False
    for idx, table in enumerate(tables):
        if table.get("table_id") == ENTRY["table_id"]:
            if table != ENTRY:
                tables[idx] = ENTRY
                changed = True
            break
    else:
        tables.append(ENTRY)
        changed = True
    if changed:
        tables.sort(key=lambda t: (str(t.get("vol") or t.get("volume") or ""), int((t.get("pages") or [t.get("page") or 999999])[0]), str(t.get("table_id") or "")))
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
        return 1
    return 0


def patch_reader() -> tuple[int, int]:
    text = HTML.read_text(encoding="utf-8")
    t062_matches = list(TABLE_RE_T062.finditer(text))
    if len(t062_matches) != 1:
        raise RuntimeError(f"expected exactly one T062 table block, found {len(t062_matches)}")
    t062_block = t062_matches[0].group(0).strip()
    without_t062, removed = TABLE_RE_T062.subn("\n", text, count=1)
    replacement = "\n" + render_table(ENTRY) + "\n" + t062_block + f'\n<p class="table-note">{html.escape(NOTE)}</p>\n'
    new, replaced = RESIDUE_RE.subn(replacement, without_t062, count=1)
    if replaced != 1:
        raise RuntimeError(f"expected to replace one road transport enterprise residue, replaced {replaced}")
    HTML.write_text(new, encoding="utf-8")
    return removed, replaced


def write_reports(json_changed: bool, site_changed: int, removed: int, replaced: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    cont_entry = json.loads(CONT_DATA.read_text(encoding="utf-8"))
    result = {
        "time": now,
        "head_table_id": ENTRY["table_id"],
        "continuation_table_id": cont_entry.get("table_id"),
        "table_number": ENTRY["table_number"],
        "title": ENTRY["title"],
        "source_pages": ["workbench/ocr/paddle_ocr/中/part02/page_0036.txt", "workbench/ocr/paddle_ocr/中/part02/page_0037.txt"],
        "json_changed": json_changed,
        "site_changed": site_changed,
        "existing_t062_blocks_moved": removed,
        "reader_flattened_blocks_replaced": replaced,
        "head_rows": ENTRY["row_count"],
        "head_columns": ENTRY["col_count"],
        "continuation_rows": cont_entry.get("row_count"),
        "continuation_columns": cont_entry.get("col_count"),
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第三十卷公路运输企业基本情况表残文修复

- 时间：{now}
- 首页表ID：`LYG-中-T135`
- 续页表ID：`LYG-中-T062`
- 表题：表30-9 `1990年连云港市公路运输企业基本情况表`
- 源页：`workbench/ocr/paddle_ocr/中/part02/page_0036.txt`、`workbench/ocr/paddle_ocr/中/part02/page_0037.txt`

## 修复动作

- 新增 verified 结构化表：`workbench/table_entries/中/data/LYG-中-T135.json`，表30-9 首页，{ENTRY['row_count']} 行、{ENTRY['col_count']} 列。
- 复用既有 verified 续表：`workbench/table_entries/中/data/LYG-中-T062.json`，{cont_entry.get('row_count')} 行、{cont_entry.get('col_count')} 列。
- 同步结构化表格站：`output/structured_tables/index.html`。
- 从最终阅读版原位置移出 `table-LYG-中-T062` 续表块：{removed} 组。
- 将第三十卷第一章第四节末尾 `(辆/吨)省汽车连云港分...12085/6·1339` 压平残文替换为首页表块、续表块和源页注释：{replaced} 组。

## 核对说明

- 首页数据来自 page_0036；续页数据来自 page_0037。
- 源页中市港务管理处经济性质和成立年份纵向拆行，按版面对应关系核为 `全民代集体`、`1960`；市运输公司为 `集体`、`1949`。
- 联运公司挂车、半挂车栏源页未见数值，保留空值。
- 本轮只清理明确表格残文，不触碰同章其它正文段落。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(removed: int, replaced: int) -> None:
    marker = "## 2026-07-01 第三十卷公路运输企业基本情况表残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第三十卷交通运输 `省汽车连云港分全民新浦通灌路34号...` 表格压平残文回源处理。
- 据 `workbench/ocr/paddle_ocr/中/part02/page_0036.txt` 新增 `workbench/table_entries/中/data/LYG-中-T135.json`：表30-9《1990年连云港市公路运输企业基本情况表》首页，9 行 9 列。
- 复用已核续表 `workbench/table_entries/中/data/LYG-中-T062.json`，将其从旧位置移动到首页表后，并在阅读版补回源页注释。
- 阅读版中表30-9 首页压平残文已替换为 verified 表块 {replaced} 组，旧位置续表块移出 {removed} 组，并同步结构化表格站。
- 报告：`output/reports/reader_readability_road_transport_enterprise_table_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    json_changed = write_json()
    site_changed = patch_site()
    removed, replaced = patch_reader()
    write_reports(json_changed, site_changed, removed, replaced)
    update_memory(removed, replaced)
    print(f"json_changed={int(json_changed)}")
    print(f"site_changed={site_changed}")
    print(f"existing_t062_blocks_moved={removed}")
    print(f"reader_flattened_blocks_replaced={replaced}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Add verified illegal business cases table and replace flattened reader residue."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T053.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_illegal_business_cases_table_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_illegal_business_cases_table_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第八卷查处非法经营案件统计表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

COLUMNS = [
    "年份",
    "案件类型",
    "案件总数(件)",
    "大案非法获利金额1000~10000元",
    "大案非法获利金额10000元以上",
    "非法获利金额(万元)",
    "罚款没收总额(万元)",
    "其中：大案罚款没收金额(万元)",
]

ROWS = [
    ["1983", "违章违法", "5626", "", "", "", "13.34", ""],
    ["1983", "投机倒把", "699", "3", "3", "5.32", "11.93", ""],
    ["1984", "违章违法", "3979", "1", "1", "", "16.44", ""],
    ["1984", "投机倒把", "286", "3", "3", "8.17", "7.89", ""],
    ["1985", "违章违法", "3883", "1", "1", "", "100.70", ""],
    ["1985", "投机倒把", "493", "13", "13", "83.43", "114.39", ""],
    ["1986", "违章违法", "6484", "3", "3", "24.36", "16.58", "21.22"],
    ["1986", "投机倒把", "684", "3", "3", "19.33", "16.92", "22.55"],
    ["1987", "违章违法", "10031", "1", "1", "10.23", "1.60", "117.18"],
    ["1987", "投机倒把", "369", "4", "4", "106.89", "104.90", "21.22"],
    ["1988", "违章违法", "4604", "3", "3", "16.21", "5.85", "17.27"],
    ["1988", "投机倒把", "182", "11", "11", "23.76", "20.31", "22.12"],
    ["1989", "违章违法", "94", "4", "4", "18.79", "17.80", "19.08"],
    ["1989", "投机倒把", "48", "6", "6", "30.24", "29.62", "30.50"],
    ["1990", "违章违法", "70", "15", "15", "71.55", "56.64", "57.01"],
    ["1990", "投机倒把", "47", "13", "13", "38.78", "38.48", "43.01"],
]

ENTRY = {
    "table_id": "LYG-上-T053",
    "title": "1983~1990年连云港市查处非法经营案件统计表",
    "table_number": "表8-15",
    "page": 501,
    "pages": [501],
    "part": "part02",
    "vol": "上",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/上/part02/page_0201.txt；并参考 raw OCR：workbench/ocr/raw/上/part02/page_0201.txt/json。源页复合表头整理为案件总数、大案非法获利金额两档、非法获利金额、罚款没收总额及其中大案罚款没收金额；源页未见数值处保留空值。",
    "volume": "上",
}

RESIDUE_RE = re.compile(
    r"\n?<p>大案非法案件非法获利非法获利其中：大案年份案件类型获利金额总数（件）</p>\s*"
    r"<p>金额 1000金额10000总额罚款没收（万元）</p>\s*"
    r"<p>～10000元元以上金额（万元）</p>\s*"
    r"<p>违章违法13\.34投机倒把5\.3211\.93违章违法16\.44投机倒把8\.177\.89违章违法100\.70投机倒把83\.43114\.39违章违法24\.3616\.5821\.22投机倒把19\.3316\.9222\.55违章违法1003110\.231\.60117\.18投机倒把106\.89104\.9021\.22违章违法16\.215\.8517\.27投机倒把23\.7620\.3122\.12违章违法18\.7917\.8019\.08投机倒把30\.2429\.6230\.50违章违法71\.5556\.6457\.01投机倒把38\.7838\.4843\.01</p>\s*",
    re.S,
)


def render_table() -> str:
    thead = "".join(f"<th>{html.escape(col)}</th>" for col in COLUMNS)
    body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>"
        for row in ROWS
    )
    return (
        '<section class="verified-table-block" id="table-LYG-上-T053"><div class="structured-table-meta">'
        '表ID：LYG-上-T053；源页：501</div>'
        '<table class="structured-table"><caption>表8-15 1983~1990年连云港市查处非法经营案件统计表</caption>'
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


def patch_reader() -> int:
    text = HTML.read_text(encoding="utf-8")
    new, replaced = RESIDUE_RE.subn("\n" + render_table() + "\n", text, count=1)
    if replaced != 1:
        raise RuntimeError(f"expected to replace one illegal business table residue, replaced {replaced}")
    HTML.write_text(new, encoding="utf-8")
    return replaced


def write_reports(json_changed: bool, site_changed: int, replaced: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    result = {
        "time": now,
        "table_id": ENTRY["table_id"],
        "table_number": ENTRY["table_number"],
        "title": ENTRY["title"],
        "source_pages": ENTRY["pages"],
        "json_changed": json_changed,
        "site_changed": site_changed,
        "reader_flattened_blocks_replaced": replaced,
        "rows": ENTRY["row_count"],
        "columns": ENTRY["col_count"],
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第八卷查处非法经营案件统计表残文修复

- 时间：{now}
- 表ID：`LYG-上-T053`
- 表题：表8-15 `1983~1990年连云港市查处非法经营案件统计表`
- 源页：`workbench/ocr/paddle_ocr/上/part02/page_0201.txt`

## 修复动作

- 新增 verified 结构化表：`workbench/table_entries/上/data/LYG-上-T053.json`，{ENTRY['row_count']} 行、{ENTRY['col_count']} 列。
- 同步结构化表格站：`output/structured_tables/index.html`。
- 将第八卷第五章第四节末尾 `违章违法13.34投机倒把5.3211.93...` 的压平残文替换为 verified 表块：{replaced} 组。

## 核对说明

- 表8-15位于 `page_0201`，表后即进入“第五节 经济合同管理”。
- 源页复合表头整理为案件总数、大案非法获利金额两档、非法获利金额、罚款没收总额及其中大案罚款没收金额。
- 源页未见数值处保留空值；未按相邻年份或案件类型推算。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(replaced: int) -> None:
    marker = "## 2026-07-01 第八卷查处非法经营案件统计表残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第八卷工商行政管理 `违章违法13.34投机倒把5.3211.93...` 表格压平残文回源处理。
- 据 `workbench/ocr/paddle_ocr/上/part02/page_0201.txt` 新增 `workbench/table_entries/上/data/LYG-上-T053.json`：表8-15《1983~1990年连云港市查处非法经营案件统计表》，16 行 8 列。
- 表头按源页复合结构整理为案件总数、大案非法获利金额两档、非法获利金额、罚款没收总额及其中大案罚款没收金额；源页未见值处留空。
- 阅读版中对应压平残文已替换为 verified 表块 {replaced} 组，并同步结构化表格站。
- 报告：`output/reports/reader_readability_illegal_business_cases_table_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    json_changed = write_json()
    site_changed = patch_site()
    replaced = patch_reader()
    write_reports(json_changed, site_changed, replaced)
    update_memory(replaced)
    print(f"json_changed={int(json_changed)}")
    print(f"site_changed={site_changed}")
    print(f"reader_flattened_blocks_replaced={replaced}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

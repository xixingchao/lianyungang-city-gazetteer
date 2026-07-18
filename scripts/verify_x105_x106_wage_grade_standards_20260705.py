# -*- coding: utf-8 -*-
"""Verify wage grade standard tables and repair reader text flow."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import embed_verified_tables_into_reader

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "workbench" / "table_entries" / "下" / "data"
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "wage_grade_standards_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "wage_grade_standards_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_工资等级标准表回源核录.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TABLES = [
    {
        "table_id": "LYG-下-T105",
        "title": "管理、技术人员工资标准",
        "table_number": "表47-7",
        "page": 2231,
        "pages": [2231],
        "part": "part01",
        "vol": "下",
        "volume": "下",
        "columns": ["项目", "厂长", "技师", "技术员", "课长", "一般职员", "勤杂人员"],
        "rows": [["工资分", "250~350", "290~350", "170~260", "200~280", "140~230", "90~170"]],
        "row_count": 1,
        "col_count": 7,
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0260.txt，并参考 raw OCR：workbench/ocr/raw/下/part01/page_0260.txt。raw OCR 漏识“厂长”，本轮以页级 OCR 为准。",
    },
    {
        "table_id": "LYG-下-T106",
        "title": "七、八级工资制工人工资标准",
        "table_number": "表47-8",
        "page": 2231,
        "pages": [2231],
        "part": "part01",
        "vol": "下",
        "volume": "下",
        "columns": ["标准", "一级", "二级", "三级", "四级", "五级", "六级", "七级", "八级"],
        "rows": [
            ["八级标准", "119", "136", "158", "178", "211", "245", "283", "322"],
            ["七级标准", "106", "121", "136", "156", "176", "206", "236", ""],
        ],
        "row_count": 2,
        "col_count": 9,
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0260.txt，并参考 raw OCR：workbench/ocr/raw/下/part01/page_0260.txt。源页七级标准仅列至七级，八级栏保留空值；主阅读版原将表格压入正文并与后续叙述句粘连，本轮拆分。",
    },
]

OLD = "<p>七、八级工资制工人工资标准表 47 - 8单位：工资分一级等级二级三级四级五级六级七级八级八级标准119136158178211245283322七级标准106121136156176206236至1952年末，新海连市有11836名职工执行新工资制度，占企业职工总数的56%。</p>"
NEW = "<p>至1952年末，新海连市有11836名职工执行新工资制度，占企业职工总数的56%。</p>"

SOURCES = [
    "workbench/ocr/paddle_ocr/下/part01/page_0260.txt",
    "workbench/ocr/raw/下/part01/page_0260.txt",
    "output/final_reader/连云港市志_全书.html:20273",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_jsons() -> int:
    changed = 0
    for table in TABLES:
        path = DATA_DIR / f"{table['table_id']}.json"
        new = json.dumps(table, ensure_ascii=False, indent=2) + "\n"
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        if old != new:
            path.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise RuntimeError("TABLES payload not found")
    tables = json.loads(match.group(1))
    before = json.dumps(tables, ensure_ascii=False, sort_keys=True)
    ids = {table["table_id"] for table in TABLES}
    tables = [table for table in tables if table.get("table_id") not in ids]
    tables.extend(TABLES)
    tables.sort(key=lambda item: (str(item.get("vol") or item.get("volume") or ""), int(item.get("page") or 999999), str(item.get("table_id") or "")))
    after = json.dumps(tables, ensure_ascii=False, sort_keys=True)
    if before == after:
        return 0
    text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
    SITE.write_text(text, encoding="utf-8")
    return 1


def repair_reader() -> int:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count == 1:
        text = text.replace(OLD, NEW, 1)
        HTML.write_text(text, encoding="utf-8")
        return 1
    if count == 0 and NEW in text and "七、八级工资制工人工资标准表 47 - 8单位：工资分一级等级" not in text:
        return 0
    raise RuntimeError(f"expected wage table residue once, got {count}")


def write_reports(json_changed: int, site_changed: int, embedded_count: int, reader_changed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "tables": [table["table_id"] for table in TABLES],
        "json_changed": json_changed,
        "site_changed": site_changed,
        "embedded_count": embedded_count,
        "reader_changed": reader_changed,
        "sources": SOURCES,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 工资等级标准表回源核录",
        "",
        f"- 时间：{now}",
        "- 表格：`LYG-下-T105` 表47-7 管理、技术人员工资标准；`LYG-下-T106` 表47-8 七、八级工资制工人工资标准。",
        "- 处理：据下册 part01/page_0260 页级 OCR 核录两张小表；主阅读版撤出表47-8压扁残片，仅保留后续正文句。",
        f"- 变更：JSON {json_changed}；结构化表格站 {site_changed}；主阅读版已核表嵌回 {embedded_count} 张；正文替换 {reader_changed} 处。",
        "",
        "## 证据",
        "",
    ]
    lines.extend(f"- `{source}`" for source in SOURCES)
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 工资等级标准表回源核录"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/verify_x105_x106_wage_grade_standards_20260705.py`，据下册 part01/page_0260 页级 OCR 核录 `LYG-下-T105` 表47-7 管理、技术人员工资标准、`LYG-下-T106` 表47-8 七、八级工资制工人工资标准。
- 主阅读版原将表47-8压扁进正文，并与 `至1952年末，新海连市有11836名职工...` 粘连；本轮将表格移入已核结构化表格区，正文仅保留叙述句。
- 报告：`output/reports/wage_grade_standards_20260705.md`。
""",
    )


def main() -> None:
    json_changed = write_jsons()
    site_changed = patch_site()
    embedded_count, unplaced = embed_verified_tables_into_reader.embed()
    if unplaced:
        raise RuntimeError(f"unplaced verified tables: {unplaced}")
    embed_verified_tables_into_reader.write_progress(embedded_count, unplaced)
    embed_verified_tables_into_reader.update_memory(embedded_count, unplaced)
    reader_changed = repair_reader()
    write_reports(json_changed, site_changed, embedded_count, reader_changed)
    print("wage_grade_standards_verified")
    print(f"json_changed={json_changed}")
    print(f"site_changed={site_changed}")
    print(f"embedded_count={embedded_count}")
    print(f"reader_changed={reader_changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

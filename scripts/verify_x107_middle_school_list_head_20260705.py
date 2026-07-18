# -*- coding: utf-8 -*-
"""Verify ordinary middle school list head page and remove flattened residue."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import embed_verified_tables_into_reader

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T107.json"
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "middle_school_list_head_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_school_list_head_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_普通中学一览表首页回源核录.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ENTRY = {
    "table_id": "LYG-下-T107",
    "title": "1990年连云港市普通中学一览表（首页）",
    "table_number": "表50-11",
    "page": 2349,
    "pages": [2349],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": ["隶属", "校名", "创办年份", "班数(个)", "学生数(人)", "教职工数小计(人)", "专任教师(人)"],
    "rows": [
        ["直属单位", "新海中学", "1948", "39", "2094", "201", "127"],
        ["直属单位", "海州中学", "1953", "32", "1600", "150", "99"],
        ["直属单位", "连云港教育学院附中", "1978", "22", "1153", "88", "52"],
    ],
    "row_count": 3,
    "col_count": 7,
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0378.txt，并参考 raw OCR：workbench/ocr/raw/下/part01/page_0378.txt。该页为表50-11首页，续表见 LYG-下-T054、LYG-下-T055、LYG-下-T056；源页隶属栏为合并单元格，按直属单位向下展开。",
}

RESIDUE = "<p>班数学生数校名隶属创办年份(个)(人)小计专任教师新海中学3920942011948127直属单位海州中学32150195316009922连云港教育学院附中197811538852</p>"
SOURCES = [
    "workbench/ocr/paddle_ocr/下/part01/page_0378.txt",
    "workbench/ocr/raw/下/part01/page_0378.txt",
    "workbench/table_entries/下/data/LYG-下-T054.json",
    "output/final_reader/连云港市志_全书.html:16267",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_json() -> int:
    new = json.dumps(ENTRY, ensure_ascii=False, indent=2) + "\n"
    old = DATA.read_text(encoding="utf-8") if DATA.exists() else ""
    if old != new:
        DATA.write_text(new, encoding="utf-8")
        return 1
    return 0


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise RuntimeError("TABLES payload not found")
    tables = json.loads(match.group(1))
    before = json.dumps(tables, ensure_ascii=False, sort_keys=True)
    tables = [table for table in tables if table.get("table_id") != ENTRY["table_id"]]
    tables.append(ENTRY)
    tables.sort(key=lambda item: (str(item.get("vol") or item.get("volume") or ""), int(item.get("page") or 999999), str(item.get("table_id") or "")))
    after = json.dumps(tables, ensure_ascii=False, sort_keys=True)
    if before == after:
        return 0
    SITE.write_text(text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :], encoding="utf-8")
    return 1


def repair_reader() -> int:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(RESIDUE)
    if count == 1:
        HTML.write_text(text.replace(RESIDUE, "", 1), encoding="utf-8")
        return 1
    if count == 0 and "班数学生数校名隶属创办年份" not in text:
        return 0
    raise RuntimeError(f"expected middle-school residue once, got {count}")


def write_reports(json_changed: int, site_changed: int, embedded_count: int, removed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "table_id": ENTRY["table_id"], "json_changed": json_changed, "site_changed": site_changed, "embedded_count": embedded_count, "reader_residue_removed": removed, "sources": SOURCES}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 普通中学一览表首页回源核录",
        "",
        f"- 时间：{now}",
        f"- 表格：`{ENTRY['table_id']}` {ENTRY['table_number']} {ENTRY['title']}。",
        "- 处理：据下册 part01/page_0378 核录表50-11首页，撤出主阅读版中对应压扁残片；续表仍使用既有 T054-T056。",
        f"- 变更：JSON {json_changed}；结构化表格站 {site_changed}；主阅读版已核表嵌回 {embedded_count} 张；撤出残片 {removed} 段。",
        "",
        "## 证据",
        "",
    ]
    lines.extend(f"- `{source}`" for source in SOURCES)
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    append_once(MEMORY, "## 2026-07-05 普通中学一览表首页回源核录", f"""
## 2026-07-05 普通中学一览表首页回源核录
- 新增并运行 `scripts/verify_x107_middle_school_list_head_20260705.py`，据下册 part01/page_0378 核录 `LYG-下-T107` 表50-11《1990年连云港市普通中学一览表（首页）》。
- 主阅读版撤出 `班数学生数校名隶属创办年份...` 压扁残片；续表继续使用 `LYG-下-T054`、`LYG-下-T055`、`LYG-下-T056`。
- 报告：`output/reports/middle_school_list_head_20260705.md`。
""")


def main() -> None:
    json_changed = write_json()
    site_changed = patch_site()
    embedded_count, unplaced = embed_verified_tables_into_reader.embed()
    if unplaced:
        raise RuntimeError(f"unplaced verified tables: {unplaced}")
    embed_verified_tables_into_reader.write_progress(embedded_count, unplaced)
    embed_verified_tables_into_reader.update_memory(embedded_count, unplaced)
    removed = repair_reader()
    write_reports(json_changed, site_changed, embedded_count, removed)
    print("middle_school_list_head_verified")
    print(f"json_changed={json_changed}")
    print(f"site_changed={site_changed}")
    print(f"embedded_count={embedded_count}")
    print(f"reader_residue_removed={removed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

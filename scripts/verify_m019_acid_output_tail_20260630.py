# -*- coding: utf-8 -*-
"""Verify full sulfuric/hydrochloric/phosphoric acid output table."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import embed_verified_tables_into_reader

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "acid_output_full_table_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "acid_output_full_table_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_硫酸盐酸磷酸产量表首页补录.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

PATCHES = {
    "LYG-中-T019": {
        "title": "1970~1990年连云港市硫酸、盐酸、磷酸产量统计表",
        "table_number": "表20-1",
        "page": 1047,
        "pages": [1047, 1048],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": ["年份", "硫酸(100%)(吨)", "盐酸(100%)(吨)", "磷酸(85%)产量(吨)", "磷酸(85%)其中出口(吨)"],
        "rows": [
            ["1970", "2577", "", "", ""],
            ["1971", "3453", "264", "264", ""],
            ["1972", "2778", "382", "1456", ""],
            ["1973", "7539", "1462", "1567", ""],
            ["1974", "6501", "529", "987", ""],
            ["1975", "7862", "458", "1281", ""],
            ["1976", "5794", "1525", "1997", "76"],
            ["1977", "7958", "2422", "2093", "99"],
            ["1978", "9542", "3710", "2929", "127"],
            ["1979", "19748", "2548", "3206", "476"],
            ["1980", "29034", "3571", "4263", "420"],
            ["1981", "27017", "3563", "4913", "130"],
            ["1982", "27017", "4265", "6119", "300"],
            ["1983", "25761", "5306", "8114", "855"],
            ["1984", "28363", "7160", "8641", "578"],
            ["1985", "25110", "10797", "10950", "218"],
            ["1986", "25100", "10797", "10950", "218"],
            ["1987", "39258", "11639", "12607", "930"],
            ["1988", "42432", "12406", "13920", "546"],
            ["1989", "36106", "13839", "11940", "999"],
            ["1990", "34835", "14105", "14129", "3229"],
        ],
        "row_count": 21,
        "col_count": 5,
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0144.txt、page_0145.txt，并参考 raw OCR：workbench/ocr/raw/中/part01/page_0144.txt、page_0145.txt。表题、表号、单位和列组据 page_0144 表头补定；1970~1971年为首页行，1972~1990年为续表行。源页未见数值的单元格保留空值，不按上下文反推。",
    }
}

RESIDUE = "<p>产量其中出口1970257719712643453264</p>"
SOURCES = [
    "workbench/ocr/paddle_ocr/中/part01/page_0144.txt",
    "workbench/ocr/paddle_ocr/中/part01/page_0145.txt",
    "workbench/ocr/raw/中/part01/page_0144.txt",
    "workbench/ocr/raw/中/part01/page_0145.txt",
    "output/final_reader/连云港市志_全书.html:8991",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_entry(entry: dict) -> bool:
    patch = PATCHES.get(entry.get("table_id"))
    if not patch:
        return False
    changed = False
    for key, value in patch.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json() -> int:
    changed = 0
    for table_id in PATCHES:
        path = DATA_DIR / f"{table_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        if patch_entry(data):
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed += 1
    return changed


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise RuntimeError("TABLES payload not found")
    tables = json.loads(match.group(1))
    changed = 0
    for table in tables:
        if patch_entry(table):
            changed += 1
    if changed:
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
    return changed


def repair_reader() -> int:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(RESIDUE)
    if count == 1:
        HTML.write_text(text.replace(RESIDUE, "", 1), encoding="utf-8")
        return 1
    if count == 0 and "产量其中出口1970257719712643453264" not in text:
        return 0
    raise RuntimeError(f"expected acid output residue once, got {count}")


def write_reports(json_changed: int, site_changed: int, embedded_count: int, removed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "table_id": "LYG-中-T019",
        "json_changed": json_changed,
        "site_changed": site_changed,
        "embedded_count": embedded_count,
        "reader_residue_removed": removed,
        "sources": SOURCES,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 硫酸盐酸磷酸产量表首页补录",
        "",
        f"- 时间：{now}",
        "- 表格：`LYG-中-T019` 表20-1《1970~1990年连云港市硫酸、盐酸、磷酸产量统计表》。",
        "- 处理：据中册 part01/page_0144 补入 1970、1971 首页行，保留 page_0145 续表 1972~1990 行；撤出主阅读版中对应压扁残片。",
        f"- 变更：JSON {json_changed}；结构化表格站 {site_changed}；主阅读版已核表嵌回 {embedded_count} 张；撤出残片 {removed} 段。",
        "",
        "## 证据",
        "",
    ]
    lines.extend(f"- `{source}`" for source in SOURCES)
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    append_once(MEMORY, "## 2026-07-05 硫酸盐酸磷酸产量表首页补录", f"""
## 2026-07-05 硫酸盐酸磷酸产量表首页补录
- 更新并运行 `scripts/verify_m019_acid_output_tail_20260630.py`，据中册 part01/page_0144、page_0145 将 `LYG-中-T019` 表20-1 补为 1970~1990 年完整表。
- 主阅读版撤出 `产量其中出口1970257719712643453264` 压扁残片；1970 年仅见硫酸 2577，其余空值保留，1971 年录为硫酸 3453、盐酸 264、磷酸产量 264。
- 报告：`output/reports/acid_output_full_table_20260705.md`。
""")


def main() -> None:
    json_changed = patch_json()
    site_changed = patch_site()
    embedded_count, unplaced = embed_verified_tables_into_reader.embed()
    if unplaced:
        raise RuntimeError(f"unplaced verified tables: {unplaced}")
    embed_verified_tables_into_reader.write_progress(embedded_count, unplaced)
    embed_verified_tables_into_reader.update_memory(embedded_count, unplaced)
    removed = repair_reader()
    write_reports(json_changed, site_changed, embedded_count, removed)
    print("acid_output_full_table_verified")
    print(f"json_files_changed={json_changed}")
    print(f"site_entries_changed={site_changed}")
    print(f"embedded_count={embedded_count}")
    print(f"reader_residue_removed={removed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

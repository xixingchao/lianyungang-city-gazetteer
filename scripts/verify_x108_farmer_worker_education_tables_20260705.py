# -*- coding: utf-8 -*-
"""Verify farmer education table and remove adult-education flattened residues."""

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
REPORT_JSON = ROOT / "output" / "reports" / "farmer_worker_education_tables_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "farmer_worker_education_tables_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_农民职工教育基本情况表残留撤出.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

FARMER = {
    "table_id": "LYG-下-T108",
    "title": "1990年连云港市农民教育基本情况表",
    "table_number": "表50-18",
    "page": 2368,
    "pages": [2368],
    "part": "part01",
    "vol": "下",
    "volume": "下",
    "columns": ["类别", "学校数(所)", "教学班(个)", "在校学生数合计(人)", "在校学生数全脱产(人)", "在校学生数业余函授(人)", "教职工数专任教师(人)", "教职工数兼任教师数(人)"],
    "rows": [
        ["农民中学", "3", "71", "912", "439", "473", "58", "35"],
        ["农民技术培训学校", "76", "1105", "58407", "", "58407", "130", "942"],
        ["其中：县办农校", "1", "12", "600", "", "600", "5", "28"],
        ["农民初等学校", "", "1886", "79871", "", "79871", "106", "1667"],
        ["其中：技术班", "", "1135", "54110", "", "54110", "56", "904"],
        ["其中：小学班", "", "431", "15825", "", "15825", "23", "442"],
        ["其中：扫盲班", "", "320", "9936", "", "9936", "27", "321"],
    ],
    "row_count": 7,
    "col_count": 8,
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/下/part01/page_0397.txt，并参考 raw OCR：workbench/ocr/raw/下/part01/page_0397.txt。源页复合表头展开为学校数、教学班、在校学生数三栏和教职工数两栏；农民初等学校及其子项源页未见学校数，保留空值。",
}

RESIDUES = [
    "<p>类别(所)(个)合计全脱产业余函授专任教师兼任教师数农民中学912714394735835农民技术培训学校7611055840758407130942其中：县办农校1260060028农民初等学校188679871106798711667技术班1135541105411056904小学班431158251582523442扫盲班3209936993627321</p>",
    "<p>教学班学校数(所)(个)全脱产专任教师兼任教师数业余函授广播电视中专班成人中等34112639职工中专校专业1479干部中专校技术学校76教师进修学校458379223552195职工中学175214195328115513572904职工技术培训学校</p>",
]
SOURCES = [
    "workbench/ocr/paddle_ocr/下/part01/page_0397.txt",
    "workbench/ocr/raw/下/part01/page_0397.txt",
    "workbench/ocr/paddle_ocr/下/part01/page_0398.txt",
    "workbench/table_entries/下/data/LYG-下-T061.json",
    "output/final_reader/连云港市志_全书.html:21435,21442",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_json() -> int:
    path = DATA_DIR / f"{FARMER['table_id']}.json"
    new = json.dumps(FARMER, ensure_ascii=False, indent=2) + "\n"
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if old != new:
        path.write_text(new, encoding="utf-8")
        return 1
    return 0


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise RuntimeError("TABLES payload not found")
    tables = json.loads(match.group(1))
    before = json.dumps(tables, ensure_ascii=False, sort_keys=True)
    tables = [table for table in tables if table.get("table_id") != FARMER["table_id"]]
    tables.append(FARMER)
    tables.sort(key=lambda item: (str(item.get("vol") or item.get("volume") or ""), int(item.get("page") or 999999), str(item.get("table_id") or "")))
    after = json.dumps(tables, ensure_ascii=False, sort_keys=True)
    if before == after:
        return 0
    SITE.write_text(text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :], encoding="utf-8")
    return 1


def repair_reader() -> int:
    text = HTML.read_text(encoding="utf-8")
    removed = 0
    for residue in RESIDUES:
        count = text.count(residue)
        if count == 1:
            text = text.replace(residue, "", 1)
            removed += 1
        elif count > 1:
            raise RuntimeError(f"residue matched {count} times")
    if removed:
        HTML.write_text(text, encoding="utf-8")
    return removed


def write_reports(json_changed: int, site_changed: int, embedded_count: int, removed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "new_table_id": FARMER["table_id"], "reused_table_id": "LYG-下-T061", "json_changed": json_changed, "site_changed": site_changed, "embedded_count": embedded_count, "reader_residue_groups_removed": removed, "sources": SOURCES}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 农民职工教育基本情况表残留撤出",
        "",
        f"- 时间：{now}",
        "- 表格：新增 `LYG-下-T108` 表50-18；复用既有 `LYG-下-T061` 表50-19。",
        "- 处理：据下册 part01/page_0397 核录农民教育基本情况表，撤出主阅读版中表50-18和表50-19两段压扁残片。",
        f"- 变更：JSON {json_changed}；结构化表格站 {site_changed}；主阅读版已核表嵌回 {embedded_count} 张；撤出残片组 {removed} 组。",
        "",
        "## 证据",
        "",
    ]
    lines.extend(f"- `{source}`" for source in SOURCES)
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    append_once(MEMORY, "## 2026-07-05 农民职工教育基本情况表残留撤出", f"""
## 2026-07-05 农民职工教育基本情况表残留撤出
- 新增并运行 `scripts/verify_x108_farmer_worker_education_tables_20260705.py`，据下册 part01/page_0397 核录 `LYG-下-T108` 表50-18《1990年连云港市农民教育基本情况表》。
- 主阅读版撤出表50-18农民教育和表50-19职工教育两段压扁残片；表50-19沿用既有 verified `LYG-下-T061`。
- 报告：`output/reports/farmer_worker_education_tables_20260705.md`。
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
    print("farmer_worker_education_tables_verified")
    print(f"json_changed={json_changed}")
    print(f"site_changed={site_changed}")
    print(f"embedded_count={embedded_count}")
    print(f"reader_residue_groups_removed={removed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

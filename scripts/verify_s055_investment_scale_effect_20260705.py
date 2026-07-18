# -*- coding: utf-8 -*-
"""Verify table 7-10 investment scale/effect and remove flattened residue."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import embed_verified_tables_into_reader

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T055.json"
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "investment_scale_effect_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "investment_scale_effect_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_投资规模与效果表回源核录.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ENTRY = {
    "table_id": "LYG-上-T055",
    "title": "建国后连云港市投资规模与效果情况表",
    "table_number": "表7-10",
    "page": 445,
    "pages": [445, 446],
    "part": "part02",
    "vol": "上",
    "volume": "上",
    "columns": ["计划时期", "投资完成额小计(万元)", "生产性建设投资(万元)", "非生产性建设投资(万元)", "新增固定资产(万元)", "固定资产交付使用率(%)"],
    "rows": [
        ["恢复时期", "1239", "1087", "152", "1187", "95.8"],
        ["一五时期", "8364", "6618", "1746", "6226", "74.4"],
        ["二五时期", "14887", "12695", "2192", "12520", "84.1"],
        ["调整时期", "4414", "3560", "854", "4002", "90.7"],
        ["三五时期", "7752", "6813", "939", "5058", "65.2"],
        ["四五时期", "25931", "24066", "1865", "14999", "57.8"],
        ["五五时期", "46867", "36111", "10756", "40595", "86.6"],
        ["六五时期", "141334", "106797", "34537", "89574", "63.4"],
        ["七五时期", "436272", "367582", "68690", "338207", "77.5"],
        ["计", "687060", "565329", "121731", "512368", "74.6"],
    ],
    "row_count": 10,
    "col_count": 6,
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0147.txt、page_0148.txt，并参考 raw OCR：workbench/ocr/raw/上/part02/page_0147.txt。表头复合栏“投资完成额”展开为小计、生产性建设投资、非生产性建设投资；“固定资产支付使用率”按正文语义和 page_0148 OCR 规范为固定资产交付使用率。",
}

RESIDUE = "<p>计划时期设投资建设投资恢复时期95.8“一五”时期74.4“二五”时期14887126951252084.1</p>"
SOURCES = [
    "workbench/ocr/paddle_ocr/上/part02/page_0147.txt",
    "workbench/ocr/paddle_ocr/上/part02/page_0148.txt",
    "workbench/ocr/raw/上/part02/page_0147.txt",
    "output/final_reader/连云港市志_全书.html:4425",
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
    if count == 0 and "计划时期设投资建设投资恢复时期95.8" not in text:
        return 0
    raise RuntimeError(f"expected investment residue once, got {count}")


def write_reports(json_changed: int, site_changed: int, embedded_count: int, removed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "table_id": ENTRY["table_id"], "json_changed": json_changed, "site_changed": site_changed, "embedded_count": embedded_count, "reader_residue_removed": removed, "sources": SOURCES}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 投资规模与效果表回源核录",
        "",
        f"- 时间：{now}",
        f"- 表格：`{ENTRY['table_id']}` {ENTRY['table_number']} {ENTRY['title']}。",
        "- 处理：据上册 part02/page_0147、page_0148 核录表7-10，撤出主阅读版中对应压扁残片。",
        f"- 变更：JSON {json_changed}；结构化表格站 {site_changed}；主阅读版已核表嵌回 {embedded_count} 张；撤出残片 {removed} 段。",
        "",
        "## 证据",
        "",
    ]
    lines.extend(f"- `{source}`" for source in SOURCES)
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    append_once(MEMORY, "## 2026-07-05 投资规模与效果表回源核录", f"""
## 2026-07-05 投资规模与效果表回源核录
- 新增并运行 `scripts/verify_s055_investment_scale_effect_20260705.py`，据上册 part02/page_0147、page_0148 核录 `LYG-上-T055` 表7-10《建国后连云港市投资规模与效果情况表》。
- 主阅读版撤出 `计划时期设投资建设投资恢复时期95.8...` 压扁残片。
- 报告：`output/reports/investment_scale_effect_20260705.md`。
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
    print("investment_scale_effect_verified")
    print(f"json_changed={json_changed}")
    print(f"site_changed={site_changed}")
    print(f"embedded_count={embedded_count}")
    print(f"reader_residue_removed={removed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

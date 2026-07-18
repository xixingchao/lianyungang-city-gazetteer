# -*- coding: utf-8 -*-
"""Add conservative transcription for table 41-5 and replace flattened reader residue."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T136.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_party_org_evolution_table_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_party_org_evolution_table_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第四十一卷市委下辖机关企事业单位党组织沿革表二残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OCR_PAGES = [
    ("中", "part02", "page_0417.txt", "1719"),
    ("中", "part02", "page_0418.txt", "1720"),
    ("中", "part02", "page_0419.txt", "1721"),
    ("中", "part02", "page_0420.txt", "1722"),
    ("中", "part02", "page_0421.txt", "1723"),
]

COLUMNS = ["源页", "源页可见条目"]

ENTRY_BASE = {
    "table_id": "LYG-中-T136",
    "title": "市委下辖机关、企事业单位党组织沿革表（二）",
    "table_number": "表41-5",
    "page": 1719,
    "pages": [1719, 1720, 1721, 1722, 1723],
    "part": "part02",
    "vol": "中",
    "columns": COLUMNS,
    "status": "verified",
    "notes": "已据页级OCR回源保守核录：workbench/ocr/paddle_ocr/中/part02/page_0417.txt 至 page_0421.txt。源页为组织沿革图式，横向连线关系复杂；本表按源页可见条目和时间序列逐行转录，不强行推断未闭合括号、跨栏连线或上下层级关系。",
    "volume": "中",
}


def normalize_line(line: str) -> str:
    line = line.strip()
    line = line.replace("－", "一")
    line = re.sub(r"\s+", " ", line)
    return line


def extract_rows() -> list[list[str]]:
    rows: list[list[str]] = []
    started = False
    for vol, part, filename, book_page in OCR_PAGES:
        path = ROOT / "workbench" / "ocr" / "paddle_ocr" / vol / part / filename
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = normalize_line(raw_line)
            if not line:
                continue
            if line.startswith("# 连云港市志_"):
                continue
            if line.startswith("第二章") or line.startswith("· 172") or line.startswith("·172"):
                continue
            if "市委下辖机关、企事业单位党组织沿革表" in line:
                started = True
                continue
            if not started:
                continue
            if line == "表41-5":
                continue
            if "市(县)委下辖区委、直属人民公社党委沿革表" in line:
                return rows
            rows.append([book_page, line])
    return rows


def make_entry() -> dict:
    rows = extract_rows()
    entry = dict(ENTRY_BASE)
    entry["rows"] = rows
    entry["row_count"] = len(rows)
    entry["col_count"] = len(COLUMNS)
    return entry


def render_table(entry: dict) -> str:
    thead = "".join(f"<th>{html.escape(col)}</th>" for col in COLUMNS)
    body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row) + "</tr>"
        for row in entry["rows"]
    )
    return (
        '<section class="verified-table-block" id="table-LYG-中-T136"><div class="structured-table-meta">'
        '表ID：LYG-中-T136；源页：1719-1723；核录方式：组织沿革图式保守转录</div>'
        '<table class="structured-table"><caption>表41-5 市委下辖机关、企事业单位党组织沿革表（二）</caption>'
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


def patch_reader(entry: dict) -> int:
    text = HTML.read_text(encoding="utf-8")
    start_marker = "<p>市委下辖机关、企事业单位党组织沿革表（二）</p>"
    end_marker = "市（县）委下辖区委、直属人民公社党委沿革表（一）"
    start = text.find(start_marker)
    end = text.find(end_marker, start)
    if start == -1 or end == -1:
        raise RuntimeError("table 41-5 reader boundary not found")
    if text.find(start_marker, start + 1) != -1:
        raise RuntimeError("table 41-5 start marker is not unique")
    new_text = text[:start] + render_table(entry) + "\n\n" + text[end:]
    HTML.write_text(new_text, encoding="utf-8")
    return 1


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
        "source_files": [f"workbench/ocr/paddle_ocr/{vol}/{part}/{filename}" for vol, part, filename, _ in OCR_PAGES],
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第四十一卷表41-5党组织沿革图式残文修复

- 时间：{now}
- 表ID：`LYG-中-T136`
- 表题：表41-5 `市委下辖机关、企事业单位党组织沿革表（二）`
- 源页：`workbench/ocr/paddle_ocr/中/part02/page_0417.txt` 至 `page_0421.txt`

## 修复动作

- 新增 verified 结构化表：`workbench/table_entries/中/data/LYG-中-T136.json`，{entry['row_count']} 行、{entry['col_count']} 列。
- 同步结构化表格站：`output/structured_tables/index.html`。
- 将第四十一卷第二章 `外事系统党委一外事办公室党委...中国人民保险公司连云港分公司党组` 的压平残文替换为 verified 表块：{replaced} 组。
- 替换边界止于 `市（县）委下辖区委、直属人民公社党委沿革表（一）` 前；表41-6未在本轮处理。

## 核对说明

- 源页为党组织沿革图式，存在横向连线、跨栏和未闭合括号；本轮按页级 OCR 可见条目逐行保守转录。
- 未把跨栏连线强行拆成组织层级，也未补写源页未闭合的结束时间。
- 修复目标是撤出阅读版中不可读的图式压平残文，并保留可回溯的源页文本序列。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(entry: dict, replaced: int) -> None:
    marker = "## 2026-07-01 第四十一卷表41-5党组织沿革图式残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry_text = f"""
{marker}

- 对正文可读性审计命中的第四十一卷政党 `外事系统党委一外事办公室党委...`、`机械工业局党委一机械工业公司党委...`、`人事局党组...` 等组织沿革图式压平残文回源处理。
- 据 `workbench/ocr/paddle_ocr/中/part02/page_0417.txt` 至 `page_0421.txt` 新增 `workbench/table_entries/中/data/LYG-中-T136.json`：表41-5《市委下辖机关、企事业单位党组织沿革表（二）》，{entry['row_count']} 行 2 列。
- 源页为组织沿革图式，横向连线关系复杂；本轮按源页可见条目和时间序列保守转录，未强行推断跨栏连线、层级或未闭合时间。
- 阅读版中对应压平残文已替换为 verified 表块 {replaced} 组；切止于表41-6标题前，表41-6留待后续单独核录。
- 报告：`output/reports/reader_readability_party_org_evolution_table_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry_text.lstrip(), encoding="utf-8")


def main() -> None:
    entry = make_entry()
    if entry["row_count"] < 20:
        raise RuntimeError(f"unexpectedly few rows extracted: {entry['row_count']}")
    json_changed = write_json(entry)
    site_changed = patch_site(entry)
    replaced = patch_reader(entry)
    write_reports(entry, json_changed, site_changed, replaced)
    update_memory(entry, replaced)
    print(f"rows={entry['row_count']}")
    print(f"json_changed={int(json_changed)}")
    print(f"site_changed={site_changed}")
    print(f"reader_flattened_blocks_replaced={replaced}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

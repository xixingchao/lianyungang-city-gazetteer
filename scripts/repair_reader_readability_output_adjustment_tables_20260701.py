# -*- coding: utf-8 -*-
"""Add verified 1988 output adjustment tables and replace flattened reader residue."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_output_adjustment_tables_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_output_adjustment_tables_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第八卷总产值调整表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

COLUMNS = ["项目", "原指数", "核实数", "水份", "水份占原报数(%)"]

ENTRIES = [
    {
        "table_id": "LYG-上-T050",
        "title": "1988年连云港市工农业总产值调整表",
        "table_number": "表8-4",
        "page": 471,
        "pages": [471],
        "part": "part02",
        "vol": "上",
        "columns": COLUMNS,
        "rows": [
            ["工农业总产值总计", "578732", "503101", "75631", "13.07"],
            ["其中：赣榆县", "160019", "109092", "50927", "31.83"],
            ["其中：东海县", "130022", "110095", "19927", "15.33"],
            ["其中：灌云县", "87930", "86005", "1925", "2.19"],
            ["其中：市区", "200761", "197909", "2852", "1.42"],
        ],
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/上/part02/page_0171.txt，并参考 raw OCR：workbench/ocr/raw/上/part02/page_0171.txt/json。源页单位为万元，注：按1980年不变价计算。",
    },
    {
        "table_id": "LYG-上-T051",
        "title": "1988年连云港市农业总产值调整表",
        "table_number": "表8-5",
        "page": 472,
        "pages": [472],
        "part": "part02",
        "vol": "上",
        "columns": COLUMNS,
        "rows": [
            ["农业总产值总计", "177644", "167690", "9954", "5.60"],
            ["其中：农业", "106959", "103016", "3943", "3.69"],
            ["其中：林业", "2025", "2025", "", ""],
            ["其中：牧业", "26083", "25105", "978", "3.75"],
            ["其中：副业", "34819", "29786", "5033", "14.45"],
            ["其中：家庭手工业", "33731", "28698", "5033", "14.92"],
            ["其中：渔业", "7758", "7758", "", ""],
        ],
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/上/part02/page_0172.txt，并参考 raw OCR：workbench/ocr/raw/上/part02/page_0172.txt/json。源页单位为万元，注：按1980年不变价计算；林业、渔业源页未列水份和占比，保留空值。",
    },
    {
        "table_id": "LYG-上-T052",
        "title": "1988年连云港市工业总产值调整表",
        "table_number": "表8-6",
        "page": 472,
        "pages": [472],
        "part": "part02",
        "vol": "上",
        "columns": COLUMNS,
        "rows": [
            ["工业总产值总计", "401088", "335411", "65677", "16.37"],
            ["其中：乡以上", "294625", "281868", "12757", "4.33"],
            ["村及村以上", "106463", "53543", "52920", "49.71"],
            ["(1)三县合计", "209589", "146764", "62825", "29.98"],
            ["赣榆", "97418", "56445", "40973", "42.06"],
            ["东海", "65867", "45940", "19927", "30.25"],
            ["灌云", "46304", "44379", "1925", "4.16"],
            ["(2)四区合计", "31851", "28999", "2852", "8.95"],
            ["新浦", "5185", "4885", "300", "5.79"],
            ["海州", "8480", "8252", "228", "2.69"],
            ["云台", "12407", "11245", "1162", "9.37"],
            ["连云", "5779", "4617", "1162", "20.11"],
            ["(3)市直属单位", "159648", "159648", "", ""],
        ],
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/上/part02/page_0172.txt，并参考 raw OCR：workbench/ocr/raw/上/part02/page_0172.txt/json。源页单位为万元；注：1.按1980年不变价计算；2.村及村下产值包括城镇个体工业和城镇合作经营工业。市直属单位源页未列水份和占比，保留空值。",
    },
]

for entry in ENTRIES:
    entry["row_count"] = len(entry["rows"])
    entry["col_count"] = len(entry["columns"])
    entry["status"] = "verified"
    entry["volume"] = entry["vol"]

RESIDUE_RE = re.compile(
    r"\n?<p>工农业总产值总计5787325031017563113\.07赣榆县1600191090925092731\.83其东海县1300221100951992715\.33中灌云县87930860052\.19市区2007611979091\.42注：按1980年不变价计算。</p>\s*"
    r"<p>农业总产值总计1776441676905\.60农业1069591030163\.69林业其牧业26083251053\.75副业3481929786中14\.45其中：家庭手工业337312869814\.92渔业注：按1980年不变价计算。</p>\s*"
    r"<p>工业总产值总计4010883354116567716\.37其中：乡以上294625281868127574\.33村及村以上106463535435292049\.71（1）三县合计2095891467646282529\.98赣榆97418564454097342\.06东海65867459401992730\.25灌云46304443794\.16（2）四区合计31851289998\.95新浦5\.79海州2\.69云台12407112459\.37连云20\.11（3）市直属单位159648159648注：1。按1980年不变价计算。</p>\s*"
    r"<p>2。 村及村下产值包括城镇个体工业和城镇合作经营工业。</p>\s*",
    re.S,
)


def render_table(entry: dict) -> str:
    thead = "".join(f"<th>{html.escape(str(col))}</th>" for col in entry["columns"])
    body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row) + "</tr>"
        for row in entry["rows"]
    )
    pages = "、".join(str(page) for page in entry["pages"])
    return (
        f'<section class="verified-table-block" id="table-{entry["table_id"]}"><div class="structured-table-meta">'
        f'表ID：{entry["table_id"]}；源页：{html.escape(pages)}</div>'
        f'<table class="structured-table"><caption>{html.escape(entry["table_number"])} {html.escape(entry["title"])}</caption>'
        f"<thead><tr>{thead}</tr></thead><tbody>{body}</tbody></table></section>"
    )


def write_json_files() -> int:
    changed = 0
    for entry in ENTRIES:
        path = DATA_DIR / f"{entry['table_id']}.json"
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        new = json.dumps(entry, ensure_ascii=False, indent=2) + "\n"
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
    changed = False
    by_id = {entry["table_id"]: entry for entry in ENTRIES}
    seen = set()
    for idx, table in enumerate(tables):
        table_id = table.get("table_id")
        if table_id in by_id:
            seen.add(table_id)
            if table != by_id[table_id]:
                tables[idx] = by_id[table_id]
                changed = True
    for table_id, entry in by_id.items():
        if table_id not in seen:
            tables.append(entry)
            changed = True
    if changed:
        tables.sort(key=lambda t: (str(t.get("vol") or t.get("volume") or ""), int((t.get("pages") or [t.get("page") or 999999])[0]), str(t.get("table_id") or "")))
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
        return 1
    return 0


def patch_reader() -> int:
    text = HTML.read_text(encoding="utf-8")
    replacement = "\n" + "\n".join(render_table(entry) for entry in ENTRIES) + "\n"
    new, replaced = RESIDUE_RE.subn(replacement, text, count=1)
    if replaced != 1:
        raise RuntimeError(f"expected to replace one output adjustment residue group, replaced {replaced}")
    HTML.write_text(new, encoding="utf-8")
    return replaced


def write_reports(json_changed: int, site_changed: int, replaced: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    result = {
        "time": now,
        "tables": [
            {
                "table_id": entry["table_id"],
                "table_number": entry["table_number"],
                "title": entry["title"],
                "source_pages": entry["pages"],
                "rows": entry["row_count"],
                "columns": entry["col_count"],
            }
            for entry in ENTRIES
        ],
        "json_files_changed": json_changed,
        "site_changed": site_changed,
        "reader_flattened_groups_replaced": replaced,
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    table_lines = "\n".join(
        f"- `{entry['table_id']}`：{entry['table_number']} `{entry['title']}`，{entry['row_count']} 行、{entry['col_count']} 列。"
        for entry in ENTRIES
    )
    md = f"""# 第八卷总产值调整表残文修复

- 时间：{now}
- 源页：`workbench/ocr/paddle_ocr/上/part02/page_0171.txt`、`workbench/ocr/paddle_ocr/上/part02/page_0172.txt`

## 新增 verified 表

{table_lines}

## 修复动作

- 新增结构化表 JSON：`workbench/table_entries/上/data/LYG-上-T050.json` 至 `LYG-上-T052.json`。
- 同步结构化表格站：`output/structured_tables/index.html`。
- 将第八卷第二章“数字质量检查”下三段压平残文替换为三个 verified 表块：{replaced} 组。

## 核对说明

- 三张表源页均标注单位为万元，列序统一整理为：项目、原指数、核实数、水份、水份占原报数(%)。
- 表8-4、表8-5 注释为“按1980年不变价计算”。
- 表8-6 注释为“按1980年不变价计算；村及村下产值包括城镇个体工业和城镇合作经营工业”。
- 源页未列水份或占比的单元格保留空值，未按相邻项推算。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(replaced: int) -> None:
    marker = "## 2026-07-01 第八卷总产值调整表残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第八卷经济综合管理 `工农业总产值总计...农业总产值总计...工业总产值总计...` 三段压平残文回源处理。
- 据 `workbench/ocr/paddle_ocr/上/part02/page_0171.txt`、`page_0172.txt` 新增 `workbench/table_entries/上/data/LYG-上-T050.json` 至 `LYG-上-T052.json`：表8-4《1988年连云港市工农业总产值调整表》、表8-5《1988年连云港市农业总产值调整表》、表8-6《1988年连云港市工业总产值调整表》。
- 三表均为 verified，列序整理为项目、原指数、核实数、水份、水份占原报数(%)；源页未列数值处保留空值。
- 阅读版中对应三段压平残文已替换为 verified 表块 {replaced} 组，并同步结构化表格站。
- 报告：`output/reports/reader_readability_output_adjustment_tables_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    json_changed = write_json_files()
    site_changed = patch_site()
    replaced = patch_reader()
    write_reports(json_changed, site_changed, replaced)
    update_memory(replaced)
    print(f"json_files_changed={json_changed}")
    print(f"site_changed={site_changed}")
    print(f"reader_flattened_groups_replaced={replaced}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

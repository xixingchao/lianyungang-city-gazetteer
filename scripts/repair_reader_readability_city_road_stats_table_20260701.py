# -*- coding: utf-8 -*-
"""Add verified table 5-5 and remove its flattened reader residue."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T047.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_city_road_stats_table_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_city_road_stats_table_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第五卷全市道路统计表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

COLUMNS = [
    "地区",
    "道路总长合计(公里)",
    "其中高级、次高级道路长(公里)",
    "道路总面积合计(万平方米)",
    "其中高级、次高级道路面积(万平方米)",
    "备注",
]

ROWS = [
    ["市内", "433.00", "178.00", "294.00", "185.00", ""],
    ["赣榆县城", "22.00", "11.40", "26.34", "11.30", "村庄道路中铺装道路长3504公里"],
    ["东海县城", "24.10", "22.00", "41.40", "36.10", ""],
    ["灌云县城", "20.40", "15.70", "20.32", "16.12", ""],
    ["建制镇", "195.87", "72.22", "273.68", "103.23", ""],
    ["集镇", "483.00", "101.00", "537.00", "72.00", ""],
    ["村庄", "9997.00", "", "", "", ""],
]

ENTRY = {
    "table_id": "LYG-上-T047",
    "title": "1990年连云港市全市道路统计表",
    "table_number": "表5-5",
    "page": 294,
    "pages": [294],
    "part": "part02",
    "vol": "上",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0049.txt；并参考 raw OCR：workbench/ocr/raw/上/part02/page_0049.txt。表5-5位于市区广场正文后、第二节桥梁隧道前；复合表头整理为道路总长、道路总面积及高级/次高级分项。备注‘村庄道路中铺装道路长3504公里’按源页位置记入赣榆县城行备注，未外推至其他行。村庄行源页仅见道路总长合计9997.00，其余列保留空值。",
    "volume": "上",
}

RESIDUE_RE = re.compile(
    r"\n?<p>道路总面积（万平方米）</p>\s*"
    r"<p>地区备注其中高级、次其中高级、次合计合计高级道路长高级道路面积市内433\.00178\.00294\.00185\.00村庄道路中铺装道路长赣榆县城22\.0011\.4026\.3411\.303504公里东海县城24\.1022\.0041\.4036\.10灌云县城20\.4015\.7020\.3216\.12建制镇195\.8772\.22273\.68103\.23集镇483\.00101\.00537\.0072\.00村庄9997\.00</p>\s*",
    re.S,
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


def remove_reader_residue() -> int:
    text = HTML.read_text(encoding="utf-8")
    new, count = RESIDUE_RE.subn("\n", text, count=1)
    if count != 1:
        raise RuntimeError(f"expected to remove 1 road stats residue block, removed {count}")
    HTML.write_text(new, encoding="utf-8")
    return count


def write_reports(json_changed: bool, site_changed: int, removed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    result = {
        "time": now,
        "table_id": ENTRY["table_id"],
        "table_number": ENTRY["table_number"],
        "title": ENTRY["title"],
        "source_pages": ENTRY["pages"],
        "source_ocr": [
            "workbench/ocr/paddle_ocr/上/part02/page_0049.txt",
            "workbench/ocr/raw/上/part02/page_0049.txt",
        ],
        "json_changed": json_changed,
        "site_changed": site_changed,
        "reader_residue_blocks_removed": removed,
        "rows": len(ROWS),
        "columns": len(COLUMNS),
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第五卷全市道路统计表残文修复

- 时间：{now}
- 表ID：`{ENTRY['table_id']}`
- 表题：{ENTRY['table_number']} {ENTRY['title']}
- 源页：`workbench/ocr/paddle_ocr/上/part02/page_0049.txt`

## 修复动作

- 新增 verified 结构化表：`workbench/table_entries/上/data/LYG-上-T047.json`。
- 将表5-5核录为 {len(ROWS)} 行、{len(COLUMNS)} 列，并同步到结构化表格站。
- 从最终阅读版撤出 `道路总面积（万平方米）` 与 `地区备注其中高级、次...村庄9997.00` 压平残文：{removed} 组。

## 核对说明

- 表5-5位于市区广场正文后、`第二节桥梁隧道` 前。
- 复合表头按页级 OCR 整理为道路总长、道路总面积及高级/次高级分项。
- `村庄道路中铺装道路长3504公里` 按源页位置记入 `赣榆县城` 行备注；未按语义拆分或外推。
- `村庄` 行源页仅见道路总长合计 `9997.00`，其余列保留空值。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(removed: int) -> None:
    marker = "## 2026-07-01 第五卷全市道路统计表残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第五卷城乡建设残文 `地区备注其中高级、次...村庄9997.00` 回源处理。
- 据 `workbench/ocr/paddle_ocr/上/part02/page_0049.txt` 和 `workbench/ocr/raw/上/part02/page_0049.txt` 新增 verified 表：`workbench/table_entries/上/data/LYG-上-T047.json`，表5-5《1990年连云港市全市道路统计表》，7 行 6 列。
- 从 `output/final_reader/连云港市志_全书.html` 撤出对应压平残文 {removed} 组；桥梁隧道正文保留。
- 报告：`output/reports/reader_readability_city_road_stats_table_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    json_changed = write_json()
    site_changed = patch_site()
    removed = remove_reader_residue()
    write_reports(json_changed, site_changed, removed)
    update_memory(removed)
    print(f"json_changed={int(json_changed)}")
    print(f"site_changed={site_changed}")
    print(f"reader_residue_blocks_removed={removed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

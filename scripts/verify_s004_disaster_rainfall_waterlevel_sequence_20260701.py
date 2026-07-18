# -*- coding: utf-8 -*-
"""Verify LYG-上-T004 disaster-year rainfall and water-level table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T004.json"
RAW_DIR = ROOT / "workbench" / "ocr" / "raw" / "上" / "part01"

COLUMNS = ["源页", "源页行序", "年份", "源页可见文本序列", "说明"]
PAGE_NOISE = {"第五章", "五章", "水系", "水文", "连云港市志·自然环境"}


def line_position(item: dict) -> tuple[float, float]:
    box = item["box"]
    x = sum(point[0] for point in box) / 4
    y = sum(point[1] for point in box) / 4
    return y, x


def grouped_lines(page: int) -> list[list[tuple[float, str]]]:
    payload = json.loads((RAW_DIR / f"page_{page:04d}.json").read_text(encoding="utf-8"))
    cells = []
    for item in payload["lines"]:
        y, x = line_position(item)
        text = str(item["text"]).strip()
        if text:
            cells.append((y, x, text))
    cells.sort()
    groups: list[tuple[float, list[tuple[float, str]]]] = []
    for y, x, text in cells:
        if not groups or abs(groups[-1][0] - y) > 14:
            groups.append((y, [(x, text)]))
        else:
            groups[-1][1].append((x, text))
    return [sorted(row, key=lambda pair: pair[0]) for _y, row in groups]


def build_rows() -> list[list[str]]:
    rows: list[list[str]] = []
    for page in [174, 175, 176, 177]:
        ordinal = 0
        for cells in grouped_lines(page):
            year_cells = [(x, text) for x, text in cells if re.fullmatch(r"19\d{2}", text) and 330 <= x <= 400]
            if not year_cells:
                continue
            year = year_cells[0][1]
            values = [text for x, text in cells if x >= 430 and text not in PAGE_NOISE]
            if not values:
                continue
            ordinal += 1
            rows.append([
                str(page),
                str(ordinal),
                year,
                "、".join(values),
                "按 raw 坐标 OCR 同行横向可见顺序保留；站名和灾害性质为源页合并单元格，未在本行中反推。",
            ])
    return rows


ROWS = build_rows()

PATCH = {
    "title": "连云港市部分灾害年降雨、水位情况表",
    "table_number": "表1-20",
    "page": 174,
    "pages": [174, 175, 176, 177],
    "part": "part01",
    "vol": "上",
    "volume": "上",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据 raw 坐标OCR核录：workbench/ocr/raw/上/part01/page_0174.json 至 page_0177.json；并参考页级OCR workbench/ocr/paddle_ocr/上/part01/page_0174.txt 至 page_0177.txt。原题名串为物候表，回源确认实际为自然环境卷表1-20；源表为宽表且站名、灾害性质多为竖排合并单元格，本轮按年份行保留横向可见文本序列，不据相邻行或合计关系反推月度小格。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-上-T004":
        return False
    changed = False
    for key, value in PATCH.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if patch_entry(data):
        DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 1
    return 0


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise SystemExit("TABLES payload not found")
    tables = json.loads(match.group(1))
    changed = 0
    for table in tables:
        if patch_entry(table):
            changed += 1
    if changed:
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    print(f"rows={len(ROWS)}")
    print(f"json_files_changed={patch_json()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Verify foreign insurance self-operated income/claims statistics."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T052": {
        "title": "1974~1990年中国人民保险公司连云港分公司涉外保险自营收入理赔统计表",
        "table_number": "表29-23",
        "page": 1387,
        "pages": [1387],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": ["年份", "承保笔数", "保费收入美元(元)", "保费收入港币(元)", "保费收入人民币(元)", "赔案件数", "赔偿金额美元(元)", "赔偿金额港币(元)", "赔偿金额人民币(元)"],
        "rows": [
            ["1974", "", "31358.31", "", "", "", "", "", ""],
            ["1975", "2", "890.35", "", "", "", "", "", ""],
            ["1976", "4", "2126.81", "", "", "", "", "", ""],
            ["1977", "11", "28197.43", "", "", "2", "5933.77", "", ""],
            ["1978", "14", "5789.77", "", "", "1", "9313.62", "", ""],
            ["1979", "6", "6425.53", "", "", "4", "16797.84", "", ""],
            ["1980", "55", "203623.49", "25945.05", "", "8", "68543.46", "302574.84", ""],
            ["1981", "84", "171578.00", "96782.00", "", "11", "117529.00", "36639.00", ""],
            ["1982", "71", "121033.00", "90044.00", "", "13", "10710.00", "7022.00", ""],
            ["1983", "75", "52331.00", "65333.00", "", "16", "8453104.00", "", ""],
            ["1984", "75", "68536.00", "23539.00", "", "14", "55662612.00", "", ""],
            ["1985", "89", "108563.00", "548.00", "129721.00", "27", "78975.00", "27446.00", "109768.00"],
            ["1986", "151", "163237.00", "39420.00", "147523.00", "31", "433141.00", "2529.00", ""],
            ["1987", "151", "204881.00", "162883.00", "337058.00", "14", "68609.00", "", ""],
            ["1988", "120", "249767.00", "97899.00", "897270.00", "37", "9713.00", "216991.00", ""],
            ["1989", "102", "210170.00", "79581.00", "694655.00", "37", "399245.00", "103734.00", "67221.00"],
            ["1990", "66", "349039.00", "3884.00", "", "14", "300217.00", "71815.00", ""],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0484.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T052_1387.txt。原JSON为单列骨架。源页未见数值的币种栏保留空值。",
    }
}

for patch in PATCHES.values():
    patch["row_count"] = len(patch["rows"])
    patch["col_count"] = len(patch["columns"])


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
    print(f"json_files_changed={patch_json()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()

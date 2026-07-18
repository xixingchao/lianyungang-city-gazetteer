# -*- coding: utf-8 -*-
"""Verify commercial loan balance continuation table from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T112": {
        "title": "1949~1990年连云港市商业贷款余额统计表（续表）",
        "table_number": "表40-8",
        "page": 1785,
        "pages": [1785],
        "columns": ["年份", "合计", "国营商业贷款", "粮食贷款", "外贸贷款", "供销合作贷款", "其它商业企业", "私人合营商业"],
        "rows": [
            ["1960", "1607.90", "1200.00", "363.60", "44.30", "", "", ""],
            ["1961", "1321.80", "911.60", "332.20", "12.90", "65.10", "", ""],
            ["1962", "1140.80", "842.40", "154.80", "132.30", "11.30", "", ""],
            ["1963", "1397.20", "752.50", "556.80", "81.40", "6.50", "", ""],
            ["1964", "172.00", "5.70", "818.40", "838.20", "69.10", "", ""],
            ["1965", "2098.40", "1144.20", "785.20", "114.60", "54.40", "", ""],
            ["1966", "2932.10", "1476.60", "1266.90", "141.80", "46.80", "", ""],
            ["1967", "2934.50", "1321.20", "1206.60", "346.30", "60.40", "", ""],
            ["1968", "3325.80", "1309.70", "1554.10", "433.90", "28.10", "", ""],
            ["1969", "2995.20", "1384.90", "900.10", "684.20", "26.00", "", ""],
            ["1970", "3603.70", "1743.40", "988.60", "794.10", "77.60", "", ""],
            ["1971", "3613.50", "2473.40", "1069.70", "70.40", "", "", ""],
            ["1972", "4203.40", "2666.70", "1280.50", "256.20", "", "", ""],
            ["1973", "4968.80", "3393.50", "1427.70", "147.60", "", "", ""],
            ["1974", "4892.20", "3462.20", "1255.40", "174.60", "", "", ""],
            ["1975", "5219.50", "4236.80", "777.60", "205.10", "", "", ""],
            ["1976", "6691.70", "4562.30", "1420.20", "709.20", "", "", ""],
            ["1977", "7216.70", "5183.40", "845.20", "555.20", "632.90", "", ""],
            ["1978", "10265.80", "7421.50", "1375.60", "824.20", "644.50", "", ""],
            ["1979", "7868.10", "5266.60", "1910.30", "691.20", "", "", ""],
            ["1980", "9799.90", "7635.00", "2164.90", "", "", "", ""],
            ["1981", "43797.00", "14078.00", "16470.00", "8553.00", "2457.00", "2237.00", "2.00"],
            ["1982", "44064.00", "16969.00", "13089.00", "8284.00", "3464.00", "2239.00", "19.00"],
            ["1983", "55513.00", "14918.00", "20807.00", "9402.00", "7475.00", "2858.00", "53.00"],
            ["1984", "65942.00", "14032.00", "28895.00", "11549.00", "6126.00", "5240.00", "100.00"],
            ["1985", "73092.00", "18326.00", "25746.00", "13447.00", "9249.00", "6294.00", "30.00"],
            ["1986", "92735.00", "18509.00", "24981.00", "17058.00", "23476.00", "8650.00", "61.00"],
            ["1987", "104321.00", "19597.00", "30901.00", "19108.00", "22829.00", "11812.00", "74.00"],
            ["1988", "117259.00", "25306.00", "30099.00", "21525.00", "24966.00", "15280.00", "83.00"],
            ["1989", "133137.00", "30036.00", "31945.00", "25809.00", "27152.00", "18124.00", "71.00"],
            ["1990", "149199.00", "30335.00", "39361.00", "33950.00", "24448.00", "21043.00", "62.00"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0365.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T112_1785.txt。表题和表号依据前页 workbench/ocr/paddle_ocr/中/part02/page_0364.txt；本页为表40-8续表，单位为万元。源页未列数值的单元格保留空白。",
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

# -*- coding: utf-8 -*-
"""Verify Xinhai power plant economic indicators continuation."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

COLUMNS = [
    "年份",
    "设备容量(万千瓦)",
    "发电量(万千瓦时)",
    "总产值(万元)",
    "发电厂用电率(%)",
    "供电标准煤耗(克/千瓦时)",
    "发电标准煤耗(克/千瓦时)",
    "设备利用(小时)",
    "用煤量(吨)",
]

PATCHES = {
    "LYG-中-T035": {
        "title": "1949~1990年新海发电厂经济指标统计表（续表）",
        "table_number": "表25-1",
        "page": 1243,
        "pages": [1243],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": COLUMNS,
        "rows": [
            ["1959", "1.36", "4006", "261.00", "9.27", "607", "551", "2946", "30236"],
            ["1960", "1.36", "7062", "471.30", "7.10", "629", "584", "5009", "56796"],
            ["1961", "1.96", "5000", "329.50", "8.47", "614", "562", "2551", "40841"],
            ["1962", "1.96", "4455", "98.20", "8.86", "621", "566", "2273", "35765"],
            ["1963", "1.96", "4457", "306.70", "7.50", "624", "577", "2274", "34693"],
            ["1964", "1.96", "5309", "367.50", "6.49", "589", "551", "2709", "36607"],
            ["1965", "1.96", "9046", "588.00", "5.34", "547", "518", "4615", "63015"],
            ["1966", "2.56", "12555", "861.10", "5.04", "549", "521", "6373", "87077"],
            ["1967", "2.56", "10782", "700.10", "5.78", "590", "556", "4212", "78221"],
            ["1968", "2.56", "5783", "375.90", "7.87", "673", "614", "2259", "46688"],
            ["1969", "2.56", "7127", "463.20", "8.08", "679", "624", "2784", "58444"],
            ["1970", "2.56", "14218", "924.20", "6.68", "583", "544", "5554", "101658"],
            ["1971", "2.56", "18274", "1189.40", "6.79", "571", "532", "7142", "124356"],
            ["1972", "2.56", "19806", "1287.90", "6.50", "558", "", "7737", "139068"],
            ["1973", "3.76", "21543", "1314.40", "6.46", "552", "516", "7524", "148759"],
            ["1974", "3.76", "19989", "1301.30", "7.37", "560", "519", "5316", "138955"],
            ["1975", "3.60", "27146", "1765.50", "6.21", "544", "510", "7541", "185962"],
            ["1976", "6.10", "30333", "2037.30", "5.56", "541", "511", "8348", "210301"],
            ["1977", "8.60", "38829", "2571.90", "5.44", "516", "488", "5746", "259523"],
            ["1978", "8.60", "58135", "3778.80", "5.32", "508", "481", "6760", "354219"],
            ["1979", "8.10", "63515", "4128.50", "5.15", "504", "478", "7385", "389253"],
            ["1980", "8.60", "59803", "3906.90", "4.95", "498", "474", "6954", "379253"],
            ["1981", "8.60", "51686", "3404.60", "5.16", "494", "468", "6010", "323405"],
            ["1982", "8.25", "52603", "3481.40", "5.28", "500", "473", "6310", "335098"],
            ["1983", "8.25", "56098", "3722.30", "5.30", "497", "470", "6799", "348855"],
            ["1984", "8.25", "58254", "3939.80", "5.33", "498", "472", "7182", "383055"],
            ["1985", "8.25", "62599", "4202.00", "5.44", "502", "475", "7588", "402988"],
            ["1986", "8.25", "58951", "2989.30", "5.75", "505", "475", "7146", "393834"],
            ["1987", "8.25", "58247", "2968.80", "5.88", "507", "478", "7060", "396287"],
            ["1988", "8.25", "56378", "2882.42", "6.30", "515", "483", "6968", "388770"],
            ["1989", "8.25", "58302", "2978.98", "7.05", "511", "475", "7337", "400849"],
            ["1990", "28.25", "78054", "3804.64", "8.88", "489", "446", "5652", "462629"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0340.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T035_1243.txt。表题、表号和列组据前页 workbench/ocr/paddle_ocr/中/part01/page_0339.txt 补定。原JSON误列为主要勘察设计单位一览表；本页为表25-1续上表。1972年发电标准煤耗栏源页为横线，保留空值。",
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

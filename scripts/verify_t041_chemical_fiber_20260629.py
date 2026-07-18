# -*- coding: utf-8 -*-
"""Verify LYG-上-T041 against page-level OCR and mark it deliverable."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T041.json"

COLUMNS = [
    "年份",
    "维纶纤维/维纶长丝产量(吨)",
    "涤纶树酯切片产量(吨)",
    "涤纶长丝产量(吨)",
    "企业固定资产原值(万元)",
    "工业总产值(万元)",
    "销售收入(万元)",
    "利润(万元)",
    "税金(万元)",
]

ROWS = [
    ["1970", "", "", "", "", "2.16", "", "", "1.20"],
    ["1971", "", "", "", "", "6.10", "", "", "11.00"],
    ["1972", "", "", "", "", "252.00", "126.80", "126.06", "-66.85"],
    ["1973", "", "", "", "", "169.36", "82.68", "66.70", "-20.50"],
    ["1974", "", "", "", "", "12.98", "51.50", "41.19", "-19.80"],
    ["1975", "", "", "", "", "57.98", "88.33", "137.94", "126.50"],
    ["1976", "", "", "", "40.20", "100.90", "355.01", "476.40", "140.79"],
    ["1977", "", "", "592", "71.40", "429.00", "36.90", "51.94", ""],
    ["1978", "", "", "594.00", "65.20", "174.15", "754.30", "90.70", "724.00"],
    ["1979", "58.40", "22.54", "733.00", "90.90", "817.67", "205.39", "1012.30", ""],
    ["1980", "66.80", "77.74", "739.00", "82.60", "940.55", "183.20", "1203.20", ""],
    ["1981", "69.70", "30.24", "1671.00", "224.70", "1701.44", "278.15", "1482.00", ""],
    ["1982", "167.00", "19.92", "1615.00", "103.50", "2544.51", "506.00", "1362.80", ""],
    ["1983", "163.20", "1057.00", "1748.00", "144.40", "1979.80", "553.20", "", ""],
    ["1984", "130.10", "1478.00", "1254", "331.70", "2720.85", "2375.28", "4545.40", "300.30"],
    ["1985", "", "3761.00", "1920", "632.90", "2175.90", "2621.30", "5730.00", "450.00"],
    ["1986", "199.10", "1885.00", "1695", "128.30", "4086.50", "794.30", "2852.62", ""],
    ["1987", "", "4978.00", "4006", "736.50", "8157.50", "5712.28", "302.40", ""],
    ["1988", "", "7218.00", "4981", "1085.00", "6289.77", "10902.20", "380.50", ""],
    ["1989", "", "8918.00", "6660", "1112.90", "6592.62", "14088.50", "398.60", ""],
    ["1990", "", "10621.00", "6997", "1573.50", "6881.99", "15041.20", "576.30", ""],
]

PATCH = {
    "title": "1970~1990年连云港市化纤业生产经营情况统计表",
    "table_number": "表15-1",
    "pages": [836],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：上册part03/page_0231。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-上-T041":
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
    print(f"json_files_changed={patch_json()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()

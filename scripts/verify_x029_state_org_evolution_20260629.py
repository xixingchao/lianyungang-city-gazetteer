# -*- coding: utf-8 -*-
"""Verify LYG-下-T029 state organ evolution table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T029.json"

COLUMNS = ["机构名称", "沿革说明"]
ROWS = [
    [
        "连云港市人民代表大会",
        "自1953年实行基层普选、民主建政以来，连云港市共召开过八届人民代表大会。历届人代会首次会议的时间分别是：1954.6、1957.1、1958.5、1961.9、1963.12、1980.2、1983.4、1988.1。",
    ],
    [
        "连云港市人民代表大会常务委员会",
        "1980年起，增设人民代表大会常务委员会。市人大常委会（1980.2-）设有办公室、财政经济委员会、农村经济工作委员会、城乡建设委员会、教科文工作委员会、法制工作委员会、人大代表联络委员会、选举工作办公室等。",
    ],
    [
        "连云港市中级人民法院",
        "市人民法院（1949.12~1962.8）、市中级人民法院（1962.8~1966.3、1973.8~1973.11、1974.12~）。",
    ],
    [
        "连云港市人民检察院",
        "市人民检察院（1955.5~1958、1961.9~1966.3、1978.1~）。",
    ],
]

PATCH = {
    "title": "建国后连云港市国家权力、审判、检察机关沿革表",
    "table_number": "表46-18",
    "page": 2194,
    "pages": [2194],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T029_2194.txt；原JSON为单列待录入骨架。页首含上一表续表内容，本轮仅录入本ID对应的表46-18。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T029":
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

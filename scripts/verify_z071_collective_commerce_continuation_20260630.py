# -*- coding: utf-8 -*-
"""Verify collective commerce outlet/personnel continuation from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCHES = {
    "LYG-中-T071": {
        "title": "1981~1990年连云港市集体商业网点人员数（续表）",
        "table_number": "表33-3",
        "page": 1546,
        "pages": [1546],
        "columns": ["行业", "地区", "项目", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990"],
        "rows": [
            ["饮食业", "市区", "网点", "135", "204", "230", "234", "255", "267", "289", "319", "323", "314"],
            ["饮食业", "市区", "人员", "1079", "1344", "2071", "2194", "2329", "2633", "2224", "2320", "2237", "2381"],
            ["饮食业", "赣榆", "网点", "53", "80", "88", "95", "117", "127", "132", "135", "143", ""],
            ["饮食业", "赣榆", "人员", "346", "827", "567", "568", "813", "927", "1003", "892", "1087", ""],
            ["饮食业", "东海", "网点", "82", "88", "83", "78", "122", "109", "89", "106", "107", ""],
            ["饮食业", "东海", "人员", "805", "1001", "998", "901", "702", "701", "572", "594", "658", ""],
            ["饮食业", "灌云", "网点", "108", "129", "124", "130", "109", "106", "109", "112", "103", ""],
            ["饮食业", "灌云", "人员", "536", "732", "851", "973", "473", "465", "497", "532", "497", ""],
            ["服务业", "市区", "网点", "255", "219", "252", "273", "306", "326", "299", "313", "331", "286"],
            ["服务业", "市区", "人员", "1234", "1628", "1763", "1992", "2566", "2237", "2427", "2430", "2340", ""],
            ["服务业", "赣榆", "网点", "79", "126", "91", "127", "149", "179", "180", "141", "143", ""],
            ["服务业", "赣榆", "人员", "381", "576", "191", "250", "597", "647", "668", "534", "557", ""],
            ["服务业", "东海", "网点", "212", "236", "341", "72", "141", "125", "149", "104", "99", ""],
            ["服务业", "东海", "人员", "1020", "1092", "1198", "267", "518", "616", "715", "413", "409", ""],
            ["服务业", "灌云", "网点", "103", "106", "122", "131", "140", "133", "138", "142", "127", ""],
            ["服务业", "灌云", "人员", "338", "378", "427", "543", "415", "404", "479", "531", "483", ""],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0126.txt。该页为表33-3续表，续录饮食业、服务业两类；源页 OCR 未给出部分1990年列数值，按源可见文本保留空白。",
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

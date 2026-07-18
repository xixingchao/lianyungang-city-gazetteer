# -*- coding: utf-8 -*-
"""Verify table 41-10 party committee members from page OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

COLUMNS = ["姓名", "任职时间"]

PATCHES = {
    "LYG-中-T116": {
        "title": "历任市委常委表",
        "table_number": "表41-10",
        "page": 1849,
        "pages": [1849],
        "columns": COLUMNS,
        "rows": [
            ["梁如仁", "1953.8~1955.1"],
            ["许耀林", "1953.8~1959.2"],
            ["冯克玉", "1955.1~1959.2"],
            ["方进", "1953.8~1955.6"],
            ["杨祖彤(女)", "1953.8~1955.4"],
            ["王兴", "1953.8~1954.2"],
            ["杨玉生", "1955.5~1959.2"],
            ["余晋康", "1955.5~1959.2"],
            ["王儒现", "1955.5~1956.1"],
            ["郑鹤", "1956.5~1959.2"],
            ["周思德", "1956.5~1959.2"],
            ["张绍山", "1956.5~1959.2"],
            ["陈心文", "1956.5~1959.2"],
            ["田诚", "1963.4~1971.6"],
            ["许耀林", "1963.4~1966.3"],
            ["祝斌", "1963.4~1966.3"],
            ["宋鲁峰", "1963.4~1965.7"],
            ["杨玉生", "1965.7~1975.11"],
            ["毛光彩", "1965.7~1979.4"],
            ["张绍山", "1965.7~1971.6"],
            ["陈心文", "1965.7~1975.10"],
            ["林永", "1965.7~1971.6"],
            ["郑鹤", "1965.7~1971.6"],
            ["张国安", "1971.6~1972.10"],
            ["刘文龙", "1971.6~1974.2"],
            ["高心意", "1971.6~1981.8"],
            ["杨鸿儒", "1971.6~1974.10"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0429.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T116_1849.txt。表题和表号位于本页；原表为三组姓名/任职时间横排，本轮展开为两列。页首含表41-9续表尾段，本轮仅录入表41-10首页。",
    },
    "LYG-中-T117": {
        "title": "历任市委常委表（续表）",
        "table_number": "表41-10",
        "page": 1850,
        "pages": [1850],
        "columns": COLUMNS,
        "rows": [
            ["耿志英(女)", "1971.6~1983.2"],
            ["于同祯", "1971.6~1974.10"],
            ["王成瑞", "1971.6~1972.12"],
            ["刘强", "1971.6~1974.9"],
            ["曹良友", "1971.6~1972.12"],
            ["徐河均", "1973.8~1983.2"],
            ["金逊", "1974.2~1977.5"],
            ["姚远", "1974.4~1977.9"],
            ["祝斌", "1974.4~1975.11"],
            ["徐智", "1975.11~1976.10"],
            ["李敬松", "1975.11~1976.10"],
            ["邱效周", "1975.11~1983.2"],
            ["王遐松", "1976.3~1983.2"],
            ["林永", "1975.12~1983.2"],
            ["叶志俊", "1977.1~1983.2"],
            ["耿杰民", "1977.5~1983.2"],
            ["雷成堂", "1977.5~1983.2"],
            ["谢克东", "1977.11~1978.4"],
            ["徐智", "1979.4~1980.11"],
            ["李敬松", "1979.4~1984.7"],
            ["张绍云", "1979.4~1983.2"],
            ["杜树森", "1979.4~1983.2"],
            ["胡为德", "1981.4~1989.10"],
            ["朱传信", "1981.11~1983.9"],
            ["何仁华", "1983.2~1986.5"],
            ["李登先", "1983.2~1986.1"],
            ["鲁少时", "1983.2~1986.1"],
            ["龚来宝", "1983.2~"],
            ["俞素娥(女)", "1983.2~"],
            ["张洪儒", "1983.9~1986.5"],
            ["季允石", "1984.7~1989.9"],
            ["郑申雄", "1984.7~1988"],
            ["唐贯淮", "1984.7~"],
            ["徐沙", "1984.10~1986.5"],
            ["耿广义", "1985.11~1988"],
            ["王稳卿", "1987.2~"],
            ["宋开智", "1987.2~"],
            ["吴炳裔", "1988.6~"],
            ["戴镇基", "1988.12~"],
            ["秦兆祯", "1989.10~"],
            ["马全珍", "1989.10~"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0430.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T117_1850.txt。本页为表41-10续上表，原表为三组姓名/任职时间横排，本轮展开为两列。唐贯淮姓名按页级OCR录入，raw OCR作“唐贯准”未采。",
    },
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

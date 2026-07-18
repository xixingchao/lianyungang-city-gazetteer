# -*- coding: utf-8 -*-
"""Verify foreign contracting and labor cooperation project table T093."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"

PATCH = {
    "table_id": "LYG-中-T093",
    "title": "1987~1990年连云港市对外工程和劳务合作项目表",
    "table_number": "表35-10",
    "page": 1634,
    "pages": [1634],
    "part": "part02",
    "vol": "中",
    "volume": "中",
    "columns": [
        "序号",
        "国别(地区)",
        "项目名称",
        "对外签约年月",
        "对外签约单位",
        "项目实施单位",
        "开工年月",
        "完工年月",
        "派出人数(人)",
    ],
    "rows": [
        ["1", "科威特", "“417”住宅劳务", "1987.3", "中江公司", "东海一建", "1987.6", "1990.9", "215"],
        ["2", "西德", "厨师技术劳务", "1987.1", "中江公司", "市饮食公司", "1987.12", "1989.12", "1"],
        ["3", "喀麦隆", "水利专家劳务", "1987.10", "中江公司", "市水利局", "1988.1", "1990.1", "4"],
        ["4", "贝宁", "公路石工劳务", "1987.11", "中江公司", "海州区水建公司", "1988.2", "1990.2", "1"],
        ["5", "日本", "木工劳务研修", "1987.12", "中江公司", "市三建公司", "1988.3", "1988.9", "1"],
        ["6", "西德", "厨师技术劳务", "1988.1", "中江公司", "市饮食公司", "1989.11", "1991.11", "1"],
        ["7", "贝宁", "公路翻译劳务", "1987.11", "中江公司", "市外办", "1989.4", "1991.4", "1"],
        ["8", "伊拉克", "船闸司机", "1988.5", "中江公司", "市轻工进出口公司", "1989.7", "1990.9", "52"],
        ["9", "伊朗", "渔业合作捕捞", "1988.8", "上海国际公司", "市渔业公司", "1989.1", "1991.5", "4"],
        ["10", "突尼斯", "养虾合作试验", "1988.10", "中国水产联合总公司", "赣榆县水产局", "1989.2", "1991.2", "37"],
        ["11", "伊拉克", "管道工程劳务", "1989.5", "中江公司", "东海一建", "1989.7", "1990.3", "1"],
        ["12", "伊拉克", "水泥厂技术劳务", "1989.1", "国家建材局", "东海建材", "1989.5", "1991.5", "1"],
        ["13", "西德", "厨师技术劳务", "1989.5", "中江公司", "市饮食公司", "1990.2", "1992.2", "1"],
        ["14", "日本", "厨师劳务", "1989.7", "市经联公司", "北京饭庄", "1990.7", "1991.7", "1"],
        ["15", "西德", "厨师技术劳务3批", "1989.7", "中江公司", "市饮食公司", "1990.3", "1992.3", "4"],
        ["16", "扎伊尔", "O-W公路翻译", "1989.1", "交通部一局", "赣榆县档案馆", "1990.4", "1992.4", "1"],
        ["17", "巴基斯坦", "磷化铝项目劳务", "1990.2", "浙江国际公司", "市化工厂", "1990.7", "1991.2", "5"],
        ["18", "西德", "厨师技术劳务", "1990.7", "中江公司", "陇海饭店", "1990.11", "1992.11", "1"],
        ["19", "日本", "劳务研修", "1990.10", "省交流公司", "连云港涤纶厂", "1990.12", "1991.12", "4"],
    ],
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0204.txt。原JSON为单列骨架且标题误抽为仪器仪表接插件；跨行单位名称按源页版面合并。",
}
PATCH["row_count"] = len(PATCH["rows"])
PATCH["col_count"] = len(PATCH["columns"])


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != PATCH["table_id"]:
        return False
    changed = False
    for key, value in PATCH.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json() -> int:
    path = DATA_DIR / f"{PATCH['table_id']}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if not patch_entry(data):
        return 0
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 1


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise SystemExit("TABLES payload not found")
    tables = json.loads(match.group(1))
    changed = sum(1 for table in tables if patch_entry(table))
    if changed:
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    print(f"json_files_changed={patch_json()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()

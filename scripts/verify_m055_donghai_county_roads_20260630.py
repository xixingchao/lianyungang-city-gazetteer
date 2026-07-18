# -*- coding: utf-8 -*-
"""Verify Donghai county road overview table T055."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T055.json"

COLUMNS = [
    "类别",
    "起讫站点",
    "经过集镇",
    "里程(公里)",
    "路面宽度(米)",
    "修筑年份",
    "路面结构",
    "等级",
]

ROWS = [
    ["新牛线", "张道口一东临复线", "包庄、白塔埠、曹浦", "32.2", "14", "1987", "沙石", "2"],
    ["徐海线", "曹庄西一吉庄", "曲阳、牛山、房山", "53.8", "", "1979", "沙石", "2"],
    ["牛许线", "牛山一许沟", "马圩、双店、三铺", "29.1", "", "1965", "碎石", "3"],
    ["石辰线", "石榴一南辰", "横沟、三合村、涝村", "23.6", "", "", "沥青", "3~4"],
    ["桃线", "药材厂后堤一桃林", "石湖、陈栈", "", "", "1979", "", "4"],
    ["洪夏线", "洪庄一界沟", "双店、李埝", "29.2", "", "1970", "沥青", "3"],
    ["王洪线", "埝河一洪门西", "驼峰、白塔埠、包庄", "33.6", "", "1978", "沙石", "4"],
    ["307附线", "石梁河一水漫桥", "石梁河、黄川", "25.8", "", "1966", "", "4"],
    ["青浦线", "青湖一浦南", "时湖、陈墩、新建", "26.0", "", "1985", "", "3"],
    ["韩辰线", "韩湖一南辰", "葛沟、贾庄", "10.8", "", "1979", "简易沙石", "4"],
    ["埝刘线", "埝河一黄庄", "", "8.0", "", "1988", "沙石", "4"],
    ["石泉线", "石榴一姜庄", "浦西、博汪", "8.0", "", "1980", "沙石", "3"],
    ["湖泉线", "石湖一温泉", "金塘", "6.0", "", "1980", "沙石", "4"],
    ["温泉线", "马圩一朱沟北", "尹湾、温泉", "12.0", "", "1978", "沥青沙石", "3"],
    ["洪石线", "洪庄一上河", "塔桥、徐东、陈川", "19.2", "", "1987", "沙石", "4"],
    ["徐许线", "徐塘庄一许沟", "桃林、山左口", "24.5", "", "1967", "沙石", "4"],
    ["曹白线", "曹庄一白塔埠", "桃李、南湾、张井", "22.3", "", "1985", "沙石", "4"],
    ["赣沭线", "墩尚一沭河桥、平明、汤庄", "包庄、张湾", "30.3", "", "1985", "", "3~4"],
    ["白平线", "白塔大桥一平塔桥", "纪荡、周徐", "10.5", "", "1978", "沙石", "4"],
    ["平顾线", "平明一大顾", "马汪、关墩、南场", "12.5", "", "1984", "沙石", "4"],
    ["房汤线", "房山一汤庄", "瓦基、关墩、上房", "22.5", "", "1986", "沙石", "4"],
    ["新海线", "黑阜一草街", "阜塘、安峰", "19.5", "", "1982", "沙石", "4"],
    ["新海东线", "草街一邱庄", "", "12.6", "", "1983", "沙石", ""],
    ["曹安线", "曹浦一安峰", "薛埠", "12.0", "", "1966", "沙石", "3"],
    ["安石线", "安峰一石灰埠", "", "7.8", "", "1982", "沙石", "4"],
    ["毛北线", "种马场一小塘庄", "毛北", "6.3", "", "1983", "沙石", "4"],
    ["北环城路", "英疃一湖西桥", "化肥厂、王东", "7.2", "", "1989", "沙石", "2"],
]

PATCH = {
    "table_id": "LYG-中-T055",
    "title": "1990年东海县县级公路概况表",
    "table_number": "表30-3",
    "page": 1444,
    "pages": [1444, 1445],
    "part": "part02",
    "vol": "中",
    "volume": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：表题、表号、表头和首页主体见 workbench/ocr/paddle_ocr/中/part02/page_0024.txt；续行见 workbench/ocr/paddle_ocr/中/part02/page_0025.txt，并参考 raw OCR workbench/table_entries/中/raw/LYG-中-T055_1444.txt。原JSON为单列骨架；本次录入东海县表可见 27 条记录，page_0025 中灌云县新表未并入本条。源页未清晰给出的路面宽度、修筑年份或路面结构保留空值。",
}


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

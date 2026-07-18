# -*- coding: utf-8 -*-
"""Verify import equipment/product continuation pages T082-T083."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"
COLUMNS = ["单位", "项目(单机)名称", "金额(万美元)"]

PATCHES = {
    "LYG-中-T082": {
        "title": "1984~1990年连云港市进口设备和产品情况表（续表）",
        "table_number": "表35-5",
        "page": 1612,
        "pages": [1612],
        "part": "part02",
        "vol": "中",
        "volume": "中",
        "columns": COLUMNS,
        "rows": [
            ["市纺织工业公司系统", "针织和染整设备", "171.80"],
            ["市纺织工业公司系统", "毛纺旧设备", "294.03"],
            ["市纺织工业公司系统", "涤纶长丝成套设备", "718.73"],
            ["市纺织工业公司系统", "差量喂料机", "4.16"],
            ["市纺织工业公司系统", "FK6加弹机", "79.55"],
            ["市纺织工业公司系统", "涤纶长丝高速纺", "261.76"],
            ["市纺织工业公司系统", "加弹机备件", "10.10"],
            ["市纺织工业公司系统", "剑杆织机等设备", "48.80"],
            ["市纺织工业公司系统", "割绒刀", "2.08"],
            ["市纺织工业公司系统", "经纬编织机", "15.33"],
            ["市纺织工业公司系统", "经纬编织机", "27.20"],
            ["市纺织工业公司系统", "经纬编织机", "43.22"],
            ["市纺织工业公司系统", "高温溢流染色设备", "109.42"],
            ["市纺织工业公司系统", "毛衣生产设备", "18.66"],
            ["市纺织工业公司系统", "扩大羊衫生产设备", "12.33"],
            ["市纺织工业公司系统", "高级虎板剪机", "5.97"],
            ["市纺织工业公司系统", "氨纶包缠纱", "48.60"],
            ["市纺织工业公司系统", "意大利剑杆织机", "45.00"],
            ["市纺织工业公司系统", "浆染纱联合机", "24.50"],
            ["市纺织工业公司系统", "剑杆织机及配套设备", "164.37"],
            ["市纺织工业公司系统", "包缝机", "1.20"],
            ["市纺织工业公司系统", "西装时装生产线", "24.46"],
            ["市纺织工业公司系统", "干洗机", "1.97"],
            ["市纺织工业公司系统", "衫衣生产设备", "22.50"],
            ["市纺织工业公司系统", "服装生产线", "11.47"],
            ["市经济联合开发公司", "项目1 单机2", "413.50"],
            ["市经济联合开发公司", "货船", "129.00"],
            ["市经济联合开发公司", "空调器整机", "14.5"],
            ["市经济联合开发公司", "设备", "270.00"],
            ["市化工公司", "项目3", "180.24"],
            ["市化工公司", "热熔胶生产线115/65", "31.46"],
            ["市化工公司", "热熔涂复机HCL-110", "37.98"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0192.txt。表题、表号和列组依据前页表35-5；原JSON为单列骨架且标题误抽。页内单位按版面分组填充。",
    },
    "LYG-中-T083": {
        "title": "1984~1990年连云港市进口设备和产品情况表（续表）",
        "table_number": "表35-5",
        "page": 1613,
        "pages": [1613],
        "part": "part02",
        "vol": "中",
        "volume": "中",
        "columns": COLUMNS,
        "rows": [
            ["市化工公司", "活性炭", "110.80"],
            ["市轻工公司系统", "项目18 单机4", "1923.32"],
            ["市轻工公司系统", "芦笋、果蔬罐头", "34.03"],
            ["市轻工公司系统", "冰淇淋生产线", "12.90"],
            ["市轻工公司系统", "SKN2205斩拌机", "4.01"],
            ["市轻工公司系统", "汽水生产线", "85.86"],
            ["市轻工公司系统", "电阻焊生产线", "53.00"],
            ["市轻工公司系统", "低克重纸机", "171.70"],
            ["市轻工公司系统", "温巾纸制造机", "4.30"],
            ["市轻工公司系统", "妇女卫生巾生产线", "16.85"],
            ["市轻工公司系统", "生活用纸", "32.59"],
            ["市轻工公司系统", "每年18万令彩印设备", "40.70"],
            ["市轻工公司系统", "法式面包生产线", "10.43"],
            ["市轻工公司系统", "复合纸板和纸制容器", "100.43"],
            ["市轻工公司系统", "葡萄酒灌装设备", "49.84"],
            ["市轻工公司系统", "葡萄酒生产设备", "71.34"],
            ["市轻工公司系统", "葡萄酒过滤设备", "2.06"],
            ["市轻工公司系统", "板式家具", "18.73"],
            ["市轻工公司系统", "板式家具", "43.20"],
            ["市轻工公司系统", "NA-03丹麦制钉机", "16.15"],
            ["市轻工公司系统", "啤酒生产线", "685.00"],
            ["市轻工公司系统", "麦芽生产设备", "401.00"],
            ["市轻工公司系统", "啤酒包装线", "60.70"],
            ["市轻工公司系统", "汽车", "8.50"],
            ["市粮食局系统", "项目2", "288.19"],
            ["市粮食局系统", "年产450吨面包设备", "22.00"],
            ["市粮食局系统", "面粉加工设备", "266.19"],
            ["市旅游公司系统", "项目1 单机1", "20.73"],
            ["市旅游公司系统", "室内电器设备", "14.95"],
            ["市旅游公司系统", "麦士冲印系统", "5.78"],
            ["市交通局系统", "单机1", "86.70"],
            ["市交通局系统", "汽车", ""],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0193.txt。表题、表号和列组依据前页表35-5；原JSON为单列骨架且标题误抽。页内单位按版面分组填充；末行汽车金额源页未见，保留空值。",
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

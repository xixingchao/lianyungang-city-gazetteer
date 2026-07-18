# -*- coding: utf-8 -*-
"""Verify import equipment/product continuation pages T084-T085."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"
COLUMNS = ["单位", "项目(单机)名称", "金额(万美元)"]

PATCHES = {
    "LYG-中-T084": {
        "title": "1984~1990年连云港市进口设备和产品情况表（续表）",
        "table_number": "表35-5",
        "page": 1614,
        "pages": [1614],
        "part": "part02",
        "vol": "中",
        "volume": "中",
        "columns": COLUMNS,
        "rows": [
            ["市机械局系统", "项目3 单机2", "606.63"],
            ["市机械局系统", "硅钢片剪切生产线", "316.44"],
            ["市机械局系统", "波纹油箱生产线(液压升降台)", "98.97"],
            ["市机械局系统", "漆包线加工设备(锯床)", "2.30"],
            ["市机械局系统", "合资经营生产水表", "188.92"],
            ["市商业局", "项目4 单机2", "179.87"],
            ["市商业局", "清凉饮料", "109.78"],
            ["市商业局", "定量包装机", "4.94"],
            ["市商业局", "方便面生产线", "29.00"],
            ["市商业局", "万能糕点机", "4.00"],
            ["市商业局", "自动包馅机", "13.01"],
            ["市商业局", "海带加工设备", "19.14"],
            ["市医药公司系统", "项目1", ""],
            ["市医药公司系统", "药用铝箔生产装置", "407.13"],
            ["市广播电视局系统", "单机5", "28.01"],
            ["市广播电视局系统", "摄录设备", "7.82"],
            ["市广播电视局系统", "摄录设备", "2.60"],
            ["市广播电视局系统", "摄录设备", "2.65"],
            ["市广播电视局系统", "摄录设备", "8.41"],
            ["市广播电视局系统", "摄录、立体音响设备", "6.53"],
            ["市邮电局系统", "项目3", "272.62"],
            ["市邮电局系统", "程控交换机", "145.00"],
            ["市邮电局系统", "通电", "120.02"],
            ["市邮电局系统", "集体装箱交换机", "7.60"],
            ["市建材局系统", "项目1", ""],
            ["市建材局系统", "复合纤维", "92.89"],
            ["市皮塑公司系统", "项目10 单机7", "682.58"],
            ["市皮塑公司系统", "聚乙烯渔网", "65.93"],
            ["市皮塑公司系统", "PVC饮用水管", "40.01"],
            ["市皮塑公司系统", "KBSU-ICOS吹塑机组", "56.65"],
            ["市皮塑公司系统", "塑料复合膜", "81.00"],
            ["市皮塑公司系统", "人造革压花辊", "1.31"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0194.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T084_1614.txt。表题、表号和列组依据前页表35-5；原JSON为单列骨架且标题误抽。页内单位按版面分组向下填充，源页未见金额的汇总行保留空值。",
    },
    "LYG-中-T085": {
        "title": "1984~1990年连云港市进口设备和产品情况表（续表）",
        "table_number": "表35-5",
        "page": 1615,
        "pages": [1615],
        "part": "part02",
        "vol": "中",
        "volume": "中",
        "columns": COLUMNS,
        "rows": [
            ["市皮塑公司系统", "冲击强度试验仪", "0.47"],
            ["市皮塑公司系统", "PU软泡高级床垫", "45.44"],
            ["市皮塑公司系统", "HDPE袋生产线", "4.57"],
            ["市皮塑公司系统", "HDPE背心袋设备", "6.88"],
            ["市皮塑公司系统", "PVC板材生产线", "190.00"],
            ["市皮塑公司系统", "双色注塑鞋流水线", "36.37"],
            ["市皮塑公司系统", "挤水伸展机", "8.40"],
            ["市皮塑公司系统", "片皮机", "8.53"],
            ["市皮塑公司系统", "震荡拉软机", "3.40"],
            ["市皮塑公司系统", "削匀机", "5.50"],
            ["市皮塑公司系统", "发泡挤出设备", "12.12"],
            ["市皮塑公司系统", "尼龙拉链生产线", "116.00"],
            ["赣榆县", "项目2 单机4", "181.50"],
            ["赣榆县", "旅游鞋生产线", "36.22"],
            ["赣榆县", "饮料加工设备", "123.80"],
            ["赣榆县", "缝纫机械", "1.75"],
            ["赣榆县", "缝纫机械", "6.48"],
            ["赣榆县", "塑料加工机械", "7.60"],
            ["赣榆县", "缝纫机械", "5.65"],
            ["东海县", "项目3", "233.47"],
            ["东海县", "塑料门窗生产线", "123.96"],
            ["东海县", "五棱镜生产线", "75.88"],
            ["东海县", "花生酱生产线", "33.63"],
            ["灌云县", "单机1", ""],
            ["灌云县", "注塑机", "2.00"],
            ["市开发区", "项目2", "45.50"],
            ["市开发区", "高尔夫彩色立体印刷设备", "32.00"],
            ["市开发区", "污水处理设备", "13.50"],
            ["连云港碱厂", "60万吨/年纯碱装置", "320.08"],
            ["市工艺美术公司系统", "项目4 单机4", "232.44"],
            ["市工艺美术公司系统", "项链生产线", "9.00"],
            ["市工艺美术公司系统", "项链设备", "2.30"],
        ],
        "status": "verified",
        "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0195.txt，并参考 raw OCR：workbench/table_entries/中/raw/LYG-中-T085_1615.txt。表题、表号和列组依据前页表35-5；原JSON为单列骨架且标题误抽。页内单位按版面分组向下填充，源页未见金额的汇总行保留空值。",
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

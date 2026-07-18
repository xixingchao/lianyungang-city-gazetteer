#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T027 — 年新沭河连云港市境内穿堤建筑物情况表
页: [571, 573]
卷: 第八卷 章: 经济综合管理
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T027"
TITLE = """年新沭河连云港市境内穿堤建筑物情况表"""
PAGES = [571, 573]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_571 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
1990年新沭河连云港市境内穿堤建筑物情况表
表10-3
工程
规模
设计流量
地点
孔宽
顶高程
底高程
建筑物名称
年份
立方米/秒）
(个)
(米)
(米)
(米)
(米)
(米)
1.0
1.5
16.5
15.0
1.58
李曹埠电排涵
大岭乡
1.0
1.5
16.0
14.5
西赤金电排涵
1.5
15.5
14.0
前赤金电排涵
2.0
0.83
张庄电排涵
14.5
1.0
1.5
13.0
沙河镇
1.2
1.8
8.6
7.0
蒋庄军垦涵洞
8.6
7.0
1.2
1.8
沐北放水涵洞
10.0
9.9
6.0
- 1.0
沐北通航闸
排碱涵洞
1.5
1.8
"""


def verify_and_export():
    reader = csv.reader(io.StringIO(VERIFIED_CSV))
    header = next(reader, [])
    if header and header != COLUMNS:
        print(f"警告: CSV 表头与 COLUMNS 不匹配")
        print(f"  CSV: {header}")
        print(f"  COL: {COLUMNS}")
    rows = list(reader)
    print(f"{TABLE_ID} {TITLE.strip()}")
    cols = len(COLUMNS)
    print(f"  页: {PAGES}")
    print(f"  列数: {cols}")
    print(f"  数据行数: {len(rows)}")

    # 输出 JSON
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    entry = {
        "table_id": TABLE_ID,
        "title": TITLE.strip(),
        "pages": PAGES,
        "columns": COLUMNS,
        "rows": rows,
        "status": "draft",
    }
    out_path = data_dir / f"{TABLE_ID}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)
    print(f"  输出: {out_path}")

if __name__ == "__main__":
    verify_and_export()

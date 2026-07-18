#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T028 — 立方米，设计灌溉农田27.91万亩，实灌21.02万亩。1990年连云港市中型水库主要建筑物情况表
页: [581, 582, 583, 584, 585, 586, 587, 588]
卷: 第八卷 章: 经济综合管理
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T028"
TITLE = """立方米，设计灌溉农田27.91万亩，实灌21.02万亩。1990年连云港市中型水库主要建筑物情况表"""
PAGES = [581, 582, 583, 584, 585, 586, 587, 588]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_581 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
湾、高捻、场东水库；赣榆县建成徐山、新西、万桥1号、西陡岭、刘山、北康邑、临马疃、宋
岭、佃马厂、车辐山、大树、石埠、八一、狼山、介河、沟窝、狼窝、范良庄、竹园、下沟、姜林水
库；市郊区建成宿城、王庄、云门、胡沟、当路、张庄、李庄水库。1970年冬开始，境内进行农业学大寨运动，为改变山丘区农田易旱低产面貌，大搞蓄
水保水工程。至1975年春，东海县建成种马场、石寨、前贤、孟中、上河、后贤、朱州、龙口、
季岭、鲁庄、娄山、狼墩水库；赣榆县建成郭葛埠、石门沟、马山、申瞳、谢湖、谭湖、吴沟水
库；市郊区建成朝阳、胜利水库。1975年8月，市郊区和东海、赣榆县开始按照国家水电部颁发的水库标准，对全部水
库进行分类，逐个进行调洪核算，淘汰6座不合标准的小水库。1976年后，为提高水库防洪标准，分期分批对小水库进行除险加固工程，并兴建梯级
截水河道、截洪沟、翻水站，以河为“藤”，以库为“瓜”长藤结瓜串连大、中、小水库，蕃、引、
提、调相结合，全面提高水库调蓄能力。在此期间，赣榆县新建怀仁山、白石头水库。至1990年，全市共建成小水库136座，合计总库容14277万立方米，兴利库容8911万
立方米，设计灌溉农田27.91万亩，实灌21.02万亩。1990年连云港市中型水库主要建筑物情况表
表10-6
(米)
泄洪涵
水库名称
设计量
坝顶长度
坝顶高程
坝顶宽度
树底高程
最大坝高
孔净高
顶高程
大流量
名称
名称
(立方
(个)
(米)
(米)
(米)
米/秒)
(米)
八条路
北溢洪闸
4.0
30.0
大坝
34.7
13.4
4.0
内溢洪闸
30.0
溢洪闸
2.5
25.9
横沟
大坝
30.5
12.5
2.0
泄洪涵洞
2.6
22.5
主坝
8.2
13.0
溢洪闸
2.0
9.15
房山
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

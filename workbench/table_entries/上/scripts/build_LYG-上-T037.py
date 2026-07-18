#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T037 — ~1990年淮北盐区原盐销量统计表
页: [767, 768]
卷: 第十二卷 章: 工业
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T037"
TITLE = """~1990年淮北盐区原盐销量统计表"""
PAGES = [767, 768]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_767 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
1949~1990年淮北盐区原盐销量统计表
表13-14
单位：万吨
食盐
储备盐
合计
年份
出口盐
农用盐
工业盐
渔用盐
42. 19
41.64
0.55
46.01
46.36
0.35
0.59
43.76
42.23
0.94
54.15
55.87
0.17
1.55
72.76
70.49
0.53
1.74
0.73
2.84
70.45
66.88
65.39
0.03
2.65
0.28
68.35
79.80
2.35
86.47
1.31
3.01
8.27
82.38
69.88
1.26
2.97
3.07
96.17
8.83
1.29
82.98
9.17
6.97
97.38
11.53
125.05
5.31
90.09
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T004 — 第175页表格
页: [175, 176, 177]
卷: 第一卷 章: 自然环境
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T004"
TITLE = """第175页表格"""
PAGES = [175, 176, 177]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_175 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
续上表
站年
灾害
发生
年量
最大
发生
年雨量
百期
日期
性质
（月·日）
（月·日）
日雨量
高水位
28.2
29.4
18.2
78.8
117.6
243.4
13.2
10.7
60.8
47.9
17.2
27.7
693.1
91.5
7.21
37.9
0.6
32.3
38.9
7.80
11.3
76.8
169.7
80.7
76.0
30.4
12.8
575.2
69.0
10.26
71.2
115.5
88.3
22.1
35.2
17.5
9.4
27.9
110.1
138.8
35.9
3.2
675.1
69.2
9.23
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

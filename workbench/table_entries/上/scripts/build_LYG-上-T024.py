#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T024 — 第533页表格
页: [533, 534]
卷: 第八卷 章: 经济综合管理
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T024"
TITLE = """第533页表格"""
PAGES = [533, 534]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_533 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
续上表
粮食
年份
总产
总产
总产
面积
平均亩产
平均亩产
面积
平均亩产
(吨)
(吨)
(万亩)
(公斤）
(吨)
(公斤)
(万亩)
(公斤)
(万亩)
15.9
40.09
1.5
90.5
743.89
45.52
18.5
91.0
2.62
763.00
7.44
87.0
58.39
66.0
769.20
48.17
53.5
5.31
17.8
64.5
690.57
71.5
7.63
31.64
632.64
88.5
5.89
24.49
11.5
75.5
551.86
583.10
21.48
14.41
6.36
12.5
15.34
691.62
5.39
12.0
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

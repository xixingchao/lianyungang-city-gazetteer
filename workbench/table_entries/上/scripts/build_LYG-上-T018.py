#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T018 — 元，国内生产总值501403万元，工农业总产值559131万元。1949~1990年连云港市工农业总产值及构成表
页: [433, 434]
卷: 第六卷 章: 环境保护
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T018"
TITLE = """元，国内生产总值501403万元，工农业总产值559131万元。1949~1990年连云港市工农业总产值及构成表"""
PAGES = [433, 434]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_433 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
元，国内生产总值501403万元，工农业总产值559131万元。1949~1990年连云港市工农业总产值及构成表
表7-1
工农业产值（万元）
成（%)
年份
总产值
工业总产值
工业总产值
农业总产值
农业总产值
26.0
74.0
26.1
73.9
32.9
67.1
27.7
72.3
68.5
31.5
23.7
76.3
36.9
63.1
27.9
72.1
34.2
65.8
40.1
59.9
51.9
48.1
54.6
45.4
46.1
53.9
46.7
53.3
33.9
66.1
28.9
71.1
44.0
56.0
43.7
56.3
40.2
59.8
30.9
69.1
23.7
76.3
41.9
58.1
46.7
53.3
46.4
53.6
44.2
55.8
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

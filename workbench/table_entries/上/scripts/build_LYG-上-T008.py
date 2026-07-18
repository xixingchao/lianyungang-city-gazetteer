#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T008 — 第290页表格
页: [290]
卷: 第四卷 章: 人口
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T008"
TITLE = """第290页表格"""
PAGES = [290]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_290 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
续上表
按性别分
（以总人口为100)
年末总人口
年份
（万人）
性别比
男(万人)
女(万人)
(以女性为100)
102.76
50.70
274.54
139.14
49.30
135.40
275.50
50.50
49.50
136.28
102. 16
139.22
49.40
50.60
278.64
140.91
137.73
102.31
140.39
102.19
50.50
143.47
49.50
283.86
49.30
142.80
102.82
50.70
289.63
146.83
50.90
49.10
292.45
148.78
143.67
103.56
151,29
51.10
296.25
144.96
104.37
48.90
51.30
154.06
146.57
105.11
48.70
300.63
305.27
156.69
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

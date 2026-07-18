#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T020 — 生产总值的比重分别为45.2%、26.9%和27.9%。1978~1990年连云港市国内生产总值结构表
页: [445, 447, 448]
卷: 第六卷 章: 环境保护
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T020"
TITLE = """生产总值的比重分别为45.2%、26.9%和27.9%。1978~1990年连云港市国内生产总值结构表"""
PAGES = [445, 447, 448]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_445 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
增15.1%，第二产业年均递增11.3%，第三产业年均递增19.3%。一、二、三产业占国内
生产总值的比重分别为45.2%、26.9%和27.9%。1978~1990年连云港市国内生产总值结构表
表7-9
第二产业
第三产业
第一产业
国内生
、构
产总值
总值
总值
总值
占比重
占比重
占比重
（万元）
(%)
（万元）
(%)
（万元）
(%)
（万元）
43.6
38.8
17.6
45.3
36.9
17.8
17.6
46.1
36.3
47.6
34.8
17.6
49.8
31.5
18.7
48.8
31.6
19.6
31.1
47.8
21.1
45.3
30.2
24.5
46.8
29.6
23.6
23.8
45.8
30.4
44.5
29.2
26.3
28.8
26.5
44.7
27.9
45.2
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

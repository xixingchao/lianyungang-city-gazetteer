#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T003 — 内陆，是连云港市盐场晒盐的极好时机。连云港市各月平均蒸发量表
页: [159, 162, 164]
卷: 第一卷 章: 自然环境
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T003"
TITLE = """内陆，是连云港市盐场晒盐的极好时机。连云港市各月平均蒸发量表"""
PAGES = [159, 162, 164]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_159 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
气候
第四章
续上表
540分
720分
1440 分
定时一
60分
90分
定时一
120分
180分
240分
360分
年份5分10分
45分
15分
20分
30分
(1.5时）
(2时)
日最大
月最大
(1时)
(3时)
(6时)
(4时)
(9时)
(12时)
(24时）
122.3
324.5
7月
12.816.921.928.040.4|49.852.6
86.4100.7109.9117.5125.7
55.0
60.9
72.7
(7月）
9日
132.0
234.7
63.673.692.9124.1130.6
5月
43.0
5.27
198510.016.017.219.0|22.723.931.3
38.0
(7月）
3日
98.7
276.9
198611.0|14.616.518.019.119.221.528.5
7月
35.8
50.0
98.5
61.0/8
98.5
81.2
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T023 — 第513页表格
页: [513, 514]
卷: 第八卷 章: 经济综合管理
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T023"
TITLE = """第513页表格"""
PAGES = [513, 514]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_513 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
续上表
117.6
111.0
112.2
120.5
131.8
100.9
肉禽蛋
101.4
104.2
126.1
105.5
水产品
106.1
130.7
164.4
131.5
109.0
107.3
110.5
100.4
111.2
调味品
100.0
100.0
103.4
106.3
120.1
食糖
100.0
100.0
100.0
100.0
127.4
118.3
108.1
100.0
100.7
104.2
112.8
99.1
99.7
100.8
126.4
99.5
(3)烟酒类
133.4
100.0
100.0
100.0
100.0
100.0
111.7
98.1
109.8
112.3
100.0
99.8
102.1
102.1
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

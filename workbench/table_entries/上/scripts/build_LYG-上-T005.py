#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T005 — 连云港市沿海潮位站最高最低潮位统计表
页: [181]
卷: 第一卷 章: 自然环境
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T005"
TITLE = """连云港市沿海潮位站最高最低潮位统计表"""
PAGES = [181]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_181 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
连云港市沿海潮位站最高最低潮位统计表
表1-24
单位：米
站名
年最高潮位
年最低潮位
年最低潮位
年最高潮位
日期
日期
日期
日期
潮位
潮位
潮位
潮位
(月·日)
年份
(月·日)
(月·日）
（月·日）
1.5
5.57
- 1.58
2.18
1.5
3.38
0.08
1.14
9.1
4.3
- 1.40
5.68
3.60
7.1
11.28
0.00
5.96
3.84
7.2
- 1.43
4.4
7.2
- 0.14
1.17
8.2
- 1.52
12.1
5.82
0.02
3.45
8.2
1.16
6.5
6.5
- 1.52
10.19
3.78
5.89
- 0.40
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

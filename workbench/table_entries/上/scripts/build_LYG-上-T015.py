#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T015 — ~1990年部分年份连云港市废水及污染物排放情况表
页: [401, 402, 403, 404, 405, 408, 409, 410, 411, 412]
卷: 第六卷 章: 环境保护
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T015"
TITLE = """~1990年部分年份连云港市废水及污染物排放情况表"""
PAGES = [401, 402, 403, 404, 405, 408, 409, 410, 411, 412]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_401 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
: 346 :
1981~1990年部分年份连云港市废水及污染物排放情况表
表6-1
年份
排放量
工业废水排放量（万吨）
生活污水排放量（万吨）
化学耗氧量（吨）
0.136
0.136
0.024
0.024
总汞(吨)
0.278
0.252
0.365
0.212
总镉(吨)
0.005
0.385
0.713
7.420
1.160
0.583
1.822
1.033
0.256
六价铬（吨)
21.840
26.412
0.134
总砷(吨)
28.331
53.036
57.114
43.750
3.225
总铅(吨)
7.957
18.050
0.353
0.182
10.861
25.477
20.270
17.700
挥发酚（吨）
11.372
14.022
15.994
氰化物（吨)
16. 700
26.100
22.112
69.716
6.512
11.129
17.982
40.110
142.860
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

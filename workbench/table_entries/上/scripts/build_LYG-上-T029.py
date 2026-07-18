#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T029 — 年连云港市沭北样板控制河道基本情况表
页: [598, 599]
卷: 第九卷 章: 农林业
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T029"
TITLE = """年连云港市沭北样板控制河道基本情况表"""
PAGES = [598, 599]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_598 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
1990年连云港市沭北样板控制河道基本情况表
表10-13
河底高程
长度|排水」流量
河底宽」
堤项宽
堤顶高程
堤坡比
面积
河名
境内起迄位置
（平方（立方
(米)
(米)
(公里)
公里)米/秒)
(米)
(米)
7.5 ~ 15
塔山截洪沟夹谷山水库一小塔山水库
16.0
92.3
8.5
57.5 ~43.3
1:1 ~ 1:2
石梁河水
三清河一石梁河水库
11.0
37.3 ~ 24.4
119.0
16 ~ 21
6~8
1:2
库截洪沟
西段136
西段
沐北一级
夹谷山水库
9 ~ 25
13.0
8 ~ 10
43.2 ~ 32.4
东段83
截洪沟
四号渡槽一小塔山水库
49 ~ 40
上游段
老河长
30.0~9.7
17.7
137.5
沐北二级
石梁河水库一青口渡槽
12 ~ 35
1:2
6000 米
截洪沟
截洪沟口
18.88 ~ 16.34
1990年连云港市沭北主要控制涵闸基本情况表
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

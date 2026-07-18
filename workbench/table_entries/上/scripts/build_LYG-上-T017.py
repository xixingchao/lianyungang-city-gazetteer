#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T017 — 第四章 连云港市城市环境综合整治定量考核情况表
页: [428]
卷: 第六卷 章: 环境保护
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T017"
TITLE = """第四章 连云港市城市环境综合整治定量考核情况表"""
PAGES = [428]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_428 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
第四章 连云港市城市环境综合整治定量考核情况表
表6-19
指标值
考核项目
0.35
大气总悬浮微粒年日均值（毫克/立方米）
0.48
4.50
5.00
二氧化硫年日均值（毫克/立方米）
0.058
0.06
1.00
1.00
环境
100.00
99.00
6.00
7.00
质量
饮用水源水质达标率（%）
指标
11.40
城市地面水化学耗氧量平均值（毫克/升）
0.01
0.00
0.00
（37分）
9.00
区域环境噪声平均值（分贝A)
57.60
55.90
7.40
76.20
城市交通干线噪声平均值（分贝A)
72.20
1.90
3.50
烟尘控制区覆盖率（分贝A)
24.90
0.20
8.40
0.30
79.00
80.50
民用型煤普及率（%）
3.50
4.00
污染
万元产值工业废水排放量（吨/万元）
4.00
293.00
231.00
4.50
控制
指标
工业废水处理率（%）
22.30
40.80
0.50
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

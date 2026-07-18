#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T007 — .60万人。1949~1990年连云港市人口自然变动情况表
页: [282, 283, 284]
卷: 第四卷 章: 人口
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T007"
TITLE = """.60万人。1949~1990年连云港市人口自然变动情况表"""
PAGES = [282, 283, 284]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_282 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
:254:
续上表
年份
市区
总人口
赣榆县
东海县
灌云县
200.33
26.50
59.33
56.10
58.40
60.10
203.93
27.23
56.90
59.70
209.95
27.94
61.74
58.60
61.67
63.35
215.05
28.56
61.84
61.30
65.40
221.52
29.19
63.43
63.50
230.89
30.06
67.60
64.10
69.13
240.02
30.22
69.77
67.50
72.53
71.74
248.51
31.29
70.80
74.68
252.56
72.30
75.49
32.08
72.69
32.46
73.23
76.23
255.32
73.40
258.78
33.12
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T011 — ~1990年连云港市节约用水情况表
页: [366]
卷: 第五卷 章: 城乡建设
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T011"
TITLE = """~1990年连云港市节约用水情况表"""
PAGES = [366]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_366 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
第三章
公用事业
1983~1990年连云港市节约用水情况表
表5-9
计划户节计量
2812.5
计划户计划取水量
万吨)／年
计划户实际取水量
水量
节水
投入使用节水器
器材
具数（件/套）
工业总产值（万元）
万元产值取水量
工业取水量
2735.2
2564.5
2778.4
2460.3
（万吨/年）
万元产值取水量
（吨/万元）
节水设施项目(项)
11.5
14.5
11.5
3.4
10.4
节水设施投资
节水设施建设
(万元）
自筹
7.5
6.5
3.4
10.4
节水办补
0.5
助或贷款
形成节水能力
0.16
0.06
0.11
0.1
0.09
0.33
0.8
（元/吨日）
节水设施单位投资
（元/吨日）
工业用水量
4085.3
4314.5
5199.4
工业用水重复
（万吨/年）
利用率
工业重复利用水量
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

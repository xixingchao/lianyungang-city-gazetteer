#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T010 — 年连云港市市区干道情况表
页: [343, 344, 346, 347, 348, 349, 352, 355, 356, 357, 358]
卷: 第五卷 章: 城乡建设
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T010"
TITLE = """年连云港市市区干道情况表"""
PAGES = [343, 344, 346, 347, 348, 349, 352, 355, 356, 357, 358]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_343 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
1990年连云港市市区干道情况表
表5-2
路面面积（平方米）
人行道面积（平方米）
宽度
长度
最后修
起论地点
城区道路名称
合计
合计
(米)
建时间
(米)
水泥
沥青
土路
块石
砂石
铺装
5 + 15 + 5 = 25
解放路
新农路-临洪广场
5+4.5+2+10+2+4.5+5=33
5+6+2+10+2+6+5=36
铁路一临洪广场
海连路
5+6+2+14+2+6+5=40
幸福路
新建路一临洪广场
15+10+10 +10+15= 60
新浦区·海州厅
蔷薇路
蓄薇桥一临洪广场
1989年新建
5+6+2+15+2+6+5=41
朝阳路
南极路一干休所
1983年新建
新海路
新建路一蔷薇路
5 + 15 + 5 = 25
新建路
锦屏路一江化路
4.5 + 10+2+10+4.5=31
通灌路
民主路一机耕路
5+ 14+5=24
海昌路
民主路一机耕路
5 + 10 + 5 = 20
南极路
建国路一机耕路
7 + 10 + 7 = 24
新孔路
:345
海连路一大庆路
5 + 15 + 5 = 25
苍梧路
龙河广场一花果山
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

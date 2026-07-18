#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T016 — ~1990年连云港市环境大气、酸雨监测点统计表
页: [421]
卷: 第六卷 章: 环境保护
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T016"
TITLE = """~1990年连云港市环境大气、酸雨监测点统计表"""
PAGES = [421]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_421 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
1986~1990年连云港市环境大气、酸雨监测点统计表
表6-16
环境大气
年份
测点位置、编号
测点数
测点数
测点位置、名称、编号、功能区
1.制碘厂（S75,工业区）
2.交通旅社（S76交通枢纽区）
市站(S44)
3.监测站（S77,生活区）
海州区监测站（S45)
4.机械厂（S74工业区）
市气象台（S46)
5.海州百货仓库（S73，混合区）
6.盐务局招呼站（S78，清洁对照点）
1.制碘厂（S75，工业区）
2.交通旅社（S76,交通枢纽区）
市站(S44)
3.监测站（S77,生活区）
市气象台（S46)
4.海州百货仓库（S73，混合区）
5.盐务局招呼站（S78，清洁对照点）
1.制碘厂（S75,工业区）
2.交通旅社（S76,交通枢枢纽区)
市站(S44)
3.监测站(S77,生活区)
市气象台(S46)
4.盐务局招呼站（S78，清洁对照点）
5.墟沟石油基地（生活区）
1.制碘厂（S75，工业区）
2.交通旅社（S76，交通枢纽区）
市站(S44)
3.监测站(S77,生活区)
市气象台（S46)
4.盐务局招呼站（S78，清洁对照点）
5.墟沟石油基地(生活区)
1.制碘厂（S75,工业区）
2.交通旅社（S76,交通枢纽区）
市站(S44)
3.监测站(S77,生活区)
市气象台（S46)
4.盐务局招呼站（S78，清洁对照点）
5.墟沟石油基地（生活区）
6.经济技术开发区（开发区）
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

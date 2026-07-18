#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T033 — 年连云港市部分水产冷冻加工企业基本情况表
页: [726]
卷: 第十一卷 章: 水产/盐业
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T033"
TITLE = """年连云港市部分水产冷冻加工企业基本情况表"""
PAGES = [726]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_726 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
续上表
冷库
制冰能力
冷冻水产
冷藏品
用于加工的
冷藏能力
人造冰
单位
(吨)
(座)
(吨/日）
（吨/次）
品(吨)
水产品(吨)
（吨/日）
连云港
渔业公司
省盐务局
市水产公司
市养殖公司
1990年连云港市部分水产冷冻加工企业基本情况表
表 12 - 12
建厂时间
库容
速冻能力
1990年
地址
主要产品
(年)
(吨/日）
(吨)
产量(吨)
连云港海洋渔业公司
制冰鱼、虾、贝各种
冻30869
连云镇
冷冻厂
海产冷冻制品
冷冻品5659
鱼、虾冷冻品、鱼
连云港海洋渔业公司
墟沟镇
粉、水产熟制品、罐
水产食品厂
头制品
市水产供销公司鱼品
墟沟镇
鱼、虾、蟹冷冻品
加工厂
对虾及各种海产冷
墟沟镇
市养殖公司冷冻厂
冻品
省盐业水产养殖公司
对虾冷冻品
冷库
连云港外贸冷库冻品
墟沟镇
对虾、蔬菜速冻品
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

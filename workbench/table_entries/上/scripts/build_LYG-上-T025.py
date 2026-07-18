#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T025 — ~1990年连云港市实施农业部丰收计划项目情况表
页: [548, 549, 550]
卷: 第八卷 章: 经济综合管理
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T025"
TITLE = """~1990年连云港市实施农业部丰收计划项目情况表"""
PAGES = [548, 549, 550]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_548 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
1987~1990年连云港市实施农业部丰收计划项目情况表
表9-2
实施项目
年份
实施单位
实施面积（万亩）
赣榆县农业局
稻区粮食综合丰产技术
小麦丰产综合技术
东海县农业局
稻区粮食综合技术
赣榆县农业局
小麦综合丰产技术
赣榆县农业局
灌云县农业局
稻区粮食综合丰产技术
小麦综合增产技术
赣榆县农业局
赣榆、东海县农业局
花生综合增产技术
棉花综合增产技术
灌云县农业局
水稻综合增产技术
灌云县农业局
市作物栽培站，赣榆、东海县农业局
小麦综合增产技术
杂交玉米综合增产技术
赣榆、东海、灌云县农业局
1983~1991年连云港市承担江苏省农林厅主要农业技术研究与推广项目表
表9-3
承担单位
研究推广项目
市农业局
蔬菜塑料大棚综合利用
赣榆县农业局
杂交稻赣化二号高产栽培规律的研究
1983 ~ 1985
稻、麦、棉高产栽培模式图
市及三县农业局
市农业局
稻茬条播麦
赣榆、东海县农业局
三麦根外追肥
灌云县植保站
棉虫综合防治
市植保站
麦病综合防治
市土壤肥料站
碳铵粒肥与根瘤菌肥
市种子站
5XJ-0.5小型种子粒选机和灿型杂交稻种子真实性
鉴定技术
市农业局
玉米免耕栽培和稻茬免耕麦
灌云县农业局
超薄膜平铺覆盖棉花育苗
市及三县土壤肥料站
水稻氮素调控技术和微肥应用技术
东海县农科所
甜玉米开发
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

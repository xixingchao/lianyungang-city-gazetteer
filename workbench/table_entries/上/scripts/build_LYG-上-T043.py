#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T043 — 年连云港市纺织工业企业基本情况表
页: [875, 876, 877, 878]
卷: 第十三卷 章: 乡镇/附录
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T043"
TITLE = """年连云港市纺织工业企业基本情况表"""
PAGES = [875, 876, 877, 878]

# === 列定义 ===
COLUMNS = [
    "企业名称",
    "所在地",
    "职工人数",
    "主要产品",
    "工业产值(万元)",
    "利税(万元)"
]

# === 表格数据（企业名称已确认，其他列需对照原图录入） ===
VERIFIED_CSV = """企业名称,所在地,职工人数,主要产品,工业产值(万元),利税(万元)
连云港涤纶厂,,,,,
连云港市纺织厂,,,,,
连云港市麻纺厂,,,,,
连云港市毛巾厂,,,,,
连云港色织一厂,,,,,
连云港市床单厂,,,,,
连云港市针织内衣厂,,,,,
连云港市经纬编一厂,,,,,
连云港市针织一厂,,,,,
连云港市纺机厂,,,,,
连云港市针织二厂,,,,,
连云港市第三毛纺厂,,,,,
连云港市丝织厂,,,,,
连云港市鞋帽厂,,,,,
赣榆县织布厂,,,,,
赣榆县针织厂,,,,,
赣榆县经编厂,,,,,
赣榆县印染厂,,,,,
赣榆县丝织厂,,,,,
东海县染织厂,,,,,
灌云县织布厂,,,,,"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
第五章
续上表
企业数 (个)
工业产值（80年不变价）：万元
年份
按门类分
按系统内、外分
合计
总产值
纺织
缝纫
系统内
系统外
缝纫
纺织
t9
1990年连云港市纺织工业企业基本情况表
单位：万元
表 15 ~ 10
固定资产
职工人数
企业名称
利税
销售收入
工业总产值
原值
(人)
连云港涤纶厂
连云港市纺织厂
连云港市麻纺厂
- 245
连云港市毛巾厂
~ 65
- 415
连云港色织一厂
连云港市床单厂
- 190
- 227
连云港市针织内衣厂
- 246
连云港市经纬编一厂
- 90
连云港市针织一厂
- 36
连云港市纺机厂
连云港市针织二厂
- 154
连云港市第三毛纺厂
连云港市丝织厂
- 108
连云港市鞋帽厂
-3
续上表
固定资产
职工人数
销售收入
企业名称
利税
工业总产值
原值
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

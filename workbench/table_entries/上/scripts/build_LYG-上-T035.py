#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T035 — 米的大海堤。大海堤的建成，保障淮北盐场和人民的安全，还扩大生产面积一半以上，可作水库和蓄水滩，面积达153平方公里。1990年连云港市境内盐场海堤闸涵和扬水站统计表
页: [743, 745]
卷: 第十一卷 章: 水产/盐业
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T035"
TITLE = """米的大海堤。大海堤的建成，保障淮北盐场和人民的安全，还扩大生产面积一半以上，可作水库和蓄水滩，面积达153平方公里。1990年连云港市境内盐场海堤闸涵和扬水站统计表"""
PAGES = [743, 745]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_743 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
6米的大海堤。大海堤的建成，保障淮北盐场和人民的安全，还扩大生产面积一半以上，可作水库和蓄水滩，面积达153平方公里。1990年连云港市境内盐场海堤闸涵和扬水站统计表
表13-5
流量
孔数
所用场
建成年月
闸(站)涵名称
(个)
（米/秒）
12.5
大新排淡闸
1957.7
7.5
下口排淡闸
1958.8
青口
20.0
工商闸
1959.8
老副河排淡闸
12.5
1960.5
盐场
12.5
下口扬水站
1971.8
1988.7
12.5
三洋扬水站
西墅扬水站
33.0
1957.1
程圩排淡闸
台北
1957.1
33.0
大口港排淡闸
14.0
1971.1
刘三圩排淡闸
盐场
元宝港排淡闸（通航）
1978.2
75.0
23.0
1979.1
公兴港排淡闸
10.0
1953.12
洋桥排淡通航闸
二弯排淡闸
15.0
1953.12
22.5
东龙排淡闸
1953.12
新七圩排淡闸
22.3
盐场
38.5
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

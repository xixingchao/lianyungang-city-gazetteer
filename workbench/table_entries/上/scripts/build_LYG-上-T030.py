#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T030 — 第603页表格
页: [603]
卷: 第九卷 章: 农林业
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T030"
TITLE = """第603页表格"""
PAGES = [603]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_603 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
续上表
地点
堤坡比
堤顶宽
堤长
堤顶高程
备注
管理单位
（公里）
(米)
(米)
迎水坡
背水坡
防浪墙4.1公里，1:3
灌西盐场
洋桥闸
天生港
20.20
6 ~ 6.5
1:3
石护坡4公里
炮阵地
1:2
天生港
1.08
6.5
1:3
块石护坡960米
炮阵地
运销站
6~6.5
1:3
1:3
灌西盐场
0.61
5.5
运销站
燕尾闸下
1:3
1:3
岸墙型式
0.49
灌云县
港段
5.5
1:2
2.18
1:2
在灌西盐场海堤
六圩港西洋桥闸
17.25
4.5~5
1:3
灌云县盐场
1:4 ~ 1:8
外80~120米
第二节
挡潮闸
明代，曾在蔷薇河兴建洪门闸、托山庙闸（见沐南除涝），后年久失修毁于潮。1952年
起，人民政府为挡潮御卤、蓄淡洗碱、灌溉农田、便利水陆交通，开始兴建挡潮闸。至1990
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

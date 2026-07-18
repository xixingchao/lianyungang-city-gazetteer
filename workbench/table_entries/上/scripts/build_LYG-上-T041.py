#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T041 — 业。1970~1990年连云港市化纤业生产经营情况统计表
页: [836]
卷: 第十三卷 章: 乡镇/附录
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T041"
TITLE = """业。1970~1990年连云港市化纤业生产经营情况统计表"""
PAGES = [836]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_836 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
1990年，该企业占地面积6万平方米，建筑面积6万平方米，固定资产原值6881.99
万元，职工1082人。厂内设25个职能管理科室、7个生产、辅助车间。设备主要有年产
1000吨的国产长丝生产线1条、年产3000吨的德国产涤纶长丝高速纺生产线2条及主、
辅设施等。年产综合能力为9000吨。当年生产6997吨，实现产值1.5亿元，利税2149.8
万元，其中利润1574万元。产品主要有涤纶长丝、涤纶低弹丝。该厂为国家中型一类企
业。1970~1990年连云港市化纤业生产经营情况统计表
表15-1
涤纶树酯
企业固定
维纶纤维/
工业
税金
涤纶长丝
销售收入
利润
年份
切片产量
总产值
资产原值
维纶长丝
产量(吨)
（万元）
（万元）
（万元）
(吨)
产量(吨)
（万元）
（万元）
2.16
1.20
6.10
11.00
252.00
126.80
126.06
- 66.85
169.36
82.68
66.70
~ 20.50
12.98
51.50
41.19
19.80
57.98
88.33
137.94
126.50
- 17.40
100.90
355.01
476.40
140.79
40. 20
429.00
36.90
51.94
174. 15
754.30
90.70
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

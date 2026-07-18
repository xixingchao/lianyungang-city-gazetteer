#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T034 — 第739页表格
页: [739]
卷: 第十一卷 章: 水产/盐业
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T034"
TITLE = """第739页表格"""
PAGES = [739]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_739 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
续上表
年份
年份
蒸发量
降水量
蒸发量
降水量
625.2
2000.6
879.9
1594.0
742.9
1967.1
1009.2
1834.3
884.1
1473.3
1644.5
2122.8
1610.2
810.6
1977.2
1016.9
861.9
1881.4
853.5
1429.8
1816.7
917.5
1044.1
1391.6
1711.4
1225.7
789.9
1881.8
971.7
724.5
1599.0
1719.6
700.6
1818.3
579.1
1810.2
869.1
1633.4
611.5
2105.8
1271.0
1808.3
1290.7
1243.6
二、盐场
春秋时期，吴王阖间在江苏沿海煮海为盐。当时齐国管辖的涛雒镇就有盐亭煮盐（在
今青口盐场附近）。汉武帝时，东海郡置盐官。西汉吴王刘濞招募流放罪人来此制盐。唐宝应年间，刘晏
任盐铁使，全国设4场10监，在水设海口场。北宋天圣元年（1023年），淮北海州有板浦、惠泽、洛要三场。元代新滩不断淤现，淮
北盐区扩建板浦场，兴建临洪场（今青口场），废洛要、惠泽二场，变草滩供临洪、板浦场煎
盐用。元至正二十八年（1368年），淮北盐区设立徐渎场，后又增建莞渎场。至此，淮北盐
区所属莞渎、板浦、徐渎、临洪四场，均在今连云港市境内。明清时期，淮北盐业又有了新
发展，明正德七年（1512年)兴建了兴庄场。清康熙年间徐渎场并入板浦场，雍正年间临
洪、兴庄并为临兴场，清乾隆元年（1736年)设中正场，以莞渎场并入。清乾隆二十四年，淮安分司驻板浦，乾隆二十八年改为海州分司。清咸丰五年（1855年）黄河在河南铜瓦厢
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

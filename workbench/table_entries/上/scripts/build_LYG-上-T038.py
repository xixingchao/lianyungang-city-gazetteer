#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T038 — 第774页表格
页: [774]
卷: 第十二卷 章: 工业
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T038"
TITLE = """第774页表格"""
PAGES = [774]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_774 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
续上表
年份
税收
利润
年份
年份
税收
利润
税收
利润
795.94
555.53
305.06
64.90
718.29
436.43
386.57
516.10
649.96
- 211.63
1184.96
894.42
345.59
1041.21
1478.67
585.59
606.73
2080.35
1.17
51.92
957.70
330.89
106.25
- 575.70
缉私
第三章
盐为高税商品，按法纳税者为“官盐”，不纳税者为“私盐”。汉元狩四年（公元前119
年)政府垄断食盐产销，从此盐分官盐与私盐。唐代划区行销，越界侵销者为私盐。五代
以后盐利被封建朝廷和盐商共同垄断，利润甚高，于是私盐更多。清代两淮私盐种类主要
（61）国，，，，，，，洋政府规定：凡未经盐务署特许，制造或意图贩运而收藏的均为私盐。民国38年6月1
日，两淮盐务管理局规定：未经纳税起运之盐斤及未经盐管局批准煎晒者，即谓私盐。建国前，各代查缉私盐法规严格，晋时“凡人不得私煮盐，犯者四年刑”。唐时“刮咸煎
盐，不计斤两，并处极刑”。元时“凡伪造盐引者皆斩”，“盐民走私者鞭打七十，重则必死”。清代两准执行火伏法，管理灶民开煎、稽查。民国时期颁布《私盐治罪法》规定：“以贩私盐
者为特种罪犯·…如构成贩私罪，均按律治罪。”
民国38年（1949年）6月，两淮盐务管理总局颁布《淮盐缉私暂行办法》。1987年10
月，江苏省人民政府颁布《盐政管理办法》规定：盐场内部缉私由业务部门管理，盐场外部
由税务机关管理。从此，盐业缉私护税工作贯彻“场内依靠盐工盐民，场外依靠群众的方
针”，保护盐业生产和国家物资的安全。第一节 机构
唐代在扬州等地设十三巡院，以缉查私盐。宋代扬州置都转运盐使司，管理盐事。元
代两淮盐运司设关防管理私盐。明洪武二年（1369年）两准置盐运司，下设通州、泰州、准
安三分司，淮北在淮安设官验所。清乾隆、嘉庆时期，淮北盐区设关隘，加强缉私。洪门河
口近临兴场灶，为私盐人口要区。嘉庆七年（1802年）准于洪门河文凤阁下河面较窄之处
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

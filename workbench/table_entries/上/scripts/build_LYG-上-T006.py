#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T006 — 年底，连云港市辖东海、赣榆、灌云三县和新浦、海州、云台、连云四区。连云港市建置沿革表
页: [217, 218, 219, 220, 221, 222, 223, 224, 225, 227, 228]
卷: 第二卷 章: 建置区划
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T006"
TITLE = """年底，连云港市辖东海、赣榆、灌云三县和新浦、海州、云台、连云四区。连云港市建置沿革表"""
PAGES = [217, 218, 219, 220, 221, 222, 223, 224, 225, 227, 228]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_217 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
1983年1月18日，国务院批准江苏省政府《关于改革地市体制，调整行政区的报告》，将原属徐州地区的东海县、赣榆县和原属淮阴地区的灌云县划归连云港市管辖。至1990
年底，连云港市辖东海、赣榆、灌云三县和新浦、海州、云台、连云四区。连云港市建置沿革表
表2-1
隶属
名称
朝代(时期)
区域范围
资料来源
桃花涧旧石器晚期遗址
白鸽涧旧石器地点
据连云港市博物馆
旧石器一细石
旧石器时代（距
研究成果
将军崖细石器地点
器文化
今2万年左右）
孔望山细石器地点
马腰岭遗址
二遗址
大村遗址
新石器时代（距
大汶口一龙山
据连云港市博物馆研究成
朝阳遗址
今 7000 ~ 4000
文化
年)
赣马遗址
大伊山遗址
盐仓遗址
徐州（人方东
夏（约前21~前
晋王嘉《拾遗记》、李学勤
夷)
16世纪）
《殷商地理研究》、《尚书·
禹贡》：“海、岱及淮惟徐
徐州（人方国或
商（约前16~前
州。”
东夷、郁夷国)
11世纪)
一说属州，《海州直隶州
西周
志》：“周无徐州，分隶于青
青州
（前11世纪
州，·而海州属鲁，仍
(人方国东夷)
～前771年）
当在充州境。《太平寰宇
记)：“海州，周无徐州，并
为青兖州,则为青州之
域。"《周礼·职方》：“正东
日青州。”查《禹贡九州
郑子国
东周春秋
图，海州距青州较充州
至战国
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T032 — 年连云港市海洋捕捞分品种产量统计表
页: [711, 712]
卷: 第十一卷 章: 水产/盐业
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T032"
TITLE = """年连云港市海洋捕捞分品种产量统计表"""
PAGES = [711, 712]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_711 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
第二章
海洋捕捞
.629
续上表
渔船数量
个体捕鱼
国营渔轮
年份
捕捞产量
产量
其中机帆船
其中渔轮
渔船总数
(吨)
（吨）
(艘)
功率(千瓦)
数量(艘)
功率(千瓦)
数量(艘)
1990年连云港市海洋捕捞分品种产量统计表
单位：吨
表 12 - 6
合计
其它渔船捕捞量
国营渔轮捕捞量
2429★
鱼是
918★
5675★
3969★
续上表
合计
国营渔轮捕捞量
其它渔船捕捞量
259★
东方对虾
周氏新对虾
320★
和鹰爪虾
中国毛虾
3545★
506★
三疣梭子蟹
987★
注：有★者系海州湾渔场产量。第六节
主要企业简介
、连云港海洋渔业公司
该公司座落在连云港。1957年，江苏省水利局抽调省浒浦渔业办事处人员到连云港
进行连云港渔业基地筹备工作，1958年上半年，原来人员先后撤回，筹建工作交由新海连
市负责。1960年，建成4500吨冷库1座，从省海洋渔业公司调来184千瓦渔船4艘。1963
年又从上海调来机帆渔船14舰正式成立江苏省海洋渔业公司连云港分公司，主要从事底
拖网作业，产量不高。1962~1969年平均年产带鱼、小黄鱼、大黄鱼、鱼等1522吨，1965
年产鱼2376吨。1969年11月，公司下放给连云港市，成立连云港市海洋渔业公司，将机
帆渔船14艘有偿转给附近渔业社队。1972年增造279千瓦灯光船和441千瓦渔轮各4
艘。1973～1979年，平均每年增造441千瓦渔轮4艘。至1990年，全公司拥有渔轮37艘，16464千瓦，其中生产渔轮36艘，15876千瓦，全部从事底拖网作业。随着渔轮的增建，公
司捕捞产量逐年增加，从1962年到1990年总计捕鱼209131吨，平均每年产量7211.4吨，其中1978～1990年，平均每年产量13134.38吨，最高1986年为15930吨，所产鱼货主要供
应连云港、徐州等城市。与渔轮生产配套的设备有渔轮修造厂1个，年修造能力为441千
瓦满载排水量350吨的渔轮4艘，大中修10艘；冷库1座，冷藏4500吨/次，制冰120吨/
日，冰2500吨/次，速冻100吨/日，鱼品加工厂1座，年产各类鱼罐头600~800吨，鱼片
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

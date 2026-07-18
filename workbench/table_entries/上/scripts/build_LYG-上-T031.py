#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T031 — 分布在前三岛附近砾石底质表水海域中，是名贵海珍品，产量很
页: [698, 699, 700, 701]
卷: 第十一卷 章: 水产/盐业
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T031"
TITLE = """分布在前三岛附近砾石底质表水海域中，是名贵海珍品，产量很"""
PAGES = [698, 699, 700, 701]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_698 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
续上表
类别
种名
地方名
渔期和生长情况
离水烂
鱼期全年都可捕到，5～6月产卵，是盛渔期，海州湾外围从北到南
马鲛食
均有分布，且资源量很大，个体小，食用价值、经济价值较低。是海州湾渔场的最主要鱼种。渔期分春秋两季，春季个体大，鱼
群密，4月下旬进入渔场，5~6月下旬是产卵期，形成汛期，此时的
带鱼，又称伏带。秋季8～9月，个体小，鱼群分散，是索饵群体，鱼
带鱼
镰刀鱼
发中心偏外。因捕捞强度增加，资源遭到破坏，20世纪60年代
末，已形不成渔汛。海州湾渔场的带鱼是黄海群系，不是东海群
系。带鱼丝
小带鱼
渔汛在秋季。是海州湾渔场的重要鱼种，为远洋洄游性鱼类，来海州湾渔场的
鱼主要是产卵群体，渔期5月上旬到7月底，旺发期5月底到7
月中旬，鱼发中心分布在20米等深线一带。是海州湾渔场的重要鱼种。是远洋洄游性鱼类。渔期分春秋两
季，春季为产卵群体，4月下旬到6月上旬，5月为旺季，分布在海
兰点鲮
马鲛鱼
州湾10米到15米等深线一带；秋季是索饵群体，渔期9月中旬到
10月下旬，10月为旺季，分布在海州湾外围20米等深线附近。是洄游性中下层鱼类，海州湾是其产卵场所之，渔期是4月到7
鲳片鱼
月上旬。是海州湾常见鱼类，渔期3月底到6月中旬，旺汛是5月上中旬、
狗腿鱼
分布在秦山东、连岛北的海底。虾虎鱼
沙光鱼
栖息在浅海盐池、虾塘、河沟里，常年都有。海州湾渔场的底栖鱼类，渔期3月到5月底，4月到5月上旬产卵，鲆、鲽
比目鱼
分布在10米到20米深的水域。真鲨
九道箍
渔期6~8月，产量少。锄头鲨
双髻鲨
渔期7~9月，产量不高。是海州湾大型的名贵虾类，成熟后个体平均重100克，体长23厘
米。海州湾对虾是黄海对虾群的一个分支，是产卵群体。渔期4
东方对虾
对虾
月上旬到5月底，4月底5月初为旺期，分布在5~10米深泥质的
海域中和河口海湾。
第二章
海洋捕捞续上表
种名
类别
地方名
渔期和生长情况
是海州湾渔场产量较多的名贵虾类，肉质透明美观，渔期5月中旬
周氏
羊毛虾
到7月上旬，6月上中旬是旺汛，分布在连岛以北10米深的海域
新对虾
条虾
中。红虾
是海州湾渔场的一种名贵虾类，渔期5月中旬到7月上旬，6月上
铁壳蟹
鹰爪虾
中旬是铁壳蟹旺汛，分布在连岛以北10米深的海域中，与周氏新
硬壳虾
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

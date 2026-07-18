#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T026 — 树297246亩，年产果品35149吨。19491990年部分年份连云港市果树面积、产统计表
页: [559]
卷: 第八卷 章: 经济综合管理
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T026"
TITLE = """树297246亩，年产果品35149吨。19491990年部分年份连云港市果树面积、产统计表"""
PAGES = [559]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_559 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
开始成片栽植，主栽裁品种为玉皇李和红心季，1985年，全市植李面积达300.3亩，年产量83
吨。1990年，调整种植业，植李面积降至152.3亩，但由于加强管理，年产量提高到171
吨。樱桃明代已成片栽植，清代及民国时期以东磊最盛，色、味俱佳，诸韩、宿城次之。建国后，市、县各地均有栽培。20世纪80年代初，云台区云台乡、中云乡、赣榆县厉庄乡
开始大面积栽培。至1985年，全市裁培面积达1281.4亩，年产量75吨。主栽共两类，类为中国樱桃，主要分布在云台乡；一类为甜樱桃，主要分布在中云和厉庄乡，品种有那
翁、大紫、红灯等。否栽培历史悠久，西汉时境内已有栽植。明、清及民国时期，均为一家户零散栽
植。20世纪60年代中期开始成片栽植，至1985年，全市共栽植397.1亩，年产量79.5吨。主要栽培品种有青皮烂、小桃杏、大桃杏、草杏、脑脂红、巴斗杏、麦黄杏、水果杏、荷包杏、
羊屎蛋杏、杏梅等，其中胭脂红、巴斗杏品种较优良。二、面积与产量
境内果树栽培历史悠久。西汉时期，已栽植否树。北宋初期，银否树栽植很普遍。明、清时期，境内栽培果树的种类达28种。清末民初，地方士绅创办前云台树艺公司、海
赣垦牧公司，发展果树3600亩。由于战火及洪涝灾害，至民国37年（1948年），全境果树
仅余766亩，年产果品572吨。建国后，市、县政府重视发展果树，栽植面积逐年增加，至1957年，全境果树发展到
25359亩，年产果品1664吨。1958年起，市、县相继建立国营果园，果树面积大发展，至
灾害，出现大面积毁果种粮，1965年，果树面积降至52266亩，年产果品2031.8吨。1966~
1976年，果树栽植面积发展缓慢，10年中果树面积仅增加5930亩，但由于大部分果树进
入丰产期，果品产量大幅度增加，1970年产量4085吨，1976年达到9048吨。1978年以后，调整种植业内部结构，大力发展果树，果树面积、产量大幅度提高。1990年，全市共有果
树297246亩，年产果品35149吨。19491990年部分年份连云港市果树面积、产统计表
表9-5
年份
面积
(亩)
产量
(吨)
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T001 — 第131页表格
页: [131]
卷: 第一卷 章: 自然环境
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T001"
TITLE = """第131页表格"""
PAGES = [131]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_131 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
续上表
系统
厚度
地层名称
主要岩性
(群)
(米)
上部：以白云斜长片麻岩为主，中部夹斜长片麻岩、黑云片岩角
闪斜长片麻岩及黑云片岩、白云
片岩、混合岩化作用后为二长混
Ar -- Pt
朐山组
> 1981
合岩、混合花岗岩，均质混合岩
下部：为标志层，灰、灰白色含硅
质条纹白云石大理岩、白云石英
片岩、含磁铁石英岩、产微古植
物化石
主要由二长片麻岩及二长混合
片麻岩夹有少量变粒岩和斜长
片麻岩，局部夹薄层黑云斜长麻
Ar -- Ptt
沙河组
> 1520
岩，底部为白云石英片岩（或含
蓝晶石白云石英片岩)可相变成
片状云母石英岩（或含蓝晶石石
英岩)以此为标志层
上部：以白云斜长片麻岩二长片麻
岩为主，夹少量黑云斜长片麻岩，混合岩化后为二长混合片麻岩
Ar -- Ptf
阿湖组
>2005
中下部：以含绿帘黑云斜长片麻
dha
岩，黑云斜长片麻岩夹片麻状榴
辉岩为主，有少量的白云斜长片
麻岩，二长片麻岩及黑云变粒岩
主要以二长片麻岩、变粒岩、浅粒
岩为主夹少量黑云斜长片麻岩和
二云斜长片麻岩，混合岩化后成二
Ar - Pti
长混合片麻岩。班庄组
> 3783
dhb
底部为含透辉石石英岩、白云石
英片岩、白云石大理岩组合，此
为标志层，产微古植物化石
岩性较杂，主要为斜长片麻岩（包
括黑云斜长片麻岩、二云斜长片麻
岩)黑云变粒岩等夹斜长角闪岩、
Ar -- Pt dhj
> 338
黑云角闪片岩和黑云片岩
夹山组
(未见底）
混合岩化作用后为二长混合岩，条带状混合岩、混合片麻岩
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

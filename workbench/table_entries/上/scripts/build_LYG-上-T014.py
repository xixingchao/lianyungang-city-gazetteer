#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T014 — 调房业务。1974~1990年连云港市市区房地产交易统计表
页: [394, 397]
卷: 第五卷 章: 城乡建设
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T014"
TITLE = """调房业务。1974~1990年连云港市市区房地产交易统计表"""
PAGES = [394, 397]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_394 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
续上表
竣工房屋面积
竣工房屋面积
年份
年份
其中住宅面积
总面积
总面积
其中住宅面积
45.07
2.33
14.41
18.92
50.48
24.70
11.17
3.10
13.09
52.53
24.79
0.95
55.97
22.81
12.15
3.46
15.18
75.17
28.86
2.76
90.94
21.90
34.50
5.62
23.94
7.40
84.55
21.17
76.72
27.82
22.59
7.46
30.60
11.64
47.69
12.78
50.82
43.69
19.42
13.01
二、租赁
房屋租赁明《隆庆海州志》记载海州“房地凭租钞四十五贯九百六十文”。清末至建
国前，房屋租赁颇多。有契约、押金、担保等租赁方式。新浦为房屋租金甲等地区，海州、
连云、墟沟为乙、丙、丁等地区。20世纪40年代接收的敌伪房屋大多由中央信托局连云
办事处出租或标售给居民。建国初期，政府先设专人、后设专门机构管理房屋租赁，新浦城区出租房屋租金额为
小麦18904公斤。1956年，《新海连市民房租赁暂行办法》规定：单位租用民房，新浦地区
的租赁手续由市房地产管理部门办理，其余各区由该区人民委员会办理，还应通过人民法
院在租约上履行公证手续，保证租约的严肃性，保障租赁双方利益。私人租赁房屋，根据
主客两利的原则，双方向经办部门申请审查，订立租约（租约由房地产管理部门制定），共
同遵守。该办法还对房屋租金、房主与承租人的责任等作了相应的规定。1956年10月，市房管部门按照社会上一般房屋租价调整了公房出租租额，此后根据
房屋所在地段的繁荣偏僻程度以及房子质量的好坏，结合使用情况每年调整一次，逐步达
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T013 — 站、西跳、市东等街；其余均草房。1961年新浦地区住房调查统计表
页: [388]
卷: 第五卷 章: 城乡建设
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T013"
TITLE = """站、西跳、市东等街；其余均草房。1961年新浦地区住房调查统计表"""
PAGES = [388]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_388 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
第六章
房地产管理
.333*
1.5平方米以下，6.7%的人口居住面积在1.6~2平方米之间。新浦地区有楼房307间，主要在民主、市东、车站等街；有瓦房、平房1457间，主要分布在民主、站北、新海、通池、车
站、西跳、市东等街；其余均草房。1961年新浦地区住房调查统计表
表5-12
面积
人口
人口
房屋
面积
房屋
街名
街名
(人)
(间)
(人)
(间)
(平方米)
(平方米)
同和
新海
路南
民族
市东
通池
民主
新市
车站
陇东
站北
菜市
通灌
西跳
贾圩
市化
新村
灌青
路北
双池
市民
1963年，针对房屋产权不清、房租及房屋附属设备无档等问题在新海地区全面调查。而后，对新浦朝阳区28条街的直管公房建立28本台账。1971年3月18日统计，市区公房建设面积约77万平方米，使用面积48万平方米，人
均居住2.79平方米。新浦、海州、连云港3地区共有1449户，5399人缺房。截止1976年11月，市区有公房15243.5间、273857平方米、使用面积202544平方米。1978年6～12月，整理、核对房屋档案资料，对6条街的公房重新普查，弄清漏管、漏
收、错管、错收情况。房屋档案资料分类统计，达到分街、分户有图，房号、面积、租金基数
对号，产权来源、设备使用、房屋质量情况清楚。1982年8月成立房屋普查办公室，10月开始对市区直管公房进行普查，统计归档。1983年上半年，直管公房的图、档、卡完整齐全。1985年3月，市政府发布城镇房屋普查通告，部署第一次全国城镇房屋普查连云港
市区段的工作。由83人组成的房屋普查办公室成立，培训专业普查人员437名。1985年
6月3日至1986年3月30日，普查了3个城区（新海、云台、连云）、7个市辖镇（锦屏、连云
港、墟沟、猴嘴、徐圩、板桥、南城）、8个街道办事处的119个居民委员会，普查了三县的6
个建制镇（赣榆县青口，东海县牛山，灌云县伊山、板浦、杨集、燕尾)的31个居民委员会，普查了青口、灌西两个盐场和东辛、五图河、东海、云台5个农场。填写近50万张表格，测
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

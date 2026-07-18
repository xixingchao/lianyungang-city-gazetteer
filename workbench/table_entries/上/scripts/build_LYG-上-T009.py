#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T009 — 了规定。此后至1990年，市区和赣榆县、东海县、灌云县的22个建制镇都先后编制了规划。1990年连云港市建制镇规划情况表
页: [338]
卷: 第五卷 章: 城乡建设
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T009"
TITLE = """了规定。此后至1990年，市区和赣榆县、东海县、灌云县的22个建制镇都先后编制了规划。1990年连云港市建制镇规划情况表"""
PAGES = [338]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_338 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
第一章 规划和测绘
级政府把村镇建设摆到议事日程上来。6月22日，江苏省基本建设委员会、财政厅联合颁发
《村镇规划建设使用事业费使用管理暂行办法》，对各地村镇规划的资金来源和使用范围作
了规定。此后至1990年，市区和赣榆县、东海县、灌云县的22个建制镇都先后编制了规划。1990年连云港市建制镇规划情况表
表5-1
编制完成
镇的性质
建制镇
地区
规划年限
人口
年份
（平方公里）
（万人）
锦屏
1985 ~ 2000
工矿区和生活居住区相结合型
南城
1.60
2.00
轻工业及综合型
1985 ~ 2000
板桥
盐业及化工生产
1.20
1.50
1985 ~ 2000
徐圩
盐业及化工生产
1.50
3.50
1990 ~ 2000
以农业加工、轻工为主的地区
1.67
0.93
1983 ~ 2000
性农贸服务中心
以养殖、种植为主的地区性农
欢墩
0.85
1983 ~ 2000
贸中心
海头
以水产养殖为中心
3.70
1984 ~ 2000
沙河
2.16
1.55
以蔬菜、粮油加工为主
1986 ~ 2000
以农副产品加工和建筑材料为
城头
0.90
2.10
1986 ~ 2000
主体的工业小城镇
石桥
1.50
以干果加工及陶器为中心
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

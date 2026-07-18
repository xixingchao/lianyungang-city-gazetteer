#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LYG-上-T012 — 第370页表格
页: [370]
卷: 第五卷 章: 城乡建设
状态: draft（初稿，待对照原图核对）
"""

import csv, io, json
from pathlib import Path

TABLE_ID = "LYG-上-T012"
TITLE = """第370页表格"""
PAGES = [370]

# === 列定义（需对照原图确认） ===
COLUMNS = [
    # 请在此定义列名，例如:
    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"
]

# === 表格数据（需对照原图逐行录入） ===
# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）
# 建议对照原图 page_370 录入
VERIFIED_CSV = """"""

# === OCR 参考文本（仅供参考，请以原图为准） ===
OCR_REF = """
续上表
盏数
线路长度
光源
路名
架线方式
线材品种
(盏)
（米）
钠250瓦
架空
铜线
幸福路
汞250瓦
架空
铝线
白 40 瓦
架空
铝线
新海路
汞125瓦
地埋
铜电缆
白40瓦
龙河广场
钠250瓦
第三节 公共交通
一、客运畜力车
清末民初，东海和灌云城乡主要以士驴车（即独轮车）和客运毛驴作为交通工具。在
海州和新浦间客运使用较多。客运毛驴于民国9年（1920年）被客运马车取代。民国初
至20世纪20年代中期，南城和海州间客运通常使用驴轿。民国9年后，客运马车是新浦
和海州、新浦和大浦、新浦和连云间客运主要工具，车厢周围都有座位，可容纳五六人。1949年底，市内共有客运马车250辆。由于客运人力车的大量出现，客运马车于1956年
淘汰。二、客运人力车
民国9年（1920年），胶轮黄包车成为当地最主要的客运工具。胶轮黄包车行驶路线
多为新浦至海州和新浦至大浦。民国22年，东海县共有人力车500辆，其中租用人力车
230辆，自备人力车270辆。民国24年，当地人力车夫联合组成东海县人力车夫职业工
会。1951年，市内开始有人力搭客二轮车。1956年，当地人力车经营者用搭客二轮车前
部和黄包车后部组装成客运人力三轮车，时有115辆。同年，人民委员会将新海地区约
200辆闲散人力客运三轮车、黄包车和人力搭客二轮车组成三轮车合作社，实行统一配
载、统一调度和统一运输的管理。由于人力客运三轮车的大量使用，黄包车和人力搭客二
轮车分别于1957年和1961年停用。1957年1月，三轮车合作社改名为市搬运公司三轮
车客运队。1963年4月，市搬运公司三轮车客运队又改名为新浦三轮车服务队。这时因
市内公共汽车的日益发展，三轮车客运量大减，11月5日，新浦三轮车服务队并入新浦搬
运营业所，只保留10余辆人力客运三轮车，其余均改成平板脚踏货运车。至1967年，赣
榆县城共有客运人力车150辆和客运畜力车13辆。1970年，市内开始使用机动客运三轮
车载客，市内人力客运三轮车逐遂渐减少，1972年1月20日，市搬运公司三轮车客运队成立
时仅有人力客运三轮车25辆，1982年，已完全被机动客运三轮车取代。从1985年起，市
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

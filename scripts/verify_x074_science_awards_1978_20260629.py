# -*- coding: utf-8 -*-
"""Verify LYG-下-T074 1978 science awards table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T074.json"

COLUMNS = ["项目名称", "完成单位"]
ROWS = [
    ["BX7-120交流弧焊机", "市建筑机械厂"],
    ["广播电台中波实验发射机开关机自动程序", "市人民广播电台"],
    ["空气吹出法海水提溴", "连云港水产化工厂"],
    ["综合利用黄磷尾气生产甲酸、草酸", "市锦屏化工厂"],
    ["用纸浆液代替大豆油脂肪酸进行磷矿浮选", "市锦屏磷矿"],
    ["双侧式自动卸载矿车", "市新浦磷矿"],
    ["海水高钙镁砂", "市海滨化工厂"],
    ["高炉采用自焙碳砖试验", "市光明碳素厂"],
    ["JLQ-30.5吨集装箱起重机", "市起重机厂"],
    ["电动无芯弯管机", "市建筑安装工程处"],
    ["连云港钢板桩码头防滑坡经验总结", "连云港建港指挥部工程组"],
    ["山区水土保持综合措施研究", "赣榆县夹山乡水土站"],
    ["JLG-125旋耕型", "灌云县农机修造厂"],
    ["塑料薄膜苫盖结晶池制盐新工艺", "江苏省盐务局制盐科学研究所"],
    ["蜜蜂疗法的研究", "江苏省盐务局工人医院"],
    ["环氧乙烷灭菌器", "市墟沟电器厂"],
    ["连云港回淤问题研究", "连云港建港指挥部规划组"],
    ["高纯镁砂的合成", "市海滨化工厂"],
    ["对虾低盐度大面积高产养殖技术的研究", "市海带育苗厂"],
    ["硝酸法分解硼镁矿制硼酸", "化工部矿山设计研究院"],
    ["YK-10-31型频率制无触点分散目标远动装置", "化工部矿山设计研究院"],
    ["湖北王集胶磷矿选矿试验", "化工部矿山设计研究院"],
    ["硝酸法分解硼镁石矿制取硼酸和硼酸母液", "化工部矿山设计研究院"],
    ["轨道传输式自动化道口", "徐州铁路分局新浦工务段"],
    ["眼球内异物立体定位器", "东海县人民医院"],
    ["白内障冷冻摘除器和人工晶体", "东海县人民医院"],
    ["疟疾防治的研究", "东海县卫生防疫站"],
]

PATCH = {
    "title": "1978年连云港市获省科技大会奖项目表",
    "table_number": "表51-9",
    "page": 2403,
    "pages": [2403],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T074_2403.txt；对明显OCR字形误识按上下文规范：高钙美砂->高钙镁砂，苦盖->苫盖，疮疾->疟疾。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-下-T074":
        return False
    changed = False
    for key, value in PATCH.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if patch_entry(data):
        DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 1
    return 0


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise SystemExit("TABLES payload not found")
    tables = json.loads(match.group(1))
    changed = 0
    for table in tables:
        if patch_entry(table):
            changed += 1
    if changed:
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    print(f"json_files_changed={patch_json()}")
    print(f"site_entries_changed={patch_site()}")


if __name__ == "__main__":
    main()

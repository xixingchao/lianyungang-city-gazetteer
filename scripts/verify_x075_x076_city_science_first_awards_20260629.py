# -*- coding: utf-8 -*-
"""Verify LYG-下-T075/T076 city science first award projects table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_FILES = {
    "LYG-下-T075": ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T075.json",
    "LYG-下-T076": ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T076.json",
}

COLUMNS = ["项目名称", "获奖年份", "完成单位"]
PATCHES = {
    "LYG-下-T075": {
        "title": "1978~1990年连云港市获市科技成果、科技进步一等奖项目表",
        "table_number": "表51-12",
        "page": 2405,
        "pages": [2405],
        "columns": COLUMNS,
        "rows": [
            ["塑料薄膜苫盖结晶池新工艺大面积推广", "1978", "江苏省盐务局"],
            ["细胞离净", "1979", "市第一人民医院"],
            ["内蒙古炭窑口硫铁矿综合回收铜、锌、硫的选矿研究", "1979", "市东方红化工厂；化工部矿山设计研究院"],
            ["合成盐酸罂粟碱", "1980", "连云港制药厂"],
            ["改造国产31-6型汽轮机为低真空抽气式供热机组", "1981", "新海发电厂；南京工学院动力系"],
            ["SF12外用附墙升降机", "1981", "市机械厂；国家建委建筑机械研究"],
            ["QT80多用塔式起重机", "1981", "市机械厂；国家建委建筑机械研究"],
            ["GJ5E5-150型通过式熨皮机", "1981", "省盐务局轻工机械厂"],
            ["GQ-20手持式钢筋切断机", "1982", "连云港电机厂"],
        ],
        "status": "verified",
        "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T075_2405.txt；原JSON为单列待录入骨架。页首含上一表续表残段，本轮仅录入表51-12；“苦盖”按语境规范为“苫盖”，“罄粟碱”按药名语境规范为“罂粟碱”。续表见LYG-下-T076。",
    },
    "LYG-下-T076": {
        "title": "1978~1990年连云港市获市科技成果、科技进步一等奖项目表（续表）",
        "table_number": "表51-12",
        "page": 2406,
        "pages": [2406],
        "columns": COLUMNS,
        "rows": [
            ["赤松、黑松叶粉生产设备及工艺研究", "1982", "南京林化所、市农机厂；墟沟林场"],
            ["脉动真空蒸汽灭菌器", "1983", "市医疗器械设备厂；军事医学科学院微生物流行病研究所等"],
            ["双城耦", "1983", "赣榆县土城乡小营城农科队"],
            ["中华绒鳌蟹天然海水工厂化育苗技术的研究", "1984", "赣榆县水产研究所；赣榆县海带育苗厂"],
            ["衬布用EVAL粉末热熔胶中间试验", "1984", "市有机化工厂；市化工研究所等"],
            ["稻粒黑粉病综合防治技术", "1985", "赣榆县农业局植保站"],
            ["苦卤空气吹溴", "1986", "江苏省徐圩盐场化工厂"],
            ["爆炸法处理水下软基及施工新工艺", "1987", "连云港建港指挥部；中科院力学研究所；交通部第三航务工程勘察设计院；市锦屏磷矿"],
            ["GT2HI-180通过式磨革气流除尘机组", "1987", "连云港皮革机械厂"],
            ["瓶罐玻璃生产中掺大比例碎玻璃技术", "1988", "华东化工学院无机材料系；市玻璃二厂"],
        ],
        "status": "verified",
        "notes": "已据raw OCR回源核录：workbench/table_entries/下/raw/LYG-下-T076_2406.txt；原JSON为单列待录入骨架。本页为表51-12续表；原注说明1989年、1990年科技成果市无一等奖。",
    },
}

for patch in PATCHES.values():
    patch["row_count"] = len(patch["rows"])
    patch["col_count"] = len(patch["columns"])


def patch_entry(entry: dict) -> bool:
    patch = PATCHES.get(entry.get("table_id"))
    if not patch:
        return False
    changed = False
    for key, value in patch.items():
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    return changed


def patch_json() -> int:
    changed = 0
    for path in DATA_FILES.values():
        data = json.loads(path.read_text(encoding="utf-8"))
        if patch_entry(data):
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed += 1
    return changed


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

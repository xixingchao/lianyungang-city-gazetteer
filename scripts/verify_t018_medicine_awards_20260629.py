# -*- coding: utf-8 -*-
"""Verify LYG-中-T018 medicine awards table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T018.json"

COLUMNS = ["产品名称", "生产单位", "获奖年份", "获奖等级名称", "授奖机关"]
ROWS = [
    ["“紫兰”牌药用甘露醇", "连云港制碘厂", "1984", "江苏省优质产品、轻工部优质产品", "省政府、国家轻工业部"],
    ["“黄海”牌检眼镜片箱", "新浦光学仪器厂", "1985、1989", "江苏省优质产品、国家医药管理局优质产品", "省政府、国家医药管理局"],
    ["“连药”牌异博定", "连云港制药厂", "1986", "江苏省优质产品", "省政府"],
    ["“崛新”牌组合恒温培养箱", "连云港医疗设备厂", "1987", "江苏省优质产品", "省政府"],
    ["“东风”牌甘露醇注射液", "连云港东风制药厂", "1987", "江苏省优质产品", "省政府"],
    ["“花果山”牌微型救护车", "连云港医疗器械厂", "1988", "江苏省优质产品", "省政府"],
    ["“紫兰”牌聚稀酸树脂", "连云港制碘厂", "1988", "江苏省优质产品", "省政府"],
    ["“山环”牌药用铝箔", "连云港药用包装材料厂", "1989", "江苏省优质产品“金牛”奖", "省政府"],
    ["“东风”牌地塞米松磷酸钠注射液", "连云港东风制药厂", "1989", "江苏省优质产品", "省政府"],
    ["“连药”牌足叶乙甙原料", "连云港制药厂", "1990", "江苏省优质产品“金牛”奖、第二届国际博览会金奖", "省政府"],
    ["“连药”牌足叶乙甙注射液", "连云港制药厂", "1990", "江苏省优质产品“金牛”奖、第二届国际博览会金奖", "省政府"],
    ["“崛新”牌脉动真空灭菌器", "连云港医疗设备厂", "1990", "江苏省优质产品", "省政府"],
    ["“东风”牌大蒜素胶囊", "连云港东风制药厂", "1990", "国家医药管理局优质产品", "国家医药管理局"],
]

PATCH = {
    "title": "连云港市医药系统获奖产品一览表",
    "table_number": "表19-10",
    "page": 1043,
    "pages": [1043],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/中/raw/LYG-中-T018_1043.txt。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T018":
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

# -*- coding: utf-8 -*-
"""Verify LYG-中-T007 craft art award products continuation table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T007.json"

COLUMNS = ["获奖年月", "获奖产品", "获奖名称", "生产企业"]
ROWS = [
    ["1982.7", "“花冠”牌贝雕画", "江苏省工艺美术“百花”奖", "连云港贝雕总厂"],
    ["1982.12", "15头电热咖啡具", "全国陶瓷行业美术设计三等奖", "赣榆县瓷厂"],
    ["1983.5", "凹凸印花装饰新工艺", "江苏省轻工“四新”产品三等奖", "赣榆县瓷厂"],
    ["1983.5", "“显色自然景”花瓶", "江苏省轻工科技成果三等奖", "连云港市玻璃制品厂"],
    ["1983.5", "15头仿隋图案茶具", "江苏省轻工科技成果三等奖", "赣榆县瓷厂"],
    ["1983.5", "四人脚踏转椅", "江苏省轻工科技成果三等奖", "连云港市玩具厂"],
    ["1983.9", "机抽洗90道美术地毯整修", "轻工业部全国地毯行业质量评比单项第一名", "连云港市地毯厂"],
    ["1983.9", "机抽洗90道美术地毯片剪", "轻工业部全国地毯行业质量评比单项第一名", "连云港市地毯厂"],
    ["1983.11", "“云雾茶”茶叶听", "第五届全国印铁制罐行业质量评比优良产品", "连云港市印铁制罐"],
    ["1983.12", "凹凸印花装饰新工艺", "江苏省轻工科技成果三等奖", "赣榆县瓷厂"],
    ["1983.12", "15头仿隋图案设计", "江苏省轻工科技成果三等奖", "赣榆县瓷厂"],
    ["1984.5", "古典式地毯图案", "全国第九届地毯图案评比创新奖", "连云港市地毯厂"],
    ["1984.5", "红楼二尤", "江苏省玉雕行业质量评比二等奖", "连云港市雕塑工艺"],
    ["1984.11", "“中国名茶”茶叶听", "华东地区印铁制罐行业质量评比优秀产品", "连云港市印铁制罐"],
    ["1985.5", "“燕渔”烟缸", "江苏省轻工科技成果三等奖", "连云港市玻璃制品"],
    ["1985.6", "柳制品系列产品", "江苏省工艺美术“百花”奖", "连云港市工艺制品"],
    ["1985.6", "柳木结合贴面家具", "江苏省轻工新产品设计奖", "连云港市工艺制品"],
    ["1985.6", "“茶叶礼品盒”包装", "江苏省轻工优秀设计奖", "连云港印铁制罐厂"],
    ["1985.8", "“花冠”牌贝雕工艺品", "中国工艺美术“百花”奖，轻工部优质产品奖", "连云港贝雕总厂"],
    ["1985.8", "贝雕竹编挂盘", "江苏省轻工优秀新产品奖", "连云港贝雕总厂"],
    ["1985.8", "贝雕电子钟门铃、旅游贝雕梳蓖、贝雕桐木盒、壁灯等", "全国同行业总分第三名", "连云港贝雕总厂"],
    ["1985.10", "桐木盒", "江苏省第四届轻工优秀新产品", "连云港市工艺桐木制品厂"],
]

PATCH = {
    "title": "1963~1990年连云港市工艺美术工业获奖产品一览表（续表）",
    "table_number": "表17-16",
    "page": 961,
    "pages": [961],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0058.txt；主表题和表号见raw OCR workbench/table_entries/中/raw/LYG-中-T006_960.txt。本页为表17-16续表，跨行产品名、奖项名、企业名已按OCR版面合并；少数企业名按OCR可见文本保留。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T007":
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

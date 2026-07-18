# -*- coding: utf-8 -*-
"""Verify LYG-中-T029 machinery industry award products continuation table."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T029.json"

COLUMNS = ["产品名称", "生产企业", "获奖级别", "获奖年份"]
ROWS = [
    ["LY121JH型救护车", "连云港市医疗器械厂", "省优秀新产品“金牛”奖", "1987"],
    ["LY620JH型救护车", "连云港市医疗器械厂", "省优秀新产品“金牛”奖", "1987"],
    ["SXB-1200型半自动下部卸料离心机", "连云港化工机械厂", "省优秀新产品“金牛”奖", "1987"],
    ["CJ2H1-180型通过式磨革气流除尘机", "连云港皮革机械厂", "省优秀新产品“金牛”奖", "1987"],
    ["苏4GL-130麦稻收割机", "东海县农机厂", "省优", "1988"],
    ["40英尺集装箱半挂汽车列车", "连云港车辆厂", "省优", "1988"],
    ["IS65-50160单级吸清水离心泵", "连云港市水泵厂", "省优", "1988"],
    ["DTC36/23式提升级输送机", "东海县粮食机械厂", "省优", "1988"],
    ["S7100/0.4~10低损耗节变压器", "连云港变压器厂", "省优", "1988"],
    ["DZI2-0.98-AII卧式链条炉排快装锅炉", "连云港市锅炉厂", "省优", "1989"],
    ["CJSE2-150通过式熨平机", "连云港皮革机械厂", "部优", "1989"],
    ["QCWY-32型钢筋加工机", "灌云县通用机械厂", "省优", "1989"],
    ["东风-12型手扶拖拉机齿轮", "东海八一齿轮厂", "省优", "1989"],
    ["BGJP35集装箱平板挂车", "连云港车辆厂", "省优", "1989"],
    ["QA-1聚氨脂漆包圆铜线", "连云港电线电缆总厂", "省优", "1990"],
    ["DZ-2温度指数155的聚脂漆包圆铜线", "连云港电线电缆总厂", "省优", "1990"],
    ["9FQ-44型粉碎机", "赣榆县农业机械制造厂", "省优", "1990"],
    ["2BCS-10型少耕条播机", "灌云县农业机械修理制造厂", "省优秀新产品“金牛”奖", "1990"],
    ["7666系列门式链斗卸车机", "连云港机械厂", "省优秀新产品“金牛”奖", "1990"],
    ["YEJT90LA-4型电磁制动电机", "连云港电机厂", "省优秀新产品“金牛”奖", "1990"],
    ["YEJT100L1-4型电磁制动电机", "连云港电机厂", "省优秀新产品“金牛”奖", "1990"],
    ["1540毫米E型旋翼式温水表", "连云港水表厂", "省优秀新产品“金牛”奖", "1990"],
    ["XCY-1型表面粗糙度测量仪", "连云港光学仪器厂", "省优秀新产品“金牛”奖", "1990"],
    ["40英尺集装箱平板半挂汽车列车", "连云港车辆厂", "省优秀新产品“金牛”奖", "1990"],
    ["CJSC1-150型通过式熨平压花机", "连云港皮革机械厂", "省优秀新产品“金牛”奖", "1990"],
    ["CJ4B2-180型光电喷涂干燥机", "连云港皮革机械厂", "省优秀新产品“金牛”奖", "1990"],
    ["D型多级离心水泵", "连云港市农机厂", "省优秀新产品“金牛”奖", "1990"],
]

PATCH = {
    "title": "连云港市机械工业获奖产品一览表（续表）",
    "table_number": "表21-6",
    "page": 1136,
    "pages": [1136],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part01/page_0233.txt；主表题和表号见page_0232.txt。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T029":
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

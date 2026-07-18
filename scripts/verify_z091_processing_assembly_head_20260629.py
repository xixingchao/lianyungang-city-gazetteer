# -*- coding: utf-8 -*-
"""Verify LYG-中-T091 processing assembly project head table from raw OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T091.json"

COLUMNS = ["年份", "序号", "批准备案号", "项目内容", "承接单位", "外方单位", "加工费用总额(万元)", "单价", "数量"]
ROWS = [
    ["1986", "", "连外经贸资字(86)011号", "加工收录机计数器", "连云港市无线电四厂", "香港大兴企业公司", "4.50", "", ""],
    ["1986", "", "连外经贸资字(86)072号", "加工骑士手表", "连云港市第三塑料厂", "日本丸荣株式会社", "6.00", "", ""],
    ["1986", "", "", "加工和服腰带", "连云港市锦屏刺绣厂", "日本丸荣株式会社", "", "", ""],
    ["1988", "", "连外经贸资字(88)042号", "50T废蓄电池熔炼", "连云港市电线厂", "加拿大华源企业有限公司", "", "", ""],
    ["1988", "", "连外经贸资字(88)056号", "运动套装、连衣裙", "连云港市市东服装厂", "香港恒昌企业公司", "4.00", "", ""],
    ["1988", "", "连外经贸资字(88)056号", "被单、地毯", "连云港市市东服装厂", "香港恒昌企业公司", "1.28", "", ""],
    ["1988", "", "88苏外经贸来（连）第004号", "彩色打子成品平绣", "开发区苏锦绣品工艺公司", "日本丸荣贸易株式会社", "0.20", "", ""],
    ["1988", "", "88苏外经贸来（连）第005号", "丝绸印色相良绣", "开发区苏锦绣品工艺公司", "日本丸荣贸易株式会社", "3.00", "", ""],
    ["1988", "", "88苏外经贸来（连）第006号", "彩色打子成品平绣", "开发区苏锦绣品工艺公司", "日本丸荣贸易株式会社", "4.00", "", ""],
    ["1988", "", "88苏外经贸来（连）第007号", "加工废杂电机", "连云港市裸铜线厂", "美国联合资源公司", "10", "", ""],
    ["1988", "", "88苏外经贸来（连）第008号", "加工废蓄电瓶", "连云港市裸铜线厂", "美国联合资源公司", "0.32", "", ""],
    ["1988", "12", "88苏外经贸来（连）第009号", "骑士手套", "连云港市塑料包装制品公司", "日本丸荣贸易株式会社", "1.20", "6.12元/打", "2000打"],
    ["1988", "13", "88苏外经贸来（连）第010号", "付下着尺和服绣料", "开发区苏锦绣品工艺公司", "日本丸荣贸易株式会社", "1.40", "70元/码", "2000码"],
    ["1988", "14", "88苏外经贸来（连）第011号", "仪器仪表插件散件", "连云港市无线电元件四厂", "香港华茂实业公司", "0.20", "0.20元", "10000只"],
]

PATCH = {
    "title": "1984~1990年连云港市批准来料加工装配项目表",
    "table_number": "表35-9",
    "page": 1622,
    "pages": [1622],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据raw OCR回源核录：workbench/table_entries/中/raw/LYG-中-T091_1622.txt；原JSON为单列待录入骨架。页首含上一表续表残段，本轮仅录入表35-9；OCR未显示或未清晰读出的序号、单价、数量保留空值，未猜补。续表见LYG-中-T092。",
}


def patch_entry(entry: dict) -> bool:
    if entry.get("table_id") != "LYG-中-T091":
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

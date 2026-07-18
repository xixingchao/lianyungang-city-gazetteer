# -*- coding: utf-8 -*-
"""Verify electronics enterprise table 22-7 and remove flattened reader residue."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import embed_verified_tables_into_reader

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T141.json"
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "electronics_enterprises_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "electronics_enterprises_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_电子工业主要企业表回源核录.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ENTRY = {
    "table_id": "LYG-中-T141",
    "title": "1990年连云港市电子工业主要企业基本情况表",
    "table_number": "表22-7",
    "page": 1068,
    "pages": [1068],
    "part": "part01",
    "vol": "中",
    "volume": "中",
    "columns": ["名称", "地址", "性质", "建厂年份", "职工人数", "固定资产原值(万元)", "工业总产值(万元)", "主要产品"],
    "rows": [
        ["灌云县电子机械厂", "灌云县胜利路70号", "全民", "1970", "133", "59", "305", "矿用机车报警器、取样积分仪"],
        ["连云港市无线电元件十厂", "连云港市新浦区海连东路25号", "全民", "1977", "290", "200", "127", "继电器、报时器、振动器"],
        ["连云港市云台无线电元件厂", "连云港市南郊云台农场", "全民", "1978", "265", "98", "297", "有机实芯电位器、合成碳膜电位器"],
        ["连云港市磁性材料厂", "连云港市西站西首", "集体", "1978", "90", "122", "190", "磁轭、磁极掌"],
        ["东海县水晶厂", "东海县曲阳乡", "集体", "1979", "45", "297", "119", "人造水晶"],
        ["连云港市堂福电子有限公司", "连云港市海州区西大街34号", "三资", "1988", "160", "509", "7880", "硅整流二极管"],
        ["连云港市达灵电子元件厂", "赣榆县大岭乡", "集体", "1989", "22", "45", "27", "聚焦电位器"],
    ],
    "row_count": 7,
    "col_count": 8,
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/中/part01/page_0266.txt，并参考 raw OCR：workbench/ocr/raw/中/part01/page_0266.txt。表内多行单元格按源页列序合并；注为“简介企业不列入本表”。",
}

RESIDUE = "<p>人数矿用机车报警灌云县胜利全民197013359灌云县电子机械厂305路70号器、取样积分仪连云港市新继电器、报时连云港市无线电元件全民浦区海连东2902001977127器、振动器路25号有机实芯电位连云港市南连云港市云台无线电全民265297197898器、合成碳膜电郊云台农场元件厂位器连云港市西集体连云港市磁性材料厂190197890磁轭、磁极掌122站西首东海县曲阳集体297119人造水晶197945东海县水晶厂连云港市海连云港市堂福电子有三资州区西大街19881605097880硅整流二极管限公司34 号赣榆县大岭连云港市达灵电子元集体1989224527聚焦电位器件厂注：简介企业不列入本表。</p>"
SOURCES = [
    "workbench/ocr/paddle_ocr/中/part01/page_0266.txt",
    "workbench/ocr/raw/中/part01/page_0266.txt",
    "output/final_reader/连云港市志_全书.html:10064",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_json() -> int:
    new = json.dumps(ENTRY, ensure_ascii=False, indent=2) + "\n"
    old = DATA.read_text(encoding="utf-8") if DATA.exists() else ""
    if old != new:
        DATA.write_text(new, encoding="utf-8")
        return 1
    return 0


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise RuntimeError("TABLES payload not found")
    tables = json.loads(match.group(1))
    before = json.dumps(tables, ensure_ascii=False, sort_keys=True)
    tables = [table for table in tables if table.get("table_id") != ENTRY["table_id"]]
    tables.append(ENTRY)
    tables.sort(key=lambda item: (str(item.get("vol") or item.get("volume") or ""), int(item.get("page") or 999999), str(item.get("table_id") or "")))
    after = json.dumps(tables, ensure_ascii=False, sort_keys=True)
    if before == after:
        return 0
    SITE.write_text(text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :], encoding="utf-8")
    return 1


def repair_reader() -> int:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(RESIDUE)
    if count == 1:
        HTML.write_text(text.replace(RESIDUE, "", 1), encoding="utf-8")
        return 1
    if count == 0 and "人数矿用机车报警灌云县胜利全民197013359" not in text:
        return 0
    raise RuntimeError(f"expected electronics residue once, got {count}")


def write_reports(json_changed: int, site_changed: int, embedded_count: int, removed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "table_id": ENTRY["table_id"], "json_changed": json_changed, "site_changed": site_changed, "embedded_count": embedded_count, "reader_residue_removed": removed, "sources": SOURCES}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 电子工业主要企业表回源核录",
        "",
        f"- 时间：{now}",
        f"- 表格：`{ENTRY['table_id']}` {ENTRY['table_number']} {ENTRY['title']}。",
        f"- 变更：JSON {json_changed}；结构化表格站 {site_changed}；主阅读版已核表嵌回 {embedded_count} 张；撤出压扁残片 {removed} 段。",
        "",
        "## 证据",
        "",
    ]
    lines.extend(f"- `{source}`" for source in SOURCES)
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    append_once(MEMORY, "## 2026-07-05 电子工业主要企业表回源核录", f"""
## 2026-07-05 电子工业主要企业表回源核录
- 新增并运行 `scripts/verify_z141_electronics_enterprises_20260705.py`，据中册 part01/page_0266 核录 `LYG-中-T141` 表22-7《1990年连云港市电子工业主要企业基本情况表》。
- 主阅读版撤出 `人数矿用机车报警...注：简介企业不列入本表。` 压扁残片，表内多行单元格按源页列序合并。
- 报告：`output/reports/electronics_enterprises_20260705.md`。
""")


def main() -> None:
    json_changed = write_json()
    site_changed = patch_site()
    embedded_count, unplaced = embed_verified_tables_into_reader.embed()
    if unplaced:
        raise RuntimeError(f"unplaced verified tables: {unplaced}")
    embed_verified_tables_into_reader.write_progress(embedded_count, unplaced)
    embed_verified_tables_into_reader.update_memory(embedded_count, unplaced)
    removed = repair_reader()
    write_reports(json_changed, site_changed, embedded_count, removed)
    print("electronics_enterprises_verified")
    print(f"json_changed={json_changed}")
    print(f"site_changed={site_changed}")
    print(f"embedded_count={embedded_count}")
    print(f"reader_residue_removed={removed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

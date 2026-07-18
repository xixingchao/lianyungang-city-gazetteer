# -*- coding: utf-8 -*-
"""Verify machine/instrument output table 21-4 and remove flattened residue."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import embed_verified_tables_into_reader

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T142.json"
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "machine_instrument_output_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "machine_instrument_output_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_机床仪器仪表主要产品产量表回源核录.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ENTRY = {
    "table_id": "LYG-中-T142",
    "title": "1983~1990年连云港市机床、仪器仪表主要产品产量统计表",
    "table_number": "表21-4",
    "page": 1031,
    "pages": [1031],
    "part": "part01",
    "vol": "中",
    "volume": "中",
    "columns": ["类别", "产品", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990"],
    "rows": [
        ["弓锯床", "普通(台)", "228", "563", "659", "598", "645", "600", "570", "283"],
        ["弓锯床", "高效(台)", "", "", "28", "", "44", "62", "61", "91"],
        ["", "牛头刨床(台)", "", "", "58", "60", "50", "95", "100", ""],
        ["", "平板仪(台)", "2392", "2843", "2932", "1927", "1339", "2414", "1967", "1842"],
        ["光学仪器", "手持水准仪(台)", "2950", "3006", "2364", "3335", "2180", "1397", "3337", "3030"],
        ["光学仪器", "测斜仪(台)", "", "", "347", "591", "665", "255", "499", "577"],
        ["光学仪器", "电影机镜头(只)", "3477", "6212", "6341", "1360", "124", "50", "984", "949"],
        ["光学仪器", "片孔检查镜(只)", "1000", "1512", "1630", "1028", "1062", "425", "523", "432"],
        ["光学仪器", "目镜(万片)", "8.34", "1.05", "11.76", "13.96", "12.97", "10.50", "12.56", "6.70"],
        ["光学元件", "石英楔子(片)", "3012", "1650", "1173", "1124", "1187", "610", "740", "695"],
        ["光学元件", "锥体棱镜(块)", "23", "170", "162", "331", "232", "391", "437", "431"],
        ["光学元件", "大视场目镜(万套)", "0.60", "0.69", "0.47", "0.26", "1.31", "1.64", "1.25", "1.01"],
        ["", "轴承检查仪(台)", "300", "611", "419", "432", "353", "649", "763", "994"],
        ["", "水表(万只)", "27.37", "35.00", "34.41", "37.54", "42.04", "47.12", "48.14", "54.60"],
    ],
    "row_count": 14,
    "col_count": 10,
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/中/part01/page_0229.txt，并用 raw 坐标 OCR workbench/ocr/raw/中/part01/page_0229.json 校验年份列位。1990年轴承检查仪 raw OCR 误作 t66，按页级 OCR 及前页正文“产量994台”录为 994。源页未见数值的单元格保留空值。",
}

RESIDUE = "<p>t66611419353649763300432轴承检查仪（台）</p>"
SOURCES = [
    "workbench/ocr/paddle_ocr/中/part01/page_0229.txt",
    "workbench/ocr/raw/中/part01/page_0229.json",
    "workbench/ocr/paddle_ocr/中/part01/page_0228.txt",
    "output/final_reader/连云港市志_全书.html:9809",
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
    if count == 0 and "t66611419353649763300432轴承检查仪" not in text:
        return 0
    raise RuntimeError(f"expected machine-instrument residue once, got {count}")


def write_reports(json_changed: int, site_changed: int, embedded_count: int, removed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "table_id": ENTRY["table_id"], "json_changed": json_changed, "site_changed": site_changed, "embedded_count": embedded_count, "reader_residue_removed": removed, "sources": SOURCES}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 机床仪器仪表主要产品产量表回源核录",
        "",
        f"- 时间：{now}",
        f"- 表格：`{ENTRY['table_id']}` {ENTRY['table_number']} {ENTRY['title']}。",
        "- 处理：据中册 part01/page_0229 页级 OCR 和 raw 坐标 OCR 核录表 21-4，撤出主阅读版中轴承检查仪行压扁残片。",
        f"- 变更：JSON {json_changed}；结构化表格站 {site_changed}；主阅读版已核表嵌回 {embedded_count} 张；撤出残片 {removed} 段。",
        "",
        "## 证据",
        "",
    ]
    lines.extend(f"- `{source}`" for source in SOURCES)
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    append_once(MEMORY, "## 2026-07-05 机床仪器仪表主要产品产量表回源核录", f"""
## 2026-07-05 机床仪器仪表主要产品产量表回源核录
- 新增并运行 `scripts/verify_z142_machine_instrument_output_20260705.py`，据中册 part01/page_0229 核录 `LYG-中-T142` 表21-4《1983~1990年连云港市机床、仪器仪表主要产品产量统计表》。
- 主阅读版撤出 `t66611419353649763300432轴承检查仪（台）` 压扁残片；1990 年轴承检查仪按页级 OCR 和正文旁证录为 994。
- 报告：`output/reports/machine_instrument_output_20260705.md`。
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
    print("machine_instrument_output_verified")
    print(f"json_changed={json_changed}")
    print(f"site_changed={site_changed}")
    print(f"embedded_count={embedded_count}")
    print(f"reader_residue_removed={removed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

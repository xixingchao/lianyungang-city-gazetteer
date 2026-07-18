# -*- coding: utf-8 -*-
"""Verify table 10-14 and remove its flattened reader residue."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import embed_verified_tables_into_reader

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T054.json"
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "shubei_control_sluices_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "shubei_control_sluices_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_沭北主要控制涵闸表回源核录.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ENTRY = {
    "table_id": "LYG-上-T054",
    "title": "1990年连云港市沭北主要控制涵闸基本情况表",
    "table_number": "表10-14",
    "page": 598,
    "pages": [598, 599],
    "part": "part02",
    "vol": "上",
    "volume": "上",
    "columns": [
        "闸名",
        "闸址",
        "水系",
        "建成年月",
        "孔数",
        "每孔净宽(米)",
        "闸底高程(米)",
        "流量(立方米/秒)",
        "排水面积(平方公里)",
    ],
    "rows": [
        ["沭北闸", "罗阳小东关村西南", "沭北运河", "1978.5", "1", "10", "-1.0", "90", ""],
        ["范河闸", "临洪河西堤范河口", "范河", "1958.5", "3", "8.5", "-2.0", "367", "265"],
        ["朱稽河闸", "朱稽河新道入海口", "朱稽河", "1979.10", "5", "5", "-2.0", "162", "175"],
        ["朱堵桥闸", "朱堵乡前朱堵村南", "", "1966.10", "14", "2", "5.0", "372", "2×1"],
        ["塔林闸", "城头镇塔林村东", "朱稽河", "1967.6", "7", "2.1×6；2.5×1", "", "15.1", "156"],
        ["介沟闸", "班庄乡介沟村", "", "1972.8", "4", "5.08×3", "", "28.8", "119"],
        ["朱南闸", "朱稽河新道南黄沙引河口", "黄沙引河", "1984.10", "1", "10", "-1.0", "90", ""],
        ["朱北闸", "朱稽河新道北坝头村", "", "1983.11", "1", "10", "-1.0", "90", ""],
        ["青口河挡潮闸", "青口河入海处", "青口河", "1976.7", "7", "5；2×2", "-1.5", "600", "499"],
        ["青口闸", "青口镇", "", "1969.8", "7", "8.08×5", "", "2.6", "400"],
        ["沙汪河闸", "城东乡东沙村东北", "沙汪河", "1966.2", "4", "2；5.5×1", "-1.0", "53", ""],
        ["兴庄河闸", "兴庄河入海口", "兴庄河", "1959.9", "13", "2.4×12；2×1", "-2.5", "277", "163"],
        ["柳树漫水闸", "官河乡柳树村", "", "1966.5", "5", "5×4", "", "5", "118"],
        ["官庄河闸", "海头镇海脐村南", "官庄河", "1966", "5", "2；1.5×2", "-1.0", "99", "28"],
        ["石堰漫水闸", "前石堰村东南", "龙河", "1965.6", "8", "10×6；2×1", "", "13.8", "4450"],
        ["徐福漫水闸", "金山乡后徐阜村西南", "", "1971.5", "5", "5×4", "", "14.2", "110；16"],
        ["韩口河闸", "韩口河入海口韩口村", "", "1974.5", "6", "2", "-0.5", "95", ""],
        ["柘汪河闸", "柘汪河入海口", "柘汪河", "1982.5", "3", "4", "-1.0", "111", ""],
    ],
    "row_count": 18,
    "col_count": 9,
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0298.txt、page_0299.txt。该表跨页，page_0299 以“续上表”承接，至“第三章 挡潮工程”前结束。OCR 存在横向错位和跨行单元格，本轮按页级OCR可辨列序保守合并，未清晰单元格保留空值或以分号并列，不作常识补猜。",
}

RESIDUES = [
    "<p>沭北闸罗阳小东关村西南沭北运河1978.5-1.0范河闸临洪河西堤范河口范河1958.58.5-2.0朱稽河闸朱稽河新道入海口1979.10-2.0朱稽河朱堵桥闸朱堵乡前朱堵村南1966.105.02×1塔林闸城头镇塔林村东1967.615.12.1×6朱稽河2.5×1介沟闸班庄乡介沟村1972.828.85.08×3朱南闸朱稽河新道南黄沙引|河口黄沙引河1984.10-1.0朱北闸朱稽河新道北坝头村1983.11-1.0青口河青口河入海处1976.7-1.5挡潮闸青口河2×2青口闸青口镇1969.82.68.08×5</p>",
    "<p>沙汪河闸城东乡东沙村东北沙汪河1966.2-1.05.5×1兴庄河闸兴庄河入海口1959.9-2.5兴庄河2.4×122×1柳树漫水闸官河乡柳树村1966.55×4官庄河闸海头镇海脐村南官庄河-1.01.5×2石堰漫水闸前石堰村东南1965.613.8龙10×6河2×1徐福漫水闸金山乡后徐阜村西南1971.514.25×4韩口河闸韩口河入海口韩口村1974.5-0.5柘汪河闸柘汪河入海口柘汪河1982.5-1.0</p>",
]

SOURCES = [
    "workbench/ocr/paddle_ocr/上/part02/page_0298.txt",
    "workbench/ocr/paddle_ocr/上/part02/page_0299.txt",
    "output/final_reader/连云港市志_全书.html:5488",
    "output/final_reader/连云港市志_全书.html:5494",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_json() -> int:
    old = DATA.read_text(encoding="utf-8") if DATA.exists() else ""
    new = json.dumps(ENTRY, ensure_ascii=False, indent=2) + "\n"
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
    text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
    SITE.write_text(text, encoding="utf-8")
    return 1


def remove_reader_residues() -> int:
    text = HTML.read_text(encoding="utf-8")
    changed = 0
    for residue in RESIDUES:
        count = text.count(residue)
        if count == 1:
            text = text.replace(residue, "", 1)
            changed += 1
        elif count > 1:
            raise RuntimeError(f"reader residue matched {count} times")
    HTML.write_text(text, encoding="utf-8")
    return changed


def write_reports(json_changed: int, site_changed: int, embedded_count: int, residue_removed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "table_id": ENTRY["table_id"],
        "title": ENTRY["title"],
        "json_changed": json_changed,
        "site_changed": site_changed,
        "embedded_count": embedded_count,
        "reader_residue_paragraphs_removed": residue_removed,
        "sources": SOURCES,
        "notes": ENTRY["notes"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 沭北主要控制涵闸表回源核录",
        "",
        f"- 时间：{now}",
        f"- 表ID：`{ENTRY['table_id']}`",
        f"- 表题：{ENTRY['table_number']} {ENTRY['title']}",
        f"- 数据：{ENTRY['row_count']} 行 × {ENTRY['col_count']} 列；源页：{', '.join(str(p) for p in ENTRY['pages'])}",
        f"- 变更：JSON {json_changed}；结构化表格站 {site_changed}；主阅读版已核表嵌回 {embedded_count} 张；撤出压扁段落 {residue_removed} 段。",
        "- 口径：跨行/错位格按页级 OCR 可辨列序保守合并；未清晰单元格不猜补。",
        "",
        "## 证据",
        "",
    ]
    lines.extend(f"- `{source}`" for source in SOURCES)
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 沭北主要控制涵闸表回源核录"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/verify_s054_shubei_control_sluices_20260705.py`，据上册 part02 第 298、299 页页级 OCR 核录 {ENTRY['table_number']} `{ENTRY['title']}`，登记为 `{ENTRY['table_id']}`。
- 该表跨页，page_0299 以“续上表”承接，至 `第三章 挡潮工程` 前结束；本轮同时撤出主阅读版中两段压扁残片 `沭北闸罗阳...`、`沙汪河闸城东乡...`。
- 对 OCR 横向错位和跨行单元格采用保守口径：可辨者合并，未清晰者留空或分号并列，不作常识补猜。
- 报告：`output/reports/shubei_control_sluices_20260705.md`。
""",
    )


def main() -> None:
    json_changed = write_json()
    site_changed = patch_site()
    embedded_count, unplaced = embed_verified_tables_into_reader.embed()
    if unplaced:
        raise RuntimeError(f"unplaced verified tables: {unplaced}")
    embed_verified_tables_into_reader.write_progress(embedded_count, unplaced)
    embed_verified_tables_into_reader.update_memory(embedded_count, unplaced)
    residue_removed = remove_reader_residues()
    write_reports(json_changed, site_changed, embedded_count, residue_removed)
    print("shubei_control_sluices_verified")
    print(f"json_changed={json_changed}")
    print(f"site_changed={site_changed}")
    print(f"embedded_count={embedded_count}")
    print(f"reader_residue_paragraphs_removed={residue_removed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

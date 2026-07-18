# -*- coding: utf-8 -*-
"""Verify township enterprise tables and remove flattened reader residues."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import embed_verified_tables_into_reader

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "workbench" / "table_entries" / "中" / "data"
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "township_enterprise_tables_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "township_enterprise_tables_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_乡镇企业表格残片回源核录.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TABLES = [
    {
        "table_id": "LYG-中-T139",
        "title": "1990年连云港市三区三县“两户”企业基本情况表",
        "table_number": "表27-3",
        "page": 1300,
        "pages": [1300],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": ["项目", "分类", "海州区", "云台区", "连云区", "赣榆县", "东海县", "灌云县"],
        "rows": [
            ["企业个数(个)", "小计", "338", "483", "55", "12831", "7967", "11802"],
            ["企业个数(个)", "户办", "338", "481", "55", "12466", "7930", "11163"],
            ["企业个数(个)", "联户办", "", "2", "", "365", "37", "639"],
            ["企业人数(人)", "小计", "2349", "1184", "112", "38759", "23421", "26685"],
            ["企业人数(人)", "户办", "2349", "1176", "112", "35985", "23097", "23739"],
            ["企业人数(人)", "联户办", "", "8", "", "2774", "324", "2946"],
            ["总产值(万元)", "企业合计", "674", "1155", "49", "22615", "11757", "23071"],
            ["总产值(万元)", "其中：工业", "490", "", "", "11055", "6297", "16378"],
            ["总产值(万元)", "户办企业", "674", "1146", "49", "20096", "11508", "20484"],
            ["总产值(万元)", "户办其中：工业", "490", "", "", "10216", "6111", "14310"],
            ["总产值(万元)", "联户办企业", "", "9", "", "2529", "249", "2587"],
            ["总产值(万元)", "联户办其中：工业", "", "", "", "839", "186", "2068"],
            ["销售收入(万元)", "企业", "768", "1237", "28", "23986", "11152", "22769"],
            ["销售收入(万元)", "其中：工业", "358", "", "", "10209", "5429", "16153"],
        ],
        "row_count": 14,
        "col_count": 8,
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/中/part01/page_0397.txt，并参考 raw OCR：workbench/ocr/raw/中/part01/page_0397.txt。源页注为“新浦区无‘两户’企业”；部分空白单元格按源页保留空值，不按小计反推。",
    },
    {
        "table_id": "LYG-中-T140",
        "title": "1990年连云港市乡镇企业主要产品产量统计表（首页）",
        "table_number": "表27-8",
        "page": 1308,
        "pages": [1308],
        "part": "part01",
        "vol": "中",
        "volume": "中",
        "columns": ["类别", "产品名称", "计算单位", "合计", "乡办", "村办"],
        "rows": [
            ["工业", "耐火粘土", "吨", "505", "505", ""],
            ["", "原盐", "吨", "82118", "64892", "17226"],
            ["", "粮食加工", "万吨", "19", "3", "16"],
            ["", "其中：大米", "万吨", "7", "1", "6"],
            ["", "面粉", "万吨", "12", "1", "11"],
            ["", "食用植物油", "吨", "5433", "1708", "3725"],
            ["", "罐头", "吨", "914", "608", "306"],
            ["", "其中：水果罐头", "吨", "791", "506", "285"],
            ["", "饮料酒(商品量、混合量)", "吨", "6415", "5990", "425"],
            ["", "其中：白酒", "吨", "6185", "5787", "398"],
            ["", "汽水", "吨", "847", "612", "235"],
            ["", "配合饲料", "吨", "6499", "2172", "4327"],
            ["", "混合饲料", "吨", "1691", "1290", "401"],
            ["", "轧花", "吨", "6200", "1490", "4710"],
            ["", "针棉织品(折合用纱量)", "吨", "18", "15", "3"],
            ["", "纱", "吨/件", "632/6320", "632/6320", ""],
            ["", "布", "万米/万平方米", "330/333", "325/327", "5/6"],
            ["", "其中：纯棉布", "万米/万平方米", "263/264", "263/264", ""],
            ["", "服装", "万件", "212", "203", "9"],
            ["", "皮鞋", "万双", "7", "6", "1"],
            ["", "竹藤棕草柳葵制品", "万元", "659", "501", "158"],
            ["", "各种家具", "万件", "30", "13", "17"],
            ["", "机制纸及纸板", "吨", "11499", "11461", "38"],
            ["", "工艺美术制品", "万元", "43", "43", ""],
        ],
        "row_count": 24,
        "col_count": 6,
        "status": "verified",
        "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/中/part01/page_0405.txt，并参考 raw OCR：workbench/ocr/raw/中/part01/page_0405.txt。本条为表27-8首页，续表见 LYG-中-T038；源页未见数值处保留空值。",
    },
]

RESIDUES = [
    "<p>产值（1980年不变价、万元）</p>\n<p>企业人数（人）</p>\n<p>其中：工业102164906111143102529企业2492587联户办其中：工业8391862068企业768123728239861115222769销售收入（万元）</p>\n<p>其中：工业35854291615310209注：新浦区无“两户”企业。</p>",
    "<p>主要产品产量统计表表 27 - 8合计乡办类别产品名称计算单位村办505耐火粘土505原盐821186489217226万吨粮食加工1916万吨其中：大米面粉万吨12食用植物油170854333725罐头914608306其中：水果罐头5062857915990425饮料酒（商品量、混合量）</p>\n<p>6415其中:白酒61855787398汽水612235847配合饲料64992172432716911290401混合饲料6200轧花149047101815针棉织品（折合用纱量）</p>\n<p>吨/件632/6320632/63205/6325/327万米/万平方米330/333其中：纯梯布万米/万平方米263/264263/264万件服装212203万双皮鞋万元501158659竹藤棕草柳葵制品万件3017各种家具131146138机制纸及纸板1149943万元43工艺美术制品</p>",
]

SOURCES = [
    "workbench/ocr/paddle_ocr/中/part01/page_0397.txt",
    "workbench/ocr/paddle_ocr/中/part01/page_0405.txt",
    "workbench/ocr/paddle_ocr/中/part01/page_0406.txt",
    "output/final_reader/连云港市志_全书.html paragraphs 8850-8851, 8898-8900",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_jsons() -> int:
    changed = 0
    for table in TABLES:
        path = DATA_DIR / f"{table['table_id']}.json"
        new = json.dumps(table, ensure_ascii=False, indent=2) + "\n"
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        if old != new:
            path.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise RuntimeError("TABLES payload not found")
    tables = json.loads(match.group(1))
    before = json.dumps(tables, ensure_ascii=False, sort_keys=True)
    ids = {table["table_id"] for table in TABLES}
    tables = [table for table in tables if table.get("table_id") not in ids]
    tables.extend(TABLES)
    tables.sort(key=lambda item: (str(item.get("vol") or item.get("volume") or ""), int(item.get("page") or 999999), str(item.get("table_id") or "")))
    after = json.dumps(tables, ensure_ascii=False, sort_keys=True)
    if before == after:
        return 0
    SITE.write_text(text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :], encoding="utf-8")
    return 1


def repair_reader() -> int:
    text = HTML.read_text(encoding="utf-8")
    changed = 0
    for residue in RESIDUES:
        count = text.count(residue)
        if count == 1:
            text = text.replace(residue, "", 1)
            changed += 1
        elif count > 1:
            raise RuntimeError(f"residue matched {count} times")
    HTML.write_text(text, encoding="utf-8")
    return changed


def write_reports(json_changed: int, site_changed: int, embedded_count: int, removed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "tables": [t["table_id"] for t in TABLES], "json_changed": json_changed, "site_changed": site_changed, "embedded_count": embedded_count, "reader_residue_groups_removed": removed, "sources": SOURCES}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 乡镇企业表格残片回源核录",
        "",
        f"- 时间：{now}",
        "- 表格：`LYG-中-T139` 表27-3；`LYG-中-T140` 表27-8首页。",
        "- 处理：据中册 part01/page_0397、page_0405 页级 OCR 核录，撤出主阅读版中对应压扁残片；表27-8续表沿用既有 `LYG-中-T038`。",
        f"- 变更：JSON {json_changed}；结构化表格站 {site_changed}；主阅读版已核表嵌回 {embedded_count} 张；撤出残片组 {removed} 组。",
        "",
        "## 证据",
        "",
    ]
    lines.extend(f"- `{s}`" for s in SOURCES)
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    append_once(MEMORY, "## 2026-07-05 乡镇企业表格残片回源核录", f"""
## 2026-07-05 乡镇企业表格残片回源核录
- 新增并运行 `scripts/verify_z139_z140_township_enterprise_tables_20260705.py`，据中册 part01/page_0397 核录 `LYG-中-T139` 表27-3《1990年连云港市三区三县“两户”企业基本情况表》，据 page_0405 核录 `LYG-中-T140` 表27-8首页《1990年连云港市乡镇企业主要产品产量统计表（首页）》。
- 主阅读版撤出所有制结构末尾 `其中：工业102164...` 残片，以及产业结构末尾表27-8首页压扁残片；表27-8续表继续使用既有 `LYG-中-T038`。
- 报告：`output/reports/township_enterprise_tables_20260705.md`。
""")


def main() -> None:
    json_changed = write_jsons()
    site_changed = patch_site()
    embedded_count, unplaced = embed_verified_tables_into_reader.embed()
    if unplaced:
        raise RuntimeError(f"unplaced verified tables: {unplaced}")
    embed_verified_tables_into_reader.write_progress(embedded_count, unplaced)
    embed_verified_tables_into_reader.update_memory(embedded_count, unplaced)
    removed = repair_reader()
    write_reports(json_changed, site_changed, embedded_count, removed)
    print("township_enterprise_tables_verified")
    print(f"json_changed={json_changed}")
    print(f"site_changed={site_changed}")
    print(f"embedded_count={embedded_count}")
    print(f"reader_residue_groups_removed={removed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

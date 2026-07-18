# -*- coding: utf-8 -*-
"""Add verified table 17-6 and remove flattened bamboo-shop residue."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T134.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_bamboo_shop_table_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_bamboo_shop_table_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第十七卷竹铺经营情况表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

COLUMNS = ["铺店名称", "业主姓名", "业主籍贯", "开业时间(年、月)", "地址", "资本(元)", "固定资金(元)", "流动资本(元)"]

ROWS = [
    ["信昌竹号", "张学奎", "新浦", "1949.12", "民主路47号", "50", "20", "30"],
    ["天顺永竹货店", "魏天成", "曹县", "1950.2", "解放路90号", "200", "50", "150"],
    ["恒昌竹铺", "张同恒", "新浦", "1950.4", "通灌路46号", "100", "14", "86"],
    ["鑫隆竹铺", "李守仁", "灌云", "1950.5", "民主路270号", "210", "50", "160"],
    ["颜德记竹铺", "颜承德", "新浦", "1950.5", "民主路325号", "60", "15", "45"],
    ["寿记竹铺", "龚寿林", "灌云", "1950.5", "民主路355号", "50", "15", "35"],
    ["凤记竹器店", "朱凤领", "赣榆", "1950.5", "民主路94号", "50", "20", "30"],
    ["继成竹铺", "张继富", "", "1950.5", "民主路民生巷", "35", "15", "20"],
    ["宝华竹铺", "吴德宝", "海州", "1951.4", "车站街河边路2号", "70", "30", "40"],
    ["庆云竹铺", "孙继清", "徐州", "1951.5", "民主路544号", "150", "20", "130"],
    ["胜记竹铺", "朱凤永", "", "1951.4", "民主路1号", "25", "10", "15"],
    ["天成永竹店", "魏白氏", "曹县", "1951.7", "民主路425号", "120", "20", "100"],
    ["胜利竹铺", "孙从明", "东海", "1952", "民主路345号", "80", "30", "50"],
    ["姚代治", "姚代治", "", "1954.7", "新河街八闾", "30", "5", "25"],
    ["德祥竹铺", "姚广全", "灌云", "1954.12", "民主路8号", "20", "7", "13"],
    ["德兴竹铺", "吴学树", "", "", "刘家巷2号", "60", "20", "40"],
]

ENTRY = {
    "table_id": "LYG-中-T134",
    "title": "1949~1954年新浦独资经营竹铺（店）情况表",
    "table_number": "表17-6",
    "page": 837,
    "pages": [837],
    "part": "part01",
    "vol": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/中/part01/page_0035.txt；并参考 raw OCR：workbench/ocr/raw/中/part01/page_0035.txt。源表单位为元，资本栏展开为资本、固定资金、流动资本。源页未见业主籍贯或开业时间处保留空值。注：曹县分属山东。",
    "volume": "中",
}

RESIDUE_RE = re.compile(
    r"\n?<p>资金资本信昌竹号张学奎新浦1949\.12民主路47号502030曹县魏天成天顺永竹货店.*?注：曹县分属山东。</p>\s*",
    re.S,
)


def render_table() -> str:
    thead = "".join(f"<th>{html.escape(col)}</th>" for col in COLUMNS)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>" for row in ROWS)
    return (
        '<section class="verified-table-block" id="table-LYG-中-T134"><div class="structured-table-meta">'
        '表ID：LYG-中-T134；源页：837</div>'
        '<table class="structured-table"><caption>表17-6 1949~1954年新浦独资经营竹铺（店）情况表</caption>'
        f"<thead><tr>{thead}</tr></thead><tbody>{body}</tbody></table><p class=\"table-note\">注：曹县分属山东。</p></section>"
    )


def write_json() -> bool:
    old = DATA.read_text(encoding="utf-8") if DATA.exists() else ""
    new = json.dumps(ENTRY, ensure_ascii=False, indent=2) + "\n"
    if old != new:
        DATA.write_text(new, encoding="utf-8")
        return True
    return False


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise RuntimeError("TABLES payload not found")
    tables = json.loads(match.group(1))
    changed = False
    for idx, table in enumerate(tables):
        if table.get("table_id") == ENTRY["table_id"]:
            if table != ENTRY:
                tables[idx] = ENTRY
                changed = True
            break
    else:
        tables.append(ENTRY)
        changed = True
    if changed:
        tables.sort(key=lambda t: (str(t.get("vol") or t.get("volume") or ""), int((t.get("pages") or [t.get("page") or 999999])[0]), str(t.get("table_id") or "")))
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
        return 1
    return 0


def patch_reader() -> int:
    text = HTML.read_text(encoding="utf-8")
    if 'id="table-LYG-中-T134"' in text:
        new, count = RESIDUE_RE.subn("\n", text, count=1)
    else:
        new, count = RESIDUE_RE.subn("\n" + render_table() + "\n", text, count=1)
    if count != 1 and 'id="table-LYG-中-T134"' not in text:
        raise RuntimeError(f"expected to replace 1 bamboo-shop residue block, replaced {count}")
    if new != text:
        HTML.write_text(new, encoding="utf-8")
    return count


def write_reports(json_changed: bool, site_changed: int, replaced: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    result = {
        "time": now,
        "table_id": ENTRY["table_id"],
        "table_number": ENTRY["table_number"],
        "title": ENTRY["title"],
        "source_pages": ENTRY["pages"],
        "json_changed": json_changed,
        "site_changed": site_changed,
        "reader_flattened_blocks_replaced": replaced,
        "rows": len(ROWS),
        "columns": len(COLUMNS),
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第十七卷竹铺经营情况表残文修复

- 时间：{now}
- 表ID：`LYG-中-T134`
- 表题：表17-6 `1949~1954年新浦独资经营竹铺（店）情况表`
- 源页：`workbench/ocr/paddle_ocr/中/part01/page_0035.txt`

## 修复动作

- 新增 verified 结构化表：`workbench/table_entries/中/data/LYG-中-T134.json`，{len(ROWS)} 行、{len(COLUMNS)} 列。
- 同步结构化表格站：`output/structured_tables/index.html`。
- 将最终阅读版中 `资金资本信昌竹号...德兴竹铺...注：曹县分属山东。` 的压平残文替换为 verified 表块：{replaced} 组。

## 核对说明

- 表17-6位于第十七卷第三章竹、藤、草、柳编第一节竹编末尾、第二节藤编前。
- 表头单位为元；资本栏按源页展开为资本、固定资金、流动资本。
- 源页未见业主籍贯或开业时间处保留空值；`姚代治` 行地址据 paddle OCR 录为 `新河街八闾`。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(replaced: int) -> None:
    marker = "## 2026-07-01 第十七卷竹铺经营情况表残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第十七卷工艺美术 `资金资本信昌竹号...德兴竹铺...` 摊平残文回源处理。
- 据 `workbench/ocr/paddle_ocr/中/part01/page_0035.txt` 新增 `workbench/table_entries/中/data/LYG-中-T134.json`：表17-6《1949~1954年新浦独资经营竹铺（店）情况表》，16 行 8 列。
- 阅读版中表17-6压平残文已替换为 verified 表块 {replaced} 组，并同步结构化表格站。
- 报告：`output/reports/reader_readability_bamboo_shop_table_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    json_changed = write_json()
    site_changed = patch_site()
    replaced = patch_reader()
    write_reports(json_changed, site_changed, replaced)
    update_memory(replaced)
    print(f"json_changed={int(json_changed)}")
    print(f"site_changed={site_changed}")
    print(f"reader_flattened_blocks_replaced={replaced}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

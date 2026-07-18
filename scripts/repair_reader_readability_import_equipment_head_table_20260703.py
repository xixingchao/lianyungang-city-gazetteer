# -*- coding: utf-8 -*-
"""Add verified table 35-5 head row and remove flattened import-equipment residue."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T138.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_import_equipment_head_table_20260703.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_import_equipment_head_table_20260703.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第三十五卷进口设备和产品情况表首页残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

COLUMNS = ["单位", "项目(单机)名称", "金额(万美元)"]
ROWS = [["市纺织工业公司系统", "项目21单机4件", "2167.21"]]

ENTRY = {
    "table_id": "LYG-中-T138",
    "title": "1984~1990年连云港市进口设备和产品情况表（首页）",
    "table_number": "表35-5",
    "page": 1611,
    "pages": [1611],
    "part": "part02",
    "vol": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0191.txt。仅录入源页可见的表35-5首页汇总行；续页见LYG-中-T082至LYG-中-T087。阅读版旧压平残文已替换为结构化 verified 表块。",
    "volume": "中",
}

RESIDUE_RE = re.compile(
    r"\n?<p>项目\(单机\)名称项目21单机4件2167\.21市纺织工业公司系统·1494：</p>\s*"
    r"(?:\n\s*)*"
    r"<p>项目3单机2606\.63硅钢片剪切生产线316\.44市机械局系统98\.97波纹油箱生产线（液压升降台）</p>\s*"
    r"(?:\n\s*)*"
    r"<p>漆包线加工设备（锯床）</p>\s*",
    re.S,
)


def render_table() -> str:
    thead = "".join(f"<th>{html.escape(col)}</th>" for col in COLUMNS)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>" for row in ROWS)
    return (
        '<section class="verified-table-block" id="table-LYG-中-T138"><div class="structured-table-meta">'
        '表ID：LYG-中-T138；源页：1611</div>'
        '<table class="structured-table"><caption>表35-5 1984~1990年连云港市进口设备和产品情况表（首页）</caption>'
        f"<thead><tr>{thead}</tr></thead><tbody>{body}</tbody></table></section>"
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
    if 'id="table-LYG-中-T138"' in text:
        new, count = RESIDUE_RE.subn("\n", text, count=1)
    else:
        new, count = RESIDUE_RE.subn("\n" + render_table() + "\n", text, count=1)
    if count != 1 and 'id="table-LYG-中-T138"' not in text:
        raise RuntimeError(f"expected to replace 1 import-equipment residue block, replaced {count}")
    if new != text:
        HTML.write_text(new, encoding="utf-8")
    return count


def write_reports(json_changed: bool, site_changed: int, replaced: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    reader_block_present = 'id="table-LYG-中-T138"' in HTML.read_text(encoding="utf-8")
    displayed_replaced = replaced or int(reader_block_present)
    result = {
        "time": now,
        "table_id": ENTRY["table_id"],
        "table_number": ENTRY["table_number"],
        "title": ENTRY["title"],
        "source_pages": ENTRY["pages"],
        "source_ocr": "workbench/ocr/paddle_ocr/中/part02/page_0191.txt",
        "json_changed": json_changed,
        "site_changed": site_changed,
        "reader_flattened_blocks_replaced": replaced,
        "reader_verified_blocks_present": int(reader_block_present),
        "rows": len(ROWS),
        "columns": len(COLUMNS),
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第三十五卷进口设备和产品情况表首页残文修复

- 时间：{now}
- 表ID：`LYG-中-T138`
- 表题：表35-5 `1984~1990年连云港市进口设备和产品情况表（首页）`
- 源页：`workbench/ocr/paddle_ocr/中/part02/page_0191.txt`

## 修复动作

- 新增 verified 结构化表：`workbench/table_entries/中/data/LYG-中-T138.json`，{len(ROWS)} 行、{len(COLUMNS)} 列。
- 同步结构化表格站：`output/structured_tables/index.html`。
- 将最终阅读版中表35-5首页及后续页重复线性残文替换为首页 verified 表块：{displayed_replaced} 组。

## 核对说明

- 表35-5首页与表35-4同在 `page_0191.txt`，源页仅可见首页汇总行：`市纺织工业公司系统 / 项目21单机4件 / 2167.21`。
- 残文中的 `项目3单机2606.63...漆包线加工设备（锯床）` 已在 `LYG-中-T084` verified 续表中核录，故本轮只保留首页新增表块。
- 表35-5续页仍由 `LYG-中-T082` 至 `LYG-中-T087` 承接。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(replaced: int) -> None:
    marker = "## 2026-07-03 第三十五卷进口设备和产品情况表首页残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第三十五卷进口贸易第三节设备引进开头 `项目(单机)名称项目21单机4件2167.21...` 表格压平残文回源处理。
- 据 `workbench/ocr/paddle_ocr/中/part02/page_0191.txt` 新增 `workbench/table_entries/中/data/LYG-中-T138.json`：表35-5《1984~1990年连云港市进口设备和产品情况表（首页）》，1 行 3 列。
- 阅读版中表35-5首页残文已替换为 verified 表块 {replaced} 组；后续页仍由 `LYG-中-T082` 至 `LYG-中-T087` 承接。
- 报告：`output/reports/reader_readability_import_equipment_head_table_20260703.md`。
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

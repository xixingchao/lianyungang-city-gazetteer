# -*- coding: utf-8 -*-
"""Add verified table 35-4 and remove flattened import-agency residue."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T137.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_foreign_import_agency_table_20260703.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_foreign_import_agency_table_20260703.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第三十五卷进口办事处代理进口情况表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

COLUMNS = ["购设备单位", "进口国别和地区", "金额(美元)", "设备名称", "进口日期"]

ROWS = [
    ["连云港市桐木厂", "日本", "54474.34", "拼板加机器", "1985.2"],
    ["连云港市邮电局", "日本", "36300.00", "光纤电缆", "1985.3"],
    ["连云港市毛巾厂", "法国", "6000.00", "割绒滚刀", "1985.4"],
    ["连云港炼糖厂", "香港", "7800.00", "聚丙烯胺", "1985.5"],
    ["连云港市建材公司", "日本", "50000.00", "钢材", "1985.7"],
    ["连云港市盐业公司", "日本", "25215.00", "绒线针织机", "1985.12"],
    ["连云港市有机化工厂", "日本", "149993.50", "EVA 树脂生产线", "1986.1"],
    ["连云港市有机化工厂", "日本", "600000.00", "热熔胶生产线", "1986.1"],
    ["连云港木器厂", "瑞士", "740000.00", "席梦思生产线", "1986.4"],
    ["连云港食品总厂", "日本", "346381.00", "方便面生产线", "1986.10"],
    ["东海县光学仪器厂", "日本", "850000.00", "五棱镜生产线", "1986.10"],
    ["连云港市包装二厂", "日本", "860000.00", "纸盒包装生产线", "1986.10"],
]

ENTRY = {
    "table_id": "LYG-中-T137",
    "title": "1985~1986年连云港市进口办事处代理进口情况表",
    "table_number": "表35-4",
    "page": 1611,
    "pages": [1611],
    "part": "part02",
    "vol": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR回源核录：workbench/ocr/paddle_ocr/中/part02/page_0191.txt。阅读版原有压平残文已替换为结构化 verified 表块；表35-4紧接表35-5前页。",
    "volume": "中",
}

RESIDUE_RE = re.compile(
    r"\n?<p>和地区日本连云港市桐木厂54474\.34拼板加机器1985\.2日本光纤电缆1985\.336300\.00连云港市邮电局法国6000\.001985\. 4连云港市毛巾厂割绒滚刀香港聚丙烯胺1985\.5连云港炼糖厂7800\.00钢材50000\.001985\.7连云港市建材公司绒线针织机连云港市盐业公司1985\.1225215\.00149993\. 50连云港市有机化工厂EVA树脂生产线1986\.1热熔胶生产线600000\.001986\.1连云港市有机化工厂席梦思生产线1986\.4740000\.00连云港木器厂346381\.00方便面生产线1986\.10连云港食品总厂850000\.001986\.10五棱镜生产线东海县光学仪器厂1986\. 10860000\.00纸盒包装生产线连云港市包装二厂</p>\s*",
    re.S,
)


def render_table() -> str:
    thead = "".join(f"<th>{html.escape(col)}</th>" for col in COLUMNS)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>" for row in ROWS)
    return (
        '<section class="verified-table-block" id="table-LYG-中-T137"><div class="structured-table-meta">'
        '表ID：LYG-中-T137；源页：1611</div>'
        '<table class="structured-table"><caption>表35-4 1985~1986年连云港市进口办事处代理进口情况表</caption>'
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
    if 'id="table-LYG-中-T137"' in text:
        new, count = RESIDUE_RE.subn("\n", text, count=1)
    else:
        new, count = RESIDUE_RE.subn("\n" + render_table() + "\n", text, count=1)
    if count != 1 and 'id="table-LYG-中-T137"' not in text:
        raise RuntimeError(f"expected to replace 1 import-agency residue block, replaced {count}")
    if new != text:
        HTML.write_text(new, encoding="utf-8")
    return count


def write_reports(json_changed: bool, site_changed: int, replaced: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    reader_block_present = 'id="table-LYG-中-T137"' in HTML.read_text(encoding="utf-8")
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
    md = f"""# 第三十五卷进口办事处代理进口情况表残文修复

- 时间：{now}
- 表ID：`LYG-中-T137`
- 表题：表35-4 `1985~1986年连云港市进口办事处代理进口情况表`
- 源页：`workbench/ocr/paddle_ocr/中/part02/page_0191.txt`

## 修复动作

- 新增 verified 结构化表：`workbench/table_entries/中/data/LYG-中-T137.json`，{len(ROWS)} 行、{len(COLUMNS)} 列。
- 同步结构化表格站：`output/structured_tables/index.html`。
- 将最终阅读版中 `和地区日本连云港市桐木厂54474.34...纸盒包装生产线连云港市包装二厂` 的压平残文替换为 verified 表块：{displayed_replaced} 组。

## 核对说明

- 表35-4位于第三十五卷第三章进口贸易第二节代理进口末尾、第三节设备引进前。
- 表头按源页复合表头展开为 `购设备单位`、`进口国别和地区`、`金额(美元)`、`设备名称`、`进口日期`。
- 行值据页级 OCR 逐项核录；`EVA 树脂生产线` 保留源 OCR 可见空格。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(replaced: int) -> None:
    marker = "## 2026-07-03 第三十五卷进口办事处代理进口情况表残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第三十五卷进口贸易 `和地区日本连云港市桐木厂54474.34...纸盒包装生产线连云港市包装二厂` 摊平残文回源处理。
- 据 `workbench/ocr/paddle_ocr/中/part02/page_0191.txt` 新增 `workbench/table_entries/中/data/LYG-中-T137.json`：表35-4《1985~1986年连云港市进口办事处代理进口情况表》，12 行 5 列。
- 阅读版中表35-4压平残文已替换为 verified 表块 {replaced} 组，并同步结构化表格站。
- 报告：`output/reports/reader_readability_foreign_import_agency_table_20260703.md`。
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

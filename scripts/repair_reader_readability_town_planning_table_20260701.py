# -*- coding: utf-8 -*-
"""Repair table 5-1 data and remove duplicate flattened reader residue."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T009.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_town_planning_table_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_town_planning_table_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第五卷建制镇规划表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

COLUMNS = [
    "地区",
    "建制镇",
    "镇的性质",
    "人口(万人)",
    "用地(平方公里)",
    "规划年限",
    "编制完成年份",
]

ROWS = [
    ["市区", "锦屏", "工矿区和生活居住区相结合型", "", "", "1985~2000", "1985"],
    ["市区", "南城", "轻工业及综合型", "1.60", "2.00", "1985~2000", "1985"],
    ["市区", "板桥", "盐业及化工生产", "1.20", "1.50", "1985~2000", "1985"],
    ["市区", "徐圩", "盐业及化工生产", "1.50", "3.50", "1990~2000", "1990"],
    ["赣榆县", "赣马", "以农业加工、轻工为主的地区性农贸服务中心", "1.67", "0.93", "1983~2000", "1983"],
    ["赣榆县", "欢墩", "以养殖、种植为主的地区性农贸中心", "", "0.85", "1983~2000", "1983"],
    ["赣榆县", "海头", "以水产养殖为中心", "3.70", "", "1984~2000", "1984"],
    ["赣榆县", "沙河", "以蔬菜、粮油加工为主", "1.55", "2.16", "1986~2000", "1986"],
    ["赣榆县", "城头", "以农副产品加工和建筑材料为主体的工业小城镇", "0.90", "2.10", "1986~2000", "1986"],
    ["赣榆县", "石桥", "以干果加工及陶器为中心", "1.50", "", "1987~2000", "1987"],
    ["赣榆县", "黑林", "以开发山区为重点、森林加工为特色的区域性农副产品商贸中心", "1.30", "", "1987~2000", "1987"],
    ["赣榆县", "墩尚", "以饲料加工、交通为中心", "1.00", "3.60", "1987~2000", "1987"],
    ["东海县", "桃林", "", "1.50", "1.57", "1984~2000", "1984"],
    ["东海县", "白塔埠", "", "", "", "1987~2000", "1987"],
    ["东海县", "温泉", "以旅游、疗休服务为主、环境优美的新兴城镇", "0.70", "1.38", "1987~2000", "1987"],
    ["东海县", "青湖", "以发展农副产品和矿产品加工为主的环境优美的小城镇", "1.50", "4.00", "1990~2000", "1990"],
    ["东海县", "房山", "以镇办企业为主，满足本镇需要，畅销外县、省，经济繁荣的小城镇", "1.00", "1.70", "1990~2000", "1990"],
    ["灌云县", "燕尾", "灌云县对外开放口岸，以盐业、海产品加工为主的，并有电力和盐化潜力的港口小城市", "2.00", "2.00", "1986~2000", "1986"],
    ["灌云县", "龙苴", "以食品工业为主，农工副交通运输协调发展的中心集镇", "2.00", "1.20", "1984~2000", "1984"],
    ["灌云县", "板浦", "以发展轻纺、化工、建材、食品为主的地方性工业，环境优美，具有水乡特色的县属镇", "2.50", "", "1986~2000", "1986"],
    ["灌云县", "四队", "", "4.65", "", "1984~2000", "1984"],
    ["灌云县", "杨集", "", "", "", "1986~2000", "1986"],
]

ENTRY = {
    "table_id": "LYG-上-T009",
    "title": "1990年连云港市建制镇规划情况表",
    "table_number": "表5-1",
    "pages": [338],
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/上/part02/page_0038.txt；并参考 raw OCR：workbench/ocr/raw/上/part02/page_0038.txt。源页表题为表5-1，位于建制镇规划正文后；前四行按源页竖排分组归入市区，赣马行补入赣榆县组。源页未见人口或用地数值处保留空值。",
    "volume": "上",
}

RESIDUE_RE = re.compile(
    r"\n?<p>（平方公里）</p>\s*"
    r"<p>锦屏工矿区和生活居住区相结合型1985～2000市南城轻工业及综合型1\.602\.001985～2000.*?杨集1986～2000</p>\s*",
    re.S,
)

TABLE_RE = re.compile(
    r"<table class=\"structured-table\"><caption>表5-1 1990年连云港市建制镇规划情况表</caption>.*?</table>",
    re.S,
)

SECTION_RE = re.compile(
    r"<section class=\"verified-table-block\" id=\"table-LYG-上-T009\">.*?</section>",
    re.S,
)


def render_table() -> str:
    thead = "".join(f"<th>{html.escape(col)}</th>" for col in COLUMNS)
    rows = []
    for row in ROWS:
        rows.append("<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>")
    return (
        '<table class="structured-table"><caption>表5-1 1990年连云港市建制镇规划情况表</caption>'
        f"<thead><tr>{thead}</tr></thead><tbody>{''.join(rows)}</tbody></table>"
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


def patch_reader() -> tuple[int, int]:
    text = HTML.read_text(encoding="utf-8")
    text, table_count = TABLE_RE.subn(render_table(), text, count=1)
    if table_count != 1:
        raise RuntimeError(f"expected to replace 1 reader table, replaced {table_count}")
    section_html = (
        '<section class="verified-table-block" id="table-LYG-上-T009"><div class="structured-table-meta">'
        '表ID：LYG-上-T009；源页：338</div>'
        + render_table()
        + '</section>'
    )
    text, section_count = SECTION_RE.subn(section_html, text, count=1)
    if section_count != 1:
        raise RuntimeError(f"expected to replace 1 verified table block, replaced {section_count}")
    text, residue_count = RESIDUE_RE.subn("\n", text, count=1)
    if residue_count not in (0, 1):
        raise RuntimeError(f"expected to remove 0 or 1 flattened residue block, removed {residue_count}")
    HTML.write_text(text, encoding="utf-8")
    return table_count + section_count, residue_count


def write_reports(json_changed: bool, site_changed: int, table_replaced: int, residue_removed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    result = {
        "time": now,
        "table_id": ENTRY["table_id"],
        "table_number": ENTRY["table_number"],
        "title": ENTRY["title"],
        "source_pages": ENTRY["pages"],
        "json_changed": json_changed,
        "site_changed": site_changed,
        "reader_table_replaced": table_replaced,
        "reader_residue_blocks_removed": residue_removed,
        "rows": len(ROWS),
        "columns": len(COLUMNS),
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第五卷建制镇规划表残文修复

- 时间：{now}
- 表ID：`LYG-上-T009`
- 表题：表5-1 `1990年连云港市建制镇规划情况表`
- 源页：`workbench/ocr/paddle_ocr/上/part02/page_0038.txt`

## 修复动作

- 更新结构化表 `workbench/table_entries/上/data/LYG-上-T009.json` 为 {len(ROWS)} 行、{len(COLUMNS)} 列。
- 补入源页可见但旧 JSON 漏掉的 `赣马` 行。
- 将 `锦屏`、`南城`、`板桥`、`徐圩` 按源页竖排分组改为 `市区`。
- 同步结构化表格站，并替换最终阅读版内表5-1 HTML 表格：{table_replaced} 处。
- 撤出最终阅读版内重复的 `（平方公里）` 与 `锦屏...杨集1986～2000` 摊平残文：{residue_removed} 组；若重复执行脚本则为 0 组。

## 核对说明

- 源页表头为 `规模` 下分 `人口(万人)`、`用地(平方公里)`，本次列名按源页写为 `用地(平方公里)`。
- 源页未见数值处保留空值，未按相邻行外推。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(residue_removed: int) -> None:
    marker = "## 2026-07-01 第五卷建制镇规划表残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第五卷建制镇规划表摊平残文回源处理。
- 据 `workbench/ocr/paddle_ocr/上/part02/page_0038.txt` 和 `workbench/ocr/raw/上/part02/page_0038.txt` 更新 `workbench/table_entries/上/data/LYG-上-T009.json`：补入 `赣马` 行，前四行归入 `市区`，表5-1共 22 行 7 列。
- 同步 `output/structured_tables/index.html`，替换最终阅读版表5-1，并撤出重复摊平残文 {residue_removed} 组。
- 报告：`output/reports/reader_readability_town_planning_table_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    json_changed = write_json()
    site_changed = patch_site()
    table_replaced, residue_removed = patch_reader()
    write_reports(json_changed, site_changed, table_replaced, residue_removed)
    update_memory(residue_removed)
    print(f"json_changed={int(json_changed)}")
    print(f"site_changed={site_changed}")
    print(f"reader_table_replaced={table_replaced}")
    print(f"reader_residue_blocks_removed={residue_removed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

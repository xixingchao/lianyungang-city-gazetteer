# -*- coding: utf-8 -*-
"""Add verified table 24-3 and remove its flattened reader residue."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T133.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_major_buildings_table_20260701.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_major_buildings_table_20260701.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第二十四卷主要建筑一览表残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

COLUMNS = ["工程名称", "结构层次", "建筑面积(平方米)", "开竣工年月", "设计单位", "施工单位"]

ROWS = [
    ["市变压器厂装配车间", "排架", "5635", "1977~1978", "市建筑设计院", "连云港市第一建筑工程公司"],
    ["连云港远洋宾馆", "框架11层", "10720", "1978~1980", "省建筑设计院", "连云港市第二建筑工程公司"],
    ["市涤纶厂5000T长丝车间", "框架5层", "14447", "1981.12~1982.12", "纺织工业部设计院", "连云港市第一建筑工程公司"],
    ["写字楼", "框架15层", "17600", "1988.12~1990.4", "省建筑设计院", "连云港市建设开发公司"],
    ["神州宾馆", "组合", "5300", "1986.11~1987.7", "香港、瑞典联合", "赣榆县第一建筑安装工程公司"],
    ["华联商厦", "框架15层", "14000", "1987.5~1988.1", "国家机电部设计院", "江都县建筑安装公司"],
    ["天然居宾馆", "框架18层", "8506", "1987.6~1988.8", "连云港市建筑设计院", "宿迁县第三建筑公司"],
    ["市电信综合楼", "框架8层", "7462", "1987.11~1988.12", "化工部连云港化工矿山设计院", "连云港市第一建筑工程公司"],
    ["白塔埠机场候机楼", "框架2层", "6411", "1988.5~1989.5", "连云港市建筑设计院", "东海县第一建筑工程公司"],
    ["东方影视中心", "框架", "4288", "1988.3~1989.9", "连云港市建筑设计院", "连云港市云山建筑公司"],
    ["东方大厦", "框架10层", "5020", "1984.3~1985.11", "市建筑设计院", "连云港市第三建筑工程公司"],
    ["七一六研究所科研楼", "框架15层", "12000", "1987.3~1989.12", "市建筑设计院", "赣榆县第一建筑安装工程公司"],
    ["交通银行营业楼", "框架12层", "6014", "1989.12~1990.12", "省建筑设计院", "连云港市第三建筑工程公司"],
    ["市百货大楼", "框架7层", "10080", "一期1977.12~1979.12；二期1989~1990", "一期：化工部连云港化工矿山设计院；二期：市建筑设计院", "一期：连云港市第一建筑工程公司；二期：连云港市第二建筑工程公司"],
    ["中国银行营业楼", "框架12层", "7113", "1989年底开工", "机械工业部第七设计院", "连云港市第一建筑工程公司"],
    ["建设银行营业楼", "框架12层", "6473", "1990年开工", "省建筑设计院", "连云港市第一建筑工程公司"],
    ["灌云县棉纺厂纺纱车间", "排架", "9300", "1988.4~1990.7", "江苏省纺织工业设计院", "连云港市第三建筑工程公司"],
    ["赣榆县邮电大楼", "框架7层", "4010", "1990年开工", "化工部连云港化工矿山设计院", "赣榆县第一建筑安装工程公司"],
    ["东海温泉宾馆", "组合", "5700", "1975年建成，1984年、1990年两次扩建", "省建筑设计院；市建筑设计院", "东海县第一建筑公司"],
]

ENTRY = {
    "table_id": "LYG-中-T133",
    "title": "1990年以前连云港市主要建筑一览表",
    "table_number": "表24-3",
    "page": 1210,
    "pages": [1210],
    "part": "part01",
    "vol": "中",
    "columns": COLUMNS,
    "rows": ROWS,
    "row_count": len(ROWS),
    "col_count": len(COLUMNS),
    "status": "verified",
    "notes": "已据页级OCR核录：workbench/ocr/paddle_ocr/中/part01/page_0308.txt；并参考 raw OCR：workbench/ocr/raw/中/part01/page_0308.txt。表24-3位于第二十四卷第二章公共建筑末尾、第三章施工安装前。复合或跨行单元格按源页可见内容合并；市百货大楼一期、二期的设计单位和施工单位分别写入同一单元格说明。",
    "volume": "中",
}

RESIDUE_RE = re.compile(
    r"\n?<p>连云港市第一建市变压器厂装配排架市建筑设计院56351977 ~ 1978筑工程公司车间.*?东海温泉宾馆省建筑设计院两次扩建市建筑设计院</p>\s*",
    re.S,
)


def render_table() -> str:
    thead = "".join(f"<th>{html.escape(col)}</th>" for col in COLUMNS)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>" for row in ROWS)
    return (
        '<section class="verified-table-block" id="table-LYG-中-T133"><div class="structured-table-meta">'
        '表ID：LYG-中-T133；源页：1210</div>'
        '<table class="structured-table"><caption>表24-3 1990年以前连云港市主要建筑一览表</caption>'
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
    new, count = RESIDUE_RE.subn("\n" + render_table() + "\n", text, count=1)
    if count != 1:
        raise RuntimeError(f"expected to replace 1 flattened table block, replaced {count}")
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
    md = f"""# 第二十四卷主要建筑一览表残文修复

- 时间：{now}
- 表ID：`LYG-中-T133`
- 表题：表24-3 `1990年以前连云港市主要建筑一览表`
- 源页：`workbench/ocr/paddle_ocr/中/part01/page_0308.txt`

## 修复动作

- 新增 verified 结构化表：`workbench/table_entries/中/data/LYG-中-T133.json`，{len(ROWS)} 行、{len(COLUMNS)} 列。
- 同步结构化表格站：`output/structured_tables/index.html`。
- 将最终阅读版中 `市变压器厂装配...东海温泉宾馆` 的压平残文替换为 verified 表块：{replaced} 组。

## 核对说明

- 表24-3位于第二十四卷第二章公共建筑末尾、第三章施工安装前。
- 市百货大楼源页跨一期、二期两组设计与施工单位，已合并写入对应单元格。
- 源页 `白塔埠机场候机楼` raw OCR 前有 stray 逗号，按页级 OCR 表题清理。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(replaced: int) -> None:
    marker = "## 2026-07-01 第二十四卷主要建筑一览表残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第二十四卷建筑业 `市变压器厂装配...东海温泉宾馆` 摊平残文回源处理。
- 据 `workbench/ocr/paddle_ocr/中/part01/page_0308.txt` 和 `workbench/ocr/raw/中/part01/page_0308.txt` 新增 `workbench/table_entries/中/data/LYG-中-T133.json`：表24-3《1990年以前连云港市主要建筑一览表》，19 行 6 列。
- 从最终阅读版替换对应压平残文 {replaced} 组，并同步结构化表格站。
- 报告：`output/reports/reader_readability_major_buildings_table_20260701.md`。
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""连云港市志 上册 表格构建系统 - 核心框架"""
import json, os, sys
from pathlib import Path

ROOT = Path(r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation')
DATA_DIR = ROOT / 'workbench' / 'table_entries' / '上' / 'data'
REPORT_FILE = ROOT / 'workbench' / 'table_entries' / '上' / '表格构建报告.md'
sys.stdout.reconfigure(encoding='utf-8')

def build_tables(table_data, status="draft"):
    """构建所有表格的JSON输出"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for tid, data in sorted(table_data.items()):
        entry = {
            "table_id": tid,
            "title": data["title"],
            "table_number": data.get("table_number", ""),
            "pages": data["pages"],
            "columns": data["columns"],
            "rows": data["rows"],
            "row_count": len(data["rows"]),
            "col_count": len(data["columns"]),
            "status": status,
            "notes": data.get("notes", ""),
        }
        out_path = DATA_DIR / f"{tid}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)
        results.append((tid, data["title"], data["pages"], len(data["rows"]), len(data["columns"])))
        print(f"  ✓ {tid} — {data['title'][:30]}  ({len(data['rows'])}行×{len(data['columns'])}列)")
    return results

def write_report(results, table_data, output_path):
    """生成构建报告"""
    lines = [
        "# 连云港市志 上册 表格构建报告",
        "",
        f"生成时间: 自动生成",
        f"状态: draft（初稿，待对照原图核对）",
        "",
        "## 汇总",
        "",
        f"| 指标 | 数值 |",
        f"|--- | ---:|",
        f"| 已构建表格数 | {len(results)} |",
        f"| 总数据行数 | {sum(r[3] for r in results)} |",
        f"| 总列数 | {sum(r[4] for r in results)} |",
        "",
        "## 各表详情",
        "",
        "| ID | 标题 | 页码 | 行数 | 列数 |",
        "|--- | --- | ---: | ---: | ---: |",
    ]
    for tid, title, pages, rows, cols in results:
        pages_str = f"{pages[0]}-{pages[-1]}" if len(pages) > 1 else str(pages[0])
        lines.append(f"| {tid} | {title[:40]} | {pages_str} | {rows} | {cols} |")

    lines.extend(["", "## 待处理复杂表格", ""])
    for tid, data in sorted(table_data.items()):
        if data.get("status") == "TODO":
            lines.append(f"- {tid} — {data['title'][:40]} ({data.get('notes', '待填充')})")

    output_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"\n报告: {output_path}")

if __name__ == '__main__':
    # 导入表格数据
    from table_data import TABLE_DATA, COMPLEX_TABLES
    results = build_tables(TABLE_DATA, status="draft")
    write_report(results, TABLE_DATA, REPORT_FILE)
    print(f"\n数据目录: {DATA_DIR}")
    print(f"共构建 {len(results)} 个表格")

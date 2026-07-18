# -*- coding: utf-8 -*-
"""Mark unverified skeleton tables as pending source check.

This does not claim table data is complete. It fixes misleading metadata so
structured-table delivery audits distinguish real verified tables from backlog.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
DATA_ROOT = ROOT / "workbench" / "table_entries"
REPORT_JSON = ROOT / "output" / "reports" / "table_status_pending_source_check.json"
REPORT_MD = ROOT / "output" / "reports" / "table_status_pending_source_check.md"

BAD_TOKENS = ["待对照原图录入", "待精修", "待确认", "标题待确认", "从OCR自动提取骨架", "待对照原图"]
PENDING_STATUS = "pending-source-check"
PENDING_NOTE = "待回源核录；不得作为主交付入口"
VOLUME_DIR = {"上": "上", "中": "中", "下": "下"}


def load_tables_from_site() -> tuple[str, list[dict], str]:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise SystemExit("TABLES payload not found in structured table site")
    return text[: match.start(1)], json.loads(match.group(1)), text[match.end(1) :]


def flat_values(table: dict) -> list[str]:
    values: list[str] = []
    for key in ("table_id", "title", "table_number", "status", "notes", "volume"):
        values.append(str(table.get(key, "")))
    values.extend(str(c) for c in table.get("columns") or [])
    for row in table.get("rows") or []:
        values.extend(str(cell) for cell in row)
    return values


def needs_pending(table: dict) -> bool:
    joined = "\n".join(flat_values(table))
    rows = table.get("rows") or []
    cols = table.get("columns") or []
    has_bad_token = any(token in joined for token in BAD_TOKENS)
    empty_like = bool(rows) and len(rows) == 1 and len([c for c in rows[0] if str(c).strip()]) <= 1
    single_col_skeleton = len(cols) == 1 and cols[0] == "数值"
    return has_bad_token or empty_like or single_col_skeleton


def mark_table(table: dict) -> bool:
    if not needs_pending(table):
        return False
    changed = False
    if table.get("status") != PENDING_STATUS:
        table["status"] = PENDING_STATUS
        changed = True
    notes = str(table.get("notes", ""))
    if PENDING_NOTE not in notes:
        table["notes"] = f"{notes}；{PENDING_NOTE}" if notes else PENDING_NOTE
        changed = True
    return changed


def update_source_json(table: dict) -> bool:
    volume = str(table.get("volume", ""))
    folder = VOLUME_DIR.get(volume)
    if not folder:
        return False
    path = DATA_ROOT / folder / "data" / f"{table.get('table_id')}.json"
    if not path.exists():
        return False
    data = json.loads(path.read_text(encoding="utf-8"))
    before = json.dumps(data, ensure_ascii=False, sort_keys=True)
    mark_table(data)
    after = json.dumps(data, ensure_ascii=False, sort_keys=True)
    if after != before:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return True
    return False


def main() -> None:
    prefix, tables, suffix = load_tables_from_site()
    changed_tables = []
    source_json_updates = []
    for table in tables:
        if mark_table(table):
            changed_tables.append(table)
        if needs_pending(table) and update_source_json(table):
            source_json_updates.append(str(table.get("table_id")))

    SITE.write_text(prefix + json.dumps(tables, ensure_ascii=False) + suffix, encoding="utf-8")

    report = {
        "changed_table_count": len(changed_tables),
        "source_json_update_count": len(source_json_updates),
        "changed_tables": [
            {
                "table_id": table.get("table_id"),
                "title": table.get("title"),
                "volume": table.get("volume"),
                "pages": table.get("pages"),
                "status": table.get("status"),
            }
            for table in changed_tables
        ],
        "source_json_updates": source_json_updates,
    }
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 未核结构化表状态纠偏报告",
        "",
        "## 口径",
        "",
        "- 本批只修正元数据，不宣称表格已核录。",
        "- 含待核/待录入标记、空壳表、单列骨架表的条目统一标记为 `pending-source-check`。",
        "- `pending-source-check` 表仍必须回源 PDF/页图核录后才能进入主交付入口。",
        "",
        "## 统计",
        "",
        f"- 表格站状态纠偏：{len(changed_tables)} 张。",
        f"- 源 JSON 同步更新：{len(source_json_updates)} 个。",
        "",
        "| 表ID | 分册 | 页码 | 表题 |",
        "|---|---|---|---|",
    ]
    for table in changed_tables:
        pages = ",".join(str(p) for p in (table.get("pages") or []))
        title = str(table.get("title", "")).replace("|", "\\|")
        lines.append(f"| {table.get('table_id')} | {table.get('volume')} | {pages} | {title} |")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"changed_tables={len(changed_tables)}")
    print(f"source_json_updates={len(source_json_updates)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

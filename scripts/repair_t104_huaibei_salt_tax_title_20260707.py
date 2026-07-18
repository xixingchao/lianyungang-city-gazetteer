# -*- coding: utf-8 -*-
"""Correct T104 salt-tax table title from 准北 to 淮北."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "workbench" / "table_entries" / "中" / "data" / "LYG-中-T104.json"
SITE = ROOT / "output" / "structured_tables" / "index.html"
VERIFY = ROOT / "scripts" / "verify_t104_huaibei_salt_tax_20260629.py"
READERS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
]
REPORT_JSON = ROOT / "output" / "reports" / "t104_huaibei_salt_tax_title_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "t104_huaibei_salt_tax_title_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_淮北盐税表题更正.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
OLD = "民国3~24年准北盐税收入统计表"
NEW = "民国3~24年淮北盐税收入统计表"


def patch_json_file() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    changed = 0
    if data.get("title") == OLD:
        data["title"] = NEW
        changed += 1
    note = data.get("notes", "")
    add = "；2026-07-07 复核同页前后文 `淮北实征盐课/淮北盐场` 及脚本命名，确认 raw OCR 表题 `准北` 为 `淮北` 误识，已更正表题"
    if add not in note:
        data["notes"] = note.rstrip("。") + add + "。"
        changed += 1
    if changed:
        DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def patch_site() -> int:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise SystemExit("TABLES payload not found")
    tables = json.loads(match.group(1))
    changed = 0
    for table in tables:
        if table.get("table_id") == "LYG-中-T104":
            if table.get("title") == OLD:
                table["title"] = NEW
                changed += 1
            note = table.get("notes", "")
            add = "；2026-07-07 复核同页前后文 `淮北实征盐课/淮北盐场` 及脚本命名，确认 raw OCR 表题 `准北` 为 `淮北` 误识，已更正表题"
            if add not in note:
                table["notes"] = note.rstrip("。") + add + "。"
                changed += 1
    if changed:
        text = text[: match.start(1)] + json.dumps(tables, ensure_ascii=False) + text[match.end(1) :]
        SITE.write_text(text, encoding="utf-8")
    return changed


def patch_text_file(path: Path, old: str, new: str) -> int:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count:
        path.write_text(text.replace(old, new), encoding="utf-8")
    return count


def append_memory(total_reader: int, json_changed: int, site_changed: int, verify_changed: int) -> None:
    marker = "## 2026-07-07 淮北盐税表题更正"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 复核 `LYG-中-T104`：raw OCR 标题作 `准北盐税`，但同页前后文为 `淮北实征盐课`、`淮北盐场`，既有验证脚本文件名亦为 `huaibei_salt_tax`，判定表题 `准北` 为 OCR 误识。
- 已将当前 JSON、结构化表格站点、当前全书/中册 reader 中的表题更正为 `民国3~24年淮北盐税收入统计表`；表内数据未改。
- 本批 reader 替换 {total_reader} 处，JSON 更新 {json_changed} 项，站点更新 {site_changed} 项，验证脚本标题更新 {verify_changed} 处；报告：`output/reports/t104_huaibei_salt_tax_title_20260707.md`。
- 未打开、展示或嵌入图片。
""".strip()
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + block + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + block + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    json_changed = patch_json_file()
    site_changed = patch_site()
    verify_changed = patch_text_file(VERIFY, OLD, NEW)
    reader_counts = {str(path): patch_text_file(path, OLD, NEW) for path in READERS}
    total_reader = sum(reader_counts.values())

    payload = {
        "time": now,
        "table_id": "LYG-中-T104",
        "old_title": OLD,
        "new_title": NEW,
        "evidence": [
            "workbench/table_entries/中/raw/LYG-中-T104_1708.txt 同页前文：淮北实征盐课银700多万两",
            "workbench/table_entries/中/raw/LYG-中-T104_1708.txt 同页后文：淮北盐场被日军占领、淮北盐场的军队和苏皖边区政府",
            "scripts/verify_t104_huaibei_salt_tax_20260629.py 文件名已按 huaibei_salt_tax 命名",
        ],
        "changed": {
            "json_fields": json_changed,
            "site_fields": site_changed,
            "verify_script_occurrences": verify_changed,
            "reader_occurrences": reader_counts,
        },
        "not_changed": ["表内数据", "raw OCR 源文件", "图片或截图"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 淮北盐税表题更正",
        "",
        f"> 生成时间：{now}",
        "",
        "## 结论",
        "",
        f"- `LYG-中-T104` 表题由 `{OLD}` 更正为 `{NEW}`。",
        "- 仅更正表题和说明；表内数据未改。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 证据",
        "",
        "- raw OCR 同页前文为 `淮北实征盐课银700多万两`。",
        "- raw OCR 同页后文为 `淮北盐场被日军占领`、`淮北盐场的军队和苏皖边区政府`。",
        "- 既有验证脚本文件名为 `scripts/verify_t104_huaibei_salt_tax_20260629.py`。",
        "",
        "## 修改统计",
        "",
        f"- JSON 更新项：{json_changed}",
        f"- 结构化表格站点更新项：{site_changed}",
        f"- 验证脚本标题替换：{verify_changed}",
        f"- reader 表题替换：{total_reader}",
        "",
        "## Reader 文件",
        "",
    ]
    for path, count in reader_counts.items():
        lines.append(f"- `{path}`：{count} 处")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    append_memory(total_reader, json_changed, site_changed, verify_changed)
    print(json.dumps({"reader_changed": total_reader, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

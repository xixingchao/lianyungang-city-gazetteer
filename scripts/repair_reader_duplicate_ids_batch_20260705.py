# -*- coding: utf-8 -*-
"""Remove duplicate reader anchors/table blocks that already have an inline placement."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
STRUCTURED = ROOT / "output" / "structured_tables" / "index.html"
T063 = ROOT / "workbench" / "table_entries" / "下" / "data" / "LYG-下-T063.json"
REPORT_JSON = ROOT / "output" / "reports" / "reader_duplicate_ids_batch_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_duplicate_ids_batch_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_阅读版重复ID批量清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

DUP_TABLE_IDS = [
    "table-LYG-上-T048",
    "table-LYG-上-T049",
    "table-LYG-上-T050",
    "table-LYG-上-T051",
    "table-LYG-上-T052",
    "table-LYG-上-T053",
    "table-LYG-中-T133",
    "table-LYG-中-T134",
    "table-LYG-中-T135",
    "table-LYG-中-T062",
    "table-LYG-中-T093",
    "table-LYG-中-T104",
]
OLD_HEADING = '<h4 id="第三卷-第五章赣榆县-第三节经济">第三节经济</h4>'
NEW_DONGHAI_HEADING = '<h4 id="第三卷-第六章东海县-第三节经济">第三节经济</h4>'


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def id_counts(text: str) -> Counter[str]:
    return Counter(re.findall(r'id="([^"]+)"', text))


def remove_later_table_blocks(html: str) -> tuple[str, dict[str, int]]:
    removed: dict[str, int] = {}
    for table_id in DUP_TABLE_IDS:
        pattern = re.compile(
            r'\n?<section class="verified-table-block" id="' + re.escape(table_id) + r'">.*?</section>\s*',
            flags=re.S,
        )
        matches = list(pattern.finditer(html))
        if len(matches) < 2:
            removed[table_id] = 0
            continue
        for match in reversed(matches[1:]):
            html = html[: match.start()] + "\n" + html[match.end() :]
        removed[table_id] = len(matches) - 1
    return html, removed


def patch_t063_json() -> bool:
    data = json.loads(T063.read_text(encoding="utf-8"))
    cols = data.get("columns", [])
    changed = False
    data["columns"] = ["备注" if col == "处理说明" else col for col in cols]
    changed = data["columns"] != cols
    if changed:
        T063.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    before_dupes = {k: v for k, v in id_counts(html).items() if v > 1}

    html, removed_tables = remove_later_table_blocks(html)

    heading_occurrences = html.count(OLD_HEADING)
    if heading_occurrences != 2:
        raise RuntimeError(f"expected two identical third-section headings before patch, got {heading_occurrences}")
    first = html.find(OLD_HEADING)
    second = html.find(OLD_HEADING, first + len(OLD_HEADING))
    html = html[:second] + NEW_DONGHAI_HEADING + html[second + len(OLD_HEADING) :]

    html = html.replace("<th>处理说明</th>", "<th>备注</th>")
    structured_changed = False
    if STRUCTURED.exists():
        structured = STRUCTURED.read_text(encoding="utf-8")
        new_structured = structured.replace('"处理说明"', '"备注"')
        if new_structured != structured:
            STRUCTURED.write_text(new_structured, encoding="utf-8")
            structured_changed = True
    t063_json_changed = patch_t063_json()

    after_dupes = {k: v for k, v in id_counts(html).items() if v > 1}
    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "before_duplicate_ids": before_dupes,
        "after_duplicate_ids": after_dupes,
        "removed_duplicate_table_blocks": removed_tables,
        "heading_fix": {
            "old_duplicate": OLD_HEADING,
            "new_second_heading": NEW_DONGHAI_HEADING,
        },
        "renamed_visible_column": {
            "from": "处理说明",
            "to": "备注",
            "final_reader": True,
            "structured_index": structured_changed,
            "table_json": t063_json_changed,
        },
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    removed_total = sum(removed_tables.values())
    md = f"""# 阅读版重复ID批量清理

- 时间：{now}
- 删除重复结构化表块：{removed_total} 处。
- 修复重复章节锚点：1 处。
- 可见表头改名：`处理说明` -> `备注`。

## 删除的重复表块

"""
    for table_id, count in removed_tables.items():
        if count:
            md += f"- `{table_id}`：删除后续重复块 {count} 处，保留正文正确位置。\n"
    md += f"""
## 锚点修复

- 第二个 `{OLD_HEADING}` 改为 `{NEW_DONGHAI_HEADING}`，对应第三卷第六章东海县第三节。

## 复核

- 清理前重复 ID：{len(before_dupes)} 组。
- 清理后重复 ID：{len(after_dupes)} 组。
- 本批不改表格 JSON 数据值；仅去除阅读版重复块、修正锚点和中性化可见列名。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 阅读版重复ID批量清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 删除最终阅读版中已在正文位置展示、又在卷末“已核结构化表格”集合重复出现的表块 {removed_total} 处。
- 修复第三卷第六章东海县 `第三节经济` 误用赣榆县锚点的问题。
- 将 `LYG-下-T063` 可见列名 `处理说明` 改为 `备注`，避免读者可见工作流措辞。
- 报告：`output/reports/reader_duplicate_ids_batch_20260705.md`。
""",
    )

    print(f"removed_duplicate_table_blocks={removed_total}")
    print(f"duplicate_ids_before={len(before_dupes)}")
    print(f"duplicate_ids_after={len(after_dupes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

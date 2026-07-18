# -*- coding: utf-8 -*-
"""Remove verified-table duplicate displays when the same table is already inline."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_inline_duplicate_verified_tables_batch2_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_inline_duplicate_verified_tables_batch2_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_阅读版内联表重复展示第二批清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

DUPLICATES = [
    ("table-LYG-上-T002", "表1-3 1913~1956年海州湾岸滩伸展速度表"),
    ("table-LYG-上-T003", "表1-13 连云港市各月平均蒸发量表"),
    ("table-LYG-上-T005", "表1-24 连云港市沿海潮位站最高最低潮位统计表"),
    ("table-LYG-上-T009", "表5-1 1990年连云港市建制镇规划情况表"),
    ("table-LYG-上-T011", "1990年连云港市节约用水情况表"),
    ("table-LYG-上-T013", "表5-12 1961年新浦地区住房调查统计表"),
    ("table-LYG-上-T016", "表6-16 1986~1990年连云港市环境大气、酸雨监测点统计表"),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def remove_block(html: str, block_id: str) -> tuple[str, str]:
    start_marker = f'<section class="verified-table-block" id="{block_id}">'
    start = html.index(start_marker)
    end = html.index("</section>", start) + len("</section>")
    return html[:start] + html[end:], html[start:end]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for block_id, caption in DUPLICATES:
        caption_marker = f"<caption>{caption}</caption>"
        before = html.count(caption_marker)
        if before != 2:
            raise RuntimeError(f"expected two captions for {block_id}, got {before}: {caption}")
        html, removed = remove_block(html, block_id)
        if caption_marker not in removed:
            raise RuntimeError(f"removed block {block_id} did not contain caption: {caption}")
        after = html.count(caption_marker)
        if after != 1:
            raise RuntimeError(f"expected one caption after removing {block_id}, got {after}: {caption}")
        changes.append({"block_id": block_id, "caption": caption, "before": before, "after": after})

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "最终阅读版内联表与卷末已核集合重复展示清理第二批",
        "changes": changes,
        "principle": "正文自然位置已展示同表时，删除卷末已核集合中的重复展示块；不改结构化表格数据或站点。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 阅读版内联表重复展示第二批清理",
        "",
        f"- 时间：{now}",
        "- 范围：最终阅读版中正文自然位置已展示、卷末已核集合又重复展示的结构化表。",
        "- 原则：只删除重复展示块，不改表格数据，不改结构化表格站点。",
        "",
        "## 清理",
        "",
    ]
    for item in changes:
        lines.append(f"- `{item['block_id']}`：`{item['caption']}`，caption {item['before']} -> {item['after']}。")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")

    marker = "## 2026-07-05 阅读版内联表重复展示第二批清理"
    ids = "、".join(item[0] for item in DUPLICATES)
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 清理最终阅读版中 7 个正文已内联展示、卷末已核集合重复展示的表块：{ids}。
- 保留正文自然位置表格；结构化表格 JSON 与 `output/structured_tables/index.html` 不变。
- 报告：`output/reports/reader_inline_duplicate_verified_tables_batch2_20260705.md`。
""",
    )

    print("inline_duplicate_verified_tables_batch2_removed")
    print(f"removed={len(changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

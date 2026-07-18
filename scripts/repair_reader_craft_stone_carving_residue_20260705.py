# -*- coding: utf-8 -*-
"""Remove the craft table-tail residue before the stone-carving section."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_craft_stone_carving_residue_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_craft_stone_carving_residue_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_石雕表尾残片清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = "<p>0.2120.5019898.13- 0.30- 1.200.07- 2.6012.90-2.30199023.85.二、石雕境内出土的氏族公共墓地随葬品石斧、西周石镰、西汉晚期石象石、北朝石佛造像、晚唐石罐等，都具有较高的工艺水平。</p>"
NEW = "<h5>二、石雕</h5>\n<p>境内出土的氏族公共墓地随葬品石斧、西周石镰、西汉晚期石象石、北朝石佛造像、晚唐石罐等，都具有较高的工艺水平。</p>"
SOURCES = [
    "workbench/ocr/raw/中/part01/page_0022.txt:4-19",
    "workbench/ocr/merged/连云港市志_中_part01_OCR汇总.md:2382-2384",
    "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:179-180",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    old_count = html.count(OLD)
    if old_count == 1:
        html = html.replace(OLD, NEW, 1)
        status = "changed"
        changed = 1
    elif old_count == 0 and html.count(NEW) >= 1:
        status = "already_applied"
        changed = 0
    else:
        raise RuntimeError(f"expected stone-carving residue once, got {old_count}")

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "status": status,
        "changed": changed,
        "sources": SOURCES,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 石雕表尾残片清理",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：删除第十七卷工艺美术玉雕统计表尾残留数字串，恢复 `二、石雕` 小节标题和首段边界。",
        "",
        "## 结果",
        "",
        f"- 石雕小节前表尾残片：{status}，本次变更 {changed}",
    ]
    for source in SOURCES:
        lines.append(f"  - `{source}`")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 石雕表尾残片清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_craft_stone_carving_residue_20260705.py`，清理主阅读版第十七卷工艺美术玉雕统计表尾数字串粘连 `二、石雕` 的残片。
- 源页证据：`workbench/ocr/raw/中/part01/page_0022.txt:4-19` 显示表尾 `1990 23.85.` 后进入 `二、石雕`，正文首句从 `境内出土的氏族公共墓地...` 开始。
- 报告：`output/reports/reader_craft_stone_carving_residue_20260705.md`。
""",
    )

    print("reader_craft_stone_carving_residue_repaired")
    print(f"changed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

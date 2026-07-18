# -*- coding: utf-8 -*-
"""Clean reader-visible review wording after the earthquake statistics table."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_earthquake_table_review_note_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_earthquake_table_review_note_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_地震统计表交付措辞清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = "<p>注：据本段 OCR 可读信息结构化，地点和备注待终校复核。</p>"
NEW = "<p>注：本表据正文可读信息整理，地点和备注按源文可辨内容保留。</p>"
CAPTION = "表1-25 1973～1990年连云港市1级以上地震统计表"
SOURCE = "workbench/body_chapters/连云港市志_全书_正文汇总.md:11734; workbench/body_chapters/paddle_上/第一卷_自然环境.md:6320-6321"


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
    elif old_count == 0 and html.count(NEW) == 1:
        status = "already_applied"
        changed = 0
    else:
        raise RuntimeError(f"expected review note once, got {old_count}")
    if CAPTION not in html:
        raise RuntimeError("earthquake table caption missing after cleanup")
    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "caption": CAPTION,
        "status": status,
        "changed": changed,
        "old_note": OLD,
        "new_note": NEW,
        "source": SOURCE,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    text = f"""# 地震统计表交付措辞清理

- 时间：{now}
- 范围：`{HTML.relative_to(ROOT)}`。
- 对象：`{CAPTION}` 后的读者可见注释。
- 处理：将交付前措辞 `地点和备注待终校复核` 改为中性来源说明；不改表格数据。
- 状态：{status}，本次变更 {changed}。
- 源证据：`{SOURCE}`。
"""
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 地震统计表交付措辞清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_earthquake_table_review_note_20260705.py`，清理最终阅读版 `表1-25 1973～1990年连云港市1级以上地震统计表` 后的读者可见交付前措辞。
- 原句：`注：据本段 OCR 可读信息结构化，地点和备注待终校复核。`
- 新句：`注：本表据正文可读信息整理，地点和备注按源文可辨内容保留。`
- 报告：`output/reports/reader_earthquake_table_review_note_20260705.md`。
""",
    )

    print("reader_earthquake_table_review_note_cleaned")
    print(f"changed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

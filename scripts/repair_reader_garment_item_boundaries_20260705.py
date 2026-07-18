# -*- coding: utf-8 -*-
"""Restore source-backed garment item boundaries in the full reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_garment_item_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_garment_item_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_服装企业条目边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ITEMS = [
    ("二、连云港市服装二厂", "该厂位于连云港市连云区墟沟镇大巷，为市属集体所有制企业。", "workbench/ocr/raw/上/part03/page_0268.txt:12"),
    ("五、东海县第一服装厂", "该厂位于东海县牛山镇菜市街95号，为县属集体所有制企业。", "workbench/ocr/raw/上/part03/page_0269.txt:8"),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for title, lead, source in ITEMS:
        old = f"<p>{title}{lead}"
        new = f"<h5>{title}</h5>\n<p>{lead}"
        old_count = html.count(old)
        if old_count == 1:
            html = html.replace(old, new, 1)
            status = "changed"
            changed = 1
        elif old_count == 0 and html.count(new) >= 1:
            status = "already_applied"
            changed = 0
        else:
            raise RuntimeError(f"expected {title} once, got {old_count}")
        changes.append({"label": title, "status": status, "changed": changed, "source": source})

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "target": str(HTML.relative_to(ROOT)).replace("\\", "/"), "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 服装企业条目边界修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：按源 OCR 分行恢复上册工业卷服装企业 2 处条目标题边界，仅拆标题，不改正文文字。",
        "",
        "## 结果",
        "",
    ]
    for change in changes:
        lines.append(f"- {change['label']}：{change['status']}，本次变更 {change['changed']}")
        lines.append(f"  - `{change['source']}`")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 服装企业条目边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_garment_item_boundaries_20260705.py`，按源 OCR 分行恢复上册工业卷 2 处服装企业条目标题边界：`二、连云港市服装二厂`、`五、东海县第一服装厂`。
- 源页证据：`workbench/ocr/raw/上/part03/page_0268.txt:12`、`workbench/ocr/raw/上/part03/page_0269.txt:8`。
- 报告：`output/reports/reader_garment_item_boundaries_20260705.md`。
""",
    )

    print("reader_garment_item_boundaries_repaired")
    print(f"changed={sum(change['changed'] for change in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

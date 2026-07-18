# -*- coding: utf-8 -*-
"""Split volume 1 mountain-collapse section heading."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_mountain_collapse_heading_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_mountain_collapse_heading_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷山体崩塌小节标题版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = "<p>第九节山体崩塌云台山形成于16亿年前的震旦纪，"
NEW = "<h4>第九节 山体崩塌</h4>\n<p>云台山形成于16亿年前的震旦纪，"


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> int:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 1:
        raise RuntimeError(f"expected one heading match, got {count}")
    text = text.replace(OLD, NEW, 1)
    if OLD in text:
        raise RuntimeError("mountain-collapse heading residue remains")
    HTML.write_text(text, encoding="utf-8")
    return 1


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第一卷自然环境：第九节山体崩塌",
        "section_headings_split": changed,
        "source_evidence": ["workbench/body_chapters/paddle_上/第一卷_自然环境.md:6390"],
        "notes": ["仅拆最终 HTML 小节标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷山体崩塌小节标题版式修复

- 时间：{now}
- 范围：第一卷自然环境，第九节山体崩塌。
- 本次拆分标题：{changed} 处。

## 修复

- 将 `第九节山体崩塌` 从正文段首拆为独立小节标题。
- 仅恢复版式边界，不改正文文字。

## 依据

- `workbench/body_chapters/paddle_上/第一卷_自然环境.md:6390`
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第一卷山体崩塌小节标题版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第一卷自然环境 `第九节山体崩塌` 小节标题粘正文问题。
- 仅恢复最终阅读版标题边界，不改正文文字。
- 报告：`output/reports/reader_readability_mountain_collapse_heading_20260705.md`。
""",
    )
    print(f"section_headings_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

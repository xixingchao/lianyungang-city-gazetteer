# -*- coding: utf-8 -*-
"""Repair one remaining lower-reader people-count OCR residue."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
REPORT_JSON = ROOT / "output" / "reports" / "lower_reader_people_followup_batch122_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "lower_reader_people_followup_batch122_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_下册牛痘接种人数残留回源补修第一百二十二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "共应接种20.49方人，实际接种16.8万人",
        "共应接种20.49万人，实际接种16.8万人",
    ),
    (
        "共应接种20.49</p><p>方人，实际接种16.8万人",
        "共应接种20.49</p><p>万人，实际接种16.8万人",
    ),
]
SOURCE = "全书版同段为 `共应接种20.49万人，实际接种16.8万人`"


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    applied = []
    for old, new in REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
        applied.append({"old": old, "new": new, "count": count})
    changed = sum(item["count"] for item in applied)
    TARGET.write_text(text, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "target": str(TARGET), "changed_this_run": changed, "items": applied, "source": SOURCE}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = "\n".join([
        "# 下册牛痘接种人数残留补修第一百二十二批：全书版回源核对",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 当前下册阅读版 `output/final_reader/连云港市志_下册.html`。",
        "",
        "## 修复项",
        "",
        f"- `共应接种20.49方人/跨段方人` -> `共应接种20.49万人`，{changed} 处；源/定位：`{SOURCE}`",
        "",
        "## 边界",
        "",
        "- 其它 `方人` 命中为 `官方人员/资方人员/人证` 等正常词或表格粘连，未改。",
        "- 未展示、未嵌入图片。",
    ]) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百二十二批：下册牛痘接种人数残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 按全书版同段，补修当前下册分册读者中 `共应接种20.49方人`（含跨段 `20.49</p><p>方人`）为 `共应接种20.49万人`。
- 其它 `方人` 复扫命中为 `官方人员/资方人员/人证` 等正常词或表格粘连，未改；报告：`output/reports/lower_reader_people_followup_batch122_20260706.md`。
- 未展示、未嵌入图片。
""")
    print(json.dumps({"changed_this_run": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

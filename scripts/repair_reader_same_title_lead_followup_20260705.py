# -*- coding: utf-8 -*-
"""Restore the three remaining same-title lead boundaries in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_same_title_lead_followup_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_same_title_lead_followup_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_同名正文首词条目边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/连云港市志_全书_正文汇总.md"

ITEMS = [
    {
        "title": "三、其它收入",
        "lead": "其它收入包括规费收入、公产收入、其它杂项收入、海关罚没收入、工商罚没收入、政法罚没收入、物价罚没收入、其它罚没收入、追回赃款赃物变价收入等。",
        "source": f"{SOURCE}:78530-78533",
        "note": "正文汇总 OCR 将多处 `收入` 识作 `收人`，按同段关键词回源定位。",
    },
    {
        "title": "一、淮海戏",
        "lead": "淮海戏俗称“海州小戏”，因主要伴奏乐器为板三弦，原始唱腔尾腔往往翻高8度，又称为“三刮调”、“拉魂腔”。",
        "source": f"{SOURCE}:93699-93700",
        "note": "第五十二卷文化卷剧种条目。",
    },
    {
        "title": "一、淮海戏",
        "lead": "淮海戏原来称“小戏”，是深受广大群众所喜爱的地方戏，流传在市境内历史较久。",
        "source": f"{SOURCE}:106669-106670",
        "note": "第五十八卷风俗卷民间文娱条目。",
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for item in ITEMS:
        old = f"<p>{item['title']}{item['lead']}"
        new = f"<h5>{item['title']}</h5>\n<p>{item['lead']}"
        old_count = html.count(old)
        if old_count == 1:
            html = html.replace(old, new, 1)
            status = "changed"
            changed = 1
        elif old_count == 0 and html.count(new) >= 1:
            status = "already_applied"
            changed = 0
        else:
            raise RuntimeError(f"expected unique match for {item['title']!r}, got {old_count}")
        changes.append({**item, "status": status, "changed": changed})

    HTML.write_text(html, encoding="utf-8")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    changed_total = sum(item["changed"] for item in changes)
    payload = {"time": now, "target": str(HTML.relative_to(ROOT)).replace("\\", "/"), "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 同名正文首词条目边界补修",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：补修上一批保守跳过的 3 处同名正文首词边界；只拆标题，不改正文文字。",
        f"- 状态：本次变更 {changed_total} 处；目标清理 {len(changes)}/3 处。",
        "",
        "## 明细",
        "",
    ]
    for item in changes:
        lines.append(f"- {item['title']}：{item['status']}，源证据 `{item['source']}`；{item['note']}")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 同名正文首词条目边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_same_title_lead_followup_20260705.py`，补修上一批跳过的 3 处：财政 `三、其它收入`、文化卷 `一、淮海戏`、风俗卷 `一、淮海戏`。
- `三、其它收入` 源文 OCR 将多处 `收入` 识作 `收人`，已按同段关键词定位；两个 `淮海戏` 按不同正文首句分别定位到文化卷和风俗卷。
- 报告：`output/reports/reader_same_title_lead_followup_20260705.md`。
""",
    )

    print("reader_same_title_lead_followup_repaired")
    print(f"changed={changed_total}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

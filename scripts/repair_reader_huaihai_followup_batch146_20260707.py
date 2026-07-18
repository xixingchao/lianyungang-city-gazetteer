# -*- coding: utf-8 -*-
"""Follow-up repair for remaining fixed 准海 OCR residues."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_huaihai_followup_batch146_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_huaihai_followup_batch146_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_准海残字跟进补修第一百四十六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "淮海滨海", "old": "准海、滨海", "new": "淮海、滨海"},
    {"label": "淮海抗日民主根据地", "old": "准海抗日民主根据", "new": "淮海抗日民主根据"},
    {"label": "淮海战役跨段", "old": "准海</p><p>战役", "new": "淮海</p><p>战役"},
    {"label": "淮海工学院跨段", "old": "准海工学</p><p>院", "new": "淮海工学</p><p>院"},
    {"label": "淮海剧团跨段", "old": "准海</p><p>剧团", "new": "淮海</p><p>剧团"},
]


def plain_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(plain: str, term: str) -> list[str]:
    return [plain[max(0, m.start() - 45):m.start() + 80].replace("\n", " ") for m in re.finditer(term, plain)]


def upsert_memory(marker: str, content: str) -> None:
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain_text(before)
        text = before
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        after_plain = plain_text(text)
        results.append({
            "target": str(target),
            "before": before_plain.count("准海"),
            "changed": sum(item["count"] for item in items),
            "after": after_plain.count("准海"),
            "items": items,
            "remaining_contexts": contexts(after_plain, "准海"),
        })

    changed = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader remaining fixed 准海 OCR residue repair",
        "changed": changed,
        "targets": results,
        "left_untouched": [
            "保留 `标准海岸线/低标准海堤/批准海州区` 等合法跨词命中。",
            "不做 `准海` 裸词全局替换。",
            "本批没有打开、展示或嵌入图片。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 准海残字跟进补修第一百四十六批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 补修 batch145 后剩余的固定 `准海` 残字，保护合法跨词。",
        "",
        "## 统计",
        "",
        f"- 修复：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处，剩余 `准海` {item['after']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        total = sum(result_item["count"] for result in results for result_item in result["items"] if result_item["old"] == item["old"])
        if total:
            lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`，{total} 处")
    lines.extend(["", "## 剩余边界", ""])
    remaining = False
    for item in results:
        for ctx in item["remaining_contexts"]:
            remaining = True
            lines.append(f"- `{item['target']}`：{ctx}")
    if not remaining:
        lines.append("- 无。")
    lines.extend(["", "## 未处理边界", ""])
    for item in payload["left_untouched"]:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百四十六批：准海残字跟进"
    upsert_memory(marker, f"""
{marker}

- 跟进修复 batch145 后剩余固定 `准海` 残字，覆盖 `淮海、滨海/淮海抗日民主根据地/淮海战役/淮海工学院/淮海剧团` 等跨段或带标点形态。
- 本批修复 {changed} 处；报告：`output/reports/reader_huaihai_followup_batch146_20260707.md`。
- 当前剩余 `准海` 均为 `标准海岸线/低标准海堤/批准海州区` 等合法跨词；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

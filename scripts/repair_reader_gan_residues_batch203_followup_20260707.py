# -*- coding: utf-8 -*-
"""Repair cross-paragraph leftovers from batch203."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
TARGETS = {
    "middle": ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    "lower": ROOT / "output" / "final_reader" / "连云港市志_下册.html",
}
REPORT_JSON = ROOT / "output" / "reports" / "reader_gan_residues_batch203_followup_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_gan_residues_batch203_followup_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_干字残留补修第二百零三批补遗.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "middle": [
        ("板蓝根于糖浆", "板蓝根干糖浆", "板蓝根</p><p>于糖浆", "板蓝根</p><p>干糖浆"),
        ("二级于线自办汽车邮路", "二级干线自办汽车邮路", "二级于线自办汽车邮</p><p>路", "二级干线自办汽车邮</p><p>路"),
    ],
    "lower": [
        ("白羽半于白葡萄酒", "白羽半干白葡萄酒", "白羽</p><p>半于白葡萄酒", "白羽</p><p>半干白葡萄酒"),
    ],
}


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int, by_scope: dict[str, int]) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第二百零三批补遗：干字残留"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 复扫 batch203 后，补修分册跨段 `于 -> 干` 残留 {total} 处。
- 本批修复中册 {by_scope.get('middle', 0)} 处、下册 {by_scope.get('lower', 0)} 处；报告：`output/reports/reader_gan_residues_batch203_followup_20260707.md`。
- 未做单字替换；未打开、展示或嵌入图片。
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
    full_text = plain(FULL.read_text(encoding="utf-8"))
    evidence = {new: full_text.count(new) for items in REPLACEMENTS.values() for _old, new, _html_old, _html_new in items}
    missing = {term: count for term, count in evidence.items() if count < 1}
    if missing:
        raise SystemExit(f"missing full-reader evidence: {missing}")

    changed_items = []
    by_scope = {}
    for scope, path in TARGETS.items():
        html = path.read_text(encoding="utf-8")
        for old, new, html_old, html_new in REPLACEMENTS[scope]:
            count = html.count(html_old)
            if count:
                html = html.replace(html_old, html_new)
                changed_items.append({"scope": scope, "old": old, "new": new, "changed": count})
                by_scope[scope] = by_scope.get(scope, 0) + count
        path.write_text(html, encoding="utf-8")

    total = sum(item["changed"] for item in changed_items)
    payload = {
        "time": now,
        "changed": total,
        "by_scope": by_scope,
        "full_evidence_counts": evidence,
        "replacements": changed_items,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 干字残留补修第二百零三批补遗",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册、下册阅读稿。",
        "- 补修 batch203 后仍有全书证据的 `于 -> 干` 跨段残留。",
        "- 未做单字替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 中册修复：{by_scope.get('middle', 0)} 处",
        f"- 下册修复：{by_scope.get('lower', 0)} 处",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['scope']}`：`{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total, by_scope)
    print(json.dumps({"changed": total, "by_scope": by_scope, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

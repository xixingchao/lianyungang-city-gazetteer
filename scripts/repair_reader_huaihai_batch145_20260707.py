# -*- coding: utf-8 -*-
"""Repair fixed 准海 OCR residues as 淮海, preserving legal cross-word cases."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_huaihai_batch145_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_huaihai_batch145_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_准海残字回源补修第一百四十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

PROTECT = ["标准海岸线", "低标准海堤", "批准海州区"]
WORDS = [
    "大学", "工学院", "工学院学报", "线", "战役", "地委", "地区", "区", "军分区", "抗日民主根据地",
    "省", "省税务局", "省立东海师范学校", "报", "日报", "开发", "农业综合发展", "经济区",
    "妇救总会", "妇联", "前线", "干校", "第三中学", "区委", "水师", "按试", "浪士", "小戏",
    "戏", "戏队", "剧团", "之窗",
]
REPLACEMENTS = []
_seen = set()
for word in sorted(WORDS, key=len, reverse=True):
    old = "准海" + word
    if old in _seen:
        continue
    _seen.add(old)
    REPLACEMENTS.append({"label": "淮海" + word, "old": old, "new": "淮海" + word})


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


def repair(text: str) -> tuple[str, list[dict[str, int]]]:
    protected = {}
    work = text
    for index, phrase in enumerate(PROTECT):
        token = f"__PROTECT_ZHUNHAI_{index}__"
        protected[token] = phrase
        work = work.replace(phrase, token)

    items = []
    for item in REPLACEMENTS:
        count = work.count(item["old"])
        if count:
            work = work.replace(item["old"], item["new"])
        items.append({**item, "count": count})

    for token, phrase in protected.items():
        work = work.replace(token, phrase)
    return work, items


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain_text(before)
        after, items = repair(before)
        target.write_text(after, encoding="utf-8")
        after_plain = plain_text(after)
        results.append({
            "target": str(target),
            "before": before_plain.count("准海"),
            "changed": sum(item["count"] for item in items),
            "after": after_plain.count("准海"),
            "items": items,
            "remaining_contexts": contexts(after_plain, "准海"),
            "protected_counts": {phrase: before_plain.count(phrase) for phrase in PROTECT},
        })

    changed = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader fixed 准海 OCR residue repair",
        "changed": changed,
        "targets": results,
        "protected": PROTECT,
        "left_untouched": [
            "保留 `标准海岸线/低标准海堤/批准海州区` 等合法跨词命中。",
            "不做 `准海` 裸词全局替换。",
            "本批没有打开、展示或嵌入图片。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 准海残字补修第一百四十五批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 按 Paddle OCR 和上下文证据，将固定 `准海...` 词组修为 `淮海...`。",
        "- 保护 `标准海岸线/低标准海堤/批准海州区` 等合法跨词命中。",
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
            lines.append(f"- `{item['old']}` -> `{item['new']}`：{total} 处")
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百四十五批：准海残字"
    upsert_memory(marker, f"""
{marker}

- 按 Paddle OCR 和上下文证据，修复固定 `准海...` 词组为 `淮海...`，覆盖 `淮海工学院/淮海线/淮海战役/黄淮海/淮海区/淮海戏/淮海大学` 等。
- 本批修复 {changed} 处；报告：`output/reports/reader_huaihai_batch145_20260707.md`。
- 保护 `标准海岸线/低标准海堤/批准海州区` 等合法跨词；未做 `准海` 裸词全局替换；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

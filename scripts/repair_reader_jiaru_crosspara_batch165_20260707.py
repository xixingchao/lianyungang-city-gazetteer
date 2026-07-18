# -*- coding: utf-8 -*-
"""Repair cross-paragraph 加人共产党 OCR residues."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_jiaru_crosspara_batch165_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_jiaru_crosspara_batch165_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_加入跨段残字补修第一百六十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
TERM = "加人"

REPLACEMENTS = [
    ("加人中国</p><p>共产党", "加入中国</p><p>共产党"),
    ("加人</p><p>中国共产党", "加入</p><p>中国共产党"),
    ("加人</p><p>共产党", "加入</p><p>共产党"),
]

LEFT_UNTOUCHED = [
    "`参加人数/参加人员/增加人员` 等合法相邻字保留。",
    "未处理 `参加中国人民解放军` 等合法 `加/中国` 邻近文本。",
    "未做裸词全局替换；未打开、展示或嵌入图片。",
]


def plain_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(plain: str, term: str) -> list[str]:
    return [plain[max(0, m.start() - 55):m.start() + 85].replace("\n", " ") for m in re.finditer(term, plain)]


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
    pattern_counts = {old: 0 for old, _ in REPLACEMENTS}
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain_text(before)
        after = before
        file_patterns = []
        for old, new in REPLACEMENTS:
            count = after.count(old)
            if count:
                after = after.replace(old, new)
                pattern_counts[old] += count
                file_patterns.append({"old": old, "new": new, "count": count})
        target.write_text(after, encoding="utf-8")
        after_plain = plain_text(after)
        results.append({
            "target": str(target),
            "changed": sum(item["count"] for item in file_patterns),
            "before": before_plain.count(TERM),
            "after": after_plain.count(TERM),
            "patterns": file_patterns,
            "remaining_contexts": contexts(after_plain, TERM),
        })

    total = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader cross-paragraph 加人共产党 OCR repair",
        "changed": total,
        "pattern_counts": {k: v for k, v in pattern_counts.items() if v},
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 加入跨段残字补修第一百六十五批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 定点修复跨段 `加人中国共产党/加人共产党`，恢复为 `加入中国共产党/加入共产党`。",
        "- 未做裸词全局替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        "",
        "## 替换项",
        "",
    ]
    for old, count in sorted(((k, v) for k, v in pattern_counts.items() if v), key=lambda x: x[0]):
        lines.append(f"- `{old}` -> `{dict(REPLACEMENTS)[old]}`：{count} 处")
    lines.extend(["", "## 文件", ""])
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处；剩余 `加人` {item['after']} 处")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百六十五批：加入跨段残字"
    upsert_memory(marker, f"""
{marker}

- 跟进 `加人` 纯文本残留，定位为 `加人中国</p><p>共产党`、`加人</p><p>中国共产党`、`加人</p><p>共产党` 等跨段 OCR 残字。
- 本批修复 {total} 处；报告：`output/reports/reader_jiaru_crosspara_batch165_20260707.md`。
- 保留 `参加人数/增加人员` 与 `参加中国人民解放军` 等合法相邻字；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

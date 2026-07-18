# -*- coding: utf-8 -*-
"""Repair OCR residue 输人 -> 输入 in fixed import/input contexts."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_shuren_batch134_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_shuren_batch134_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_输人残字回源补修第一百三十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "输入货物", "old": "输人货物", "new": "输入货物"},
    {"label": "输入棉布", "old": "输人棉布", "new": "输入棉布"},
    {"label": "输入砂糖", "old": "输人砂糖", "new": "输入砂糖"},
    {"label": "输入卷烟", "old": "输人卷烟", "new": "输入卷烟"},
    {"label": "输入粮油数量", "old": "输人13367", "new": "输入13367"},
    {"label": "缅甸输入", "old": "缅甸输人", "new": "缅甸输入"},
]

LEFT_UNTOUCHED = [
    "`运输人员` 等合法词语中连续出现的 `输人` 字面组合不处理。",
    "`输出人港` 属另一疑似错字族，未纳入本批。",
    "本批没有打开、展示或嵌入图片。",
]


def plain_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(plain: str, term: str) -> list[str]:
    return [plain[max(0, m.start() - 45):m.start() + 70].replace("\n", " ") for m in re.finditer(term, plain)]


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
            "before": before_plain.count("输人"),
            "changed": sum(item["count"] for item in items),
            "after": after_plain.count("输人"),
            "items": items,
            "remaining_contexts": contexts(after_plain, "输人"),
        })

    changed = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "fixed import/input contexts for 输人 residue",
        "patterns": len(REPLACEMENTS),
        "changed": changed,
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 输人残字补修第一百三十四批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 只处理货物、商品、数量和来源语境中的固定短语 `输人 -> 输入`。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 修复：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处，剩余 `输人` {item['after']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`")
    lines.extend(["", "## 剩余边界", ""])
    remaining = False
    for item in results:
        for ctx in item["remaining_contexts"]:
            remaining = True
            lines.append(f"- `{item['target']}`：{ctx}")
    if not remaining:
        lines.append("- 无。")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百三十四批：输人残字"
    upsert_memory(marker, f"""
{marker}

- 对当前全书/中册/下册阅读稿中固定输入语境核修 `输人 -> 输入`，包括货物、棉布、砂糖、卷烟、粮油数量和缅甸输入白玉佛语境。
- 本批修复 {changed} 处；报告：`output/reports/reader_shuren_batch134_20260707.md`。
- 保留 `运输人员` 等合法字面组合；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

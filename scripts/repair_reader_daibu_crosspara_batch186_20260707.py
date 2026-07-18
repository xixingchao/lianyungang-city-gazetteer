# -*- coding: utf-8 -*-
"""Follow-up for tag-split 逮捕 OCR residues."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_daibu_crosspara_batch186_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_daibu_crosspara_batch186_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_逮捕跨段残字补修第一百八十六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
REPLACEMENTS = [
    (r"共速(?P<gap>(?:<[^>]+>)+)捕道首35人", r"共逮\g<gap>捕道首35人", "逮捕道首35人"),
    (r"清党”大速(?P<gap>(?:<[^>]+>)+)捕", r"清党”大逮\g<gap>捕", "大逮捕"),
    (r"将钟离味速(?P<gap>(?:<[^>]+>)+)捕", r"将钟离味逮\g<gap>捕", "将钟离味逮捕"),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百八十六批：逮捕跨段补遗"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 复扫 batch185 后下册剩余 3 处跨标签 `速捕`，分别为 `逮捕道首35人`、`大逮捕`、`将钟离味逮捕`。
- 已定点补修 {total} 处；当前全书、中册、下册 reader 纯文本 `速捕` 清零。
- 报告：`output/reports/reader_daibu_crosspara_batch186_20260707.md`；未打开、展示或嵌入图片。
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
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain(before)
        after = before
        file_patterns = []
        for pattern, repl, label in REPLACEMENTS:
            after, count = re.subn(pattern, repl, after)
            if count:
                file_patterns.append({"label": label, "count": count})
        target.write_text(after, encoding="utf-8")
        after_plain = plain(after)
        results.append({
            "target": str(target),
            "changed": sum(item["count"] for item in file_patterns),
            "patterns": file_patterns,
            "before_plain_速捕": before_plain.count("速捕"),
            "after_plain_速捕": after_plain.count("速捕"),
        })
    total = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader tag-split 逮捕 OCR follow-up",
        "changed": total,
        "targets": results,
        "left_untouched": ["其它 `捕` 字组合", "raw OCR", "图片或截图"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 逮捕跨段残字补修第一百八十六批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 修复 batch185 后跨标签 `速捕` 残留。",
        "- 未处理其它 `捕` 字组合；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        "",
        "## 文件",
        "",
    ]
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处；剩余 `速捕` {item['after_plain_速捕']} 处")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total)
    print(json.dumps({"changed": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

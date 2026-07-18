# -*- coding: utf-8 -*-
"""Follow-up for tag-split 淮北 residues in the lower reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
REPORT_JSON = ROOT / "output" / "reports" / "lower_reader_huaibei_crosspara_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "lower_reader_huaibei_crosspara_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_下册淮北跨段残字补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
REPLACEMENTS = [
    (r"准(?P<gap>(?:<[^>]+>)+)北行政区", r"淮\g<gap>北行政区", "淮北行政区"),
    (r"新华社准(?P<gap>(?:<[^>]+>)+)北盐场支社", r"新华社淮\g<gap>北盐场支社", "新华社淮北盐场支社"),
    (r"爱先在准(?P<gap>(?:<[^>]+>)+)北，奏改票盐", r"爱先在淮\g<gap>北，奏改票盐", "爱先在淮北"),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int) -> None:
    marker = "## 2026-07-07 下册淮北跨段残字补修"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 复扫下册 `准北 -> 淮北` 同步后剩余 3 处跨标签残留，分别为 `淮北行政区`、`新华社淮北盐场支社`、`爱先在淮北`。
- 已定点补修 {total} 处；当前下册纯文本 `准北` 清零。未处理 `准盐/两准` 等需另判词。
- 报告：`output/reports/lower_reader_huaibei_crosspara_20260707.md`；未打开、展示或嵌入图片。
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
    before = TARGET.read_text(encoding="utf-8")
    before_plain = plain(before)
    after = before
    patterns = []
    for pattern, repl, label in REPLACEMENTS:
        after, count = re.subn(pattern, repl, after)
        if count:
            patterns.append({"label": label, "count": count})
    TARGET.write_text(after, encoding="utf-8")
    after_plain = plain(after)
    total = sum(item["count"] for item in patterns)
    payload = {
        "time": now,
        "target": str(TARGET),
        "changed": total,
        "patterns": patterns,
        "before_准北": before_plain.count("准北"),
        "after_准北": after_plain.count("准北"),
        "left_untouched": ["准盐", "两准", "raw OCR", "图片或截图"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 下册淮北跨段残字补修",
        "",
        f"> 生成时间：{now}",
        "",
        "## 结论",
        "",
        f"- 修复下册跨标签 `准北 -> 淮北` 残留 {total} 处。",
        f"- 修复前 `准北`：{before_plain.count('准北')}；修复后 `准北`：{after_plain.count('准北')}。",
        "- 未处理 `准盐/两准` 等需另判词；未打开、展示或嵌入图片。",
        "",
        "## 替换项",
        "",
    ]
    for item in patterns:
        lines.append(f"- {item['label']}：{item['count']} 处")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total)
    print(json.dumps({"changed": total, "after_count": after_plain.count("准北"), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

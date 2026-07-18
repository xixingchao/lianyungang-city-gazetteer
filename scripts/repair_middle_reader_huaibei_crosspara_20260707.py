# -*- coding: utf-8 -*-
"""Follow-up for one tag-split 淮北 residue in the middle reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_huaibei_crosspara_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_huaibei_crosspara_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册淮北跨段残字补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
PATTERN = r"日军占领淮北盐场后(?P<a>.*?)准(?P<gap>(?:<[^>]+>)+)北五、六岸"
REPL = r"日军占领淮北盐场后\g<a>淮\g<gap>北五、六岸"


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(changed: int) -> None:
    marker = "## 2026-07-07 中册淮北跨段残字补修"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 复扫 `repair_middle_reader_huaibei_sync_20260707.py` 后，中册纯文本仅剩 1 处跨标签 `准北五、六岸`，上下文为 `日军占领淮北盐场后`。
- 已定点修复为 `淮北五、六岸`，本批修复 {changed} 处；未处理 `准盐/两准` 等需另判词。
- 报告：`output/reports/middle_reader_huaibei_crosspara_20260707.md`；未打开、展示或嵌入图片。
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
    after, changed = re.subn(PATTERN, REPL, before, flags=re.S)
    TARGET.write_text(after, encoding="utf-8")
    after_plain = plain(after)
    payload = {
        "time": now,
        "target": str(TARGET),
        "changed": changed,
        "before_准北": before_plain.count("准北"),
        "after_准北": after_plain.count("准北"),
        "left_untouched": ["准盐", "两准", "raw OCR", "图片或截图"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = "\n".join([
        "# 中册淮北跨段残字补修",
        "",
        f"> 生成时间：{now}",
        "",
        "## 结论",
        "",
        "- 修复中册跨标签 `淮北五、六岸` 残字 1 处。",
        f"- 修复前 `准北`：{before_plain.count('准北')}；修复后 `准北`：{after_plain.count('准北')}。",
        "- 未处理 `准盐/两准` 等需另判词；未打开、展示或嵌入图片。",
    ]) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(changed)
    print(json.dumps({"changed": changed, "after_count": after_plain.count("准北"), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

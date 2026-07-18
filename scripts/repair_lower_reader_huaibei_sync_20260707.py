# -*- coding: utf-8 -*-
"""Sync lower-reader 准北 residues to 淮北, matching the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "lower_reader_huaibei_sync_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "lower_reader_huaibei_sync_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_下册淮北残字同步修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(text: str, term: str) -> list[str]:
    return [text[max(0, m.start() - 70):m.start() + 120].replace("\n", " ") for m in re.finditer(term, text)]


def upsert_memory(total: int) -> None:
    marker = "## 2026-07-07 下册淮北残字同步修复"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 复扫发现当前全书 reader 中 `准北` 为 0，但下册 reader 残留 34 处 `准北`，均处在淮北盐务、淮北盐场、淮北盐特区、淮北行政区等语境，属分册未同步残字。
- 已仅在 `output/final_reader/连云港市志_下册.html` 执行 `准北 -> 淮北`，本批修复 {total} 处；未处理 `准盐/两准` 等需另判词。
- 报告：`output/reports/lower_reader_huaibei_sync_20260707.md`；未打开、展示或嵌入图片。
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
    full_plain = plain(FULL.read_text(encoding="utf-8"))
    before = TARGET.read_text(encoding="utf-8")
    before_plain = plain(before)
    before_contexts = contexts(before_plain, "准北")
    after = before.replace("准北", "淮北")
    TARGET.write_text(after, encoding="utf-8")
    after_plain = plain(after)
    changed = before.count("准北")
    payload = {
        "time": now,
        "target": str(TARGET),
        "full_reader_准北_count": full_plain.count("准北"),
        "before_准北_count": before_plain.count("准北"),
        "after_准北_count": after_plain.count("准北"),
        "changed": changed,
        "before_contexts": before_contexts,
        "left_untouched": ["准盐", "两准", "raw OCR", "图片或截图"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 下册淮北残字同步修复",
        "",
        f"> 生成时间：{now}",
        "",
        "## 结论",
        "",
        f"- 全书 reader 中 `准北` 计数为 {full_plain.count('准北')}，下册 reader 修复前为 {before_plain.count('准北')}。",
        f"- 已仅在下册 reader 执行 `准北 -> 淮北`，修复 {changed} 处。",
        "- 未处理 `准盐/两准` 等需另判词；未打开、展示或嵌入图片。",
        "",
        "## 残留",
        "",
        f"- 下册 `准北` 修复后计数：{after_plain.count('准北')}",
    ]
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(changed)
    print(json.dumps({"changed": changed, "after_count": after_plain.count("准北"), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

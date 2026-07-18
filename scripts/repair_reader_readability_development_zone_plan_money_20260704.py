# -*- coding: utf-8 -*-
"""Repair source-verified money-unit slips in the development zone plan paragraph."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_development_zone_plan_money_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_development_zone_plan_money_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_开发区九五规划金额单位回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = "workbench/ocr/paddle_ocr/中/part01/page_0423.txt:14-15"
OLD = "每年引办投资过1000方美元的项自不少于5个，投资过500方美元的项自不少于5个"
NEW = "每年引办投资过1000万美元的项目不少于5个，投资过500万美元的项目不少于5个"


def patch_reader() -> int:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count:
        text = text.replace(OLD, NEW)
        HTML.write_text(text, encoding="utf-8")
    elif NEW not in text:
        raise RuntimeError("neither old nor new text found")
    verify_reader()
    return count


def verify_reader() -> None:
    text = HTML.read_text(encoding="utf-8")
    if NEW not in text or OLD in text:
        raise RuntimeError("verification failed")


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    if next_start == -1:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def write_reports(count: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第二十八卷开发区",
        "source": SOURCE,
        "reader_path": str(HTML),
        "current_run_replacements": count,
        "old": OLD,
        "new": NEW,
        "principle": "仅修复页级 OCR 可直接证明的开发区九五规划金额单位和项目错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 开发区九五规划金额单位回源修复",
        "",
        f"- 时间：{now}",
        "- 范围：第二十八卷开发区",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本次脚本复跑实际改写：{count} 处",
        "- 重点：`1000方美元/500方美元/项自` → `1000万美元/500万美元/项目`。",
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 开发区九五规划金额单位回源修复

- 对第二十八卷开发区九五规划段做小修复，源文依据：`{SOURCE}`。
- 修复 `1000方美元/500方美元/项自` → `1000万美元/500万美元/项目`。
- 报告：`output/reports/reader_readability_development_zone_plan_money_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 开发区九五规划金额单位回源修复", memory)


def main() -> None:
    count = patch_reader()
    write_reports(count)
    print(json.dumps({"current_run_replacements": count, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

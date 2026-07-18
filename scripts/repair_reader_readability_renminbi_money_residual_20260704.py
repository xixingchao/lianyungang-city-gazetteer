# -*- coding: utf-8 -*-
"""Repair source-checked RMB money-unit OCR slips left in final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_renminbi_money_residual_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_renminbi_money_residual_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_人民币金额残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = (
    "workbench/ocr/tesseract_check/money_units_20260704/中_part02_page_0289.txt:11; "
    "下_part01_page_0040.txt:5; 下_part01_page_0053.txt:30; "
    "下_part01_page_0302.txt:23-24; 下_part02_page_0048.txt:3; "
    "下_part02_page_0051.txt:18; 下_part02_page_0353.txt:30; "
    "下_part02_page_0424.txt:9-10"
)

REPLACEMENTS = [
    ("财政契税牙税", "牙税7.28方元", "牙税7.28万元", "中_part02_page_0289.txt:11"),
    ("民政募捐留用", "留用96方元", "留用96万元", "下_part01_page_0040.txt:5"),
    ("殡仪馆火化炉造价", "总造价3方元", "总造价3万元", "下_part01_page_0053.txt:30"),
    ("侨务捐赠折合", "折合人民币400多方元", "折合人民币400多万元", "下_part01_page_0302.txt:23"),
    ("侨务费培捐款", "捐款10方港市", "捐款10万港币", "下_part01_page_0302.txt:23-24"),
    ("侨务夏浩原捐赠", "3万元人民市", "3万元人民币", "下_part01_page_0302.txt:24"),
    ("东海县文化馆收入", "年均收入约3.5方元", "年均收入约3.5万元", "下_part02_page_0048.txt:3"),
    ("文化馆训练班经费", "经费200方元（旧人民市）", "经费200万元（旧人民币）", "下_part02_page_0051.txt:18"),
    ("缪秋杰盐补贴", "49方元盐补贴款", "49万元盐补贴款", "下_part02_page_0353.txt:30"),
    ("附录市里集资", "市里集资七千方元", "市里集资七千万元", "下_part02_page_0424.txt:9"),
]

SKIPPED = ["作品名《方元户的追求》保留不改。"]


def patch_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    counts: dict[str, int] = {}
    for label, old, new, _source in REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
        elif new not in text:
            raise RuntimeError(f"neither old nor new text found: {label}")
        counts[label] = count
    HTML.write_text(text, encoding="utf-8")
    verify_reader()
    return counts


def verify_reader() -> None:
    text = HTML.read_text(encoding="utf-8")
    missing = [new for _label, _old, new, _source in REPLACEMENTS if new not in text]
    residuals = [old for _label, old, new, _source in REPLACEMENTS if old in text and old not in new]
    bad_money = [term for term in ["方美元", "方马克"] if term in text]
    if missing or residuals or bad_money:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}, bad_money={bad_money}")


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


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    items = [
        {"label": label, "old": old, "new": new, "source": source, "count": counts[label]}
        for label, old, new, source in REPLACEMENTS
    ]
    payload = {
        "time": now,
        "scope": "第三十八、四十三、四十八、五十二、六十卷及附录",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "skipped": SKIPPED,
        "principle": "用针对性 Tesseract 复核文本确认 raw/Paddle 同错的人民币金额单位残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 人民币金额残留回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 重点：清理 `方元/方港市/人民市` 金额单位残留；作品名《方元户的追求》保留。",
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 人民币金额残留回源修复

- 对第三十八、四十三、四十八、五十二、六十卷及附录做人民币金额单位残留修复。
- 源文依据：`{SOURCE}`。
- 修复 `7.28方元/96方元/3方元/400多方元/10方港市/人民市/3.5方元/200方元/49方元/七千方元` 等同源错识。
- 作品名《方元户的追求》保留不改。
- 报告：`output/reports/reader_readability_renminbi_money_residual_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 人民币金额残留回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

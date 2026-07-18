# -*- coding: utf-8 -*-
"""Repair source-verified money-unit OCR slips in Volumes 21-22."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_machinery_electronics_money_units_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_machinery_electronics_money_units_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_机械电子工业金额单位错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第二十一卷-机械工业">第二十一卷机械工业</h2>'
SCOPE_END = '<h2 id="第二十三卷-建材工业">第二十三卷建材工业</h2>'
SOURCE = (
    "workbench/ocr/paddle_ocr/中/part01/page_0194.txt:13-16; "
    "page_0206.txt:7-9; page_0236.txt:27-30; page_0256.txt:8-10; "
    "page_0259.txt:25-26; page_0260.txt:11-14; page_0264.txt:20-23"
)

REPLACEMENTS = [
    ("机械工业总产值", "实现工业总产值13650方元", "实现工业总产值13650万元", "page_0194.txt:13-14"),
    ("车辆厂亏损", "出现亏损241方元", "出现亏损241万元", "page_0206.txt:7-8"),
    ("电台利润", "实现利润80.6方元", "实现利润80.6万元", "page_0236.txt:29-30"),
    (
        "直流伺服电机经费",
        "赣榆县科学技术委员会拨给试制经费1方元，江苏省电子工业局拨款6方元",
        "赣榆县科学技术委员会拨给试制经费1万元，江苏省电子工业局拨款6万元",
        "page_0256.txt:8-10",
    ),
    (
        "人造水晶技改",
        "该厂投资200方元，新增年产5吨的人造水晶技改项自",
        "该厂投资200万元，新增年产5吨的人造水晶技改项目",
        "page_0259.txt:25-26",
    ),
    ("铁氧磁体投资53万", "该厂投资53方元", "该厂投资53万元", "page_0260.txt:11-12"),
    ("铁氧磁体投资22万", "该厂投资22方元", "该厂投资22万元", "page_0260.txt:14"),
    (
        "数控钻床拨款",
        "四机部工艺处又拨款54方元，该广贷款21万元",
        "四机部工艺处又拨款54万元，该厂贷款21万元",
        "page_0264.txt:20-23",
    ),
]

SKIPPED = [
    "第二十二卷仍有 `方只` 等量词类文本，本批只处理页级 OCR 可直接确认的金额单位。",
    "`投人/进人` 暂不批量替换，继续逐条回源。",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    original = text[start:end]
    segment = original
    counts: dict[str, int] = {}
    for label, old, new, _source in REPLACEMENTS:
        count = segment.count(old)
        if count:
            segment = segment.replace(old, new)
        elif new not in segment:
            raise RuntimeError(f"neither old nor new text found: {label}")
        counts[label] = count
    if segment != original:
        HTML.write_text(text[:start] + segment + text[end:], encoding="utf-8")
    verify_reader()
    return counts


def verify_reader() -> None:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [new for _label, _old, new, _source in REPLACEMENTS if new not in segment]
    residuals = [old for _label, old, new, _source in REPLACEMENTS if old in segment and old not in new]
    if missing or residuals:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}")


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
        "scope": "第二十一卷机械工业、第二十二卷电子工业",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "skipped": SKIPPED,
        "principle": "仅修复页级 OCR 可直接证明的金额单位错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 机械电子工业金额单位错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 重点：修正 `13650方元/241方元/80.6方元/1方元/6方元/200方元/53方元/22方元/54方元` 等金额单位错识，并同步修正同源行 `技改项自/该广贷款`。",
        "- 保留：" + "；".join(SKIPPED),
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 机械电子工业金额单位错识回源修复

- 对第二十一卷机械工业、第二十二卷电子工业做小批金额单位错识修复，范围限定在 `第二十一卷-机械工业` 到 `第二十三卷-建材工业` 前。
- 源文依据：`{SOURCE}`。
- 修复 `13650方元/241方元/80.6方元/1方元/6方元/200方元/53方元/22方元/54方元` → 对应 `万元`，并按同源行修正 `技改项自`→`技改项目`、`该广贷款`→`该厂贷款`。
- 未对 `投人/进人` 和量词类 `方只` 做批量替换，继续逐条回源。
- 报告：`output/reports/reader_readability_machinery_electronics_money_units_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 机械电子工业金额单位错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

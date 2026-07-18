# -*- coding: utf-8 -*-
"""Repair source-verified money-unit slips in material circulation, tax, and finance volumes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_finance_tax_material_money_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_finance_tax_material_money_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_物资税务金融金额单位回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = (
    "workbench/ocr/paddle_ocr/中/part02/page_0260.txt:41; page_0261.txt:4; "
    "page_0337.txt:5,19-20,27-28; page_0353.txt:21; page_0354.txt:7; "
    "page_0370.txt:7; page_0371.txt:23,32; page_0375.txt:26; "
    "page_0389.txt:10; page_0390.txt:8,38"
)

REPLACEMENTS = [
    ("物资借入资金", "借入资金10029方元", "借入资金10029万元", "page_0260.txt:41"),
    ("物资折旧资金", "折旧资金1541方元", "折旧资金1541万元", "page_0261.txt:4"),
    ("税务技改免税", "技术改造的企业免税450方元", "技术改造的企业免税450万元", "page_0337.txt:5"),
    ("税务减免税款", "减免税款4720方元", "减免税款4720万元", "page_0337.txt:19"),
    ("税务税前还贷", "税前还贷509方元", "税前还贷509万元", "page_0337.txt:19"),
    ("税务出口退税670", "出口产品退税670.5方元", "出口产品退税670.5万元", "page_0337.txt:19-20"),
    ("税务投入产出", "“投入产出原则引人了税收减免", "“投入产出”原则引入了税收减免", "page_0337.txt:20"),
    ("税务出口退税1347", "出口退税1347.9方元", "出口退税1347.9万元", "page_0337.txt:27-28"),
    ("金融现金投放早段", "净投放现金9523方元", "净投放现金9523万元", "page_0353.txt:21"),
    ("金融存款余额", "存款余额为7579方元", "存款余额为7579万元", "page_0354.txt:7"),
    ("金融润滑油产值", "实现产值1030方元", "实现产值1030万元", "page_0370.txt:7"),
    ("金融锦屏化工贷款", "投资贷款200方元，支持市锦屏化工广", "投资贷款200万元，支持市锦屏化工厂", "page_0371.txt:23"),
    ("金融船舶车辆贷款", "发放贷款176方元", "发放贷款176万元", "page_0371.txt:32"),
    ("金融信用卡存款", "存款余额为人民币35.45方元", "存款余额为人民币35.45万元", "page_0375.txt:26"),
    ("金融1957贷款余额", "贷款余额4862方元", "贷款余额4862万元", "page_0389.txt:10"),
    ("金融贷款达现金投放", "现金投放量9523方元", "现金投放量9523万元", "page_0390.txt:8"),
    ("金融节约建设资金", "节约建设资金10841方元", "节约建设资金10841万元", "page_0390.txt:38"),
]

SKIPPED = [
    "商业、文化、人物、附录等剩余 `方元/方美元` 尚未逐页核完，本批不处理。",
]


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
        "scope": "第三十七卷物资流通、第三十九卷税务、第四十卷金融",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "skipped": SKIPPED,
        "principle": "仅修复页级 OCR 可直接证明为 `万元` 的金额单位错识及同源短错。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 物资税务金融金额单位回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 重点：修正物资、税务、金融卷中页级 OCR 明确为 `万元` 的 `方元` 错识，并同步修正 `化工广`、`引人` 等同源短错。",
        "- 保留：" + "；".join(SKIPPED),
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 物资税务金融金额单位回源修复

- 对第三十七卷物资流通、第三十九卷税务、第四十卷金融做金额单位错识回源修复。
- 源文依据：`{SOURCE}`。
- 修复 `10029方元/1541方元/450方元/4720方元/509方元/670.5方元/1347.9方元/9523方元/7579方元/1030方元/200方元/176方元/35.45方元/4862方元/10841方元` → 对应 `万元`，并同步修正 `化工广`→`化工厂`、`引人`→`引入`。
- 商业、文化、人物、附录等剩余 `方元/方美元` 尚未逐页核完，本批不处理。
- 报告：`output/reports/reader_readability_finance_tax_material_money_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 物资税务金融金额单位回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

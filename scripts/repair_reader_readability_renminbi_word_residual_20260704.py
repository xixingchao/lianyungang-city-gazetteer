# -*- coding: utf-8 -*-
"""Repair source-checked 人民市/北海市 currency-word OCR slips."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_renminbi_word_residual_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_renminbi_word_residual_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_人民币词形残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = (
    "workbench/ocr/tesseract_check/renminbi_20260704/中_part01_page_0512.txt:11; "
    "中_part02_page_0351.txt:31,36-38; 中_part02_page_0352.txt:17-18; "
    "workbench/ocr/paddle_ocr/中/part02/page_0351.txt:33; "
    "workbench/ocr/paddle_ocr/中/part02/page_0395.txt:4; "
    "workbench/ocr/tesseract_check/renminbi_20260704/中_part02_page_0371.txt:4,9"
)

REPLACEMENTS = [
    ("口岸磷酸二胺索赔", "索赔人民市74万元", "索赔人民币74万元", "中_part01_page_0512.txt:11"),
    ("金融本位币", "以北海市为本位市", "以北海币为本位币", "中_part02_page_0351.txt:37-38"),
    ("金融人民币兑换", "人民银行以人民市1元兑北海市或华中币", "人民银行以人民币1元兑北海币或华中币", "paddle_ocr/中/part02/page_0351.txt:33"),
    ("人民币发行", "发行人民市，境内", "发行人民币，境内", "中_part02_page_0352.txt:17-18"),
    ("外汇贷款资金", "在人民市信贷资金不足时", "在人民币信贷资金不足时", "中_part02_page_0371.txt:4,9"),
    ("外汇额度价格", "价格为1元人民市。现汇按国家外汇牌价加1元人民市结算", "价格为1元人民币。现汇按国家外汇牌价加1元人民币结算", "paddle_ocr/中/part02/page_0395.txt:4"),
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
    if missing or residuals or "人民市" in text:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}, 人民市={text.count('人民市')}")


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
        "scope": "第二十九卷口岸、第四十卷金融",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "principle": "仅修复 Tesseract 或 PaddleOCR 明确确认的 人民市/北海市 货币词形错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 人民币词形残留回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 重点：清理 `人民市` 残留，并在同句源文支持下修正 `北海市/本位市` 为 `北海币/本位币`。",
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 人民币词形残留回源修复

- 对第二十九卷口岸、第四十卷金融做 `人民市/北海市` 货币词形残留修复。
- 源文依据：`{SOURCE}`。
- 修复 `索赔人民市74万元/发行人民市/人民市信贷资金/1元人民市` → `人民币`；同句修正 `北海市/本位市` → `北海币/本位币`。
- 报告：`output/reports/reader_readability_renminbi_word_residual_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 人民币词形残留回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

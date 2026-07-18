# -*- coding: utf-8 -*-
"""Repair source-verified poverty relief OCR slips in Volume 43."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_civil_affairs_poverty_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_civil_affairs_poverty_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第四十三卷民政信访扶贫段高置信错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第四十三卷-民政-信访">第四十三卷民政 信访</h2>'
SCOPE_END = '<h2 id="第四十四卷-治安司法">第四十四卷治安司法</h2>'
SOURCE = "workbench/ocr/paddle_ocr/下/part01/page_0034.txt:8-37"
REPLACEMENTS = [
    ("1984救灾款单位", "救灾款33.66方元", "救灾款33.66万元"),
    ("1985救济款单位", "救济款13.21方元", "救济款13.21万元"),
    ("1985低息农贷单位", "低息农贷款121.77方元", "低息农贷款121.77万元"),
    ("灌云包扶缺句", "贫困户脱贫成为专业户。1988年，全市扶贫工作形成“带包”新格局，赣榆县供电、水利、供销社、物资、粮食5个局共包扶5个贫困村。灌1988年，全市扶持16361户", "贫困户脱贫成为专业户。1988年，全市扶贫工作形成“带包”新格局，赣榆县供电、水利、供销社、物资、粮食5个局共包扶5个贫困村。灌云县53个部、委、办、局包扶53个贫困村，21个乡镇机关和干部包扶2400多个贫困户。1988年，全市扶持16361户"),
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
    for label, old, new in REPLACEMENTS:
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
    missing = [new for _label, _old, new in REPLACEMENTS if new not in segment]
    residuals = [old for _label, old, new in REPLACEMENTS if old in segment and old not in new]
    if missing or residuals:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}")


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    current_changes = sum(counts.values())
    verified_items = len(REPLACEMENTS)
    payload = {
        "time": now,
        "scope": "第四十三卷民政 信访 扶贫段",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": verified_items,
        "current_run_replacements": current_changes,
        "counts": counts,
        "principle": "仅修复页级 OCR 清楚证明的扶贫段单位错识和短句缺漏。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第四十三卷民政信访扶贫段高置信错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{verified_items} 项",
        f"- 本次脚本复跑实际改写：{current_changes} 处",
        "- 重点：修正扶贫资金单位 `方元` 为 `万元`，并补回灌云县包扶贫困村、贫困户短句。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-04 第四十三卷民政信访扶贫段高置信错识回源修复

- 对第四十三卷民政信访 `第三章救灾救济扶贫 / 第三节扶贫` 进行小批回源修复。
- 源文依据：`{SOURCE}`。
- 修复 `救灾款33.66方元`、`救济款13.21方元`、`低息农贷款121.77方元` 为 `万元`；补回 `灌云县53个部、委、办、局包扶53个贫困村，21个乡镇机关和干部包扶2400多个贫困户`。
- 本批核验修复 {verified_items} 项；报告：`output/reports/reader_readability_civil_affairs_poverty_20260704.md`。
"""
    append_once(MEMORY, "## 2026-07-04 第四十三卷民政信访扶贫段高置信错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

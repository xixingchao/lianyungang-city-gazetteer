# -*- coding: utf-8 -*-
"""Repair source-verified OCR slips in Volume 39 tax."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_tax_batch_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_tax_batch_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第三十九卷税务高置信错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第三十九卷-税务">第三十九卷税务</h2>'
SCOPE_END = '<h2 id="第四十卷-金融">第四十卷金融</h2>'
SOURCE = "workbench/ocr/paddle_ocr/中/part02/page_0335.txt:18-24; page_0341.txt:14-35"

REPLACEMENTS = [
    ("盐入猴嘴坨", "大浦工区盐人猴嘴坨", "大浦工区盐入猴嘴坨", "page_0335.txt:18"),
    ("盐税划入金库", "盐税当天划人金库", "盐税当天划入金库", "page_0335.txt:22-23"),
    ("税款及时入库", "税款及时人库", "税款及时入库", "page_0335.txt:23"),
    ("市区盐税入库", "市区盐税人库：6644.4万元", "市区盐税入库6644.4万元", "page_0335.txt:23-24"),
    ("1988追补税款单位", "共追补税款541.43元，有4名", "共追补税款541.43万元，有4名", "page_0341.txt:18-19"),
    ("1988依法逮捕", "因偷抗税情节严重被依法速捕、判刑", "因偷抗税情节严重被依法逮捕、判刑", "page_0341.txt:19"),
    ("1989投入干部", "在重点检查阶段，投人580名税务干部", "在重点检查阶段，投入580名税务干部", "page_0341.txt:21-22"),
    ("1989漏句", "抽查个体工商业7622户，查出假全民、假集体、假民政福和处收罚款1021.1万元", "抽查个体工商业7622户，查出假全民、假集体、假民政福利、假校办企业819户，批发代扣税企业491户，应纳个人收入调节税者410人，追补税款和处收罚款1021.1万元", "page_0341.txt:22-24"),
    ("1989逮捕", "其中速捕8人，判刑2人", "其中逮捕8人，判刑2人", "page_0341.txt:24-25"),
    ("1989税收大检查漏句", "全市抽调税年人库625.5万元", "全市抽调税务干部500人参加税收大检查，重点检查各类企业1349户，查出应补税款759.2万元，当年人库625.5万元", "page_0341.txt:25-27"),
    ("1990开头残点", "<p>.1990年4月起", "<p>1990年4月起", "page_0341.txt:28"),
    ("1990偷漏税单位", "查出偷漏税241方元", "查出偷漏税241万元", "page_0341.txt:30-31"),
    ("1990投入检查", "抽调426名税务于部投人“三项大检查”", "抽调426名税务干部投入“三项大检查”", "page_0341.txt:31-32"),
    ("1990逮捕", "因偷税2.3万元被速捕", "因偷税2.3万元被逮捕", "page_0341.txt:34-35"),
]

SKIPPED = [
    "`当年人库625.5万元` 源 OCR 仍写 `人库`，本批暂不凭习惯替换。",
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
        "scope": "第三十九卷税务",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "skipped": SKIPPED,
        "principle": "仅修复页级 OCR 可直接证明的税务段错识和漏句。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第三十九卷税务高置信错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 重点：修正 `盐人/划人/人库/速捕/方元/投人` 等源页明确错识，并补回 1989 年个体税收专项检查和税收大检查漏句。",
        f"- 保留：{SKIPPED[0]}",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-04 第三十九卷税务高置信错识回源修复

- 对第三十九卷税务做小批回源修复，范围限定在 `第三十九卷-税务` 到 `第四十卷-金融` 前。
- 源文依据：`{SOURCE}`。
- 修复 `盐人猴嘴坨`→`盐入猴嘴坨`、`划人金库`→`划入金库`、`税款及时人库/市区盐税人库`→`入库`、`速捕`→`逮捕`、`541.43元/241方元`→`万元`、`投人`→`投入`，并补回 1989 年个体税收专项检查中 `假民政福利、假校办企业819户，批发代扣税企业491户，应纳个人收入调节税者410人，追补税款` 和税收大检查 `税务干部500人参加税收大检查...应补税款759.2万元` 等漏句。
- `当年人库625.5万元` 因源 OCR 仍写 `人库`，本批暂不凭习惯替换。
- 报告：`output/reports/reader_readability_tax_batch_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第三十九卷税务高置信错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Repair source-verified OCR slips in Volume 38 finance."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_finance_batch_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_finance_batch_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第三十八卷财政高置信错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第三十八卷-财政">第三十八卷财政</h2>'
SCOPE_END = '<h2 id="第三十九卷-税务">第三十九卷税务</h2>'
SOURCE = (
    "workbench/ocr/paddle_ocr/中/part02/page_0279.txt:17-20; "
    "page_0285.txt:5-13; page_0292.txt:4-20; page_0293.txt:6; "
    "page_0295.txt:16-38; page_0296.txt:15-27; page_0297.txt:6-16; "
    "page_0298.txt:14-31; page_0304.txt:28-35; page_0307.txt:6-19; page_0308.txt:18-20"
)

REPLACEMENTS = [
    ("1990财政收支", "财政收入39808方元", "财政收入39808万元", "page_0279.txt:19"),
    ("1990财政支出", "财政支出38583方元", "财政支出38583万元", "page_0279.txt:19-20"),
    ("支出基数", "支出基数调整为7898方元", "支出基数调整为7898万元", "page_0285.txt:9-11"),
    ("调节基金入库", "1381万元（人市县财政金库部分）", "1381万元（入市县财政金库部分）", "page_0292.txt:4-6"),
    ("排污费纳入", "1983年7月起纳人财政预算内管理，交人市县国库", "1983年7月起纳入财政预算内管理，交入市县国库", "page_0292.txt:8-10"),
    ("养港纳入", "的办法，纳人地方财政预算", "的办法，纳入地方财政预算", "page_0292.txt:14-16"),
    ("养港收入", "以港养港收人共6225万元", "以港养港收入共6225万元", "page_0292.txt:16-17"),
    ("预算内纳入", "并纳人预算内管理，同各项附加收入统筹安排", "并纳入预算内管理，同各项附加收入统筹安排", "page_0293.txt:6"),
    ("化工支出", "化工1056方元", "化工1056万元", "page_0295.txt:16-19"),
    ("科技三项1984", "1984年支出274方元", "1984年支出274万元", "page_0295.txt:27-30"),
    ("科技三项总额", "科技三项费用支出3022方元", "科技三项费用支出3022万元", "page_0295.txt:30-32"),
    ("流动资金工业", "工业部门3061方元", "工业部门3061万元", "page_0295.txt:36-38"),
    ("畜牧事业费", "畜牧事业费613方元", "畜牧事业费613万元", "page_0296.txt:15-18"),
    ("农业投入", "国家对农业大幅度增加投人，“七五”计划期间，国家投人连云港市支农资金2.5亿元", "国家对农业大幅度增加投入，“七五”计划期间，国家投入连云港市支农资金2.5亿元", "page_0296.txt:24-27"),
    ("文教投入", "增加对文教科卫事业的投人", "增加对文教科卫事业的投入", "page_0297.txt:6-8"),
    ("教育经费", "教育经费46477方元", "教育经费46477万元", "page_0297.txt:9-11"),
    ("加大投入", "基本建设支出等加大投人", "基本建设支出等加大投入", "page_0297.txt:14-16"),
    ("专项支出", "专项支出共9054方元", "专项支出共9054万元", "page_0298.txt:18-19"),
    ("预算外纳入", "预算外资金收入，纳人预算内统筹安排支出", "预算外资金收入，纳入预算内统筹安排支出", "page_0298.txt:27-31"),
    ("科学事业费投入", "对科学事业费投人逐年增长", "对科学事业费投入逐年增长", "page_0304.txt:32"),
    ("差额预算", "单位，般采用定项补助", "单位，一般采用定项补助", "page_0304.txt:34-35"),
    ("预算外计划", "预算外资金纳人计划管理", "预算外资金纳入计划管理", "page_0307.txt:6-8"),
    ("财政专户", "原则，纳人财政部门在建设银行开设的专户", "原则，纳入财政部门在建设银行开设的专户", "page_0307.txt:17-19"),
    ("罚没款", "罚没款150余方元", "罚没款150余万元", "page_0308.txt:18-20"),
]

SKIPPED = [
    "`7.28方元` 未在页级 OCR 中定位到直接证据，本批保留。",
    "`列人财政预算支出` 源页 OCR 同样写作 `列人`，本批不凭语感替换。",
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
        "scope": "第三十八卷财政",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "skipped": SKIPPED,
        "principle": "仅修复页级 OCR 可直接证明的财政卷金额单位、入/纳入/投入等错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第三十八卷财政高置信错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 重点：修正 `39808方元/38583方元/7898方元/1056方元/274方元/3022方元/3061方元/613方元/46477方元/9054方元/150余方元` 等金额单位错识，以及 `纳人/交人/收人/投人/般采用` 等源页明确错识。",
        "- 保留：" + "；".join(SKIPPED),
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 第三十八卷财政高置信错识回源修复

- 对第三十八卷财政做小批回源修复，范围限定在 `第三十八卷-财政` 到 `第三十九卷-税务` 前。
- 源文依据：`{SOURCE}`。
- 修复金额单位 `39808方元/38583方元/7898方元/1056方元/274方元/3022方元/3061方元/613方元/46477方元/9054方元/150余方元` → 对应 `万元`，并修正 `纳人/交人/收人/投人/般采用` 等源页明确错识。
- `7.28方元` 与源页 OCR 同样有疑点的 `列人财政预算支出` 暂不凭语感替换。
- 报告：`output/reports/reader_readability_finance_batch_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第三十八卷财政高置信错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

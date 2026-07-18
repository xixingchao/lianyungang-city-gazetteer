# -*- coding: utf-8 -*-
"""Repair source-verified OCR slips in Volume 17 crafts chapter."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_crafts_batch_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_crafts_batch_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第十七卷工艺美术高置信错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第十七卷-工艺美术">第十七卷工艺美术</h2>'
SCOPE_END = '<h2 id="第十八卷-食品工业">第十八卷食品工业</h2>'
SOURCE = "workbench/ocr/paddle_ocr/中/part01/page_0024.txt:23-36; page_0025.txt:6-20; page_0029.txt:11-13; page_0036.txt:30-32; page_0038.txt:3-6; page_0040.txt:30-32; page_0042.txt:35-36"
REPLACEMENTS = [
    ("购地面积", "购地1方平方米", "购地1万平方米"),
    ("贝雕厂徘徊", "13万元左右律迥", "13万元左右徘徊"),
    ("赣榆工艺厂徘徊", "4万元左右律", "4万元左右徘徊"),
    ("贝雕厂生产", "市贝雕广生产", "市贝雕厂生产"),
    ("日元收购", "28万元收购", "28万日元收购"),
    ("花冠引号", "生产的花冠牌贝雕画", "生产的“花冠”牌贝雕画"),
    ("旅游梳蓖", "旅游梳葩", "旅游梳蓖"),
    ("万壑藏幽", "万警藏幽", "万壑藏幽"),
    ("虎神女图引号", "设计的虎神女图”", "设计的“虎神女图”"),
    ("春", "“春徐”等9幅产品", "“春”等9幅产品"),
    ("赣榆美术厂", "赣榆美术研制", "赣榆美术厂研制"),
    ("项目竣工试产", "画框条生产线项自工试产", "画框条生产线项目竣工试产"),
    ("白塔美术厂", "白塔美术广", "白塔美术厂"),
    ("销售收入", "销售收入608.72方元", "销售收入608.72万元"),
    ("草编列入", "产品列人省“星火计划”，由省科委拨专项贷款20方元", "产品列入省“星火计划”，由省科委拨专项贷款20万元"),
    ("柳编列入", "系列产品列人省“星火计划”", "系列产品列入省“星火计划”"),
    ("刺绣购机", "用7.3方元从苏州购置", "用7.3万元从苏州购置"),
    ("刺绣利税", "利税总额14.16方元", "利税总额14.16万元"),
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
    residuals = [old for _label, old, _new in REPLACEMENTS if old in segment]
    if missing or residuals:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}")


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(counts.values())
    payload = {
        "time": now,
        "scope": "第十七卷工艺美术",
        "source": SOURCE,
        "reader_path": str(HTML),
        "total_replacements": total,
        "counts": counts,
        "principle": "仅修复页级 OCR 清楚给出正确写法的第十七卷错识；源 OCR 本身未能确认的候选保留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第十七卷工艺美术高置信错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本次替换：{total} 处",
        "- 保留：源 OCR 未能直接确认的其它疑点不凭猜测修。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-03 第十七卷工艺美术高置信错识回源修复

- 对第十七卷工艺美术进行小批回源修复，范围限定在 `第十七卷-工艺美术` 到 `第十八卷-食品工业` 前。
- 源文依据：`{SOURCE}`。
- 修复示例：`购地1方平方米`→`购地1万平方米`，`画框条生产线项自工试产`→`画框条生产线项目竣工试产`，`7.3方元`→`7.3万元`，`列人省“星火计划”`→`列入省“星火计划”`。
- 本次替换 {total} 处；源 OCR 本身未能确认的候选保留。
- 报告：`output/reports/reader_readability_crafts_batch_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第十七卷工艺美术高置信错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"total_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

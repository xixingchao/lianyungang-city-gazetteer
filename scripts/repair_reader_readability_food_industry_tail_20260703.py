# -*- coding: utf-8 -*-
"""Repair source-verified OCR slips in the tail of Volume 18 food industry."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_food_industry_tail_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_food_industry_tail_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第十八卷食品工业后半段高置信错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第十八卷-食品工业">第十八卷食品工业</h2>'
SCOPE_END = '<h2 id="第十九卷-医药">第十九卷医药</h2>'
SOURCE = "workbench/ocr/paddle_ocr/中/part01/page_0094.txt:26-28; page_0100.txt:35-36; page_0101.txt:3-6; page_0102.txt:38-41; page_0104.txt:3-7; page_0105.txt:26-28"
REPLACEMENTS = [
    ("葡萄酒厂产值利税", "实现产值2669方元，利税172方元", "实现产值2669万元，利税172万元"),
    ("葡萄酒厂骨干企业", "轻工业重点骨于企业", "轻工业重点骨干企业"),
    ("异维C钠出资", "出资5方元", "出资5万元"),
    ("异抗坏血酸钠名称", "异维生素C钠（D异抗坏血酸钠）", "异维生素C钠（D-异抗坏血酸钠）"),
    ("异维C钠标准号", "GB8273一87标准", "GB8273-87标准"),
    ("赣榆酿造厂固定资产", "固定资产原值129方元", "固定资产原值129万元"),
    (
        "制碘厂产能产值",
        "糖化酶1000元，利税365方元",
        "糖化酶1000吨、异维C钠100吨、丙烯酸树脂80吨。当年完成工业产值2624万元，出口创汇200万元，利税365万元",
    ),
    ("灌豆一号引号", "灌云县“灌豆一号大豆特产资源", "灌云县“灌豆一号”大豆特产资源"),
    ("康乐食品厂投资", "投资30方元，在灌云县伊山镇筹建国营江苏灌云县康乐食品厂", "投资30万元，在灌云县伊山镇筹建国营江苏灌云县康乐食品厂"),
    ("康乐食品厂生产状态", "生产一一直不正常", "生产一直不正常"),
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
        "scope": "第十八卷食品工业后半段",
        "source": SOURCE,
        "reader_path": str(HTML),
        "total_replacements": total,
        "counts": counts,
        "principle": "仅修复页级 OCR 清楚给出正确写法的第十八卷后半段错识；源 OCR 本身未能确认的候选保留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第十八卷食品工业后半段高置信错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本次替换：{total} 处",
        "- 重点：修正葡萄酒厂、食品添加剂、酿造厂、制碘厂、康乐食品厂段落中的单位、标准号、漏字和截断信息。",
        "- 保留：`罗旋压榨机`、`豆浆晶生产` 等源 OCR 未能进一步确认的疑点未改。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-03 第十八卷食品工业后半段高置信错识回源修复

- 对第十八卷食品工业后半段继续小批回源修复，范围限定在 `第十八卷-食品工业` 到 `第十九卷-医药` 前。
- 源文依据：`{SOURCE}`。
- 修复示例：`实现产值2669方元，利税172方元`→`实现产值2669万元，利税172万元`，`GB8273一87标准`→`GB8273-87标准`，补回制碘厂 `异维C钠100吨、丙烯酸树脂80吨` 及当年产值、创汇信息。
- 本次替换 {total} 处；`罗旋压榨机`、`豆浆晶生产` 等源 OCR 未能进一步确认的候选保留。
- 报告：`output/reports/reader_readability_food_industry_tail_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第十八卷食品工业后半段高置信错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"total_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

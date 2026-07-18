# -*- coding: utf-8 -*-
"""Repair source-checked 纳人 -> 纳入 OCR slips in final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_naru_residual_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_naru_residual_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_纳人纳入残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = (
    "workbench/ocr/paddle_ocr/中/part01/page_0429.txt:30; page_0458.txt:38; page_0497.txt:13; "
    "workbench/ocr/paddle_ocr/中/part02/page_0041.txt:96; page_0068.txt:28; "
    "page_0166.txt:28; page_0170.txt:27; page_0265.txt:18,27; page_0269.txt:9; "
    "page_0271.txt:6,16,23; page_0275.txt:15; page_0354.txt:34; page_0355.txt:5; "
    "page_0390.txt:16; workbench/ocr/paddle_ocr/下/part01/page_0058.txt:13; "
    "page_0234.txt:37; page_0245.txt:11; page_0315.txt:13; page_0376.txt:24; "
    "page_0429.txt:23; page_0456.txt:33"
)

REPLACEMENTS = [
    ("开发区水电计划", "水、电纳人计划", "水、电纳入计划", "中/part01/page_0429.txt:30"),
    ("方案列车", "车流都纳人了方案列车", "车流都纳入了方案列车", "中/part01/page_0458.txt:38"),
    ("准安关境管理", "征税纳人准安关境管理", "征税纳入准安关境管理", "中/part01/page_0497.txt:13"),
    ("养路费财政预算", "养路费用纳人各级财政预算", "养路费用纳入各级财政预算", "中/part02/page_0041.txt:96"),
    ("邮路邮件", "邮件纳人新浦至板桥", "邮件纳入新浦至板桥", "中/part02/page_0068.txt:28"),
    ("农药国家计划", "农药被纳人国家计划", "农药被纳入国家计划", "中/part02/page_0166.txt:28"),
    ("茶叶国家计划", "茶叶全部纳人国家计划", "茶叶全部纳入国家计划", "中/part02/page_0170.txt:27"),
    ("不纳入国家分配", "不纳人国家分配计划", "不纳入国家分配计划", "中/part02/page_0265.txt:18"),
    ("国民经济计划", "纳人全市国民经济计划", "纳入全市国民经济计划", "中/part02/page_0265.txt:27"),
    ("地方资源计划", "纳人地方资源计划", "纳入地方资源计划", "中/part02/page_0269.txt:9"),
    ("市补给计划", "纳人市补给计划", "纳入市补给计划", "中/part02/page_0271.txt:6"),
    ("水泥市区平衡", "水泥被纳人市区平衡分配", "水泥被纳入市区平衡分配", "中/part02/page_0271.txt:16"),
    ("机电统配计划", "机电产品被纳人国家统配计划", "机电产品被纳入国家统配计划", "中/part02/page_0271.txt:23"),
    ("市场体系", "商品纳人市场体系", "商品纳入市场体系", "中/part02/page_0275.txt:15"),
    ("建行中央信贷", "建设银行纳人中央信贷资金", "建设银行纳入中央信贷资金", "中/part02/page_0354.txt:34"),
    ("信托综合信贷", "信托投资机构纳人国家综合信贷计划", "信托投资机构纳入国家综合信贷计划", "中/part02/page_0355.txt:5"),
    ("建行信贷计划", "建设银行纳人信贷计划管理范围", "建设银行纳入信贷计划管理范围", "中/part02/page_0390.txt:16"),
    ("信用宏观控制", "信用活动纳人市人民银行", "信用活动纳入市人民银行", "金融章源文同段"),
    ("社团法制轨道", "纳人法制轨道", "纳入法制轨道", "下/part01/page_0058.txt:13"),
    ("劳动力国家计划", "劳动力管理纳人国家计划范围", "劳动力管理纳入国家计划范围", "下/part01/page_0234.txt:37"),
    ("招工轨道", "纳人正常招工用工轨道", "纳入正常招工用工轨道", "下/part01/page_0245.txt:11"),
    ("共保合同", "内部分配纳人共保合同", "内部分配纳入共保合同", "下/part01/page_0315.txt:13"),
    ("中学正轨", "中学教学秩序逐步纳人正轨", "中学教学秩序逐步纳入正轨", "下/part01/page_0376.txt:24"),
    ("科技计划", "科技情报调研项目纳人市科技发展计划", "科技情报调研项目纳入市科技发展计划", "下/part01/page_0429.txt:23"),
    ("地震台网", "纳人国家Ⅱ类台网", "纳入国家Ⅱ类台网", "下/part01/page_0456.txt:33"),
    ("区域台网", "纳人地方区域台网", "纳入地方区域台网", "下/part01/page_0456.txt:33"),
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
    residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in text]
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
        "scope": "多卷正文 `纳人` 残留",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "principle": "仅修复源页支持为 `纳入` 的 `纳人`；不做全局字形替换。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 纳人/纳入残留回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验条目：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 采用逐短语替换，未做全局 `纳人` 替换。",
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 纳人/纳入残留回源修复

- 对开发区、口岸、交通、邮电、供销、物资、金融、民政、劳动、教育、科技等卷 `纳人` 残留做逐短语回源修复。
- 源文依据：`{SOURCE}`。
- 修复 `纳人计划/纳人方案列车/纳人管理/纳人财政预算/纳人国家计划/纳人市场体系/纳人信贷计划/纳人法制轨道/纳人正轨/纳人台网` 等 26 处为 `纳入`。
- 本批未做全局字形替换；后续继续处理剩余 `投人`。
- 报告：`output/reports/reader_readability_naru_residual_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 纳人/纳入残留回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

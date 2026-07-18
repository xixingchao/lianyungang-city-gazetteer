# -*- coding: utf-8 -*-
"""Repair source-verified residual short OCR slips across small scoped sections."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_residual_short_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_residual_short_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_跨卷残留短错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "电力人身事故隐患",
        "scope": "第二十五卷电力工业",
        "start": '<h2 id="第二十五卷-电力工业">第二十五卷电力工业</h2>',
        "end": '<h2 id="第二十六卷-矿产">第二十六卷矿产</h2>',
        "old": '增加了“人身事故隐惠"类别的分析统计',
        "new": '增加了“人身事故隐患”类别的分析统计',
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0338.txt:7-8",
    },
    {
        "label": "劳动妥善处理",
        "scope": "第四十七卷劳动",
        "start": '<h2 id="第四十七卷-劳动">第四十七卷劳动</h2>',
        "end": '<h2 id="第四十八卷-外事侨务">第四十八卷外事侨务</h2>',
        "old": "并做了要善处理",
        "new": "并做了妥善处理",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0274.txt:33-34",
    },
    {
        "label": "劳动事故隐患",
        "scope": "第四十七卷劳动",
        "start": '<h2 id="第四十七卷-劳动">第四十七卷劳动</h2>',
        "end": '<h2 id="第四十八卷-外事侨务">第四十八卷外事侨务</h2>',
        "old": "共查出事故隐惠934处，其中较大隐惠120处",
        "new": "共查出事故隐患934处，其中较大隐患120处",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0274.txt:35-38",
    },
    {
        "label": "劳动列入目标管理",
        "scope": "第四十七卷劳动",
        "start": '<h2 id="第四十七卷-劳动">第四十七卷劳动</h2>',
        "end": '<h2 id="第四十八卷-外事侨务">第四十八卷外事侨务</h2>',
        "old": "把安全指标列人各单位的目标管理范围",
        "new": "把安全指标列入各单位的目标管理范围",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0275.txt:8-9",
    },
]

SKIPPED = [
    "未对全书 `纳人/迁人/人库/速捕` 做词级批量替换；这些词在古文、人物传和专名语境中可能不是同一种错误。",
]


def scoped_segment(text: str, item: dict[str, str]) -> tuple[int, int, str]:
    start = text.index(item["start"])
    end = text.index(item["end"], start)
    return start, end, text[start:end]


def patch_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    counts: dict[str, int] = {}
    for item in REPLACEMENTS:
        start, end, segment = scoped_segment(text, item)
        count = segment.count(item["old"])
        if count:
            segment = segment.replace(item["old"], item["new"])
            text = text[:start] + segment + text[end:]
        elif item["new"] not in segment:
            raise RuntimeError(f"neither old nor new text found: {item['label']}")
        counts[item["label"]] = count
    HTML.write_text(text, encoding="utf-8")
    verify_reader()
    return counts


def verify_reader() -> None:
    text = HTML.read_text(encoding="utf-8")
    missing = []
    residuals = []
    for item in REPLACEMENTS:
        _start, _end, segment = scoped_segment(text, item)
        if item["new"] not in segment:
            missing.append(item["label"])
        if item["old"] in segment and item["old"] != item["new"]:
            residuals.append(item["label"])
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
    payload = {
        "time": now,
        "scope": "第二十五卷电力工业；第四十七卷劳动",
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": [{**item, "count": counts[item["label"]]} for item in REPLACEMENTS],
        "skipped": SKIPPED,
        "principle": "仅修复页级 OCR 可直接证明的残留短错识，不按单词全书批量替换。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    source_lines = [f"- `{item['source']}`：{item['old']} -> {item['new']}" for item in REPLACEMENTS]
    lines = [
        "# 跨卷残留短错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 源文与修复：",
        *source_lines,
        f"- 保留：{SKIPPED[0]}",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-04 跨卷残留短错识回源修复

- 对第二十五卷电力工业、第四十七卷劳动做残留短错识回源修复。
- 源文依据：`workbench/ocr/paddle_ocr/中/part01/page_0338.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0274.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0275.txt`。
- 修复 `人身事故隐惠`→`人身事故隐患`、`要善处理`→`妥善处理`、`事故隐惠/较大隐惠`→`事故隐患/较大隐患`、`列人各单位的目标管理范围`→`列入各单位的目标管理范围`。
- 未对全书 `纳人/迁人/人库/速捕` 做词级批量替换，继续逐条回源。
- 报告：`output/reports/reader_readability_residual_short_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 跨卷残留短错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

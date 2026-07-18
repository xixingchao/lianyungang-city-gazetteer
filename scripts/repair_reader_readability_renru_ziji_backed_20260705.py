# -*- coding: utf-8 -*-
"""Source-backed 人/入 and 自/己 reader repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
    ROOT / "workbench" / "body_chapters" / "paddle_上" / "第十卷至第十六卷（part03）.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_PaddleOCR正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_renru_ziji_backed_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_renru_ziji_backed_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_人入自己小批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "中正场莞渎场并入",
        "old": "以莞渎场并人",
        "new": "以莞渎场并入",
        "evidence": [
            "workbench/ocr/raw/上/part03/page_0134.txt:87",
            "workbench/ocr/paddle_ocr/上/part03/page_0134.txt:87",
        ],
    },
    {
        "label": "陈港盐坨自己设计自己制造",
        "old": "自已设计、自已制造",
        "new": "自己设计、自己制造",
        "evidence": ["workbench/ocr/paddle_ocr/上/part03/page_0156.txt:23"],
    },
    {
        "label": "陈港盐坨自己设计自己制造换行残留",
        "old": "自已设计、自已\n制造",
        "new": "自己设计、自己\n制造",
        "evidence": ["workbench/ocr/paddle_ocr/上/part03/page_0156.txt:23"],
    },
    {
        "label": "陈港盐坨自己制造趸船皮带机",
        "old": "自己设计、自已制造",
        "new": "自己设计、自己制造",
        "evidence": ["workbench/ocr/paddle_ocr/上/part03/page_0156.txt:23"],
    },
    {
        "label": "塑料门窗列入中高档名录",
        "old": "被列人中、高档名录",
        "new": "被列入中、高档名录",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0292.txt:24"],
    },
    {
        "label": "打预制桩进入深度",
        "old": "进人深度可达20米",
        "new": "进入深度可达20米",
        "evidence": ["workbench/ocr/paddle_ocr/中/part01/page_0314.txt:30"],
    },
    {
        "label": "电机并入连云港变压器厂",
        "old": "电机并人连云港变压器厂",
        "new": "电机并入连云港变压器厂",
        "evidence": ["workbench/ocr/raw/中/part01/page_0220.txt:24"],
    },
    {
        "label": "东山电厂并入35千伏电网",
        "old": "运后即并人地区35千伏电网",
        "new": "运后即并入地区35千伏电网",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0343.txt:15",
            "workbench/ocr/paddle_ocr/中/part01/page_0343.txt:14",
        ],
    },
    {
        "label": "电子产品列入省计划",
        "old": "该产品列人省计划经济委员会",
        "new": "该产品列入省计划经济委员会",
        "evidence": [
            "workbench/ocr/raw/上/part03/page_0208.txt:54",
            "workbench/ocr/paddle_ocr/上/part03/page_0208.txt:55",
        ],
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        changed = sum(item["count"] for item in items)
        targets.append({"target": str(path), "changed": changed, "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(target["changed"] for target in targets)
    payload = {
        "time": now,
        "scope": "人/入、自/己小批回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "仅修 raw/PaddleOCR 有明确反向证据的短语；OCR 自身仍读错的 深人基层、列人工商业 等暂缓。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人入自己小批回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：仅修 raw/PaddleOCR 有明确反向证据的 `人/入`、`自/己` 短语；OCR 自身仍读错的项目暂缓。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for target in targets:
        for item in target["items"]:
            if item["count"]:
                evidence = "；".join(f"`{source}`" for source in item["evidence"])
                lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`；{target['target']} 命中 {item['count']} 处；证据：{evidence}。")
    lines += [
        "",
        "## 暂缓",
        "- `深人基层`、`把渔业列人工商业` 等项目在 raw/PaddleOCR 中仍显示旧形，本批不凭语感修复。",
        "",
    ]
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-05 人入自己小批回源修复"
    memory = f"""
{marker}
- 依据 raw/PaddleOCR 明确证据，修复 `以莞渎场并人`、`自已设计/自已制造`、`被列人中、高档名录`、`进人深度可达20米`、`电机并人连云港变压器厂`、`运后即并人地区35千伏电网`、`该产品列人省计划经济委员会` 等短语，共 {total} 处。
- 同步目标包括最终阅读版、全书/上册正文汇总、相关分卷正文稿；OCR 原始证据文件不改。
- `深人基层`、`把渔业列人工商业` 等 OCR 自身仍读错的项目暂缓，继续等待更强证据，不做语感替换。
- 报告：`output/reports/reader_readability_renru_ziji_backed_20260705.md`。
"""
    append_once(MEMORY, marker, memory)


if __name__ == "__main__":
    main()

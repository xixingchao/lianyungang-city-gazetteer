# -*- coding: utf-8 -*-
"""Repair a seventh small source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch6_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch6_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第七批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("机关绿化骨干树种", "合欢为骨于树种", "合欢为骨干树种", "workbench/ocr/raw/上/part02/page_0085.txt:7; merged:上_part02:6832"),
    ("沭南排涝骨干", "排涝骨于", "排涝骨干", "workbench/ocr/raw/上/part02/page_0295.txt:20; merged:上_part02:21367"),
    ("纪念币流入境内", "从外地流人境内", "从外地流入境内", "workbench/ocr/paddle_ocr/中/part02/page_0352.txt:36"),
    ("国民党党团骨干分子", "国民党党团骨于分子", "国民党党团骨干分子", "workbench/ocr/paddle_ocr/下/part01/page_0051.txt:62"),
    ("难民救济转入生产", "使其转人生产", "使其转入生产", "workbench/ocr/paddle_ocr/下/part01/page_0051.txt:63"),
    ("外国籍船员入境签证", "办理人境签证、出境签证", "办理入境签证、出境签证", "workbench/ocr/paddle_ocr/下/part01/page_0080.txt:20"),
    ("涉外事件非法入境", "非法人境3起", "非法入境3起", "workbench/ocr/paddle_ocr/下/part01/page_0081.txt:4"),
    ("涉外事件打架斗殴", "打架斗殿5起", "打架斗殴5起", "workbench/ocr/paddle_ocr/下/part01/page_0081.txt:4"),
    ("职工文艺骨干", "培训文艺骨于113人", "培训文艺骨干113人", "workbench/ocr/paddle_ocr/下/part01/page_0318.txt:36"),
    ("小学文艺骨干", "输送文艺骨于50多人", "输送文艺骨干50多人", "workbench/ocr/paddle_ocr/下/part01/page_0357.txt:9"),
    ("教学方法流入境内", "教学方法流人境内", "教学方法流入境内", "workbench/ocr/paddle_ocr/下/part01/page_0368.txt:84"),
    ("注入式教学方法", "注人式教学方法", "注入式教学方法", "workbench/ocr/paddle_ocr/下/part01/page_0368.txt:86"),
    ("天主教日军侵入境内", "日军侵人境内", "日军侵入境内", "workbench/ocr/paddle_ocr/下/part02/page_0266.txt:16"),
]

SKIPPED = [
    "`调整领导骨于`：raw/merged/PaddleOCR 仍未形成可靠异源证据，本批暂缓。",
    "口岸卫生检疫若干 `人境`：同页源仍有分歧，暂不做机械替换。",
    "`传人境内` 等宗教/医学上下文：可能为 `传入`，但本批未逐页核证，暂缓。",
]


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


def main() -> None:
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for label, old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            items.append({"label": label, "old": old, "new": new, "source": source, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(item["changed"] for item in targets)
    payload = {
        "time": now,
        "scope": "第七批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "只修复可由 PaddleOCR 或 raw/merged 异源文本支撑的长上下文问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第七批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修 PaddleOCR 或 raw/merged 异源文本明确支撑的长上下文问题。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项"])
    for label, old, new, source in REPLACEMENTS:
        lines.append(f"- {label}: `{old}` -> `{new}`；源：`{source}`")
    lines.extend(["", "## 暂缓"])
    for item in SKIPPED:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-04 第七批正文残留回源修复

- 对最终阅读版和正文汇总补做 13 项回源修复，本次替换 {total} 处。
- 修复范围包括机关绿化、水利排涝、钱币、民政救济、治安涉外事件、职工/小学文艺、初等教育教学方法、宗教章节中的 `骨于/人境/流人/注人/侵人/斗殿` 残留。
- 依据：`output/reports/reader_readability_source_backed_batch6_20260704.md`。
- 暂缓：`调整领导骨于`、口岸卫生检疫若干 `人境`、宗教/医学 `传人境内`，继续逐页核证。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第七批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

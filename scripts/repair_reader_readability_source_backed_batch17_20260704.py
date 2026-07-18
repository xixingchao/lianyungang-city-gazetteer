# -*- coding: utf-8 -*-
"""Repair an eighteenth small source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch17_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch17_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第十八批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "党外人士后备干部",
        "145名党外人士后备于部名单",
        "145名党外人士后备干部名单",
        "workbench/ocr/paddle_ocr/下/part01/page_0197.txt:13",
    ),
    (
        "进入县处级",
        "1人进人县处级领导班子",
        "1人进入县处级领导班子",
        "workbench/ocr/paddle_ocr/下/part01/page_0197.txt:14",
    ),
    (
        "军队转业干部301人",
        "军队转业于部301人",
        "军队转业干部301人",
        "workbench/ocr/paddle_ocr/下/part01/page_0198.txt:41",
    ),
    (
        "军管干部调派",
        "调来的于部有重点地派到各镇工作",
        "调来的干部有重点地派到各镇工作",
        "workbench/ocr/paddle_ocr/下/part01/page_0199.txt:32",
    ),
    (
        "调配原则",
        "对于部调配原则及其手续作了规定",
        "对干部调配原则及其手续作了规定",
        "workbench/ocr/paddle_ocr/下/part01/page_0199.txt:43",
    ),
    (
        "路北东海干部南下",
        "率部分于部南下支前",
        "率部分干部南下支前",
        "workbench/ocr/paddle_ocr/下/part01/page_0200.txt:28",
    ),
    (
        "1960调进干部",
        "1960～1966年5月调进于部179人",
        "1960～1966年5月调进干部179人",
        "workbench/ocr/paddle_ocr/下/part01/page_0200.txt:32",
    ),
    (
        "下放干部抽调",
        "从全省下放千部中抽调100名于部到连云港工作",
        "从全省下放干部中抽调100名干部到连云港工作",
        "workbench/ocr/paddle_ocr/下/part01/page_0200.txt:34",
    ),
    (
        "专业技术干部占比",
        "其中专业技术于部占一半以上",
        "其中专业技术干部占一半以上",
        "workbench/ocr/paddle_ocr/下/part01/page_0200.txt:38",
    ),
    (
        "分居两地干部",
        "解决夫妻分居两地于部77人",
        "解决夫妻分居两地干部77人",
        "workbench/ocr/paddle_ocr/下/part01/page_0200.txt:40",
    ),
    (
        "调出干部1400人",
        "调出于部1400人",
        "调出干部1400人",
        "workbench/ocr/paddle_ocr/下/part01/page_0201.txt:7",
    ),
    (
        "科技干部考核晋升",
        "市科技于部考核晋升技术职称领导小组",
        "市科技干部考核晋升技术职称领导小组",
        "workbench/ocr/paddle_ocr/下/part01/page_0201.txt:30",
    ),
    (
        "工程技术干部职称",
        "成立了工程技术于部职称评定委员会",
        "成立了工程技术干部职称评定委员会",
        "workbench/ocr/paddle_ocr/下/part01/page_0201.txt:33",
    ),
]

SKIPPED = [
    "仍不处理其它卷/其它章节中未读源页的 `于部/千部/人学/人园` 残留。",
    "检察信访 `于部违法乱纪75件` 源 OCR 自身未证明，继续暂缓。",
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
        "scope": "第十八批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "只修复页级 PaddleOCR 明确支撑的长上下文问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第十八批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修页级 PaddleOCR 明确支撑的长上下文问题。",
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
## 2026-07-04 第十八批正文残留回源修复

- 对最终阅读版和正文汇总补做 {len(REPLACEMENTS)} 项下册人事页级 PaddleOCR 支撑修复，共替换 {total} 处。
- 修复范围包括干部使用、军队转业干部、市内调配、易地调动、技术职称评定中的 `于部/千部/进人/提拨` 残留。
- 依据：`output/reports/reader_readability_source_backed_batch17_20260704.md`。
- 暂缓：未读源页或源 OCR 自身未证明的其它残留。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第十八批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

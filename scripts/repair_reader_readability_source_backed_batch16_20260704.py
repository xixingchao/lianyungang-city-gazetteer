# -*- coding: utf-8 -*-
"""Repair a seventeenth small source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch16_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch16_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第十七批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "科技干部进修学院",
        "科技于部进修学院",
        "科技干部进修学院",
        "workbench/ocr/paddle_ocr/下/part01/page_0423.txt:36",
    ),
    (
        "文化干部培训班",
        "文化于部培训班",
        "文化干部培训班",
        "workbench/ocr/paddle_ocr/下/part02/page_0052.txt:5",
    ),
    (
        "干部中专校表项",
        "千部中专校技术学校",
        "干部中专校技术学校",
        "workbench/ocr/paddle_ocr/下/part01/page_0398.txt:51",
    ),
    (
        "经济管理干部中专学校",
        "管理于部中专学校",
        "管理干部中专学校",
        "workbench/ocr/paddle_ocr/下/part01/page_0399.txt:16",
    ),
    (
        "附录领导干部",
        "社内的领导于部，大社必须分工分业",
        "社内的领导干部，大社必须分工分业",
        "workbench/ocr/paddle_ocr/下/part02/page_0415.txt:38",
    ),
    (
        "附录专业干部专职",
        "三十名专业于部专职从事这项工作",
        "三十名专业干部专职从事这项工作",
        "workbench/ocr/paddle_ocr/下/part02/page_0424.txt:25",
    ),
]

SKIPPED = [
    "教育、托幼段 `人园/人学率` 在页级 OCR 中也多处误识，暂缓到有更强证据或专门批次。",
    "检察信访 `于部违法乱纪75件` 页级 OCR 自身仍未证明，继续暂缓。",
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
        "scope": "第十七批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "只修复页级 PaddleOCR 明确支撑的长上下文问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第十七批正文残留回源修复",
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
## 2026-07-04 第十七批正文残留回源修复

- 对最终阅读版和正文汇总补做 {len(REPLACEMENTS)} 项下册页级 PaddleOCR 支撑修复，共替换 {total} 处。
- 修复范围包括教育成人教育表、科技培训、文化馆辅导、附录开放方案/重要文献中的 `于部/千部` 残留。
- 依据：`output/reports/reader_readability_source_backed_batch16_20260704.md`。
- 暂缓：页级 OCR 自身也误识的 `人园/人学率`、检察信访 `于部违法乱纪75件`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第十七批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

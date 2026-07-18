# -*- coding: utf-8 -*-
"""Repair a sixteenth small source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch15_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch15_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第十六批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "政法干部管理科",
        "政法千部管理科",
        "政法干部管理科",
        "workbench/ocr/paddle_ocr/下/part01/page_0193.txt:27",
    ),
    (
        "六十年代干部科",
        "60年代设组织科和千部科",
        "60年代设组织科和干部科",
        "workbench/ocr/paddle_ocr/下/part01/page_0193.txt:28",
    ),
    (
        "干部一科",
        "千部一科、干部二科",
        "干部一科、干部二科",
        "workbench/ocr/paddle_ocr/下/part01/page_0193.txt:34",
    ),
    (
        "专业技术干部",
        "各类专业技术于部",
        "各类专业技术干部",
        "workbench/ocr/paddle_ocr/下/part01/page_0195.txt:12",
    ),
    (
        "干部缺额",
        "于部缺额达288人",
        "干部缺额达288人",
        "workbench/ocr/paddle_ocr/下/part01/page_0196.txt:21",
    ),
    (
        "人事科提拔干部",
        "市人事科提拨于部243人",
        "市人事科提拔干部243人",
        "workbench/ocr/paddle_ocr/下/part01/page_0196.txt:23",
    ),
    (
        "调解干部走上街头",
        "调解于部走上街头宣传法律",
        "调解干部走上街头宣传法律",
        "workbench/ocr/paddle_ocr/下/part01/page_0149.txt:24",
    ),
]

SKIPPED = [
    "`于部违法乱纪75件` 在页级 OCR 中仍识作 `于部`，虽同段后文有 `干部违法乱纪31件`，仍暂缓。",
    "`科技于部进修学院`、附录 `领导于部/专业于部` 尚未定位到页级强证据。",
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
        "scope": "第十六批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "只修复页级 PaddleOCR 明确支撑的长上下文问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第十六批正文残留回源修复",
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
## 2026-07-04 第十六批正文残留回源修复

- 对最终阅读版和正文汇总补做 {len(REPLACEMENTS)} 项下册页级 PaddleOCR 支撑修复，共替换 {total} 处。
- 修复范围包括人事干部管理/使用段和司法法制宣传段中的 `千部/于部/提拨` 残留。
- 依据：`output/reports/reader_readability_source_backed_batch15_20260704.md`。
- 暂缓：源 OCR 未独立证明的信访 `于部违法乱纪75件`，以及科技、附录等仍需继续定位的残留。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第十六批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

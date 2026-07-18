# -*- coding: utf-8 -*-
"""Repair a thirteenth small source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch12_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch12_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第十三批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "党政机关干部经商办企业",
        "党政机关于部经商办企业",
        "党政机关干部经商办企业",
        "workbench/ocr/paddle_ocr/上/part02/page_0194.txt:22",
    ),
    (
        "佛教路线逐步向东延伸",
        "一日海上丝绸之路，二\n日西域通往内地的陆地丝绸之路逐遂步问东延伸所至",
        "一曰海上丝绸之路，二\n曰西域通往内地的陆地丝绸之路逐步向东延伸所至",
        "workbench/ocr/paddle_ocr/下/part02/page_0102.txt:16-17",
    ),
    (
        "工商管理干部",
        "工商管理于部",
        "工商管理干部",
        "workbench/ocr/paddle_ocr/中/part02/page_0332.txt:36",
    ),
    (
        "工商业界人士",
        "工商业界有代表性的人土",
        "工商业界有代表性的人士",
        "workbench/ocr/paddle_ocr/中/part02/page_0332.txt:36",
    ),
    (
        "登记入簿",
        "登记人簿",
        "登记入簿",
        "workbench/ocr/paddle_ocr/中/part02/page_0332.txt:37",
    ),
    (
        "停机加封引号",
        "采用停机加封、启机揭封”的办法",
        "采用“停机加封、启机揭封”的办法",
        "workbench/ocr/paddle_ocr/中/part02/page_0332.txt:39",
    ),
]

SKIPPED = [
    "`市级机关千部2117人` 尚未定位到页级 OCR 强证据，本批暂缓。",
    "其它 `方吨/项自/加人/于部/千部` 残留继续逐页核证，不做全局替换。",
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
        "scope": "第十三批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "只修复页级 PaddleOCR 明确支撑的长上下文问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第十三批正文残留回源修复",
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
## 2026-07-04 第十三批正文残留回源修复

- 对最终阅读版和正文汇总补做 {len(REPLACEMENTS)} 项页级 PaddleOCR 支撑修复，共替换 {total} 处。
- 修复范围包括工商管理/税务复议会、佛教艺术传入路线中的 `于部/人土/人簿/逐遂步问` 等残留。
- 依据：`output/reports/reader_readability_source_backed_batch12_20260704.md`。
- 暂缓：`市级机关千部2117人` 和其它未取得强证据项。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第十三批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

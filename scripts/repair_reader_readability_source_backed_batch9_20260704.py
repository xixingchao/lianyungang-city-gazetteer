# -*- coding: utf-8 -*-
"""Repair a tenth small source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch9_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch9_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第十批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "云台山茶树逐步增加",
        "该场遂步增加茶树种植面积",
        "该场逐步增加茶树种植面积",
        "workbench/ocr/paddle_ocr/中/part01/page_0112.txt:10",
    ),
    (
        "中药饮片逐步机械化",
        "中药加工炮制生产由原来的手\n工操作遂步被机械设备所代替",
        "中药加工炮制生产由原来的手\n工操作逐步被机械设备所代替",
        "workbench/ocr/paddle_ocr/中/part01/page_0122.txt:20-21",
    ),
    (
        "中药饮片逐步机械化HTML",
        "中药加工炮制生产由原来的手工操作遂步被机械设备所代替",
        "中药加工炮制生产由原来的手工操作逐步被机械设备所代替",
        "workbench/ocr/paddle_ocr/中/part01/page_0122.txt:20-21",
    ),
    (
        "开发区供热逐步实行",
        "远期可遂步实行工业与民用分两片相对集中供热",
        "远期可逐步实行工业与民用分两片相对集中供热",
        "workbench/ocr/paddle_ocr/中/part01/page_0425.txt:21",
    ),
    (
        "开发区土地逐步转向",
        "土地有偿使用开始遂步转向土地使用权有偿出让、转让和土地包片开发",
        "土地有偿使用开始逐步转向土地使用权有偿出让、转让和土地包片开发",
        "workbench/ocr/paddle_ocr/中/part01/page_0427.txt:6",
    ),
    (
        "港口装卸机械逐步增多",
        "随着港口装卸机械的遂步增多",
        "随着港口装卸机械的逐步增多",
        "workbench/ocr/paddle_ocr/中/part01/page_0465.txt:28",
    ),
    (
        "城市人民生活经济逐步恢复",
        "经济遂步恢复。在生产发展的基础上",
        "经济逐步恢复。在生产发展的基础上",
        "workbench/ocr/paddle_ocr/上/part02/page_0149.txt:32",
    ),
    (
        "粮油调运近现代逐步发展",
        "近现代遂步发展为汽车、火车、轮船运载",
        "近现代逐步发展为汽车、火车、轮船运载",
        "workbench/ocr/paddle_ocr/中/part02/page_0245.txt:20",
    ),
    (
        "企业改革逐步完善配套",
        "遂步完善、配套措施",
        "逐步完善、配套措施",
        "workbench/ocr/paddle_ocr/中/part02/page_0495.txt:12",
    ),
]

SKIPPED = [
    "未做 `遂步` 全局替换；只处理页级 PaddleOCR 已明确为 `逐步` 的长上下文。",
    "其它 `于部/骨于/项自/方吨/传人` 残留继续逐页核证。",
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
        "scope": "第十批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "只修复页级 PaddleOCR 明确支撑的长上下文问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第十批正文残留回源修复",
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
## 2026-07-04 第十批正文残留回源修复

- 对最终阅读版和正文汇总补做 {len(REPLACEMENTS)} 项页级 PaddleOCR 支撑修复，共替换 {total} 处。
- 修复范围包括制茶、中药饮片、开发区供热和土地出让、港口装卸、城市人民生活、粮油调运、企业改革中的 `遂步` 残留。
- 依据：`output/reports/reader_readability_source_backed_batch9_20260704.md`。
- 暂缓：其它 `于部/骨于/项自/方吨/传人` 等未取得强证据项。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第十批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

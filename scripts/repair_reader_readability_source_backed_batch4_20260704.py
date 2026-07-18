# -*- coding: utf-8 -*-
"""Repair a fifth small PaddleOCR-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch4_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch4_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第五批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("电工电器进入80年代", "进人80年代，电工电器及电工材料行业", "进入80年代，电工电器及电工材料行业", "workbench/ocr/paddle_ocr/中/part01/page_0219.txt:7"),
    ("变压器厂进入恢复发展", "连云港变压器厂进人恢复、发展时期", "连云港变压器厂进入恢复、发展时期", "workbench/ocr/paddle_ocr/中/part01/page_0219.txt:26"),
    ("变压器产能千伏安", "12.5万于伏安", "12.5万千伏安", "workbench/ocr/paddle_ocr/中/part01/page_0219.txt:26"),
    ("水晶厂进入发展时期", "东海县水晶厂进人发展时期", "东海县水晶厂进入发展时期", "workbench/ocr/paddle_ocr/中/part01/page_0259.txt:29"),
    ("制瓦业进入新发展期", "全市制瓦业进人新的发展期", "全市制瓦业进入新的发展期", "workbench/ocr/paddle_ocr/中/part01/page_0274.txt:18"),
    ("制瓦厂创建厂历史最高", "创建广历史最高水平", "创建厂历史最高水平", "workbench/ocr/paddle_ocr/中/part01/page_0274.txt:20"),
    ("电报业务进入稳步发展", "电报业务进人稳步发展时期", "电报业务进入稳步发展时期", "workbench/ocr/paddle_ocr/中/part02/page_0080.txt:15"),
    ("连云港市进入自动转报网", "连云港市进人全国自动转报网", "连云港市进入全国自动转报网", "workbench/ocr/paddle_ocr/中/part02/page_0080.txt:24"),
    ("食糖进入市场", "外用糖进人市场", "外用糖进入市场", "workbench/ocr/paddle_ocr/中/part02/page_0144.txt:9"),
    ("砂糖输入", "输人砂糖24537吨", "输入砂糖24537吨", "workbench/ocr/paddle_ocr/中/part02/page_0144.txt:12"),
    ("葛藤粉进入市场", "很少进人市场", "很少进入市场", "workbench/ocr/paddle_ocr/中/part02/page_0174.txt:9"),
]

SKIPPED = [
    "其它 `进人80年代`：分布在水产、电力、教育、电子等章，本批未逐页核完，暂缓。",
    "`米栖糖/米牺糖`：PaddleOCR 与 reader 不一致但不能确认正字，暂缓。",
    "口岸、治安司法 `出人境/人境`：继续按页核证，不做机械替换。",
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
    payload = {"time": now, "scope": "第五批正文可读性残留回源修复", "targets": targets, "total_replacements": total, "verified_items": len(REPLACEMENTS), "skipped": SKIPPED, "principle": "仅修复 PaddleOCR 明确支撑的长上下文问题。"}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = ["# 第五批正文残留回源修复", "", f"- 时间：{now}", "- 原则：只修 PaddleOCR 明确支撑的长上下文问题。", f"- 核验项：{len(REPLACEMENTS)} 项。", f"- 本次替换：{total} 处。", "", "## 文件"]
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
## 2026-07-04 第五批正文残留回源修复

- 对最终阅读版和正文汇总补做 11 项 PaddleOCR 回源修复，本次替换 {total} 处。
- 修复项覆盖电工电器、变压器、水晶、制瓦、邮电、食糖、供销葛藤粉等段落的 `进人/输人/于伏安/创建广` 残留。
- 依据：`output/reports/reader_readability_source_backed_batch4_20260704.md`。
- 暂缓：其它 `进人80年代`、`米栖糖/米牺糖`、口岸/治安司法 `出人境/人境`，继续逐页核证。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第五批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

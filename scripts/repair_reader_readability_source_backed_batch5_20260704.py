# -*- coding: utf-8 -*-
"""Repair a sixth small PaddleOCR-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch5_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch5_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第六批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("口岸查验出入", "查验出人连云港口岸", "查验出入连云港口岸", "workbench/ocr/paddle_ocr/中/part01/page_0505.txt:21"),
    ("口岸入境后医学观察", "在人境后继续对船员进行医学观察", "在入境后继续对船员进行医学观察", "workbench/ocr/paddle_ocr/中/part01/page_0507.txt:8"),
    ("口岸船员出入境检查标题", "船员出人境检查", "船员出入境检查", "workbench/ocr/paddle_ocr/中/part01/page_0509.txt:20"),
    ("口岸出入境名单查验", "船舶出人境时只收名单", "船舶出入境时只收名单", "workbench/ocr/paddle_ocr/中/part01/page_0510.txt:25"),
    ("口岸旅客入境手续", "旅客人境手续", "旅客入境手续", "workbench/ocr/paddle_ocr/中/part01/page_0510.txt:33"),
    ("治安出入境管理标题", "三、出人境管理", "三、出入境管理", "workbench/ocr/paddle_ocr/下/part01/page_0080.txt:5"),
    ("治安入出境签证", "人出境签证5件", "入出境签证5件", "workbench/ocr/paddle_ocr/下/part01/page_0080.txt:8"),
    ("治安入出境通行证", "中国公民人出境通行证签证5人次", "中国公民入出境通行证签证5人次", "workbench/ocr/paddle_ocr/下/part01/page_0080.txt:13"),
    ("治安外国人出入境证件", "外国人出人境证件签证101人次", "外国人出入境证件签证101人次", "workbench/ocr/paddle_ocr/下/part01/page_0080.txt:15"),
    ("劳动优秀骨干", "少数优秀骨于可升2级", "少数优秀骨干可升2级", "workbench/ocr/paddle_ocr/下/part01/page_0269.txt:13"),
    ("文化京剧团骨干", "留20名骨于调吕剧团成立京剧队", "留20名骨干调吕剧团成立京剧队", "workbench/ocr/paddle_ocr/下/part02/page_0036.txt:25"),
]

SKIPPED = [
    "口岸 `入境船舶356艘次`：PaddleOCR 该行仍为 `人境`，本批暂缓。",
    "口岸 `入出境的外籍船舶，人境时...必要时人证对照`：同页 PaddleOCR 未完全纠正，暂缓。",
    "`排涝骨于`：仅 raw/merged 支持 `骨干`，仍未取得清晰 PaddleOCR 文本定位，暂缓。",
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
    payload = {"time": now, "scope": "第六批正文可读性残留回源修复", "targets": targets, "total_replacements": total, "verified_items": len(REPLACEMENTS), "skipped": SKIPPED, "principle": "仅修复 PaddleOCR 明确支撑的长上下文问题。"}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = ["# 第六批正文残留回源修复", "", f"- 时间：{now}", "- 原则：只修 PaddleOCR 明确支撑的长上下文问题。", f"- 核验项：{len(REPLACEMENTS)} 项。", f"- 本次替换：{total} 处。", "", "## 文件"]
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
## 2026-07-04 第六批正文残留回源修复

- 对最终阅读版和正文汇总补做 11 项 PaddleOCR 回源修复，本次替换 {total} 处。
- 修复项覆盖口岸卫生检疫/边防检查、治安司法出入境管理、劳动调资和文化京剧团段落的 `出人/人境/骨于` 残留。
- 依据：`output/reports/reader_readability_source_backed_batch5_20260704.md`。
- 暂缓：PaddleOCR 仍未清晰纠正的口岸 `入境船舶356艘次`、外籍船舶入境细句，以及 `排涝骨于`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第六批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

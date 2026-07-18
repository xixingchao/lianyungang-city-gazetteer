# -*- coding: utf-8 -*-
"""Repair a small PaddleOCR-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch2_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch2_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第三批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "商业改造加入公私合营",
        "加人公私合营新浦五金车料零售商店",
        "加入公私合营新浦五金车料零售商店",
        "workbench/ocr/paddle_ocr/中/part02/page_0138.txt:11",
    ),
    (
        "粮食收购一步入库",
        "一步人库，粮食检验吸收群众参加",
        "一步入库，粮食检验吸收群众参加",
        "workbench/ocr/paddle_ocr/中/part02/page_0215.txt:115",
    ),
    (
        "干部理论培训骨干",
        "培训骨于，180多位领导干部",
        "培训骨干，180多位领导干部",
        "workbench/ocr/paddle_ocr/中/part02/page_0442.txt:13",
    ),
    (
        "在职干部理论学习进入80年代",
        "进人20世纪80年代，随着党的工作中心转向以经济建设为主",
        "进入20世纪80年代，随着党的工作中心转向以经济建设为主",
        "workbench/ocr/paddle_ocr/中/part02/page_0443.txt:33",
    ),
    (
        "党员教育进入80年代后",
        "进人20世纪80年代后，党员教育的制度进一步健全",
        "进入20世纪80年代后，党员教育的制度进一步健全",
        "workbench/ocr/paddle_ocr/中/part02/page_0444.txt:41",
    ),
]

SKIPPED = [
    "`涌人新浦`：只见 raw 同形，未取得 PaddleOCR 纠正证据，暂缓。",
    "`深人基层`：PaddleOCR 同样保留 `深人基层`，暂缓。",
    "船舶、电力章节 `进人20世纪80年代`：本轮未完成对应源页回证，暂缓。",
    "`方吨啤酒灌装线`、`食盐积压5方吨`、矿产若干 `方吨`：仍缺强证据，暂缓。",
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
        "scope": "第三批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "仅修复 PaddleOCR 明确支撑的长上下文问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第三批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修 PaddleOCR 明确支撑的长上下文问题。",
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
## 2026-07-04 第三批正文残留回源修复

- 对最终阅读版和正文汇总补做 5 项 PaddleOCR 回源修复，本次替换 {total} 处。
- 修复项：`加人公私合营`、`一步人库`、`培训骨于`、政党章两处 `进人20世纪80年代`。
- 依据：`output/reports/reader_readability_source_backed_batch2_20260704.md`。
- 暂缓：`涌人新浦`、`深人基层`、船舶/电力章节 `进人20世纪80年代`、若干 `方吨` 残留，因本轮缺少足够强的异源证据。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第三批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

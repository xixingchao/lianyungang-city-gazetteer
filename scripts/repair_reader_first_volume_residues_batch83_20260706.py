# -*- coding: utf-8 -*-
"""Repair PaddleOCR-backed first-volume source residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "上" / "总述与大事记.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第一卷_自然环境.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第三卷_区县概况.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_first_volume_residues_batch83_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_first_volume_residues_batch83_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第八十三批_上册残留.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("总述修葺保护", "寺观庙堂、风景名胜进行修茸和保护", "寺观庙堂、风景名胜进行修葺和保护", "workbench/ocr/paddle_ocr/上/part01/page_0040.txt"),
    ("赣榆学宫修葺", "赣榆学宫始建，至崇祯十五年（1642年），共修茸10次。", "赣榆学宫始建，至崇祯十五年（1642年），共修葺10次。", "workbench/ocr/paddle_ocr/上/part01/page_0049.txt"),
    ("自然灾害倾圮", "数次，房屋有倾妃者。", "数次，房屋有倾圮者。", "workbench/ocr/paddle_ocr/上/part01/page_0211.txt"),
    ("海州区增建修葺", "后屡次增建修茸，城区逐步扩大。", "后屡次增建修葺，城区逐步扩大。", "workbench/ocr/paddle_ocr/上/part01/page_0241.txt"),
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        items = []
        for label, old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            items.append({"label": label, "old": old, "new": new, "source": source, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {target}: {residuals[:3]}")
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "PaddleOCR-backed first-volume residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_total": sum(target["changed"] for target in applied),
        "targets": applied,
        "principle": "Only exact context phrases backed by cited PaddleOCR pages are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第八十三批：上册残留",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版、上册源稿、上册正文汇总、全书正文汇总中的少量上册残留。",
        "- 只处理 PaddleOCR 同页明确支撑的 `修葺` 与 `倾圮`。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次实际替换：{payload['changed_total']} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for label, old, new, source in REPLACEMENTS:
        lines.append(f"- {label}: `{old}` -> `{new}`；源：`{source}`")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-06 高置信 OCR 错字补修第八十三批：上册残留

- 依据上册 PaddleOCR 页 `page_0040`、`page_0049`、`page_0211`、`page_0241`，修复主阅读版、上册源稿、上册汇总、全书汇总中的少量上册残留。
- 典型修复：`修茸和保护/共修茸10次/增建修茸` 改为 `修葺和保护/共修葺10次/增建修葺`，`房屋有倾妃者` 改为 `房屋有倾圮者`。
- 本批证据短语 {len(REPLACEMENTS)} 项，实际替换 {payload['changed_total']} 处；报告：`output/reports/reader_first_volume_residues_batch83_20260706.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-06 高置信 OCR 错字补修第八十三批：上册残留", memory)
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_total": payload["changed_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

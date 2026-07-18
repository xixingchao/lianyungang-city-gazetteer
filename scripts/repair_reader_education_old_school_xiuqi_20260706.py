# -*- coding: utf-8 -*-
"""Repair PaddleOCR-backed old-school education section OCR residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_education_old_school_xiuqi_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_education_old_school_xiuqi_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第八十一批_旧学州学.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("州学扩建修葺", "扩建、修茸，成为海州城内的大建筑群。", "扩建、修葺，成为海州城内的大建筑群。", "workbench/ocr/paddle_ocr/下/part01/page_0348.txt"),
    ("州学修葺学宫", "田租作为修茸学宫、诸生会课、贫生丧葬费用。", "田租作为修葺学宫、诸生会课、贫生丧葬费用。", "workbench/ocr/paddle_ocr/下/part01/page_0349.txt"),
    ("康熙六十一", "康照六十一年（1722", "康熙六十一年（1722", "workbench/ocr/paddle_ocr/下/part01/page_0349.txt"),
    ("八顷三十", "存8颅30亩，收入不敷使用。", "存8顷30亩，收入不敷使用。", "workbench/ocr/paddle_ocr/下/part01/page_0349.txt"),
    ("钤海州儒学宫书", "每册铃“海州儒学宫书”。", "每册钤“海州儒学宫书”。", "workbench/ocr/paddle_ocr/下/part01/page_0349.txt"),
    ("八顷三十-汇总收人", "存8颅30亩，收人不敷使用。", "存8顷30亩，收入不敷使用。", "workbench/ocr/paddle_ocr/下/part01/page_0349.txt"),
    ("钤海州儒学宫书-断行", "每册铃“海\n州儒学宫书”。", "每册钤“海\n州儒学宫书”。", "workbench/ocr/paddle_ocr/下/part01/page_0349.txt"),
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
        "scope": "PaddleOCR-backed education old-school section repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_total": sum(target["changed"] for target in applied),
        "targets": applied,
        "principle": "Only exact context phrases backed by PaddleOCR page_0348/page_0349 are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第八十一批：旧学州学",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版、下册 part01 源稿、全书正文汇总中的教育卷旧学州学段。",
        "- 只处理 PaddleOCR 同页明确支撑的形近字残留。",
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
## 2026-07-06 高置信 OCR 错字补修第八十一批：旧学州学

- 依据下册 part01 教育卷 PaddleOCR 页 `page_0348`、`page_0349`，修复主阅读版、下册 part01 源稿、全书正文汇总中的旧学州学段 OCR 残留。
- 典型修复：`扩建、修茸/修茸学宫` 改为 `扩建、修葺/修葺学宫`，`康照六十一/8颅30亩/每册铃` 改为 `康熙六十一/8顷30亩/每册钤`。
- 本批证据短语 {len(REPLACEMENTS)} 项，实际替换 {payload['changed_total']} 处；报告：`output/reports/reader_education_old_school_xiuqi_20260706.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-06 高置信 OCR 错字补修第八十一批：旧学州学", memory)
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_total": payload["changed_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

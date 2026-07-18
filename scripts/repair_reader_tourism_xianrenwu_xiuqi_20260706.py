# -*- coding: utf-8 -*-
"""Repair PaddleOCR-backed tourism section residue around Xianrenwu and xiuqi."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_tourism_xianrenwu_xiuqi_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_tourism_xianrenwu_xiuqi_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第八十批_旅游仙人屋修葺.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("旅游仙人屋陶澍", "据说陶廚来游时，突然", "据说陶澍来游时，突然", "workbench/ocr/paddle_ocr/中/part02/page_0106.txt"),
    ("龙洞庵拨款修葺", "龙洞庵至建国前已破损不堪，后政府拨款修茸，并对外开放", "龙洞庵至建国前已破损不堪，后政府拨款修葺，并对外开放", "workbench/ocr/paddle_ocr/中/part02/page_0112.txt"),
    ("旅游概述修葺保护", "年久失修的寺庙古道、风景名胜进行修茸保护，", "年久失修的寺庙古道、风景名胜进行修葺保护，", "workbench/ocr/paddle_ocr/中/part02/page_0116.txt"),
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
        "scope": "PaddleOCR-backed tourism section repair for Xianrenwu and 修葺 residues",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_total": sum(target["changed"] for target in applied),
        "targets": applied,
        "principle": "Only exact context phrases backed by the cited PaddleOCR pages are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第八十批：旅游仙人屋、修葺",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版、中册 part02 源稿、全书正文汇总中的名胜旅游卷短片段。",
        "- 只处理 PaddleOCR 同页明确支撑的 `陶澍` 与 `修葺` 残留。",
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
## 2026-07-06 高置信 OCR 错字补修第八十批：旅游仙人屋、修葺

- 依据中册 part02 名胜旅游卷 PaddleOCR 页 `page_0106`、`page_0112`、`page_0116`，修复主阅读版、中册 part02 源稿、全书正文汇总中的旅游段残留 OCR 错字。
- 典型修复：仙人屋段 `陶廚来游` 改为 `陶澍来游`；龙洞庵和旅游概述段 `修茸` 改为 `修葺`。
- 本批证据短语 {len(REPLACEMENTS)} 项，实际替换 {payload['changed_total']} 处；报告：`output/reports/reader_tourism_xianrenwu_xiuqi_20260706.md`。
- 边界：总述中的 `修茸和保护` 及其他卷 `修茸` 残留仍需逐页证据，不做全局替换。
"""
    upsert_memory(MEMORY, "## 2026-07-06 高置信 OCR 错字补修第八十批：旅游仙人屋、修葺", memory)
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_total": payload["changed_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

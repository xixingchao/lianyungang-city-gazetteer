# -*- coding: utf-8 -*-
"""Repair narrowly source-backed reader OCR residues, batch 91."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_residues_batch91_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_residues_batch91_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第九十一批_Paddle回源残留.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "爪墩旧石器时代",
        "old": "具有伯石器时代晚期人类加工石器的特点",
        "new": "具有旧石器时代晚期人类加工石器的特点",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0075.txt:29",
    },
    {
        "label": "爪墩楔形石核",
        "old": "石核中的形石核、船底形石核和刮削器中的圆头刮削器",
        "new": "石核中的楔形石核、船底形石核和刮削器中的圆头刮削器",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0075.txt:26",
    },
    {
        "label": "海州西门外耶稣堂传教士源稿断行",
        "old": "国传教土建立的海州西门外耶稣堂",
        "new": "国传教士建立的海州西门外耶稣堂",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0272.txt:26",
    },
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
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {target}: {residuals[:3]}")
        for item in items:
            item["verified"] = verify.count(item["new"])
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "Paddle-backed source sync and reader residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "principle": "Only exact contexts with PaddleOCR support are changed; visually plausible but unsupported strings are left untouched.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第九十一批：Paddle 回源残留",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的可回源错字残留。",
        "- 只处理 PaddleOCR 明确支撑的精确短语。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次运行新增替换：{payload['changed_this_run']} 处",
        f"- 当前核验覆盖：{payload['verified_total']} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}: `{item['old']}` -> `{item['new']}`；源/定位：`{item['source']}`")
    lines.extend([
        "",
        "## 未处理边界",
        "",
        "- `标石英` 在 PaddleOCR 与 raw OCR 中均同读，未改。",
        "- `中西合壁` 多处当前 OCR 同读，除上一批上海大旅社有额外汇总证据外，本批不全局改。",
        "- 医学 `丙酮酸晦/LISR` 与书末序跋硬点继续等待更强证据。",
    ])
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-06 高置信 OCR 错字补修第九十一批：Paddle 回源残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做窄范围回源修复，处理爪墩旧石器地点 `伯石器 -> 旧石器`、`形石核 -> 楔形石核`，并同步源稿断行残留 `国传教土建立 -> 国传教士建立`。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_residues_batch91_20260706.md`。
- 边界：`标石英`、其它 `中西合壁`、医学 `丙酮酸晦/LISR`、书末序跋硬点未改；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

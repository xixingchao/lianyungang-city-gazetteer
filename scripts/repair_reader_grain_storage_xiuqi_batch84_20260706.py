# -*- coding: utf-8 -*-
"""Repair PaddleOCR-backed grain storage warehouse residue."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_grain_storage_xiuqi_batch84_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_grain_storage_xiuqi_batch84_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第八十四批_常平仓修葺.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("常平仓仓廒修葺", "各建仓廠3所，额储谷2.1万石。雍正十年（1732年），海州修盖平仓廠房60间，至乾隆三十年（1765年）历加修茸达15廠71间，额储谷3.5万石。", "各建仓廒3所，额储谷2.1万石。雍正十年（1732年），海州修盖平仓廒房60间，至乾隆三十年（1765年）历加修葺达15廒71间，额储谷3.5万石。", "workbench/ocr/paddle_ocr/中/part02/page_0236.txt"),
    ("常平仓仓廒修葺-断行", "各建仓廠3所，额储谷2.1万石。雍正十年（1732年），海州修盖平仓廠房60间，至乾隆\n三十年（1765年）历加修茸达15廠71间，额储谷3.5万石。", "各建仓廒3所，额储谷2.1万石。雍正十年（1732年），海州修盖平仓廒房60间，至乾隆\n三十年（1765年）历加修葺达15廒71间，额储谷3.5万石。", "workbench/ocr/paddle_ocr/中/part02/page_0236.txt"),
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
        "scope": "PaddleOCR-backed grain storage warehouse repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_total": sum(target["changed"] for target in applied),
        "targets": applied,
        "principle": "Only exact context phrases backed by PaddleOCR page_0236 are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第八十四批：常平仓修葺",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版、中册 part02 源稿、全书正文汇总中的粮油购销常平仓段。",
        "- 只处理 PaddleOCR 同页明确支撑的 `仓廒/修葺/15廒`。",
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
## 2026-07-06 高置信 OCR 错字补修第八十四批：常平仓修葺

- 依据中册 part02 粮油购销卷 PaddleOCR 页 `page_0236`，修复主阅读版、中册 part02 源稿、全书正文汇总中的常平仓段。
- 典型修复：`仓廠/平仓廠房/历加修茸/15廠71间` 改为 `仓廒/平仓廒房/历加修葺/15廒71间`。
- 本批证据短语 {len(REPLACEMENTS)} 项，实际替换 {payload['changed_total']} 处；报告：`output/reports/reader_grain_storage_xiuqi_batch84_20260706.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-06 高置信 OCR 错字补修第八十四批：常平仓修葺", memory)
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_total": payload["changed_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

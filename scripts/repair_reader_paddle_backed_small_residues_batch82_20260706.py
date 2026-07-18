# -*- coding: utf-8 -*-
"""Repair a small PaddleOCR-backed batch across biography, Buddhist, and port sections."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_small_residues_batch82_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_small_residues_batch82_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第八十二批_人物佛教港口.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("刘梦松儒吏", "时有儒更之誉。", "时有儒吏之誉。", "workbench/ocr/paddle_ocr/下/part02/page_0382.txt"),
    ("大慈禅寺倾圮道辕", "后大殿倾妃，正德九年，僧正道重修。", "后大殿倾圮，正德九年，僧正道辕重修。", "workbench/ocr/paddle_ocr/下/part02/page_0261.txt"),
    ("一号码头倾圮", "木栈桥码头被海虫蛀蚀和风浪侵袭而倾妃。", "木栈桥码头被海虫蛀蚀和风浪侵袭而倾圮。", "workbench/ocr/paddle_ocr/中/part01/page_0438.txt"),
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
        "scope": "PaddleOCR-backed small residue batch across biography, Buddhist, and port sections",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_total": sum(target["changed"] for target in applied),
        "targets": applied,
        "principle": "Only exact context phrases backed by cited PaddleOCR pages are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第八十二批：人物、佛教、港口",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版、相关中下册源稿、全书正文汇总中的三个短片段。",
        "- 只处理 PaddleOCR 同页明确支撑的 `儒吏`、`倾圮`、`道辕`。",
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
## 2026-07-06 高置信 OCR 错字补修第八十二批：人物、佛教、港口

- 依据 PaddleOCR 页 `下/part02/page_0382`、`下/part02/page_0261`、`中/part01/page_0438`，修复人物、佛教、港口卷的三个短片段。
- 典型修复：`儒更之誉` 改为 `儒吏之誉`，`大殿倾妃，僧正道重修` 改为 `大殿倾圮，僧正道辕重修`，`木栈桥码头...倾妃` 改为 `倾圮`。
- 本批证据短语 {len(REPLACEMENTS)} 项，实际替换 {payload['changed_total']} 处；报告：`output/reports/reader_paddle_backed_small_residues_batch82_20260706.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-06 高置信 OCR 错字补修第八十二批：人物、佛教、港口", memory)
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_total": payload["changed_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

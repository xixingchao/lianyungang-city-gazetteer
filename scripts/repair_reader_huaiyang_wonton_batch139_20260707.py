# -*- coding: utf-8 -*-
"""Repair Paddle-backed 准阳馄饨 OCR residue."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_huaiyang_wonton_batch139_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_huaiyang_wonton_batch139_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_淮阳馄饨残字回源补修第一百三十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = "准阳馄饨"
NEW = "淮阳馄饨"
PADDLE_TXT = ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0152.txt"
RAW_TXT = ROOT / "workbench" / "ocr" / "raw" / "中" / "part02" / "page_0152.txt"


def plain_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def evidence_lines(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return [line for line in text.splitlines() if any(term in line for term in ["美味斋", OLD, NEW, "淮扬菜"])]


def contexts(text: str, term: str) -> list[str]:
    plain = plain_text(text)
    return [plain[max(0, m.start() - 45):m.start() + 70].replace("\n", " ") for m in re.finditer(term, plain)]


def upsert_memory(marker: str, content: str) -> None:
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_count = plain_text(before).count(OLD)
        after = before.replace(OLD, NEW)
        target.write_text(after, encoding="utf-8")
        results.append({
            "target": str(target),
            "before": before_count,
            "changed": before_count,
            "after": plain_text(after).count(OLD),
            "new_count": plain_text(after).count(NEW),
            "remaining_contexts": contexts(after, OLD),
        })

    changed = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader Paddle-backed 准阳馄饨 residue repair",
        "old": OLD,
        "new": NEW,
        "changed": changed,
        "targets": results,
        "evidence": {
            "paddle_txt": str(PADDLE_TXT),
            "paddle_lines": evidence_lines(PADDLE_TXT),
            "raw_txt": str(RAW_TXT),
            "raw_lines": evidence_lines(RAW_TXT),
        },
        "left_untouched": [
            "不将相邻的 淮扬菜 改成 淮阳菜。",
            "不处理 方人、进人、自已、输人 等其它残留候选。",
            "本批没有打开、展示或嵌入图片。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 淮阳馄饨残字补修第一百三十九批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        f"- 按 Paddle OCR 同页证据，将固定短语 `{OLD}` 修为 `{NEW}`。",
        "",
        "## 证据",
        "",
        f"- Paddle OCR：`{PADDLE_TXT}`",
    ]
    for line in payload["evidence"]["paddle_lines"]:
        lines.append(f"  - {line}")
    lines.append(f"- Raw OCR：`{RAW_TXT}`")
    for line in payload["evidence"]["raw_lines"]:
        lines.append(f"  - {line}")
    lines.extend([
        "- 判定：raw 将 `淮` 误为 `准`；Paddle 同行给出 `淮阳馄饨`，且下一行另有 `淮扬菜`，两者不混改。",
        "",
        "## 统计",
        "",
        f"- 修复：{changed} 处",
        "",
        "## 文件",
        "",
    ])
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处，剩余 `{OLD}` {item['after']} 处")
    lines.extend(["", "## 未处理边界", ""])
    for item in payload["left_untouched"]:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百三十九批：淮阳馄饨残字"
    upsert_memory(marker, f"""
{marker}

- 按 `workbench/ocr/paddle_ocr/中/part02/page_0152.txt` 同页证据，将当前阅读稿固定短语 `{OLD}` 修为 `{NEW}`。
- 本批修复 {changed} 处，覆盖全书 1 处、中册 1 处；报告：`output/reports/reader_huaiyang_wonton_batch139_20260707.md`。
- 保留同页 `淮扬菜` 不混改；未处理 `方人/进人/自已/输人` 等其它候选；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

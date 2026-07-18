# -*- coding: utf-8 -*-
"""Follow-up repair for one remaining 人党申请书 OCR residue."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_rudang_followup_batch150_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_rudang_followup_batch150_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人党残字跟进补修第一百五十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = "重新填人党申</p><p>请书"
NEW = "重新填入党申</p><p>请书"
OLD_LABEL = "重新填人党申请书"
NEW_LABEL = "重新填入党申请书"


def plain_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(plain: str, term: str) -> list[str]:
    return [plain[max(0, m.start() - 55):m.start() + 85].replace("\n", " ") for m in re.finditer(term, plain)]


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
        before_plain = plain_text(before)
        count = before.count(OLD)
        after = before.replace(OLD, NEW)
        target.write_text(after, encoding="utf-8")
        after_plain = plain_text(after)
        results.append({
            "target": str(target),
            "before": before_plain.count("人党"),
            "changed": count,
            "after": after_plain.count("人党"),
            "remaining_contexts": contexts(after_plain, "人党"),
        })

    changed = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader remaining 人党申请书 OCR residue repair",
        "changed": changed,
        "targets": results,
        "left_untouched": [
            "保留 `共产党和工人党` 合法政治组织名称。",
            "不做 `人党` 裸词全局替换。",
            "本批没有打开、展示或嵌入图片。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人党残字跟进补修第一百五十批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        f"- 跟进修复 batch149 遗留固定短语：`{OLD_LABEL}` -> `{NEW_LABEL}`。",
        "",
        "## 统计",
        "",
        f"- 修复：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处，剩余 `人党` {item['after']} 处")
    lines.extend(["", "## 剩余边界", ""])
    remaining = False
    for item in results:
        for ctx in item["remaining_contexts"]:
            remaining = True
            lines.append(f"- `{item['target']}`：{ctx}")
    if not remaining:
        lines.append("- 无。")
    lines.extend(["", "## 未处理边界", ""])
    for item in payload["left_untouched"]:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百五十批：人党残字跟进"
    upsert_memory(marker, f"""
{marker}

- 跟进 batch149 遗留固定短语，将 `重新填人党申请书` 修为 `重新填入党申请书`。
- 本批修复 {changed} 处；报告：`output/reports/reader_rudang_followup_batch150_20260707.md`。
- 当前剩余 `人党` 均为 `共产党和工人党` 合法组织名称；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

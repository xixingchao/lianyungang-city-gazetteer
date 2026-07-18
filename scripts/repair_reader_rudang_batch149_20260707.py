# -*- coding: utf-8 -*-
"""Repair fixed 人党 OCR residues while preserving 工人党."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_rudang_batch149_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_rudang_batch149_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人党残字补修第一百四十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

PROTECT = ["共产党和工人党"]
REPLACEMENTS = [
    {"label": "女青年入党", "old": "女青年人党", "new": "女青年入党"},
    {"label": "入党对象", "old": "培养人党对象", "new": "培养入党对象"},
    {"label": "入党的党员", "old": "后，人党的9000", "new": "后，入党的9000"},
    {"label": "集体入党", "old": "集体人党", "new": "集体入党"},
    {"label": "填入党申请书", "old": "填人党申请书", "new": "填入党申请书"},
    {"label": "填写入党申请书", "old": "填写人党申请书", "new": "填写入党申请书"},
    {"label": "重新入党", "old": "重新人党", "new": "重新入党"},
    {"label": "1939年12月入党", "old": "1939年）12月人党", "new": "1939年）12月入党"},
    {"label": "烈士表表头入党团", "old": "人党团", "new": "入党团"},
    {"label": "烈士表单元入党", "old": ">人党<", "new": ">入党<"},
]
LEFT_UNTOUCHED = [
    "保留 `共产党和工人党` 合法政治组织名称。",
    "不做 `人党` 裸词全局替换。",
    "本批没有打开、展示或嵌入图片。",
]


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


def repair(text: str) -> tuple[str, list[dict[str, int]]]:
    protected = {}
    work = text
    for index, phrase in enumerate(PROTECT):
        token = f"__PROTECT_RUDANG_{index}__"
        protected[token] = phrase
        work = work.replace(phrase, token)

    items = []
    for item in REPLACEMENTS:
        count = work.count(item["old"])
        if count:
            work = work.replace(item["old"], item["new"])
        items.append({**item, "count": count})

    for token, phrase in protected.items():
        work = work.replace(token, phrase)
    return work, items


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain_text(before)
        after, items = repair(before)
        target.write_text(after, encoding="utf-8")
        after_plain = plain_text(after)
        results.append({
            "target": str(target),
            "before": before_plain.count("人党"),
            "changed": sum(item["count"] for item in items),
            "after": after_plain.count("人党"),
            "items": items,
            "protected_counts": {phrase: before_plain.count(phrase) for phrase in PROTECT},
            "remaining_contexts": contexts(after_plain, "人党"),
        })

    changed = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader fixed 人党 OCR residue repair",
        "changed": changed,
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人党残字补修第一百四十九批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 保护合法 `共产党和工人党` 后，定点修复 `人党` 应为 `入党` 的正文和烈士表线性占位残字。",
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
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        total = sum(result_item["count"] for result in results for result_item in result["items"] if result_item["old"] == item["old"])
        if total:
            lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`，{total} 处")
    lines.extend(["", "## 剩余边界", ""])
    remaining = False
    for item in results:
        for ctx in item["remaining_contexts"]:
            remaining = True
            lines.append(f"- `{item['target']}`：{ctx}")
    if not remaining:
        lines.append("- 无。")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百四十九批：人党残字"
    upsert_memory(marker, f"""
{marker}

- 保护 `共产党和工人党` 合法组织名称后，定点修复当前阅读稿中 `人党` 应为 `入党` 的残字。
- 本批修复 {changed} 处，覆盖中册妇女运动、党员教育、国民党申请书语境，以及下册人物传记和烈士表线性占位文本的 `入党/入党团`；报告：`output/reports/reader_rudang_batch149_20260707.md`。
- 未做 `人党` 裸词全局替换；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Repair fixed 加人 OCR residues to 加入 while preserving 参加/增加 crossings."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_jiaru_batch151_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_jiaru_batch151_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_加人残字补修第一百五十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "加入行列", "old": "加人到", "new": "加入到"},
    {"label": "加入公私合营", "old": "加人公私", "new": "加入公私"},
    {"label": "加入粮谷组合", "old": "加人粮谷组合", "new": "加入粮谷组合"},
    {"label": "加入共产党", "old": "加人中国共产党", "new": "加入中国共产党"},
    {"label": "加入国民党", "old": "加人中国国民党", "new": "加入中国国民党"},
    {"label": "加入国民党", "old": "加人国民党", "new": "加入国民党"},
    {"label": "加入所在国国籍", "old": "加人所在", "new": "加入所在"},
    {"label": "加入科技报研究会", "old": "加人中国科技报研究会", "new": "加入中国科技报研究会"},
    {"label": "加入工农红军", "old": "加人中国工农红军", "new": "加入中国工农红军"},
    {"label": "加入抗日队伍", "old": "加人抗日队伍", "new": "加入抗日队伍"},
    {"label": "加入共青团", "old": "加人中国共产主义青年团", "new": "加入中国共产主义青年团"},
    {"label": "加入党跨段", "old": "加人中</p><p>国共产党", "new": "加入中</p><p>国共产党"},
]
LEFT_UNTOUCHED = [
    "保留 `参加人数/参加人员/增加人员/贫困户参加` 等合法跨词命中。",
    "不做 `加人` 裸词全局替换。",
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


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    results = []
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        before_plain = plain_text(before)
        text = before
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        after_plain = plain_text(text)
        results.append({
            "target": str(target),
            "before": before_plain.count("加人"),
            "changed": sum(item["count"] for item in items),
            "after": after_plain.count("加人"),
            "items": items,
            "remaining_contexts": contexts(after_plain, "加人"),
        })

    changed = sum(item["changed"] for item in results)
    payload = {
        "time": now,
        "scope": "current reader fixed 加人 OCR residue repair",
        "changed": changed,
        "targets": results,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 加人残字补修第一百五十一批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 定点修复 `加人` 应为 `加入` 的组织、团体、国籍和行列语境，保留 `参加/增加` 合法跨词。",
        "",
        "## 统计",
        "",
        f"- 修复：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处，剩余 `加人` {item['after']} 处")
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百五十一批：加人残字"
    upsert_memory(marker, f"""
{marker}

- 定点修复当前阅读稿中 `加人` 应为 `加入` 的组织、团体、国籍和行列语境，覆盖 `加入中国共产党/加入国民党/加入粮谷组合/加入到...行列` 等。
- 本批修复 {changed} 处；报告：`output/reports/reader_jiaru_batch151_20260707.md`。
- 保留 `参加人数/参加人员/增加人员/贫困户参加` 等合法跨词；未打开、展示或嵌入图片。
""")
    print(json.dumps({"changed": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

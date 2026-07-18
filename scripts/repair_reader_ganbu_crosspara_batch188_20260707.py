# -*- coding: utf-8 -*-
"""Repair cross-paragraph 干部 OCR residues after batch187."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_ganbu_crosspara_batch188_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ganbu_crosspara_batch188_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_干部跨段残字补修第一百八十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("于部</p><p>缺额", "干部</p><p>缺额"),
    ("对于部调配", "对干部调配"),
    ("中青年于部", "中青年干部"),
    ("县</p><p>处级于部", "县</p><p>处级干部"),
    ("采取于部联</p><p>系", "采取干部联</p><p>系"),
    ("文化</p><p>于部培训班", "文化</p><p>干部培训班"),
    ("市</p><p>于部疗养院", "市</p><p>干部疗养院"),
    ("51</p><p>名于部乘海船", "51</p><p>名干部乘海船"),
    ("于部总数", "干部总数"),
]

SKIPPED_BOUNDARIES = [
    "由于部分",
    "属于部管",
    "便于部队",
    "低于部颁",
    "机电排粮，于部每夜补助",
    "剧自近于部",
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def contexts(text: str, term: str) -> list[str]:
    return [text[max(0, m.start() - 60):m.start() + 110].replace("\n", " ") for m in re.finditer(re.escape(term), text)]


def upsert_memory(total: int, remaining: dict[str, int]) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百八十八批：干部跨段补遗"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    rem = ", ".join(f"{k}:{v}" for k, v in remaining.items())
    block = f"""
{marker}

- 复扫 batch187 后，继续修复跨 `<p>` 标签或表格行残留的 `于部` 干部误识，包括 `干部缺额/对干部调配原则/中青年干部/县处级干部/干部联系/文化干部培训班/市干部疗养院/51名干部乘海船/干部总数`。
- 本批修复 {total} 处；报告：`output/reports/reader_ganbu_crosspara_batch188_20260707.md`。
- 保留 `由于部分/属于部管/便于部队/低于部颁/机电排粮，于部每夜补助/剧自近于部` 等边界；未打开、展示或嵌入图片。
- 修后当前 reader 纯文本 `于部` 剩余：{rem}。
""".strip()
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + block + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + block + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    results = []
    total = 0
    for target in TARGETS:
        before = target.read_text(encoding="utf-8")
        after = before
        per_file = []
        for old, new in REPLACEMENTS:
            count = after.count(old)
            if count:
                after = after.replace(old, new)
                per_file.append({"old": old, "new": new, "changed": count})
                total += count
        target.write_text(after, encoding="utf-8")
        after_plain = plain(after)
        results.append({
            "target": str(target),
            "changed": sum(item["changed"] for item in per_file),
            "after_plain_yubu": after_plain.count("于部"),
            "remaining_contexts": contexts(after_plain, "于部"),
            "replacements": per_file,
        })

    remaining = {Path(item["target"]).name: item["after_plain_yubu"] for item in results}
    payload = {
        "time": now,
        "scope": "current reader cross-paragraph high-confidence 干部 OCR repair",
        "changed": total,
        "targets": results,
        "skipped_boundaries": SKIPPED_BOUNDARIES,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 干部跨段残字补修第一百八十八批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书、中册、下册阅读稿。",
        "- 修复 batch187 后跨标签或表格行残留的 `于部` 干部误识。",
        "- 未做 `于部 -> 干部` 全局替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        "",
        "## 文件",
        "",
    ]
    for item in results:
        lines.append(f"- `{item['target']}`：修复 {item['changed']} 处；剩余 `于部` {item['after_plain_yubu']} 处")
    lines.extend(["", "## 保留边界", ""])
    for term in SKIPPED_BOUNDARIES:
        lines.append(f"- `{term}`")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total, remaining)
    print(json.dumps({"changed": total, "remaining": remaining, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

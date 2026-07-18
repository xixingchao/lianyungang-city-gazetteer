# -*- coding: utf-8 -*-
"""Repair evidence-backed 广->厂 residues in middle reader, batch206."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_factory_guang_batch206_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_factory_guang_batch206_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_厂字残留补修第二百零六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("东辛农场砖瓦广", "东辛农场砖瓦厂"),
    ("灌云龙苴砖广", "灌云龙苴砖厂"),
    ("东海县砖瓦广", "东海县砖瓦厂"),
    ("第二、第三砖瓦广", "第二、第三砖瓦厂"),
    ("煤渣砖广", "煤渣砖厂"),
    ("炉渣砖广更名", "炉渣砖厂更名"),
    ("临洪滩办窑广", "临洪滩办窑厂"),
    ("连云港制瓦广", "连云港制瓦厂"),
    ("创建广历史最高", "创建厂历史最高"),
    ("专业工广，前身", "专业工厂，前身"),
    ("市玻璃纤维广开始", "市玻璃纤维厂开始"),
    ("连云港市耐火材料广已发展", "连云港市耐火材料厂已发展"),
    ("连云港市耐火材料广投资", "连云港市耐火材料厂投资"),
    ("电灯广又改为", "电灯厂又改为"),
    ("电广经常低压", "电厂经常低压"),
    ("日用化工广；建于", "日用化工厂；建于"),
    ("市罐头广从丹麦", "市罐头厂从丹麦"),
    ("市绝缘材料广私设", "市绝缘材料厂私设"),
    ("市锦屏化工广与湖北", "市锦屏化工厂与湖北"),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def count_candidates(text: str, full_text: str) -> int:
    total = 0
    for m in re.finditer("广", text):
        ctx = text[max(0, m.start() - 14): min(len(text), m.end() + 14)]
        good = ctx.replace("广", "厂", 1)
        if full_text.count(good) and not full_text.count(ctx):
            total += 1
    return total


def upsert_memory(total: int, remaining_candidates: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第二百零六批：中册厂字残留"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 对照当前全书 reader 正确文本，修复中册建材、电力、管理等段 `广 -> 厂` 高置信残留 {total} 处。
- 本批仅替换完整短语，不做单字 `广 -> 厂`；报告：`output/reports/reader_factory_guang_batch206_20260707.md`。
- 修后按短上下文扫描，中册仍有 {remaining_candidates} 条 `广 -> 厂` 候选待分批核修；未打开、展示或嵌入图片。
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
    full_text = plain(FULL.read_text(encoding="utf-8"))
    evidence = {new: full_text.count(new) for _old, new in REPLACEMENTS}
    missing = {term: count for term, count in evidence.items() if count < 1}
    if missing:
        raise SystemExit(f"missing full-reader evidence: {missing}")

    html = MIDDLE.read_text(encoding="utf-8")
    changed_items = []
    for old, new in REPLACEMENTS:
        count = html.count(old)
        if count:
            html = html.replace(old, new)
            changed_items.append({"old": old, "new": new, "changed": count})
    MIDDLE.write_text(html, encoding="utf-8")
    after_plain = plain(html)
    total = sum(item["changed"] for item in changed_items)
    remaining_candidates = count_candidates(after_plain, full_text)

    payload = {
        "time": now,
        "changed": total,
        "full_evidence_counts": evidence,
        "replacements": changed_items,
        "middle_remaining_factory_candidates": remaining_candidates,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 厂字残留补修第二百零六批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿。",
        "- 以当前全书 reader 正确句为证据，修复 `广 -> 厂` 的固定短语错识。",
        "- 未做单字替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 修后中册 `广 -> 厂` 短上下文候选剩余：{remaining_candidates} 条",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total, remaining_candidates)
    print(json.dumps({"changed": total, "remaining_candidates": remaining_candidates, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Repair evidence-backed 广->厂 residues in middle reader, batch205."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_factory_guang_batch205_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_factory_guang_batch205_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_厂字残留补修第二百零五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("小氮肥广、小磷肥厂", "小氮肥厂、小磷肥厂"),
    ("云台农场综合广", "云台农场综合厂"),
    ("市化工机械广投资", "市化工机械厂投资"),
    ("市化工广（原新浦农药厂）", "市化工厂（原新浦农药厂）"),
    ("磷肥广相继建立", "磷肥厂相继建立"),
    ("市第二农药广的相继建成", "市第二农药厂的相继建成"),
    ("市红旗化工广应上海外贸", "市红旗化工厂应上海外贸"),
    ("连云港市发酵广", "连云港市发酵厂"),
    ("市红旗化工广引进上海", "市红旗化工厂引进上海"),
    ("市锦屏化工广成功研制", "市锦屏化工厂成功研制"),
    ("铁工广相继开业", "铁工厂相继开业"),
    ("东海县农机修造广", "东海县农机修造厂"),
    ("连云港市农业机械广试制", "连云港市农业机械厂试制"),
    ("连云港市农业机械广。产品", "连云港市农业机械厂。产品"),
    ("畜牧机械3个分广", "畜牧机械3个分厂"),
    ("上海客车厂连云港分广", "上海客车厂连云港分厂"),
    ("连云港分公司修理广3家", "连云港分公司修理厂3家"),
    ("附属电机广分别开始", "附属电机厂分别开始"),
    ("海州电器广开始生产", "海州电器厂开始生产"),
    ("从新海电广划出", "从新海电厂划出"),
    ("锦屏机械广、赣榆县", "锦屏机械厂、赣榆县"),
    ("南京无线电广转让", "南京无线电厂转让"),
    ("北京电视设备广转让", "北京电视设备厂转让"),
    ("迁入新广址生产", "迁入新厂址生产"),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def count_candidates(text: str, full_text: str) -> int:
    total = 0
    for m in re.finditer("广", text):
        ctx = text[max(0, m.start() - 12): min(len(text), m.end() + 12)]
        good = ctx.replace("广", "厂", 1)
        if full_text.count(good) and not full_text.count(ctx):
            total += 1
    return total


def upsert_memory(total: int, remaining_candidates: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第二百零五批：中册厂字残留"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 对照当前全书 reader 正确文本，修复中册化工、机械、电器等段 `广 -> 厂` 高置信残留 {total} 处。
- 本批仅替换完整短语，不做单字 `广 -> 厂`；报告：`output/reports/reader_factory_guang_batch205_20260707.md`。
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
        "# 厂字残留补修第二百零五批",
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

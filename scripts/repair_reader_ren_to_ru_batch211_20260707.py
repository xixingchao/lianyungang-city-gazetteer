# -*- coding: utf-8 -*-
"""Repair evidence-backed lower-reader 人->入 residues, batch211."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
LOWER = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_ren_to_ru_batch211_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ren_to_ru_batch211_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人入残留补修第二百一十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("人出境签证", "入出境签证"),
    ("中国公民人出境通行证", "中国公民入出境通行证"),
    ("因人股集资", "因入股集资"),
    ("入园人托", "入园入托"),
    ("人园幼儿", "入园幼儿"),
    ("人园率", "入园率"),
    ("幼儿人园", "幼儿入园"),
    ("被选人《中国现代小说选》", "被选入《中国现代小说选》"),
    ("被郭沫若选人《中国史稿》", "被郭沫若选入《中国史稿》"),
    ("栽人笔内", "栽入笔内"),
    ("透人疗法", "透入疗法"),
    ("共有人托儿童", "共有入托儿童"),
    ("人托儿童减少", "入托儿童减少"),
    ("人幼儿园或托儿所", "入幼儿园或托儿所"),
    ("日本人唐求法僧", "日本入唐求法僧"),
    ("人东京政法大学", "入东京政法大学"),
    ("被捕人狱", "被捕入狱"),
    ("打人伪军内部", "打入伪军内部"),
    ("逮捕人狱", "逮捕入狱"),
    ("人抗日军政大学", "入抗日军政大学"),
    ("潜人新浦", "潜入新浦"),
    ("打人敌伪内部", "打入敌伪内部"),
    ("符竹庭人抗日军政大学", "符竹庭入抗日军政大学"),
    ("14岁人灌云县立初级中学", "14岁入灌云县立初级中学"),
    ("打人沈小街据点", "打入沈小街据点"),
    ("打人国际市场", "打入国际市场"),
    ("跃人新的发展阶段", "跃入新的发展阶段"),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def count_candidates(text: str, full_text: str) -> int:
    total = 0
    for m in re.finditer("人", text):
        ctx = text[max(0, m.start() - 18): min(len(text), m.end() + 18)]
        rel = m.start() - max(0, m.start() - 18)
        good = ctx[:rel] + "入" + ctx[rel + 1:]
        if full_text.count(good) and not full_text.count(ctx):
            total += 1
    return total


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    full_text = plain(FULL.read_text(encoding="utf-8"))
    evidence = {new: full_text.count(new) for _old, new in REPLACEMENTS}
    missing = {term: count for term, count in evidence.items() if count < 1}
    if missing:
        raise SystemExit(f"missing full-reader evidence: {missing}")
    html = LOWER.read_text(encoding="utf-8")
    changed_items = []
    for old, new in REPLACEMENTS:
        count = html.count(old)
        if count:
            html = html.replace(old, new)
            changed_items.append({"old": old, "new": new, "changed": count})
    LOWER.write_text(html, encoding="utf-8")
    total = sum(item["changed"] for item in changed_items)
    remaining = count_candidates(plain(html), full_text)
    payload = {"time": now, "changed": total, "replacements": changed_items, "lower_remaining_ren_to_ru_candidates": remaining}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 人入残留补修第二百一十一批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前下册阅读稿。",
        "- 以当前全书 reader 正确句为证据，修复 `人 -> 入` 固定短语错识。",
        "- 未做单字替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 修后下册 `人 -> 入` 短上下文候选剩余：{remaining} 条",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    MEMORY.write_text(MEMORY.read_text(encoding="utf-8").rstrip() + f"\n\n## 2026-07-07 高置信 OCR 错字补修第二百一十一批：下册人入残留\n\n- 对照当前全书 reader 正确文本，修复下册 `人 -> 入` 高置信残留 {total} 处，覆盖入出境、入园入托、入股、入狱、打入、潜入等固定语境。\n- 本批仅替换完整短语，不做单字 `人 -> 入`；报告：`output/reports/reader_ren_to_ru_batch211_20260707.md`。\n- 修后按短上下文扫描，下册仍有 {remaining} 条候选待补遗；未打开、展示或嵌入图片。\n", encoding="utf-8")
    print(json.dumps({"changed": total, "remaining_candidates": remaining, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

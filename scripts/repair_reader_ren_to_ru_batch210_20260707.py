# -*- coding: utf-8 -*-
"""Repair evidence-backed middle-reader 人->入 residues, batch210."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_ren_to_ru_batch210_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ren_to_ru_batch210_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_人入残留补修第二百一十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("被选人《江苏省地毯图案集）", "被选入《江苏省地毯图案集）"),
    ("打人国际市场", "打入国际市场"),
    ("跌人低谷", "跌入低谷"),
    ("步人健康发展的轨道", "步入健康发展的轨道"),
    ("引人排淡河", "引入排淡河"),
    ("传人或由国内传出", "传入或由国内传出"),
    ("汇人蕃薇河", "汇入蕃薇河"),
    ("步人天庭", "步入天庭"),
    ("调人等方式", "调入等方式"),
    ("调人外地菜", "调入外地菜"),
    ("步人了新的阶段", "步入了新的阶段"),
    ("调人大批救济粮", "调入大批救济粮"),
    ("涌人新浦", "涌入新浦"),
    ("调人75吨生油", "调入75吨生油"),
    ("调人各粮15282.5吨", "调入各粮15282.5吨"),
    ("（人市县财政金库部分）", "（入市县财政金库部分）"),
    ("交人市县国库", "交入市县国库"),
    ("登记人簿", "登记入簿"),
    ("盐人猴嘴坨", "盐入猴嘴坨"),
    ("引人干部管理", "引入干部管理"),
    ("步人自主经营的新阶段", "步入自主经营的新阶段"),
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

    html = MIDDLE.read_text(encoding="utf-8")
    changed_items = []
    for old, new in REPLACEMENTS:
        count = html.count(old)
        if count:
            html = html.replace(old, new)
            changed_items.append({"old": old, "new": new, "changed": count})
    MIDDLE.write_text(html, encoding="utf-8")
    total = sum(item["changed"] for item in changed_items)
    remaining = count_candidates(plain(html), full_text)

    payload = {"time": now, "changed": total, "replacements": changed_items, "middle_remaining_ren_to_ru_candidates": remaining}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 人入残留补修第二百一十批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿。",
        "- 以当前全书 reader 正确句为证据，修复 `人 -> 入` 固定短语错识。",
        "- 未做单字替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 修后中册 `人 -> 入` 短上下文候选剩余：{remaining} 条",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    MEMORY.write_text(MEMORY.read_text(encoding="utf-8").rstrip() + f"\n\n## 2026-07-07 高置信 OCR 错字补修第二百一十批：中册人入残留\n\n- 对照当前全书 reader 正确文本，修复中册 `人 -> 入` 高置信残留 {total} 处，覆盖打入、步入、汇入、调入等固定语境。\n- 本批仅替换完整短语，不做单字 `人 -> 入`；报告：`output/reports/reader_ren_to_ru_batch210_20260707.md`。\n- 修后按短上下文扫描，中册仍有 {remaining} 条候选待补遗；未打开、展示或嵌入图片。\n", encoding="utf-8")
    print(json.dumps({"changed": total, "remaining_candidates": remaining, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

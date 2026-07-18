# -*- coding: utf-8 -*-
"""Repair evidence-backed 广->厂 residues in middle reader, batch204."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_factory_guang_batch204_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_factory_guang_batch204_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_厂字残留补修第二百零四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("市贝雕广生产的贝雕画", "市贝雕厂生产的贝雕画"),
    ("白塔美术广冯寿干", "白塔美术厂冯寿干"),
    ("工广变成一片废墟", "工厂变成一片废墟"),
    ("水产品冷冻加工广约79家", "水产品冷冻加工厂约79家"),
    ("大中型肉联广和北京", "大中型肉联厂和北京"),
    ("开发区肉联广有5000吨低温冷库", "开发区肉联厂有5000吨低温冷库"),
    ("市罐头食品广不断扩大", "市罐头食品厂不断扩大"),
    ("鱼品加工广后，投产瓶装鱼罐头", "鱼品加工厂后，投产瓶装鱼罐头"),
    ("洪门酒广由4锅蒸馏操作", "洪门酒厂由4锅蒸馏操作"),
    ("连云港市酶制剂广", "连云港市酶制剂厂"),
    ("襄河乳品广因奶源", "襄河乳品厂因奶源"),
    ("新浦淀粉广并入新浦制冰厂", "新浦淀粉厂并入新浦制冰厂"),
    ("洪门果酒广协助该厂", "洪门果酒厂协助该厂"),
    ("新海油广生产谷维素", "新海油厂生产谷维素"),
    ("曙光化工广生产无水硫酸钠", "曙光化工厂生产无水硫酸钠"),
    ("连云港向阳制药广", "连云港向阳制药厂"),
    ("建设兵团一师制药广改名", "建设兵团一师制药厂改名"),
    ("东北制药总广", "东北制药总厂"),
    ("上海化工广、广州深圳口岸", "上海化工厂、广州深圳口岸"),
    ("新浦五金工具广", "新浦五金工具厂"),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int, remaining_candidates: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第二百零四批：中册厂字残留"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 对照当前全书 reader 正确文本，修复中册轻工、食品、医药等段 `广 -> 厂` 高置信残留 {total} 处。
- 本批仅替换完整短语，不做单字 `广 -> 厂`；报告：`output/reports/reader_factory_guang_batch204_20260707.md`。
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


def count_candidates(text: str, full_text: str) -> int:
    total = 0
    for m in re.finditer("广", text):
        ctx = text[max(0, m.start() - 10): min(len(text), m.end() + 10)]
        good = ctx.replace("广", "厂", 1)
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
        "# 厂字残留补修第二百零四批",
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

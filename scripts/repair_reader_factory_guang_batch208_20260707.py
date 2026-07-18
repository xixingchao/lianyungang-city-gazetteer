# -*- coding: utf-8 -*-
"""Repair remaining evidence-backed middle-reader 广->厂 residues, batch208."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_factory_guang_batch208_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_factory_guang_batch208_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_厂字残留补修第二百零八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "学校办糕点厂及乡村办水产品冷</p><p>冻加工广约79家除外",
        "学校办糕点厂及乡村办水产品冷</p><p>冻加工厂约79家除外",
        "校办糕点厂及乡村办水产品冷冻加工厂约79家除外",
    ),
    (
        "大中型肉</p><p>联广和北京、天津、上海、贵州、湖南、河南、山东、辽宁、福建等省、市30多家企业",
        "大中型肉</p><p>联厂和北京、天津、上海、贵州、湖南、河南、山东、辽宁、福建等省、市30多家企业",
        "省内11个大中型肉联厂和北京",
    ),
    (
        "日宰3000只鸡的流水线、开</p><p>发区肉联广有5000吨低温冷库",
        "日宰3000只鸡的流水线、开</p><p>发区肉联厂有5000吨低温冷库",
        "开发区肉联厂有5000吨低温冷库",
    ),
    (
        "市毛巾厂、朝阳卫生材料</p><p>广的纱布、药棉",
        "市毛巾厂、朝阳卫生材料</p><p>厂的纱布、药棉",
        "朝阳卫生材料厂的纱布",
    ),
    (
        "东海、赣榆、灌云三县化肥厂、磷</p><p>肥广相继建立",
        "东海、赣榆、灌云三县化肥厂、磷</p><p>肥厂相继建立",
        "化肥厂、磷肥厂相继建立",
    ),
    (
        "连云港市锦屏机</p><p>械广、赣榆县农机修造厂生产电动机1381台",
        "连云港市锦屏机</p><p>械厂、赣榆县农机修造厂生产电动机1381台",
        "连云港市锦屏机械厂、赣榆县农机修造厂",
    ),
    (
        "1986年，北京电视设</p><p>备广转让U/V转换器的生产技术",
        "1986年，北京电视设</p><p>备厂转让U/V转换器的生产技术",
        "北京电视设备厂转让U/V转换器",
    ),
    (
        "同年东辛农场砖瓦</p><p>广、赣榆县砖瓦厂成立",
        "同年东辛农场砖瓦</p><p>厂、赣榆县砖瓦厂成立",
        "东辛农场砖瓦厂、赣榆县砖瓦厂成立",
    ),
    (
        "灌云县砖瓦厂、灌云龙</p><p>苴砖广、云台胜利砖瓦厂",
        "灌云县砖瓦厂、灌云龙</p><p>苴砖厂、云台胜利砖瓦厂",
        "灌云龙苴砖厂、云台胜利砖瓦厂",
    ),
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def count_candidates(text: str, full_text: str) -> int:
    total = 0
    for m in re.finditer("广", text):
        ctx = text[max(0, m.start() - 16): min(len(text), m.end() + 16)]
        good = ctx.replace("广", "厂", 1)
        if full_text.count(good) and not full_text.count(ctx):
            total += 1
    return total


def upsert_memory(total: int, remaining_candidates: int) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第二百零八批：中册厂字残留"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 对照当前全书 reader 正确文本，修复中册剩余 `广 -> 厂` 高置信残留 {total} 处。
- 本批仅替换完整 HTML 片段，不做单字 `广 -> 厂`；报告：`output/reports/reader_factory_guang_batch208_20260707.md`。
- 修后按短上下文扫描，中册仍有 {remaining_candidates} 条 `广 -> 厂` 候选；未打开、展示或嵌入图片。
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
    evidence = {evidence_text: full_text.count(evidence_text) for _old, _new, evidence_text in REPLACEMENTS}
    missing = {term: count for term, count in evidence.items() if count < 1}
    if missing:
        raise SystemExit(f"missing full-reader evidence: {missing}")

    html = MIDDLE.read_text(encoding="utf-8")
    changed_items = []
    for old, new, _evidence_text in REPLACEMENTS:
        count = html.count(old)
        if count:
            html = html.replace(old, new)
            changed_items.append({"old": plain(old), "new": plain(new), "changed": count})
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
        "# 厂字残留补修第二百零八批",
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

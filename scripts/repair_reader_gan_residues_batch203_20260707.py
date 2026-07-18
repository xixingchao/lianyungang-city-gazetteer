# -*- coding: utf-8 -*-
"""Repair evidence-backed 干 residues written as 于 in split readers."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
TARGETS = {
    "middle": ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    "lower": ROOT / "output" / "final_reader" / "连云港市志_下册.html",
}
REPORT_JSON = ROOT / "output" / "reports" / "reader_gan_residues_batch203_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_gan_residues_batch203_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_干字残留补修第二百零三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "middle": [
        ("白羽半于白葡萄酒", "白羽半干白葡萄酒"),
        ("重点骨于企业", "重点骨干企业"),
        ("板蓝根于糖浆", "板蓝根干糖浆"),
        ("二级于线邮路", "二级干线邮路"),
        ("二级于线自办汽车邮路", "二级干线自办汽车邮路"),
        ("收入包于范围", "收入包干范围"),
        ("收支挂钩，比例包于”的财政管理体制", "收支挂钩，比例包干”的财政管理体制"),
        ("的包于办法", "的包干办法"),
        ("计划包于、差额管理", "计划包干、差额管理"),
        ("差额包于的基础", "差额包干的基础"),
        ("培训骨于，180多位", "培训骨干，180多位"),
        ("领导骨于。在整党整风", "领导骨干。在整党整风"),
    ],
    "lower": [
        ("按“归口包于”的办法安置", "按“归口包干”的办法安置"),
        ("党团骨于分子", "党团骨干分子"),
        ("公安于警学校", "公安干警学校"),
        ("包于费级别", "包干费级别"),
        ("“大包于”制度", "“大包干”制度"),
        ("文艺骨于113人", "文艺骨干113人"),
        ("文艺骨于50多人", "文艺骨干50多人"),
        ("白羽半于白葡萄酒", "白羽半干白葡萄酒"),
        ("留20名骨于调吕剧团", "留20名骨干调吕剧团"),
    ],
}


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int, by_scope: dict[str, int]) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第二百零三批：干字残留"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 对照当前全书 reader 正确文本，修复分册 `于` 对 `干` 的错识 {total} 处，包括骨干、包干、干线、干警、半干白等固定短语。
- 本批仅替换完整短语：中册 {by_scope.get('middle', 0)} 处、下册 {by_scope.get('lower', 0)} 处；报告：`output/reports/reader_gan_residues_batch203_20260707.md`。
- 保留合法 `由于/属于/低于/便于/对于` 等语境；未做单字替换；未打开、展示或嵌入图片。
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
    evidence = {new: full_text.count(new) for items in REPLACEMENTS.values() for _old, new in items}
    missing = {term: count for term, count in evidence.items() if count < 1}
    if missing:
        raise SystemExit(f"missing full-reader evidence: {missing}")

    changed_items = []
    by_scope = {}
    remaining_yubu = {}
    for scope, path in TARGETS.items():
        html = path.read_text(encoding="utf-8")
        for old, new in REPLACEMENTS[scope]:
            count = html.count(old)
            if count:
                html = html.replace(old, new)
                changed_items.append({"scope": scope, "old": old, "new": new, "changed": count})
                by_scope[scope] = by_scope.get(scope, 0) + count
        path.write_text(html, encoding="utf-8")
        remaining_yubu[scope] = plain(html).count("于部")

    total = sum(item["changed"] for item in changed_items)
    payload = {
        "time": now,
        "changed": total,
        "by_scope": by_scope,
        "full_evidence_counts": evidence,
        "replacements": changed_items,
        "remaining_yubu": remaining_yubu,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 干字残留补修第二百零三批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册、下册阅读稿。",
        "- 以当前全书 reader 正确句为证据，修复 `于` 对 `干` 的固定短语错识。",
        "- 保留合法 `由于/属于/低于/便于/对于` 等语境；未做单字替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 中册修复：{by_scope.get('middle', 0)} 处",
        f"- 下册修复：{by_scope.get('lower', 0)} 处",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['scope']}`：`{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total, by_scope)
    print(json.dumps({"changed": total, "by_scope": by_scope, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

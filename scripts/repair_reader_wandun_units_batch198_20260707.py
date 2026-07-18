# -*- coding: utf-8 -*-
"""Repair verified 万吨 residues written as 方吨 in split readers."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_wandun_units_batch198_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_wandun_units_batch198_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_万吨单位错字补修第一百九十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "middle": [
        ("全市加工水产冻品2.95方吨", "全市加工水产冻品2.95万吨"),
        ("合成氨年产能力达到7.10方吨", "合成氨年产能力达到7.10万吨"),
        ("全市实产合成氨6.98方吨", "全市实产合成氨6.98万吨"),
        ("实产合成氨3.64方吨", "实产合成氨3.64万吨"),
        ("实产1.06方吨", "实产1.06万吨"),
        ("民国26年上半年14.7方吨", "民国26年上半年14.7万吨"),
        ("枣庄煤炭运往日本，仅民国30年4月至31年3月达118方吨", "枣庄煤炭运往日本，仅民国30年4月至31年3月达118万吨"),
        ("数量为22.17方吨", "数量为22.17万吨"),
        ("1962~1969年出口煤炭122.66方吨", "1962~1969年出口煤炭122.66万吨"),
        ("1.5~2方吨大米", "1.5~2万吨大米"),
        ("达到19.8方吨", "达到19.8万吨"),
        ("煤炭64.19方吨", "煤炭64.19万吨"),
        ("水产品9.1方吨", "水产品9.1万吨"),
    ],
    "lower": [
        ("暂不能利用储量905方吨", "暂不能利用储量905万吨"),
        ("工业储量2253方吨", "工业储量2253万吨"),
        ("工业储量1076方吨", "工业储量1076万吨"),
        ("下层远景储量83方吨", "下层远景储量83万吨"),
        ("日供水能力达9方吨", "日供水能力达9万吨"),
    ],
}


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def upsert_memory(total: int, by_scope: dict[str, int]) -> None:
    marker = "## 2026-07-07 高置信 OCR 错字补修第一百九十八批：万吨单位"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    block = f"""
{marker}

- 对照当前全书 reader 正确文本，修复中册/下册 `方吨` 对 `万吨` 的单位错识 {total} 处。
- 本批仅替换带上下文的完整短语：中册 {by_scope.get('middle', 0)} 处、下册 {by_scope.get('lower', 0)} 处；报告：`output/reports/reader_wandun_units_batch198_20260707.md`。
- 保留 `1方吨/3方吨/650.00方吨/方立方米` 等未逐条核证候选；未打开、展示或嵌入图片。
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
    evidence = {}
    for items in REPLACEMENTS.values():
        for _old, new in items:
            evidence[new] = full_text.count(new)
    missing = {term: count for term, count in evidence.items() if count < 1}
    if missing:
        raise SystemExit(f"missing full-reader evidence: {missing}")

    changed_items = []
    by_scope = {}
    remaining = {}
    for scope, path in TARGETS.items():
        before = path.read_text(encoding="utf-8")
        after = before
        for old, new in REPLACEMENTS[scope]:
            count = after.count(old)
            if count:
                after = after.replace(old, new)
                changed_items.append({"scope": scope, "old": old, "new": new, "changed": count})
                by_scope[scope] = by_scope.get(scope, 0) + count
        path.write_text(after, encoding="utf-8")
        remaining[scope] = plain(after).count("方吨")

    total = sum(item["changed"] for item in changed_items)
    payload = {
        "time": now,
        "changed": total,
        "by_scope": by_scope,
        "full_evidence_counts": evidence,
        "replacements": changed_items,
        "remaining_fang_ton": remaining,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 万吨单位错字补修第一百九十八批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册、下册阅读稿。",
        "- 以当前全书 reader 正确句为证据，修复 `方吨` 对 `万吨` 的单位错识。",
        "- 未做泛化替换；未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 修复：{total} 处",
        f"- 中册修复：{by_scope.get('middle', 0)} 处",
        f"- 下册修复：{by_scope.get('lower', 0)} 处",
        f"- 修后中册纯文本 `方吨` 剩余：{remaining.get('middle', 0)} 处",
        f"- 修后下册纯文本 `方吨` 剩余：{remaining.get('lower', 0)} 处",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['scope']}`：`{item['old']}` -> `{item['new']}`：{item['changed']} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    upsert_memory(total, by_scope)
    print(json.dumps({"changed": total, "by_scope": by_scope, "remaining_fang_ton": remaining, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

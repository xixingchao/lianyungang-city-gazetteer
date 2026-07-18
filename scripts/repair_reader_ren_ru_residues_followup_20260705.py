# -*- coding: utf-8 -*-
"""Second exact-match pass for source-clear 人/入 OCR residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_ren_ru_residues_followup_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ren_ru_residues_followup_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_正文人入错识第二批修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("公路入境", "响水口人境内", "响水口入境内", 1),
    ("清代河流入海", "东流人海", "东流入海", 1),
    ("蔷薇河入海口", "此河人海口", "此河入海口", 1),
    ("五图河入海", "洋桥人海", "洋桥入海", 1),
    ("凤凰山入海", "是人海必由之路", "是入海必由之路", 1),
    ("徐福入海", "为其人海求仙药", "为其入海求仙药", 1),
    ("青口河入海口", "在人海口开挖", "在入海口开挖", 1),
    ("漕粮入海", "自淮人海", "自淮入海", 1),
    ("电话自动网", "进人全国自动网", "进入全国自动网", 1),
    ("景区道路", "为进人花果山的要道", "为进入花果山的要道", 1),
    ("渔湾山谷", "一进人山谷", "一进入山谷", 1),
    ("小商贩划出", "并人国营和供销社", "并入国营和供销社", 1),
    ("百货公司合并", "并人百货公司", "并入百货公司", 1),
    ("市场销售", "进人市场", "进入市场", 3),
    ("公粮入库", "人库公粮", "入库公粮", 2),
    ("接粮入库", "人库时", "入库时", 1),
    ("征购入库", "征购人库", "征购入库", 4),
    ("粮质评库", "进行人库粮质", "进行入库粮质", 2),
    ("合同粮入库", "人库合同定购粮", "入库合同定购粮", 1),
    ("粮食实际入库", "实际人库", "实际入库", 3),
    ("期刊入阅览室", "送人阅览室", "送入阅览室", 1),
    ("馆藏入库", "直接人库收藏", "直接入库收藏", 1),
    ("调查研究", "深人调查研究", "深入调查研究", 2),
    ("妇女解放", "运动不断深人", "运动不断深入", 1),
    ("改革深入", "改革深人", "改革深入", 2),
    ("敌占区", "深人敌占区", "深入敌占区", 1),
    ("侦察", "深人连云港", "深入连云港", 1),
    ("城乡工作", "深人城乡", "深入城乡", 3),
    ("码头斗争", "进人高潮", "进入高潮", 1),
    ("工会演出", "深人厂矿", "深入厂矿", 1),
    ("文艺创作", "深人生活", "深入生活", 1),
    ("教学改革", "广泛深人地开展教学改革", "广泛深入地开展教学改革", 1),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for label, old, new, expected in REPLACEMENTS:
        count = html.count(old)
        if count != expected:
            raise RuntimeError(f"expected {expected} occurrence(s) for {label}, got {count}: {old}")
        html = html.replace(old, new)
        changes.append({"label": label, "old": old, "new": new, "count": count})
    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "principle": "第二批仅修复检索残留中上下文明确的入海、进入、并入、入库、深入等 exact-match；不处理表格压缩段、古文/人名和语义未核定项。",
        "changes": changes,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文人/入错识第二批修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 原则：只修上下文明确的 exact-match；表格压缩段、古文/人名和语义未核定项暂不处理。",
        "",
        "## 修复清单",
        "",
        "| 项 | 原文 | 修复后 | 次数 |",
        "|---|---|---|---|",
    ]
    for item in changes:
        lines.append(f"| {item['label']} | `{item['old']}` | `{item['new']}` | {item['count']} |")
    md = "\n".join(lines) + "\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 正文人/入错识第二批修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_ren_ru_residues_followup_20260705.py`，继续清理第一批后残留检索中可确定的 `人/入` 错识。
- 覆盖入海/入境、进入、并入、入库、深入等 {len(REPLACEMENTS)} 类片段，合计 {sum(item[3] for item in REPLACEMENTS)} 处。
- 明确跳过表格压缩段、古文/人名、正常 `人` 字和语义未核定项。
- 报告：`output/reports/reader_ren_ru_residues_followup_20260705.md`。
""",
    )

    print("reader_ren_ru_residues_followup_repaired")
    print(f"changes={len(changes)}")
    print(f"total_changed_occurrences={sum(item['count'] for item in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

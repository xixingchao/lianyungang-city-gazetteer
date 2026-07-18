# -*- coding: utf-8 -*-
"""Exact-match cleanup for clear glyph OCR residues in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_glyph_residues_batch1_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_glyph_residues_batch1_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_正文字形错识第一批修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("科技界人士", "科技界人土", "科技界人士", 1),
    ("党外人士", "党外人土", "党外人士", 2),
    ("爱国人士", "爱国人土", "爱国人士", 1),
    ("经济界人士", "经济界人土", "经济界人士", 1),
    ("工商界人士", "工商界人土", "工商界人士", 2),
    ("各界人士", "各界人土", "各界人士", 6),
    ("社会人士", "社会人土", "社会人士", 1),
    ("知名人士", "知名人土", "知名人士", 1),
    ("女爱国知名人士", "女爱国知名人土", "女爱国知名人士", 1),
    ("进步人士", "进步人土", "进步人士", 1),
    ("人士联系", "人土联系", "人士联系", 1),
    ("人士意见", "人土意见", "人士意见", 1),
    ("人士代表", "人土代表", "人士代表", 2),
    ("人士自我教育", "人土自我教育", "人士自我教育", 1),
    ("人士学习", "人土学习", "人士学习", 1),
    ("人士学文件", "人土学《", "人士学《", 1),
    ("人士座谈", "人土座谈", "人士座谈", 1),
    ("工商界人士接待", "人土20多次", "人士20多次", 1),
    ("无记名投票方式", "提票方式", "投票方式", 1),
    ("疏散保障", "蔬散保障", "疏散保障", 1),
    ("人口疏散", "人口蔬散", "人口疏散", 1),
    ("联谊工作", "联联谊工作", "联谊工作", 1),
    ("促进祖国统一", "促进祖国统，为", "促进祖国统一，为", 1),
    ("防外力破坏", "防外力破环", "防外力破坏", 1),
    ("破坏农业合作社", "破环农业合作社", "破坏农业合作社", 1),
    ("党组织遭破坏", "党组织遭破环", "党组织遭破坏", 1),
    ("龙会破坏抗日", "龙会破环抗日", "龙会破坏抗日", 1),
    ("入土最深", "人土最深", "入土最深", 1),
    ("混入土匪队伍", "混人土匪队伍", "混入土匪队伍", 1),
    ("埋入土坑", "埋人土坑", "埋入土坑", 1),
    ("牺牲", "牺性", "牺牲", 11),
    ("忠勇指战员", "忠勇的指点员", "忠勇的指战员", 1),
    ("流传万世", "流传方世", "流传万世", 1),
    ("瞻仰敬礼", "瞻仰敬战五周年", "瞻仰敬礼。抗战五周年", 1),
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
        if count == expected:
            html = html.replace(old, new)
            changes.append({"label": label, "old": old, "new": new, "count": count, "expected": expected, "status": "changed"})
        elif count == 0 and html.count(new) >= expected:
            changes.append({"label": label, "old": old, "new": new, "count": 0, "expected": expected, "status": "already_applied"})
        else:
            raise RuntimeError(f"expected {expected} occurrence(s) for {label}, got {count}: {old}")

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sources = [
        "workbench/ocr/merged/连云港市志_中_part02_OCR汇总.md",
        "workbench/ocr/merged/连云港市志_下_part01_OCR汇总.md",
        "workbench/ocr/merged/连云港市志_上册_OCR汇总.md",
        "output/final_reader/连云港市志_最终阅读版.html",
    ]
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "principle": "只修 exact-match 且语义固定的字形 OCR 残留；跳过入土/人士语义不清的裸词。",
        "sources": sources,
        "changes": changes,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文字形错识第一批修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 原则：只修 exact-match 且语义固定的字形 OCR 残留；不做裸词全局替换。",
        "",
        "## 依据",
        "",
    ]
    lines.extend(f"- `{source}`" for source in sources)
    lines.extend(["", "## 修复清单", "", "| 项 | 本次变更 | 目标次数 | 状态 |", "|---|---:|---:|---|"])
    for item in changes:
        lines.append(f"| {item['label']} | {item['count']} | {item['expected']} | {item['status']} |")
    md = "\n".join(lines) + "\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 正文字形错识第一批修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_glyph_residues_batch1_20260705.py`，修复主阅读版中一批上下文固定的字形 OCR 残留。
- 覆盖 `人土/人士`、`人土/入土`、`破环/破坏`、`牺性/牺牲`、`蔬散/疏散`、`提票/投票`、`联联谊/联谊` 等 {len(REPLACEMENTS)} 类片段。
- 本脚本本次实际变更 {sum(item['count'] for item in changes)} 处；跳过语义不固定的裸词全局替换。
- 报告：`output/reports/reader_glyph_residues_batch1_20260705.md`。
""",
    )

    print("reader_glyph_residues_batch1_repaired")
    print(f"changes={len(changes)}")
    print(f"total_changed_occurrences={sum(item['count'] for item in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

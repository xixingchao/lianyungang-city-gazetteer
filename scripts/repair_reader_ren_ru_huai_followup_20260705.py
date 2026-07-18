# -*- coding: utf-8 -*-
"""Fourth exact-match pass for clear 人/入 and 准/淮 OCR residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_ren_ru_huai_followup_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_ren_ru_huai_followup_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_正文人入准淮错识第四批修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("渔业列入工商业", "渔业列人工商业", "渔业列入工商业", 1),
    ("星火计划列入", "并列人江苏省1990年“星火计划”项目", "并列入江苏省1990年“星火计划”项目", 1),
    ("战备航道列入", "曾被列人战备航道", "曾被列入战备航道", 1),
    ("物资计划列入", "有些物资并未列人计划分配", "有些物资并未列入计划分配", 1),
    ("统配物资列入", "列人国家统配的物资", "列入国家统配的物资", 1),
    ("市计划列入", "列人市计划分配", "列入市计划分配", 1),
    ("财政预算列入", "列人财政预算支出", "列入财政预算支出", 1),
    ("包干范围", "不列人包于范围", "不列入包干范围", 1),
    ("政府序列", "列人市政府序列", "列入市政府序列", 1),
    ("文保单位", "三元宫已被列人市级文物保护单位", "三元宫已被列入市级文物保护单位", 1),
    ("商品进入港口", "外地商品多经青口港、大浦港进人", "外地商品多经青口港、大浦港进入", 1),
    ("粮油输入", "从连云港输出粮油达266025吨，输人13367吨", "从连云港输出粮油达266025吨，输入13367吨", 1),
    ("输出入港", "成为新的输出人港", "成为新的输出入港", 1),
    ("货物查验", "免办其进人货物的查验", "免办其进入货物的查验", 1),
    ("税收入库额", "增加了人库额", "增加了入库额", 1),
    ("牌照税入库", "同月并征人库", "同月并征入库", 1),
    ("印花税并入", "部分凭证，分别并人商品流通税", "部分凭证，分别并入商品流通税", 1),
    ("盐税并入", "300元并人盐税征收", "300元并入盐税征收", 1),
    ("税款入库", "组织人库", "组织入库", 1),
    ("实物入库", "实物人库", "实物入库", 1),
    ("检查税款入库136", "当年人库136.5元", "当年入库136.5元", 1),
    ("检查税款入库261", "当年人库261.7万元", "当年入库261.7万元", 1),
    ("基藏书库", "送一套人基藏书库", "送一套入基藏书库", 1),
    ("复本入流通书库", "复本送人流通书库", "复本送入流通书库", 1),
    ("体制改革深入", "随着经济体制改革的深人", "随着经济体制改革的深入", 1),
    ("改革深入", "随着改革的深人", "随着改革的深入", 1),
    ("催调深入", "催调人员要深人矿区、林区", "催调人员要深入矿区、林区", 1),
    ("盐场深入", "深人盐场、坨地", "深入盐场、坨地", 1),
    ("吕剧团深入", "深人农村演出", "深入农村演出", 1),
    ("盐场辅导深入", "深人沿海各盐场", "深入沿海各盐场", 1),
    ("改革开放深入", "随着改革开放的深人", "随着改革开放的深入", 1),
    ("乡镇演出深入", "深人广矿乡镇演出", "深入广矿乡镇演出", 1),
    ("民间教化深入", "深人民间以德政教导开化", "深入民间以德政教导开化", 1),
    ("居民迁入内地", "迁人内地", "迁入内地", 1),
    ("辗转入川", "辗转人川", "辗转入川", 1),
    ("入东京政法", "人东京政法大学政法系求学", "入东京政法大学政法系求学", 1),
    ("编入中央军", "编人中国国民党中央军", "编入中国国民党中央军", 1),
    ("淮阴", "准阴", "淮阴", 29),
    ("淮北", "准北", "淮北", 45),
    ("淮海", "准海", "淮海", 32),
    ("淮安", "准安", "淮安", 12),
    ("淮河", "准河", "淮河", 1),
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
        "principle": "第四批仅修复词组级可判定的列入/进入/入库/深入/并入/准淮错识；跳过表格压缩段、古文用例和语义未核定项。",
        "changes": changes,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文人/入与准/淮错识第四批修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 原则：只修词组级可判定项；表格压缩段、古文用例和语义未核定项暂不处理。",
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

    marker = "## 2026-07-05 正文人/入与准/淮错识第四批修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_ren_ru_huai_followup_20260705.py`，继续清理词组级可判定的 `人/入` 与 `准/淮` OCR 错识。
- 覆盖列入、进入、输入、入库、深入、迁入、编入，以及淮阴、淮北、淮海、淮安、淮河等 {len(REPLACEMENTS)} 类片段。
- 跳过表格压缩段、古文用例和语义未核定项。
- 报告：`output/reports/reader_ren_ru_huai_followup_20260705.md`。
""",
    )

    print("reader_ren_ru_huai_followup_repaired")
    print(f"changes={len(changes)}")
    print(f"total_changed_occurrences={sum(item['count'] for item in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

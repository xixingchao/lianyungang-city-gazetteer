# -*- coding: utf-8 -*-
"""Remove duplicate flattened table residues that already have verified tables."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_duplicate_verified_table_residues_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_duplicate_verified_table_residues_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_已核表格重复残片清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "节约用水情况表正文重复残片",
        "old": (
            "<p>万元产值取水量工业总产值（万元）</p>\n"
            "\n"
            "<p>万元产值取水量（吨/万元）</p>\n"
            "<p>节水设施项目（项）</p>\n"
            "<p>节水设施投资10.411.53.414.511.5节水设施建设（万元）</p>\n"
            "\n"
            "<p>节水设施单位投资（元/吨日）</p>\n"
            "<p>工业用水量4085.34314.55199.4工业用水重复（万吨/年）</p>\n"
            "<p>利用率工业重复利用水量（万吨/年）</p>\n"
            "<p>工业用水重复利用率38.239.340.541.3（%）</p>\n"
            "<p>工业计划户实际取水量工业计划1364.71490.31770.21835.4用水率（万吨/年）</p>\n"
            "<p>全市工业计划用水率（%）</p>"
        ),
        "new": "",
        "verified_table": "LYG-上-T011",
        "sources": [
            "output/final_reader/连云港市志_全书.html:3668",
            "workbench/table_entries/上/data/LYG-上-T011.json",
        ],
    },
    {
        "label": "纺织工业企业基本情况表正文重复残片",
        "old": (
            "<p>主要产品时间制不变价）（万元）</p>\n"
            "<p>（万元）</p>\n"
            "<p>原值（万元）</p>\n"
            "<p>（人）</p>\n"
            "<p>灌云县织布厂集体布连云港市卫生材料厂集体脱脂纱、布赣榆县青口棉织厂集体布东海县牛山色织厂集体布-0.6连云港市染整厂全民染色布-246连云港市第二染整厂全民染色布-227赣榆县朱堵帆布厂集体纯布、帆布251.98.745.9注：简介企业不列入此表。</p>"
        ),
        "new": "",
        "verified_table": "LYG-上-T043",
        "sources": [
            "output/final_reader/连云港市志_全书.html:7630",
            "workbench/table_entries/上/data/LYG-上-T043.json",
        ],
    },
    {
        "label": "罐头食品加工企业基本情况表正文重复残片",
        "old": "<p>东海县浦南乡东海县太平渔业集体150500.200.0245603.50250鱼类罐头公司水产食品厂太平村东海县龙门罐头东海县山左口集体110.056834- 1.002000水果罐头0.20120食品厂</p>",
        "new": "",
        "verified_table": "LYG-中-T010",
        "sources": [
            "output/final_reader/连云港市志_全书.html:8689",
            "workbench/table_entries/中/data/LYG-中-T010.json",
        ],
    },
]

DEFERRED = [
    "水闸/涵闸长串残片：疑似未闭合到已核结构化表，暂不删除。",
    "竹藤工艺企业残片：未在本轮闭合到对应已核表，暂不删除。",
    "社会福利企业、教育经费残片：仍需确认是否已有完整结构化表，暂不删除。",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for item in REPLACEMENTS:
        old_count = html.count(item["old"])
        if old_count == 1:
            html = html.replace(item["old"], item["new"], 1)
            status = "changed"
            changed = 1
        elif old_count == 0:
            if item["label"].startswith("节约用水") and "节水设施投资10.411.53.414.511.5" in html:
                raise RuntimeError(f"unmatched residue still present for {item['label']}")
            if item["label"].startswith("纺织") and "灌云县织布厂集体布" in html:
                raise RuntimeError(f"unmatched residue still present for {item['label']}")
            if item["label"].startswith("罐头") and "东海县浦南乡东海县太平渔业" in html:
                raise RuntimeError(f"unmatched residue still present for {item['label']}")
            status = "already_applied"
            changed = 0
        else:
            raise RuntimeError(f"expected {item['label']} once, got {old_count}")
        changes.append({
            "label": item["label"],
            "status": status,
            "changed": changed,
            "verified_table": item["verified_table"],
            "sources": item["sources"],
        })

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": changes,
        "deferred": DEFERRED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 已核表格重复残片清理",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：仅删除已在 verified table block 中存在的重复压扁表格残片。",
        "",
        "## 结果",
        "",
    ]
    for change in changes:
        lines.append(f"- {change['label']}：{change['status']}，本次变更 {change['changed']}，对应 `{change['verified_table']}`")
        for source in change["sources"]:
            lines.append(f"  - `{source}`")
    lines.extend(["", "## 暂不处理", ""])
    for item in DEFERRED:
        lines.append(f"- {item}")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 已核表格重复残片清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_duplicate_verified_table_residues_20260705.py`，从主阅读版删除 3 组已核表格的正文重复压扁残片：节约用水情况表、纺织工业企业基本情况表、罐头食品加工企业基本情况表。
- 本轮只删已有 verified table block 可对应的重复残片；水闸、竹藤、社会福利、教育经费等疑似表格残片先列入暂不处理，避免未闭合证据时误删正文。
- 报告：`output/reports/reader_duplicate_verified_table_residues_20260705.md`。
""",
    )

    print("reader_duplicate_verified_table_residues_repaired")
    print(f"changed={sum(item['changed'] for item in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

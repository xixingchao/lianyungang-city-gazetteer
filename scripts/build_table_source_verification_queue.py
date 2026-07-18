# -*- coding: utf-8 -*-
"""Build a source-verification queue from the table delivery readiness audit."""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "output" / "reports" / "结构化表格交付就绪审计报告.json"
REPORT_MD = ROOT / "output" / "reports" / "结构化表格回源核录优先队列.md"

PRIORITY_KIND = {
    "含待核/待录入标记": 1,
    "表题未确认": 2,
    "表题疑似OCR粘连": 3,
    "单列骨架表": 4,
    "疑似空壳表": 5,
    "verified状态与待核内容冲突": 6,
}
VOLUME_ORDER = {"上": 1, "中": 2, "下": 3}


def parse_pages(value: str) -> list[int]:
    pages = []
    for part in str(value or "").split(","):
        part = part.strip()
        if part.isdigit():
            pages.append(int(part))
    return pages


def main() -> None:
    data = json.loads(AUDIT_JSON.read_text(encoding="utf-8"))
    grouped: dict[str, dict] = {}
    for item in data["issues"]:
        table_id = item["table_id"]
        entry = grouped.setdefault(table_id, {
            "table_id": table_id,
            "title": item["title"],
            "volume": item["volume"],
            "pages": item["pages"],
            "kinds": set(),
            "excerpt": item["excerpt"],
        })
        entry["kinds"].add(item["kind"])

    rows = []
    for entry in grouped.values():
        pages = parse_pages(entry["pages"])
        first_page = min(pages) if pages else 99999
        severity = min(PRIORITY_KIND.get(kind, 99) for kind in entry["kinds"])
        rows.append((VOLUME_ORDER.get(entry["volume"], 9), first_page, severity, entry))
    rows.sort(key=lambda row: (row[0], row[1], row[2], row[3]["table_id"]))

    lines = [
        "# 结构化表格回源核录优先队列",
        "",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 口径",
        "",
        "- 本队列来自结构化表格交付就绪审计。",
        "- 队列中的表不得进入主交付入口，必须回源 PDF/页图核读、补全行列、修正表题后再标为可交付。",
        "- 优先顺序：上册在前，页码靠前在前，待录入/待确认优先于一般标题粘连。",
        "",
        f"待回源表格：{len(rows)}",
        "",
        "| 优先序 | 表ID | 分册 | 页码 | 问题类型 | 表题 |",
        "|---:|---|---|---|---|---|",
    ]
    for idx, (_, _, _, entry) in enumerate(rows, 1):
        kinds = "；".join(sorted(entry["kinds"], key=lambda k: PRIORITY_KIND.get(k, 99)))
        title = (entry["title"] or entry["excerpt"]).replace("|", "\\|")
        lines.append(f"| {idx} | {entry['table_id']} | {entry['volume']} | {entry['pages']} | {kinds} | {title} |")

    lines.extend([
        "",
        "## 下一批建议",
        "",
        "- 先处理前 10 张上册早期表：物候、建置沿革、市区干道、房地产交易、污染物排放、工农业总产值、商品零售、GDP结构、住宅水平、工商企业登记。",
        "- 每张表需要打开对应 PDF 页图核对，不得仅凭 OCR 或现有表格站数据修复。",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"queued={len(rows)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

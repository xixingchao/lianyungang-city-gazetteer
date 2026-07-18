# -*- coding: utf-8 -*-
"""Follow-up source-backed fixes for port health quarantine OCR slips."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_port_health_quarantine_followup_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_port_health_quarantine_followup_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第二十九卷卫生检疫错识回源第二批修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCES = [
    "workbench/ocr/paddle_ocr/中/part01/page_0506.txt",
    "workbench/ocr/paddle_ocr/中/part01/page_0507.txt",
]
SCOPE_START = '<h4 id="第二十九卷-第四章管理-第四节卫生检疫">第四节卫生检疫</h4>'
SCOPE_END = '<h4 id="第二十九卷-第四章管理-第五节边防检查">第五节边防检查</h4>'

REPLACEMENTS = [
    ("EL-TOR弧菌", "EL一TOR弧菌", "EL-TOR弧菌", SOURCES[0]),
    ("天花接种人数", "预防接种关花854人次", "预防接种天花854人次", SOURCES[1]),
    (
        "卫生监督漏句",
        "凡船方的废水、废物、生活垃圾和交通工具的卫生面貌，改变环境",
        "凡船方的废水、废物、生活垃圾等未经卫生检疫所许可，不经卫生处理一律不准在港内排放或丢弃，以彻底改善国境口岸和交通工具的卫生面貌，改变环境",
        SOURCES[1],
    ),
    ("除鼠方式", "1985年以前般采取器械毒饵除鼠", "1985年以前一般采取器械毒饵除鼠", SOURCES[1]),
    ("鼠患", "鼠惠特别严重", "鼠患特别严重", SOURCES[1]),
    ("熏蒸药剂", "“漠化甲烷”", "“溴化甲烷”", SOURCES[1]),
    ("病媒标点", "病媒昆虫，啮齿动物", "病媒昆虫、啮齿动物", SOURCES[1]),
    ("蜚蠊", "蛋（蟑螂）3种", "蜚蠊(蟑螂)3种", SOURCES[1]),
    ("废钢船入境", "卫生检疫所对人境的废钢船", "卫生检疫所对入境的废钢船", SOURCES[1]),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    start = html.index(SCOPE_START)
    end = html.index(SCOPE_END, start)
    segment = html[start:end]

    changes = []
    for label, old, new, source in REPLACEMENTS:
        count = segment.count(old)
        if count != 1:
            raise RuntimeError(f"expected one occurrence for {label}, got {count}: {old}")
        segment = segment.replace(old, new, 1)
        changes.append({"label": label, "old": old, "new": new, "source": source})

    HTML.write_text(html[:start] + segment + html[end:], encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第二十九卷口岸 / 第四章管理 / 第四节卫生检疫",
        "sources": SOURCES,
        "changes": changes,
        "principle": "仅修复 page_0506/page_0507 PaddleOCR 明确支持的错识与漏句，不处理证据不足内容。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第二十九卷卫生检疫错识回源第二批修复",
        "",
        f"- 时间：{now}",
        "- 范围：第二十九卷口岸 / 第四章管理 / 第四节卫生检疫。",
        "- 源文依据：`" + "`、`".join(SOURCES) + "`。",
        "",
        "## 修复",
        "",
    ]
    for item in changes:
        lines.append(f"- `{item['old']}` -> `{item['new']}`。")
    lines.extend([
        "",
        "## 原则",
        "",
        "只采用 page_0506/page_0507 PaddleOCR 明确支持的字词和漏句；不改表格数据，不处理证据不足内容。",
        "",
    ])
    md = "\n".join(lines)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第二十九卷卫生检疫错识回源第二批修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 依据 `{SOURCES[0]}`、`{SOURCES[1]}` 继续修复卫生检疫节 page_0506/page_0507 可证错识和漏句，共 {len(changes)} 处。
- 覆盖 `EL-TOR`、`天花854人次`、卫生监督漏句、`一般采取器械毒饵除鼠`、`鼠患`、`溴化甲烷`、`蜚蠊(蟑螂)`、`入境的废钢船` 等。
- 报告：`output/reports/reader_port_health_quarantine_followup_20260705.md`。
""",
    )

    print("port_health_quarantine_followup_repaired")
    print(f"changes={len(changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

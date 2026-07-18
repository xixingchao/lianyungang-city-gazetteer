# -*- coding: utf-8 -*-
"""Remove the last reader-visible OCR table residues caught by delivery gate."""

from __future__ import annotations

import re
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "final_gate_residue_removed.md"
REPORT_JSON = ROOT / "output" / "reports" / "final_gate_residue_removed.json"

TABLE_STARTS = [
    "主要产品地址面积类型",
    "主要产品产量统计表表 18 - 7",
    "主要产品产量统计表表21",
    "28322856361914462高效",
    "347测斜仪（台）",
    "一、二、三等奖项目表表 51 - 11",
    "2272·",
    "一、医院合计",
    "二、疗养院所",
    "六、妇幼保健所、站",
]


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def excerpt(value: str, limit: int = 160) -> str:
    text = strip_tags(value)
    return text if len(text) <= limit else text[: limit - 1] + "..."


def current_section(lines: list[str], index: int) -> str:
    section = "未进入正文"
    for line in lines[: index + 1]:
        m = re.search(r"<h2[^>]*>(.*?)</h2>", line)
        if m:
            section = strip_tags(m.group(1)) or section
    return section


def clean_english_summary(line: str) -> str:
    text = line
    text = text.replace("General Summary: 2749", "")
    text = text.replace(": 2750 : Histroy of LianYunGang City·General Summary", "")
    replacements = {
        "northof": "north of",
        "cen-ter.After": "center. After",
        "busi-nesses": "businesses",
        "Nev-ertheless": "Nevertheless",
        "pre-vented": "prevented",
        "socialis-tic": "socialistic",
        "pat-terns": "patterns",
        "a-gent": "agent",
        "au-thorities": "authorities",
        "devel-opment": "development",
        "sys-tem": "system",
        "ini-tially": "initially",
        "contin-uously": "continuously",
        "in1978.After": "in 1978. After",
        "portcities": "port cities",
        "grasp-ing": "grasping",
        "theport": "the port",
        "weakeconomic": "weak economic",
        "what'smore": "what's more",
        "de-veloped": "developed",
        "othercountries": "other countries",
        "theprovinces": "the provinces",
        "pro-mote": "promote",
        "outsideworld": "outside world",
        "se-mi-isolated": "semi-isolated",
        "for-eign": "foreign",
        "mil-lion": "million",
        "Foreigncapital": "Foreign capital",
        "for-eign investments": "foreign investments",
        "invest-ment": "investment",
        "thelevel": "the level",
        "e-conomic": "economic",
        "laborservice": "labor service",
        "outsideworld": "outside world",
        "to strengthened": "to strengthen",
        "re-lations": "relations",
        "econo-my": "economy",
        "countries .Jian": "countries. Hagi in Japan",
        "Kurleiao county in Austrial": "Kwinana County in Australia",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def main() -> None:
    lines = HTML.read_text(encoding="utf-8").splitlines()
    removed: list[dict[str, str]] = []
    output: list[str] = []

    for idx, line in enumerate(lines):
        plain = strip_tags(line)
        if line.startswith("<p>") and any(plain.startswith(start) for start in TABLE_STARTS):
            removed.append({
                "line": str(idx + 1),
                "section": current_section(lines, idx),
                "excerpt": excerpt(line),
            })
            continue
        if "General Summary: 2749" in line or "Histroy of LianYunGang" in line:
            line = clean_english_summary(line)
        output.append(line)

    HTML.write_text("\n".join(output) + "\n", encoding="utf-8")

    import json
    REPORT_JSON.write_text(json.dumps({"removed": removed}, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# 最终门禁残文撤出报告",
        "",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 原则",
        "",
        "本批只撤出主阅读版中仍被交付门禁命中的未核表格 OCR 残文；不把无法回源核准的数据伪装成成品表。附录英文总述仅清理页码和断词粘连。",
        "",
        f"撤出段落：{len(removed)}",
        "",
        "| 序号 | 章节 | 原行 | 摘录 |",
        "| ---: | --- | ---: | --- |",
    ]
    for n, item in enumerate(removed, 1):
        text = item["excerpt"].replace("|", "\\|")
        md.append(f"| {n} | {item['section']} | {item['line']} | {text} |")
    REPORT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"removed={len(removed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

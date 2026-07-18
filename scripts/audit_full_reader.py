# -*- coding: utf-8 -*-
"""Audit current full-reader HTML and related table inventory."""

from __future__ import annotations

import re
from collections import Counter
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
TABLE_INDEX_PATH = ROOT / "output" / "structured_tables" / "index.html"
PLACEHOLDER_CSV = ROOT / "workbench" / "qa" / "baseline" / "table_placeholders.csv"
REPORT_PATH = ROOT / "output" / "reports" / "章节数据审计报告.md"


def strip_tags(value: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", value)).strip()


def extract_toc(html: str) -> list[tuple[str, str]]:
    return [
        (m.group(1), strip_tags(m.group(2)))
        for m in re.finditer(r'<li class="toc-item(?: [^"]+)?"><a href="#([^"]+)">(.+?)</a></li>', html, re.S)
    ]


def extract_headings(html: str) -> list[dict[str, str | int]]:
    headings = []
    for m in re.finditer(r'<h([23])(?:\s+id="([^"]+)")?[^>]*>(.*?)</h\1>', html, re.S):
        headings.append({"level": int(m.group(1)), "id": m.group(2) or "", "title": strip_tags(m.group(3)), "pos": m.start()})
    return headings


def count_table_site_entries() -> int:
    if not TABLE_INDEX_PATH.exists():
        return 0
    text = TABLE_INDEX_PATH.read_text(encoding="utf-8")
    return len(set(re.findall(r"LYG-[上中下]-T\d+", text)))


def section_sizes(html: str, headings: list[dict[str, str | int]]) -> list[tuple[str, int, int, int]]:
    top = [h for h in headings if h["level"] == 2]
    rows = []
    for idx, h in enumerate(top):
        start = int(h["pos"])
        end = int(top[idx + 1]["pos"]) if idx + 1 < len(top) else len(html)
        block = html[start:end]
        placeholder_count = len(re.findall(r'class="table-placeholder"', block))
        rows.append((str(h["title"]), len(block.encode("utf-8")), placeholder_count, len(re.findall(r"[ɑəɕʂʐɻŋøɛɔɡ]", block))))
    return rows


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    toc = extract_toc(html)
    ids = set(re.findall(r'\sid="([^"]+)"', html))
    missing = [title for href, title in toc if href not in ids]
    headings = extract_headings(html)
    h2 = [h for h in headings if h["level"] == 2]
    h3 = [h for h in headings if h["level"] == 3]
    placeholders = len(re.findall(r'class="table-placeholder"', html))
    none_errors = len(re.findall(r"\bNone\b", html))
    decimal_cn_period = len(re.findall(r"\d+\.。", html))
    ipa_chars = len(re.findall(r"[ɑəɕʂʐɻŋøɛɔɡ]", html))
    table_site_entries = count_table_site_entries()
    json_files = len(list((ROOT / "workbench" / "table_entries").rglob("*.json")))
    csv_files = len(list((ROOT / "workbench" / "table_entries").rglob("*.csv")))
    sections = section_sizes(html, headings)
    placeholder_by_section = Counter()
    for title, _size, count, _ipa in sections:
        if count:
            placeholder_by_section[title] += count

    lines = [
        "# 连云港市志 章节数据审计报告",
        "",
        f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> 基于: {HTML_PATH.relative_to(ROOT)}",
        "",
        "## 总体统计",
        "",
        "| 指标 | 数值 |",
        "|------|:----:|",
        f"| 全书HTML大小 | {len(html.encode('utf-8')):,} 字节 |",
        f"| TOC链接数 | {len(toc)} |",
        f"| H2标题数 | {len(h2)} |",
        f"| H3标题数 | {len(h3)} |",
        f"| 表格站登记表格 | {table_site_entries} |",
        f"| 表格JSON文件 | {json_files} |",
        f"| 表格CSV文件 | {csv_files} |",
        f"| 正文表格占位符 | {placeholders} |",
        f"| None错误 | {none_errors} |",
        f"| 小数点。残留 | {decimal_cn_period} |",
        f"| 方言IPA字符 | {ipa_chars} |",
        "",
        "## TOC 检查",
        "",
        f"- 缺失锚点：{', '.join(missing) if missing else '无'}",
        "",
        "## 表格占位符分布",
        "",
        "| 章节/最近H2 | 占位符 |",
        "|---|---:|",
    ]
    for title, count in placeholder_by_section.most_common():
        lines.append(f"| {title} | {count} |")

    lines.extend([
        "",
        "## 各 H2 章节统计",
        "",
        "| 章节 | 字节数 | 表格占位 | IPA字符 |",
        "|---|---:|---:|---:|",
    ])
    for title, size, table_count, ipa in sorted(sections, key=lambda x: x[1], reverse=True):
        lines.append(f"| {title} | {size:,} | {table_count} | {ipa} |")

    lines.extend([
        "",
        "## 验收结论",
        "",
        "- TOC锚点全部可达。" if not missing else "- TOC仍存在缺失锚点。",
        "- 正文表格占位符仍需后续按章处理。" if placeholders else "- 正文表格占位符已清零。",
        "- 本报告仅做结构审计，不代表文字校勘完成。",
    ])

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"TOC links: {len(toc)}")
    print(f"Missing anchors: {missing}")
    print(f"H2: {len(h2)} H3: {len(h3)}")
    print(f"Table site entries: {table_site_entries}")
    print(f"Placeholders: {placeholders}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Baseline repair and audit for the Lianyungang gazetteer full reader.

This script intentionally works on the current full-reader HTML as the stage-1
baseline. Chapter-by-chapter repair will later move fixes back into source MD and
structured table data.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
TABLE_INDEX_PATH = ROOT / "output" / "structured_tables" / "index.html"
REPORT_DIR = ROOT / "output" / "reports"
WORKBENCH_DIR = ROOT / "workbench" / "qa" / "baseline"
PLACEHOLDER_CSV = WORKBENCH_DIR / "table_placeholders.csv"
PLACEHOLDER_JSON = WORKBENCH_DIR / "table_placeholders.json"
TOC_CSV = WORKBENCH_DIR / "toc_links.csv"
AUDIT_REPORT = REPORT_DIR / "连云港市志_基线审计修复报告.md"


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    return unescape(value).strip()


def ensure_da_shi_ji_anchor(html: str, actions: list[str]) -> str:
    if 'id="大事记"' in html:
        return html

    pattern = re.compile(r"<p>大事记[a-zA-Z\-]+([^<]+)</p>")
    match = pattern.search(html)
    if match:
        entry = match.group(1).strip()
        replacement = f'<h2 id="大事记">大事记</h2>\n<p class="year-entry">{entry}</p>'
        html = html[: match.start()] + replacement + html[match.end() :]
        actions.append("补写 `大事记` 正文锚点，并清理标题后 OCR 噪声。")
        return html

    fallback = re.search(r"<h2 id=\"第一卷-自然环境\">", html)
    if fallback:
        html = html[: fallback.start()] + '<h2 id="大事记">大事记</h2>\n' + html[fallback.start() :]
        actions.append("未找到大事记混入段落，已在第一卷前补写 `大事记` 锚点。")
    return html


def ensure_appendix_anchor(html: str, actions: list[str]) -> str:
    if 'id="附录"' in html:
        return html

    # The appendix material currently appears after the sixtieth volume and before
    # the compilation-history heading. The heading was lost during OCR/HTML build.
    pattern = re.compile(r"(<p>《连云港市志》全书400余万字，[^<]+</p>)")
    match = pattern.search(html)
    if match:
        html = html[: match.start()] + '<h2 id="附录">附录</h2>\n' + html[match.start() :]
        actions.append("在第六十卷之后、编纂始末之前补写 `附录` 锚点。")
        return html

    fallback = re.search(r"<h2 id=\"anchor\">编纂始末</h2>|<h2 id=\"编纂始末\">编纂始末</h2>", html)
    if fallback:
        html = html[: fallback.start()] + '<h2 id="附录">附录</h2>\n' + html[fallback.start() :]
        actions.append("未找到附录正文特征段，已在编纂始末前补写 `附录` 锚点。")
    return html


def normalize_bianzuan_anchor(html: str, actions: list[str]) -> str:
    if '<h2 id="anchor">编纂始末</h2>' in html and 'href="#编纂始末"' not in html:
        html = html.replace('<h2 id="anchor">编纂始末</h2>', '<h2 id="编纂始末">编纂始末</h2>', 1)
        actions.append("将 `编纂始末` 的通用 anchor 规范为稳定锚点。")
    return html


def extract_toc(html: str) -> list[dict[str, str]]:
    links = []
    for idx, match in enumerate(re.finditer(r'<li class="toc-item(?: [^"]+)?"><a href="#([^"]+)">(.+?)</a></li>', html), 1):
        links.append({"index": str(idx), "href": match.group(1), "title": strip_tags(match.group(2))})
    return links


def extract_ids(html: str) -> set[str]:
    return set(re.findall(r'\sid="([^"]+)"', html))


def nearest_heading(html_before: str) -> tuple[str, str]:
    matches = list(re.finditer(r"<h([234])\s+[^>]*>(.*?)</h\1>", html_before, flags=re.S))
    if not matches:
        return "", ""
    last = matches[-1]
    return f"h{last.group(1)}", strip_tags(last.group(2))


def extract_table_placeholders(html: str) -> list[dict[str, str | int]]:
    placeholders = []
    line_starts = [0]
    for m in re.finditer(r"\n", html):
        line_starts.append(m.end())

    def line_number(pos: int) -> int:
        lo, hi = 0, len(line_starts)
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if line_starts[mid] <= pos:
                lo = mid
            else:
                hi = mid
        return lo + 1

    for idx, match in enumerate(re.finditer(r'<p class="table-placeholder">(.*?)</p>', html, flags=re.S), 1):
        before = html[: match.start()]
        level, heading = nearest_heading(before)
        placeholders.append(
            {
                "index": idx,
                "line": line_number(match.start()),
                "heading_level": level,
                "nearest_heading": heading,
                "text": strip_tags(match.group(1)),
                "status": "pending-structure-or-embed-check",
            }
        )
    return placeholders


def write_toc_csv(links: list[dict[str, str]], ids: set[str]) -> None:
    with TOC_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["index", "title", "href", "target_exists"])
        writer.writeheader()
        for item in links:
            writer.writerow(
                {
                    "index": item["index"],
                    "title": item["title"],
                    "href": item["href"],
                    "target_exists": "yes" if item["href"] in ids else "no",
                }
            )


def write_placeholder_files(placeholders: list[dict[str, str | int]]) -> None:
    with PLACEHOLDER_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["index", "line", "heading_level", "nearest_heading", "text", "status"],
        )
        writer.writeheader()
        for item in placeholders:
            writer.writerow(item)
    PLACEHOLDER_JSON.write_text(json.dumps(placeholders, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def count_table_site_entries() -> int:
    if not TABLE_INDEX_PATH.exists():
        return 0
    text = TABLE_INDEX_PATH.read_text(encoding="utf-8")
    return len(set(re.findall(r"LYG-[上中下]-T\d+", text)))


def write_report(
    *,
    before_missing: list[str],
    after_missing: list[str],
    actions: list[str],
    toc_links: list[dict[str, str]],
    ids: set[str],
    placeholders: list[dict[str, str | int]],
    table_site_entries: int,
    table_json_files: int,
    table_csv_files: int,
) -> None:
    heading_counts = Counter(str(item["nearest_heading"]) for item in placeholders)
    lines = [
        "# 连云港市志 基线审计修复报告",
        "",
        f"生成时间：{now_text()}",
        "",
        "## 修复动作",
        "",
    ]
    if actions:
        lines.extend(f"- {action}" for action in actions)
    else:
        lines.append("- 本轮未修改 HTML，仅重新审计。")

    lines.extend(
        [
            "",
            "## TOC 验收",
            "",
            f"- 修复前缺失锚点：{', '.join(before_missing) if before_missing else '无'}",
            f"- 修复后缺失锚点：{', '.join(after_missing) if after_missing else '无'}",
            f"- TOC 链接数：{len(toc_links)}",
            f"- HTML id 数：{len(ids)}",
            f"- TOC 明细：`{TOC_CSV.relative_to(ROOT)}`",
            "",
            "## 表格占位符账本",
            "",
            f"- 当前表格占位符：{len(placeholders)}",
            f"- 表格站登记表格：{table_site_entries}",
            f"- 表格 JSON 数据文件：{table_json_files}",
            f"- 表格 CSV 数据文件：{table_csv_files}",
            "- 说明：当前全书 HTML 仍以正文占位为主，结构化表格主要在独立表格站中展示。",
            f"- CSV 清单：`{PLACEHOLDER_CSV.relative_to(ROOT)}`",
            f"- JSON 清单：`{PLACEHOLDER_JSON.relative_to(ROOT)}`",
            "",
            "### 占位符按最近标题统计",
            "",
            "| 最近标题 | 数量 |",
            "| --- | ---: |",
        ]
    )
    for heading, count in heading_counts.most_common():
        lines.append(f"| {heading or '未识别'} | {count} |")

    lines.extend(
        [
            "",
            "## 验收结论",
            "",
            "- TOC 缺失锚点已清零。" if not after_missing else "- TOC 仍有缺失锚点，需要继续处理。",
            "- 表格占位符已形成可追踪账本，后续按章节逐项核对。",
            "- 本轮是基线修复，不代表章节文字或表格已完成最终核校。",
            "",
            "## 下一步",
            "",
            "1. 从 `序与凡例`、`总述与大事记` 开始做章节样板核对。",
            "2. 对照 `table_placeholders.csv` 逐章处理表格占位。",
            "3. 每完成一章写入 `output/reports/progress/` 并当场验收。",
        ]
    )
    AUDIT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    WORKBENCH_DIR.mkdir(parents=True, exist_ok=True)

    html = HTML_PATH.read_text(encoding="utf-8")
    before_links = extract_toc(html)
    before_ids = extract_ids(html)
    before_missing = [item["href"] for item in before_links if item["href"] not in before_ids]

    actions: list[str] = []
    fixed = ensure_da_shi_ji_anchor(html, actions)
    fixed = ensure_appendix_anchor(fixed, actions)
    fixed = normalize_bianzuan_anchor(fixed, actions)

    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")

    links = extract_toc(fixed)
    ids = extract_ids(fixed)
    after_missing = [item["href"] for item in links if item["href"] not in ids]
    placeholders = extract_table_placeholders(fixed)
    table_site_entries = count_table_site_entries()
    table_json_files = len(list((ROOT / "workbench" / "table_entries").rglob("*.json")))
    table_csv_files = len(list((ROOT / "workbench" / "table_entries").rglob("*.csv")))

    write_toc_csv(links, ids)
    write_placeholder_files(placeholders)
    write_report(
        before_missing=before_missing,
        after_missing=after_missing,
        actions=actions,
        toc_links=links,
        ids=ids,
        placeholders=placeholders,
        table_site_entries=table_site_entries,
        table_json_files=table_json_files,
        table_csv_files=table_csv_files,
    )

    print("Baseline repair complete")
    print(f"Before missing: {before_missing}")
    print(f"After missing: {after_missing}")
    print(f"TOC links: {len(links)}")
    print(f"Table placeholders: {len(placeholders)}")
    print(f"Table site entries: {table_site_entries}")
    print(f"Table JSON files: {table_json_files}")
    print(f"Table CSV files: {table_csv_files}")
    print(f"Report: {AUDIT_REPORT}")


if __name__ == "__main__":
    main()

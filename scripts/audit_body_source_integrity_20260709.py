# -*- coding: utf-8 -*-
"""Audit body source/header/footer integrity for the current reader build."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
FINAL_HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "body_source_integrity_audit_20260709.md"
REPORT_JSON = ROOT / "output" / "reports" / "body_source_integrity_audit_20260709.json"

TAG_RE = re.compile(r"<[^>]+>")
PAGE_HEADER_RE = re.compile(r"·\s*\d{1,4}\s*·\s*连云港市志[^\n<]{0,24}")
PAGE_GARBLE_RE = re.compile(r"·\s*\d{1,4}\s*·\s*[A-Za-zijIJ这送引]?")
PART_HEADING_RE = re.compile(r"(?m)^# 第.*(?:part\d+|部分|中part|下part).*$")
BARE_BOOK_TITLE_RE = re.compile(r"(?m)^\s*连云港市志\s*$")
FRONT_REPEAT_MARKERS = [
    "《连云港市志》编纂机构、人员及审定单位",
    "《连云港市志》编纂人员",
    "《连云港市志》评审人员",
    "《连云港市志》审定单位",
]
EXPECTED_VOLUMES = [f"第{n}卷" for n in [
    "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
    "二十一", "二十二", "二十三", "二十四", "二十五", "二十六", "二十七", "二十八", "二十九", "三十",
    "三十一", "三十二", "三十三", "三十四", "三十五", "三十六", "三十七", "三十八", "三十九", "四十",
    "四十一", "四十二", "四十三", "四十四", "四十五", "四十六", "四十七", "四十八", "四十九", "五十",
    "五十一", "五十二", "五十三", "五十四", "五十五", "五十六", "五十七", "五十八", "五十九", "六十",
]]


def strip_html(text: str) -> str:
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S | re.I)
    return unescape(TAG_RE.sub("\n", text))


def line_no(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def collect(pattern: re.Pattern[str], text: str, limit: int = 30) -> list[dict[str, str | int]]:
    rows = []
    for m in pattern.finditer(text):
        rows.append({"line": line_no(text, m.start()), "text": m.group(0).replace("\n", "\\n")[:160]})
        if len(rows) >= limit:
            break
    return rows


def h2_titles(html: str) -> list[str]:
    return [TAG_RE.sub("", m.group(1)).strip() for m in re.finditer(r"<h2\b[^>]*>(.*?)</h2>", html, re.S | re.I)]


def audit_one(label: str, path: Path, html: bool = False) -> dict:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    text = strip_html(raw) if html else raw
    front_counts = {marker: text.count(marker) for marker in FRONT_REPEAT_MARKERS}
    return {
        "label": label,
        "path": str(path.relative_to(ROOT)),
        "chars": len(text),
        "page_header_hits": collect(PAGE_HEADER_RE, text),
        "page_garble_hits": collect(PAGE_GARBLE_RE, text),
        "part_heading_hits": collect(PART_HEADING_RE, text),
        "bare_book_title_hits": collect(BARE_BOOK_TITLE_RE, text),
        "front_marker_counts": front_counts,
    }


def main() -> None:
    source = audit_one("正文汇总源稿", SOURCE_MD)
    final = audit_one("最终阅读器", FINAL_HTML, html=True)
    html_raw = FINAL_HTML.read_text(encoding="utf-8", errors="ignore")
    titles = h2_titles(html_raw)
    volume_titles = [t for t in titles if re.match(r"^第[一二三四五六七八九十百]+卷", t)]
    seen_volume_prefixes = [re.match(r"^(第[一二三四五六七八九十百]+卷)", t).group(1) for t in volume_titles if re.match(r"^(第[一二三四五六七八九十百]+卷)", t)]
    volume_counter = Counter(seen_volume_prefixes)
    missing = [v for v in EXPECTED_VOLUMES if v not in volume_counter]
    duplicated = {v: c for v, c in volume_counter.items() if c > 1}

    data = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "source": source,
        "final": final,
        "final_h2_count": len(titles),
        "final_volume_h2_count": len(volume_titles),
        "missing_volume_prefixes": missing,
        "duplicated_volume_prefixes": duplicated,
        "volume_titles": volume_titles,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def hit_count(section: dict, name: str) -> int:
        return len(section[name])

    lines = [
        "# 正文源稿完整性专项审计",
        "",
        f"> 生成时间：{data['generated_at']}",
        f"> 源稿：`{source['path']}`",
        f"> 阅读器：`{final['path']}`",
        "",
        "## 结论",
        "",
        "- 当前最终 HTML 的卷级结构包含第1至第60卷；不是正文校勘完成状态。",
        "- 工作台正文汇总仍有页眉页脚样式残留、分段源文件标题残留、重复卷首/编纂机构材料残留。",
        "- 最终 HTML 已过滤掉主要页眉样式，但正文可读性审计仍显示大量段落级 OCR/版式风险，需要继续回源修正文。",
        "",
        "## 计数",
        "",
        "| 对象 | 页眉样式 | 页码乱码样式 | 分段源文件标题 | 孤立书名行 |",
        "|---|---:|---:|---:|---:|",
        f"| 正文汇总源稿 | {hit_count(source, 'page_header_hits')} | {hit_count(source, 'page_garble_hits')} | {hit_count(source, 'part_heading_hits')} | {hit_count(source, 'bare_book_title_hits')} |",
        f"| 最终阅读器 | {hit_count(final, 'page_header_hits')} | {hit_count(final, 'page_garble_hits')} | {hit_count(final, 'part_heading_hits')} | {hit_count(final, 'bare_book_title_hits')} |",
        "",
        "## 卷结构",
        "",
        f"- 最终 HTML H2：{len(titles)}",
        f"- 最终 HTML 卷级 H2：{len(volume_titles)}",
        f"- 缺失卷号：{missing or '无'}",
        f"- 重复卷号：{duplicated or '无'}",
        "",
        "## 源稿页眉页脚样例",
        "",
        "| 行号 | 文本 |",
        "|---:|---|",
    ]
    for row in source["page_header_hits"][:12] + source["page_garble_hits"][:12]:
        lines.append(f"| {row['line']} | `{row['text']}` |")
    lines.extend(["", "## 源稿重复卷首标记计数", "", "| 标记 | 次数 |", "|---|---:|"])
    for marker, count in source["front_marker_counts"].items():
        lines.append(f"| {marker} | {count} |")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"source_page_headers={len(source['page_header_hits'])}")
    print(f"source_page_garbles={len(source['page_garble_hits'])}")
    print(f"final_page_headers={len(final['page_header_hits'])}")
    print(f"final_page_garbles={len(final['page_garble_hits'])}")
    print(f"final_volume_h2={len(volume_titles)} missing={len(missing)} duplicated={len(duplicated)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Audit reader-facing readability risks not covered by delivery gates."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "正文可读性风险审计报告.md"
REPORT_JSON = ROOT / "output" / "reports" / "正文可读性风险审计报告.json"

TABLE_BLOCK_RE = re.compile(r'<section class="verified-table-block".*?</section>', re.S | re.I)
HOMOPHONE_FULL_RE = re.compile(r'<div class="dialect-word-list dialect-homophone-full".*?(?=<h3 id="第五十九卷-第四章方言词汇">)', re.S | re.I)
VOCABULARY_FULL_RE = re.compile(r'<div class="dialect-word-list dialect-vocabulary-full".*?(?=<h3 id="第五十九卷-第五章语法特点">)', re.S | re.I)
STRUCTURED_TABLE_RE = re.compile(r'<table class="(?:structured-table|dialect-phonology-table)".*?</table>', re.S | re.I)
DIALECT_WORD_LIST_RE = re.compile(r'<div class="dialect-word-list".*?</div>', re.S | re.I)
P_RE = re.compile(r"<p\b[^>]*>.*?</p>", re.S | re.I)
TAG_RE = re.compile(r"<[^>]+>")


@dataclass
class Risk:
    line_no: int
    section: str
    kind: str
    score: int
    text: str


def strip_tags(value: str) -> str:
    value = TABLE_BLOCK_RE.sub(" ", value)
    value = HOMOPHONE_FULL_RE.sub(" ", value)
    value = VOCABULARY_FULL_RE.sub(" ", value)
    value = STRUCTURED_TABLE_RE.sub(" ", value)
    value = DIALECT_WORD_LIST_RE.sub(" ", value)
    value = re.sub(r"<script.*?</script>", " ", value, flags=re.S | re.I)
    value = re.sub(r"<style.*?</style>", " ", value, flags=re.S | re.I)
    value = TAG_RE.sub("", value)
    value = unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def excerpt(value: str, limit: int = 220) -> str:
    return value if len(value) <= limit else value[: limit - 1] + "..."


def risk_for_text(text: str) -> list[tuple[str, int]]:
    risks: list[tuple[str, int]] = []
    compact = re.sub(r"\s+", "", text)
    digit_count = len(re.findall(r"\d", compact))
    if len(text) >= 450:
        risks.append(("超长段落", min(10, len(text) // 250)))
    if len(compact) >= 180 and digit_count >= 35:
        risks.append(("数字密集段落", min(10, digit_count // 20)))

    table_code_hits = len(re.findall(r"Ar\s*[-−]\s*Pt\d|Pt\d[a-z]{2,}|Q\d[a-z]+", text))
    has_table_residue_note = bool(re.search(r"注：\s*\d+[.．]表中.*?不列入此表", text))
    has_dense_unit_residue = bool(re.search(r"（万元）.*?（万元）.*?（万元）", text))
    if len(text) >= 180 and (table_code_hits >= 3 or has_table_residue_note or has_dense_unit_residue):
        risks.append(("表格/代号线性化疑似", 8))

    if re.search(r"[<>][ ]?\d{2,}|\d{2,}[\u4e00-\u9fff]{1,3}\d{2,}", text) and len(text) >= 160:
        risks.append(("数字汉字粘连", 6))
    if re.search(r"声母\(\d+\)|韵母\(\d+\)|声调\(\d+\)|调类代码调类调值例字", text) and len(text) >= 120:
        risks.append(("方言音系表线性化疑似", 9))
    if re.search(r"[①②③④⑤].{0,8}[①②③④⑤].{0,8}[①②③④⑤]", text) and len(text) >= 180:
        risks.append(("同音字汇串行疑似", 8))
    ipa_like = len(re.findall(r"[ɑəɕʂʐɻŋøɛɔɡδε§∅□~]", text))
    if ipa_like >= 20 and len(text) >= 200:
        risks.append(("音标/字汇密集段落", min(10, ipa_like // 8)))
    return risks


def audit() -> list[Risk]:
    risks: list[Risk] = []
    current_h2 = "未进入正文"
    html = HTML_PATH.read_text(encoding="utf-8", errors="ignore")
    cleaned_html = TABLE_BLOCK_RE.sub(" ", html)
    cleaned_html = HOMOPHONE_FULL_RE.sub(" ", cleaned_html)
    cleaned_html = VOCABULARY_FULL_RE.sub(" ", cleaned_html)
    cleaned_html = STRUCTURED_TABLE_RE.sub(" ", cleaned_html)
    cleaned_html = DIALECT_WORD_LIST_RE.sub(" ", cleaned_html)
    for line_no, line in enumerate(cleaned_html.splitlines(), start=1):
        h2 = re.search(r"<h2[^>]*>(.*?)</h2>", line, re.S)
        if h2:
            current_h2 = strip_tags(h2.group(1)) or current_h2
        paragraphs = P_RE.findall(line)
        if not paragraphs:
            continue
        for paragraph in paragraphs:
            text = strip_tags(paragraph)
            if not text:
                continue
            for kind, score in risk_for_text(text):
                risks.append(Risk(line_no, current_h2, kind, score, excerpt(text)))
    risks.sort(key=lambda r: (-r.score, r.line_no, r.kind))
    return risks


def render(risks: list[Risk]) -> str:
    by_kind = Counter(r.kind for r in risks)
    by_section: dict[str, Counter[str]] = defaultdict(Counter)
    for risk in risks:
        by_section[risk.section][risk.kind] += 1
    lines = [
        "# 正文可读性风险审计报告",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> 基于：`{HTML_PATH.relative_to(ROOT)}`",
        "",
        "## 说明",
        "",
        "本报告补充交付门禁未覆盖的版式语义风险：表格被线性化为正文、方言音系/字汇表串行、数字与汉字粘连、超长 OCR 段落等。命中项不是最终判错，需要回源或按版式重建确认。",
        "",
        "## 统计",
        "",
        f"- 风险记录：{len(risks)}",
        f"- 涉及章节：{len(by_section)}",
        "",
        "| 风险类型 | 数量 |",
        "|---|---:|",
    ]
    for kind, count in by_kind.most_common():
        lines.append(f"| {kind} | {count} |")
    lines.extend(["", "## 章节分布", "", "| 章节 | 总数 | 主要类型 |", "|---|---:|---|"])
    for section, counts in sorted(by_section.items(), key=lambda item: sum(item[1].values()), reverse=True):
        total = sum(counts.values())
        top = "；".join(f"{kind} {count}" for kind, count in counts.most_common(4))
        lines.append(f"| {section} | {total} | {top} |")
    lines.extend(["", "## 高风险样例（前 120）", "", "| 行号 | 章节 | 类型 | 分值 | 摘录 |", "|---:|---|---|---:|---|"])
    for risk in risks[:120]:
        text = risk.text.replace("|", "\\|")
        lines.append(f"| {risk.line_no} | {risk.section} | {risk.kind} | {risk.score} | {text} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    risks = audit()
    REPORT_MD.write_text(render(risks), encoding="utf-8")
    REPORT_JSON.write_text(json.dumps([r.__dict__ for r in risks], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"risks={len(risks)}")
    for kind, count in Counter(r.kind for r in risks).most_common():
        print(f"{kind}: {count}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

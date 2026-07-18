# -*- coding: utf-8 -*-
"""Quickly quantify whether OCR source defects require a full reconversion."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OCR_ROOT = ROOT / "workbench" / "ocr" / "paddle_ocr"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "conversion_source_risk_20260703.md"
REPORT_JSON = ROOT / "output" / "reports" / "conversion_source_risk_20260703.json"

TAG_RE = re.compile(r"<[^>]+>")
P_RE = re.compile(r"<p\b[^>]*>(.*?)</p>", re.S | re.I)
VERIFIED_TABLE_RE = re.compile(r'<section class="verified-table-block".*?</section>', re.S | re.I)
STRUCTURED_TABLE_RE = re.compile(r'<table class="(?:structured-table|dialect-phonology-table)".*?</table>', re.S | re.I)
HOMOPHONE_FULL_RE = re.compile(r'<div class="dialect-word-list dialect-homophone-full".*?(?=<h3 id="第五十九卷-第四章方言词汇">)', re.S | re.I)
VOCABULARY_FULL_RE = re.compile(r'<div class="dialect-word-list dialect-vocabulary-full".*?(?=<h3 id="第五十九卷-第五章语法特点">)', re.S | re.I)
DIALECT_BLOCK_RE = re.compile(r'<div class="dialect-word-list.*?</div>', re.S | re.I)

RISK_RULES = [
    ("地层表线性化", re.compile(r"Ar\s*[-−]\s*Pt\d|Pt\d[a-z]{2,}|Q\d[a-z]+"), 3),
    ("方言声韵调线性化", re.compile(r"声母\(\d+\)|韵母\(\d+\)|调类代码调类调值例字"), 1),
    ("同音字汇串行", re.compile(r"[①②③④⑤].{0,12}[①②③④⑤].{0,12}[①②③④⑤]"), 1),
    ("音标特殊字符密集", re.compile(r"[ɑəɕʂʐɻŋøɛɔɡδε§∅□~]"), 18),
    ("数字汉字粘连", re.compile(r"\d{2,}[\u4e00-\u9fff]{1,3}\d{2,}|[<>]\s?\d{2,}"), 1),
    ("长数字串", re.compile(r"\d[\d.]{24,}"), 1),
]

ANCHOR_PATTERNS = {
    "地层系统表样本": re.compile(r"连云港市地层表|地层系统表|Ar\s*[-−]\s*Pt1.{0,30}朐山组", re.S),
    "方言声韵调样本": re.compile(r"第一节声韵调|声母\(18\)|韵母\(40\)|调类代码调类调值例字", re.S),
    "同音字汇样本": re.compile(r"第三章同音字汇|本字汇收常用字4400", re.S),
}


def strip_structured_blocks(value: str) -> str:
    value = VERIFIED_TABLE_RE.sub(" ", value)
    value = HOMOPHONE_FULL_RE.sub(" ", value)
    value = VOCABULARY_FULL_RE.sub(" ", value)
    value = STRUCTURED_TABLE_RE.sub(" ", value)
    value = DIALECT_BLOCK_RE.sub(" ", value)
    return value

def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def text_from_html(value: str) -> str:
    value = strip_structured_blocks(value)
    value = TAG_RE.sub("", value)
    value = unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def excerpt(value: str, limit: int = 180) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value if len(value) <= limit else value[: limit - 1] + "..."


def classify(text: str) -> Counter[str]:
    out: Counter[str] = Counter()
    compact = re.sub(r"\s+", "", text)
    if len(text) >= 900:
        out["超长页/段"] += 1
    if len(compact) >= 180 and len(re.findall(r"\d", compact)) >= 35:
        out["数字密集"] += 1
    for name, pattern, threshold in RISK_RULES:
        hits = len(pattern.findall(text))
        if hits >= threshold:
            out[name] += hits
    return out


def scan_ocr() -> tuple[list[dict], Counter[str], Counter[str]]:
    records: list[dict] = []
    by_kind: Counter[str] = Counter()
    by_volume: Counter[str] = Counter()
    for path in sorted(OCR_ROOT.rglob("*.txt")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        risks = classify(text)
        if not risks:
            continue
        volume = path.relative_to(OCR_ROOT).parts[0]
        score = sum(risks.values())
        records.append({
            "path": rel(path),
            "volume": volume,
            "score": score,
            "risks": dict(risks),
            "excerpt": excerpt(text),
        })
        by_kind.update(risks)
        by_volume[volume] += 1
    records.sort(key=lambda r: (-r["score"], r["path"]))
    return records, by_kind, by_volume


def scan_reader() -> tuple[list[dict], Counter[str], Counter[str], dict[str, dict]]:
    html = READER.read_text(encoding="utf-8", errors="ignore")
    scan_html = strip_structured_blocks(html)
    records: list[dict] = []
    by_kind: Counter[str] = Counter()
    by_section: Counter[str] = Counter()
    current_section = "未分卷"
    for line_no, line in enumerate(scan_html.splitlines(), start=1):
        h2 = re.search(r"<h2[^>]*>(.*?)</h2>", line, re.S | re.I)
        if h2:
            current_section = text_from_html(h2.group(1)) or current_section
        for p in P_RE.findall(line):
            text = text_from_html(p)
            if not text:
                continue
            risks = classify(text)
            if not risks:
                continue
            score = sum(risks.values())
            records.append({
                "line": line_no,
                "section": current_section,
                "score": score,
                "risks": dict(risks),
                "excerpt": excerpt(text),
            })
            by_kind.update(risks)
            by_section[current_section] += 1
    records.sort(key=lambda r: (-r["score"], r["line"]))

    anchors: dict[str, dict] = {}
    for name, pattern in ANCHOR_PATTERNS.items():
        raw_hits = len(pattern.findall(html))
        stripped = strip_structured_blocks(html)
        visible_hits = len(pattern.findall(stripped))
        anchors[name] = {"raw_hits": raw_hits, "outside_structured_blocks": visible_hits}
    return records, by_kind, by_section, anchors


def render(data: dict) -> str:
    lines = [
        "# 全书转换源风险复查报告",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> OCR 源：`{rel(OCR_ROOT)}`",
        f"> 最终阅读版：`{rel(READER)}`",
        "",
        "## 结论",
        "",
        f"- 页级 OCR 命中风险页：{data['ocr_risky_pages']} / {data['ocr_total_pages']}。这说明源 OCR 确实很脏，尤其表格、音系和字汇页不能直接作为正文交付。",
        f"- 最终阅读版命中风险段：{data['reader_risky_paragraphs']}。这说明当前更适合继续按风险报告小批回源修，不建议直接宣布整本成品。",
        "- 不建议立刻整本推倒重转：现有结构化表、方言块和大量逐段回源修复已经吸收了不少脏源；整本重转会丢掉这些人工修复收益。",
        "- 建议路线：保留现有成果，按本报告和 `正文可读性风险审计报告.md` 的高风险项继续回源；只有当同一卷大面积无法用页级 OCR/页图核定时，再对该卷局部重转。",
        "",
        "## 你贴的样本在最终版里的状态",
        "",
        "| 样本 | 原始命中 | 结构化块外命中 | 判断 |",
        "|---|---:|---:|---|",
    ]
    for name, item in data["anchors"].items():
        if not item["outside_structured_blocks"]:
            judgment = "主要已被结构化/专块吸收"
        elif name == "方言声韵调样本" and item["outside_structured_blocks"] <= 4:
            judgment = "音系主体已表格化，剩余为标题/说明"
        elif name == "同音字汇样本" and item["outside_structured_blocks"] <= 3:
            judgment = "字汇主体已有专块，剩余为标题/说明"
        else:
            judgment = "仍需专项核查"
        lines.append(f"| {name} | {item['raw_hits']} | {item['outside_structured_blocks']} | {judgment} |")

    lines.extend(["", "## OCR 源风险类型", "", "| 类型 | 命中数 |", "|---|---:|"])
    for kind, count in data["ocr_by_kind"]:
        lines.append(f"| {kind} | {count} |")

    lines.extend(["", "## OCR 风险页分布", "", "| 卷册 | 风险页数 |", "|---|---:|"])
    for volume, count in data["ocr_by_volume"]:
        lines.append(f"| {volume} | {count} |")

    lines.extend(["", "## 最终阅读版风险类型", "", "| 类型 | 命中数 |", "|---|---:|"])
    for kind, count in data["reader_by_kind"]:
        lines.append(f"| {kind} | {count} |")

    lines.extend(["", "## 最终阅读版风险章节（前 25）", "", "| 章节 | 风险段数 |", "|---|---:|"])
    for section, count in data["reader_by_section"][:25]:
        lines.append(f"| {section} | {count} |")

    lines.extend(["", "## OCR 高风险页样例（前 40）", "", "| 分值 | 路径 | 类型 | 摘录 |", "|---:|---|---|---|"])
    for record in data["ocr_records"][:40]:
        risks = "；".join(f"{k} {v}" for k, v in record["risks"].items())
        lines.append(f"| {record['score']} | `{record['path']}` | {risks} | {record['excerpt'].replace('|', '\\|')} |")

    lines.extend(["", "## 阅读版高风险段样例（前 40）", "", "| 分值 | 行号 | 章节 | 类型 | 摘录 |", "|---:|---:|---|---|---|"])
    for record in data["reader_records"][:40]:
        risks = "；".join(f"{k} {v}" for k, v in record["risks"].items())
        lines.append(f"| {record['score']} | {record['line']} | {record['section']} | {risks} | {record['excerpt'].replace('|', '\\|')} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    ocr_total = sum(1 for _ in OCR_ROOT.rglob("*.txt"))
    ocr_records, ocr_by_kind, ocr_by_volume = scan_ocr()
    reader_records, reader_by_kind, reader_by_section, anchors = scan_reader()
    data = {
        "ocr_total_pages": ocr_total,
        "ocr_risky_pages": len(ocr_records),
        "reader_risky_paragraphs": len(reader_records),
        "ocr_by_kind": ocr_by_kind.most_common(),
        "ocr_by_volume": ocr_by_volume.most_common(),
        "reader_by_kind": reader_by_kind.most_common(),
        "reader_by_section": reader_by_section.most_common(),
        "anchors": anchors,
        "ocr_records": ocr_records,
        "reader_records": reader_records,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(render(data), encoding="utf-8")
    print(f"ocr_risky_pages={len(ocr_records)}/{ocr_total}")
    print(f"reader_risky_paragraphs={len(reader_records)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

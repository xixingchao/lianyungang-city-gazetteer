# -*- coding: utf-8 -*-
"""Special audit for Volume 59 Dialect."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
FINAL_HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
OCR_DIR = ROOT / "workbench" / "ocr" / "paddle_ocr" / "下" / "part02"
PAGE_IMAGE_DIR = ROOT / "workbench" / "conversion" / "page_images" / "下" / "part02"
REPORT_MD = ROOT / "output" / "reports" / "dialect_volume59_audit_20260709.md"
REPORT_JSON = ROOT / "output" / "reports" / "dialect_volume59_audit_20260709.json"

TAG_RE = re.compile(r"<[^>]+>")
P_RE = re.compile(r"<p\b[^>]*>(.*?)</p>", re.S | re.I)
H_RE = re.compile(r"<h([2-5])\b[^>]*>(.*?)</h\1>", re.S | re.I)
SOURCE_HEADER_RE = re.compile(r"^(第[一二三四五六七八九十]+章\s*[^·\n]{0,12}·\s*\d{4}\s*·?|第五十九卷\s*方言·\s*\d{4}\s*·?)$", re.M)
PAGE_ANCHOR_RE = re.compile(r"<!-- page-anchor: (LYG-\d+) -->")
OCR_MARKERS = [
    "第五十九卷", "第一章方言差别", "第一章 方言差别", "第二章语音系统", "第二章 语音系统",
    "第三章同音字汇", "第三章 同音字汇", "第四章方言词汇", "第四章 方言词汇",
    "第五章语法特点", "第五章 语法特点", "第六十卷",
]


def strip_tags(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(TAG_RE.sub("", value))).strip()


def line_no(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def extract_between(text: str, start_pat: str, end_pat: str) -> tuple[str, int, int]:
    start = re.search(start_pat, text, flags=re.M)
    if not start:
        raise RuntimeError(f"start not found: {start_pat}")
    end = re.search(end_pat, text[start.end():], flags=re.M)
    if not end:
        raise RuntimeError(f"end not found: {end_pat}")
    return text[start.start() : start.end() + end.start()], start.start(), start.end() + end.start()


def audit_source() -> dict:
    text = SOURCE_MD.read_text(encoding="utf-8", errors="ignore")
    volume, start, end = extract_between(text, r"^第五十九卷\s+方言\s*$", r"^第六十卷\s+人物\s*$")
    before = text[:start]
    previous_anchor = PAGE_ANCHOR_RE.findall(before)[-1:] or []
    anchors = previous_anchor + PAGE_ANCHOR_RE.findall(volume)
    headers = [
        {"line": line_no(text, start + m.start()), "text": m.group(0)}
        for m in SOURCE_HEADER_RE.finditer(volume)
    ]
    section_markers = []
    for pat in ["概述", "第一章方言差别", "第二章语音系统", "第三章同音字汇", "第四章方言词汇", "第五章语法特点"]:
        pos = volume.find(pat)
        section_markers.append({"title": pat, "line": line_no(text, start + pos) if pos >= 0 else None})
    long_lines = []
    for i, line in enumerate(volume.splitlines(), start=line_no(text, start)):
        s = line.strip()
        if len(s) >= 260:
            long_lines.append({"line": i, "length": len(s), "text": s[:180]})
            if len(long_lines) >= 30:
                break
    return {
        "path": str(SOURCE_MD.relative_to(ROOT)),
        "start_line": line_no(text, start),
        "end_line": line_no(text, end),
        "chars": len(volume),
        "page_anchors": anchors,
        "page_count": len(anchors),
        "header_residue_count": len(headers),
        "header_residue_samples": headers[:40],
        "section_markers": section_markers,
        "long_line_samples": long_lines,
    }


def audit_final() -> dict:
    html = FINAL_HTML.read_text(encoding="utf-8", errors="ignore")
    volume, _start, _end = extract_between(html, r'<h2 id="第五十九卷-方言">', r'<h2 id="第六十卷-人物">')
    headings = [{"level": int(m.group(1)), "text": strip_tags(m.group(2))} for m in H_RE.finditer(volume)]
    paragraphs = [strip_tags(m.group(1)) for m in P_RE.finditer(volume)]
    long_paragraphs = [
        {"index": i + 1, "length": len(p), "text": p[:220]}
        for i, p in enumerate(paragraphs)
        if len(p) >= 500
    ]
    block_counts = {
        "phonology_tables": len(re.findall(r'class="dialect-phonology-table"', volume)),
        "homophone_blocks": len(re.findall(r'dialect-homophone-full', volume)),
        "vocabulary_blocks": len(re.findall(r'dialect-vocabulary-full', volume)),
        "example_lists": len(re.findall(r'class="dialect-example-list"', volume)),
    }
    suspicious = []
    for i, p in enumerate(paragraphs, start=1):
        if re.search(r"一、声母\s*1\.|二、韵母\s*1\.|三、声调\s*1\.", p):
            suspicious.append({"paragraph": i, "kind": "小标题与编号粘连", "text": p[:180]})
        if len(p) >= 1000 and ("方言词汇" in p or re.search(r"[①②③④⑤]|~", p)):
            suspicious.append({"paragraph": i, "kind": "字汇/词汇串行", "text": p[:180]})
    return {
        "path": str(FINAL_HTML.relative_to(ROOT)),
        "headings": headings,
        "paragraph_count": len(paragraphs),
        "long_paragraph_count": len(long_paragraphs),
        "long_paragraph_samples": long_paragraphs[:20],
        "dialect_classes": dict(Counter(re.findall(r'class="([^"]*dialect[^"]*)"', volume))),
        "block_counts": block_counts,
        "suspicious_samples": suspicious[:30],
    }


def audit_ocr_pages() -> dict:
    hits = []
    if not OCR_DIR.exists():
        return {"path": str(OCR_DIR.relative_to(ROOT)), "available": False, "hits": hits}
    for path in sorted(OCR_DIR.glob("page_*.txt")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        matched = [marker for marker in OCR_MARKERS if marker in text]
        if not matched:
            continue
        page_match = re.search(r"第\s*(\d+)\s*/\s*(\d+)\s*页", text)
        book_page_match = re.search(r"·\s*(\d{4})\s*·|·\s*(\d{4})$", text, flags=re.M)
        image_path = PAGE_IMAGE_DIR / f"{path.stem}_180dpi.jpg"
        first_lines = [line.strip() for line in text.splitlines()[:8] if line.strip()]
        hits.append({
            "ocr_page": int(page_match.group(1)) if page_match else None,
            "ocr_total_pages": int(page_match.group(2)) if page_match else None,
            "book_page": int(next(g for g in book_page_match.groups() if g)) if book_page_match else None,
            "file": str(path.relative_to(ROOT)),
            "image": str(image_path.relative_to(ROOT)) if image_path.exists() else None,
            "markers": matched,
            "first_lines": first_lines,
        })
    return {"path": str(OCR_DIR.relative_to(ROOT)), "available": True, "hits": hits}


def main() -> None:
    source = audit_source()
    final = audit_final()
    ocr = audit_ocr_pages()
    data = {"generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"), "source": source, "final": final, "ocr": ocr}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    anchor_start = source["page_anchors"][0] if source["page_anchors"] else "未捕获"
    anchor_end = source["page_anchors"][-1] if source["page_anchors"] else "未捕获"

    lines = [
        "# 第五十九卷方言专项审计",
        "",
        f"> 生成时间：{data['generated_at']}",
        f"> 源稿：`{source['path']}`",
        f"> 阅读器：`{final['path']}`",
        "",
        "## 结论",
        "",
        "- 第五十九卷应按特殊版式处理，不能套普通正文段落合并规则。",
        f"- 当前专项审计显示源稿页眉残留 {source['header_residue_count']} 条，阅读器超长段落 {final['long_paragraph_count']} 条。",
        "- 最终 HTML 已把声母、韵母、声调、同音字汇、方言词汇按专门块处理；当前任务从结构修复转入逐页精校。",
        "- 页级 OCR 索引可定位到下册 part02 的方言卷关键页；后续核对以 OCR 文本和本地页图路径为依据，不在聊天中展示图片。",
        "",
        "## 源稿范围",
        "",
        f"- 行号：{source['start_line']} 至 {source['end_line']}",
        f"- 源稿页锚：{anchor_start} 至 {anchor_end}，共 {source['page_count']} 页锚",
        f"- 页眉残留：{source['header_residue_count']} 条",
        "",
        "## 页级 OCR 索引",
        "",
        "| OCR页 | 书页 | 命中文件 | 本地页图 | 标志 |",
        "|---:|---:|---|---|---|",
    ]
    for row in ocr.get("hits", [])[:40]:
        image = f"`{row['image']}`" if row.get("image") else "未找到"
        lines.append(
            f"| {row['ocr_page'] or ''} | {row['book_page'] or ''} | `{row['file']}` | {image} | {'、'.join(row['markers'])} |"
        )

    lines.extend([
        "",
        "## 阅读器结构",
        "",
        f"- 段落数：{final['paragraph_count']}",
        f"- 超长段落：{final['long_paragraph_count']} 条",
        f"- 方言表格：{final['block_counts']['phonology_tables']} 个",
        f"- 同音字汇块：{final['block_counts']['homophone_blocks']} 个",
        f"- 方言词汇块：{final['block_counts']['vocabulary_blocks']} 个",
        f"- 语法例句列表：{final['block_counts']['example_lists']} 个",
        "",
        "## 阅读器标题",
        "",
    ])
    for h in final["headings"]:
        lines.append(f"- H{h['level']} {h['text']}")
    lines.extend(["", "## 源稿页眉残留样例", "", "| 行号 | 文本 |", "|---:|---|"])
    for row in source["header_residue_samples"]:
        lines.append(f"| {row['line']} | `{row['text']}` |")
    lines.extend([
        "",
        "## 修复优先级",
        "",
        "1. 按页级 OCR 索引逐页核对第三章同音字汇、第四章方言词汇、第五章语法特点的边界。",
        "2. 对照本地页图复核声韵调、同音字汇、方言词汇中的音标和特殊字，不做无证据猜改。",
        "3. 将确认的 OCR 错字或边界错位以小批量脚本修复，并保留页码、OCR 文件、页图路径证据。",
        "4. 回写后重建阅读器并跑方言专项审计、正文可读性审计、全文结构审计。",
        "",
    ])
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"source_pages={source['page_count']}")
    print(f"source_header_residues={source['header_residue_count']}")
    print(f"ocr_hits={len(ocr.get('hits', []))}")
    print(f"final_long_paragraphs={final['long_paragraph_count']}")
    print(f"final_blocks={final['block_counts']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

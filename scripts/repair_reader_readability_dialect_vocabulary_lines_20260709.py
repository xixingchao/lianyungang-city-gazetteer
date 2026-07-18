# -*- coding: utf-8 -*-
"""Rebuild 第五十九卷方言词汇 as line-preserved specialist word-list text."""

from __future__ import annotations

import json
import re
from datetime import datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SOURCE = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_dialect_vocabulary_lines_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_dialect_vocabulary_lines_20260709.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷方言词汇压平修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

START = '<h3 id="第五十九卷-第四章方言词汇">第四章方言词汇</h3>'
END = '<h3 id="第五十九卷-第五章语法特点">第五章语法特点</h3>'
SOURCE_START = "第四章方言词汇"
SOURCE_END = "第五章语法特点"
SOURCE_NOTE = "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:14682-16861"

TAG_RE = re.compile(r"<[^>]+>")
P_RE = re.compile(r"<p\b[^>]*>(.*?)</p>", re.S | re.I)
HEAD_RE = re.compile(r"^[A-Za-z0-9εəæɑδ§∅şSXPcztkpmiuãēioyIQ\.'’°-]{1,8}$")


def source_lines() -> list[str]:
    source = SOURCE.read_text(encoding="utf-8")
    start = source.index(SOURCE_START)
    end = source.index(SOURCE_END, start + len(SOURCE_START))
    lines = [line.strip() for line in source[start:end].splitlines() if line.strip()]
    if not lines or lines[0] != SOURCE_START:
        raise RuntimeError("unexpected vocabulary source heading")
    filtered = [line for line in lines[1:] if not (line.startswith("<!--") and line.endswith("-->"))]
    if len(filtered) < 1300:
        raise RuntimeError(f"vocabulary source looks truncated: {len(filtered)} lines")
    return filtered


def make_paragraph(line: str) -> str:
    value = escape(line, quote=False)
    if HEAD_RE.match(line):
        value = f'<span class="dialect-word-head">{value}</span>'
    return f"<p>{value}</p>"


def build_block(lines: list[str]) -> str:
    intro_lines = lines[:3]
    body_lines = lines[3:]
    intro = f"<p>{escape(''.join(intro_lines), quote=False)}</p>"
    paragraphs = "\n".join(make_paragraph(line) for line in body_lines)
    return "\n" + intro + "\n" + '<div class="dialect-word-list dialect-vocabulary-full">' + "\n" + paragraphs + "\n</div>\n"


def count_long_paragraphs(block: str, limit: int = 500) -> int:
    count = 0
    for match in P_RE.finditer(block):
        text = TAG_RE.sub("", match.group(1)).strip()
        if len(text) > limit:
            count += 1
    return count


def patch_reader() -> dict[str, object]:
    lines = source_lines()
    html = HTML.read_text(encoding="utf-8")
    start = html.index(START) + len(START)
    end = html.index(END, start)
    old_block = html[start:end]
    new_block = build_block(lines)
    changed = old_block != new_block
    if changed:
        HTML.write_text(html[:start] + new_block + html[end:], encoding="utf-8")
    return {
        "changed": changed,
        "source_effective_lines": len(lines),
        "word_list_lines": len(lines) - 3,
        "old_long_paragraphs_over_500": count_long_paragraphs(old_block),
        "new_long_paragraphs_over_500": count_long_paragraphs(new_block),
    }


def write_reports(result: dict[str, object]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十九卷方言 / 第四章方言词汇",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "principle": "依据源文行界重建方言词汇块；不改写词条、音值、释义，只恢复行界。",
        "result": result,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第五十九卷方言词汇压平修复

- 时间：{now}
- 范围：`第五十九卷方言 / 第四章方言词汇`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 使用源文 `第四章方言词汇` 到 `第五章语法特点` 之间的有效行重建阅读版词汇块。
- 保留说明段，说明段之后每个源文有效行输出为一个词汇小段落。
- 本轮不重录、不猜改词条、音值、释义，只恢复行界和词汇表版式。

## 结果

- 阅读版发生改写：{result['changed']}
- 源文有效行：{result['source_effective_lines']}
- 词汇小段落：{result['word_list_lines']}
- 当前运行前本章超过 500 字的段落：{result['old_long_paragraphs_over_500']}
- 当前运行后本章超过 500 字的段落：{result['new_long_paragraphs_over_500']}
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(result: dict[str, object]) -> None:
    marker = "## 2026-07-09 第五十九卷方言词汇压平修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十九卷方言 `第四章方言词汇` 超大串行块进行修复。
- 源文依据：`{SOURCE_NOTE}`，按源文有效行重建词汇块，不改写词条、音值、释义。
- 输出词汇小段落 {result['word_list_lines']} 行；本章超过 500 字段落由 {result['old_long_paragraphs_over_500']} 降为 {result['new_long_paragraphs_over_500']}。
- 报告：`output/reports/reader_readability_dialect_vocabulary_lines_20260709.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    result = patch_reader()
    write_reports(result)
    update_memory(result)
    print("dialect vocabulary lines rebuilt")
    print(f"changed={int(result['changed'])}")
    print(f"word_list_lines={result['word_list_lines']}")
    print(f"long_paragraphs_after={result['new_long_paragraphs_over_500']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

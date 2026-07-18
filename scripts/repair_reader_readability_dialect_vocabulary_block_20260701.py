# -*- coding: utf-8 -*-
"""Mark 第五十九卷第四章方言词汇 as a specialist vocabulary block."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_dialect_vocabulary_block_20260701.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_dialect_vocabulary_block_20260701.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260701_第五十九卷方言词汇章词汇块标记.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

START = '<h3 id="第五十九卷-第四章方言词汇">第四章方言词汇</h3>'
END = '<h3 id="第五十九卷-第五章语法特点">第五章语法特点</h3>'
INTRO_RE = re.compile(r"^(\s*<p>本章记录连云港市城区的方言词约1600条.*?</p>)(.*)$", re.S)
WRAP_RE = re.compile(r'^\s*<div class="dialect-word-list dialect-vocabulary-full">.*</div>\s*$', re.S)


def write_artifacts(paragraph_count: int) -> None:
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "scope": "第五十九卷方言 第四章方言词汇",
        "html_path": str(HTML_PATH),
        "principle": "方言词汇章属于带音值、释义和例词的专门词汇表；保留内容，仅标记版式语义。",
        "wrapped_paragraphs": paragraph_count,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_MD.write_text(f"""# 第五十九卷方言词汇章词汇块标记报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 修复对象

最终阅读版 `第五十九卷方言 / 第四章方言词汇` 的词条正文。该章是带音值、释义、例词的专门词汇表，不是普通叙述段落。

## 处理方式

保留章节说明段，保留后续词条内容，不改写字词、音值和释义；仅将说明段之后、`第五章语法特点` 之前的词条正文包入 `dialect-word-list dialect-vocabulary-full` 容器。

## 结果

- 包入词汇块的 `<p>` 段落数：{paragraph_count}
""", encoding="utf-8")
    PROGRESS_PATH.write_text(f"""# 第五十九卷方言词汇章词汇块标记

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成

- 将 `第四章方言词汇` 说明段之后的词条正文整体标记为 `dialect-word-list dialect-vocabulary-full`。
- 本次不删除、不改写词条内容，只修复版式语义标记。
- 包入词汇块段落数：{paragraph_count}。
""", encoding="utf-8")
    marker = "## 2026-07-01 第五十九卷方言词汇章词汇块标记"
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    if marker not in memory:
        MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + f"""{marker}

- 新增脚本：`scripts/repair_reader_readability_dialect_vocabulary_block_20260701.py`。
- 将最终阅读版第五十九卷方言 `第四章方言词汇` 说明段之后、`第五章语法特点` 之前的词条正文整体包入 `dialect-word-list dialect-vocabulary-full`，包入段落 {paragraph_count} 段。
- 本批不删除、不改写词条内容，只把专门词汇表从普通正文风险审计中区分出来。
- 报告：`output/reports/reader_readability_dialect_vocabulary_block_20260701.md`。
""", encoding="utf-8")


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    start = html.index(START) + len(START)
    end = html.index(END)
    chapter = html[start:end]
    match = INTRO_RE.match(chapter)
    if not match:
        raise RuntimeError("Cannot split dialect vocabulary intro and body")
    intro, body = match.groups()
    if WRAP_RE.match(body):
        paragraph_count = len(re.findall(r"<p\b", body))
    else:
        paragraph_count = len(re.findall(r"<p\b", body))
        if paragraph_count < 2:
            raise RuntimeError(f"vocabulary body looks too small: {paragraph_count} paragraphs")
        wrapped = intro + '<div class="dialect-word-list dialect-vocabulary-full">' + body.strip() + "</div>"
        HTML_PATH.write_text(html[:start] + wrapped + html[end:], encoding="utf-8")
    write_artifacts(paragraph_count)
    print("dialect vocabulary chapter marked as word-list block")
    print(f"wrapped_paragraphs={paragraph_count}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

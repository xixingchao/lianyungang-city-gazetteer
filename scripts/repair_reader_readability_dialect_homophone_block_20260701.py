# -*- coding: utf-8 -*-
"""Mark the whole 第五十九卷同音字汇 body as a specialist word-list block."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_dialect_homophone_block_20260701.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_dialect_homophone_block_20260701.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260701_第五十九卷同音字汇整章字汇块标记.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

START = '<h3 id="第五十九卷-第三章同音字汇">第三章同音字汇</h3>'
END = '<h3 id="第五十九卷-第四章方言词汇">第四章方言词汇</h3>'
INTRO_RE = re.compile(r"^(\s*<p>本字汇收常用字4400多个.*?</p>)(.*)$", re.S)
WRAP_RE = re.compile(r'^\s*<div class="dialect-word-list dialect-homophone-full">.*</div>\s*$', re.S)


def write_reports(paragraph_count: int) -> None:
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "scope": "第五十九卷方言 第三章同音字汇",
        "html_path": str(HTML_PATH),
        "principle": "同音字汇整章属于专门字汇表，保留原内容，仅用字汇块容器标记，避免按普通正文段落审计。",
        "wrapped_paragraphs": paragraph_count,
        "source_ocr_pages": [f"workbench/ocr/paddle_ocr/下/part02/page_{i:04d}.txt" for i in range(303, 313)],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_MD.write_text(f"""# 第五十九卷同音字汇整章字汇块标记报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 修复对象

最终阅读版 `第五十九卷方言 / 第三章同音字汇` 的字汇正文。该章不是普通叙述正文，而是按韵母、声母、声调排列的专门字汇表。

## 处理方式

保留章节说明段，保留后续字汇内容，不改写字词和音标；仅将说明段之后、`第四章方言词汇` 之前的字汇内容包入 `dialect-word-list dialect-homophone-full` 容器，使阅读样式和可读性审计按“字汇表”处理。

## 结果

- 包入字汇块的 `<p>` 段落数：{paragraph_count}
- 源 OCR 参考页：`workbench/ocr/paddle_ocr/下/part02/page_0303.txt` 至 `page_0312.txt`
""", encoding="utf-8")


def write_progress(paragraph_count: int) -> None:
    PROGRESS_PATH.write_text(f"""# 第五十九卷同音字汇整章字汇块标记

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 已完成

- 将 `第三章同音字汇` 说明段之后的字汇正文整体标记为 `dialect-word-list dialect-homophone-full`。
- 本次不删除、不改写字汇内容，只修复版式语义标记。
- 包入字汇块段落数：{paragraph_count}。

## 下一步

- 复跑 `scripts/audit_reader_readability_risks.py`，确认同音字汇串行疑似从普通正文风险中退出。
- 继续处理剩余章节中真正的表格线性化和超长 OCR 段落。
""", encoding="utf-8")


def update_memory(paragraph_count: int) -> None:
    marker = "## 2026-07-01 第五十九卷同音字汇整章字汇块标记"
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 新增脚本：`scripts/repair_reader_readability_dialect_homophone_block_20260701.py`。
- 将最终阅读版第五十九卷方言 `第三章同音字汇` 说明段之后、`第四章方言词汇` 之前的字汇正文整体包入 `dialect-word-list dialect-homophone-full`，包入段落 {paragraph_count} 段。
- 本批不删除、不改写字汇内容，只把专门字汇表从普通正文风险审计中区分出来。
- 报告：`output/reports/reader_readability_dialect_homophone_block_20260701.md`。
"""
    MEMORY_PATH.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    start = html.index(START) + len(START)
    end = html.index(END)
    chapter = html[start:end]
    match = INTRO_RE.match(chapter)
    if not match:
        raise RuntimeError("Cannot split homophone intro and body")
    intro, body = match.groups()
    if WRAP_RE.match(body):
        paragraph_count = len(re.findall(r"<p\b", body))
        print("homophone block already wrapped")
    else:
        paragraph_count = len(re.findall(r"<p\b", body))
        if paragraph_count < 2:
            raise RuntimeError(f"homophone body looks too small: {paragraph_count} paragraphs")
        wrapped = intro + '<div class="dialect-word-list dialect-homophone-full">' + body.strip() + "</div>"
        html = html[:start] + wrapped + html[end:]
        HTML_PATH.write_text(html, encoding="utf-8")
    write_reports(paragraph_count)
    write_progress(paragraph_count)
    update_memory(paragraph_count)
    print("dialect homophone chapter marked as word-list block")
    print(f"wrapped_paragraphs={paragraph_count}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

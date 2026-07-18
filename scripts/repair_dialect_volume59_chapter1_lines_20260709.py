# -*- coding: utf-8 -*-
"""Rebuild Volume 59 chapter 1 as line-preserved dialect examples."""

from __future__ import annotations

import json
from datetime import datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SOURCE = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
REPORT_MD = ROOT / "output" / "reports" / "dialect_volume59_chapter1_lines_20260709.md"
REPORT_JSON = ROOT / "output" / "reports" / "dialect_volume59_chapter1_lines_20260709.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷方言第一章行界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

HTML_START = '<h3 id="第五十九卷-第一章方言差别">第一章方言差别</h3>'
HTML_END = '<h3 id="第五十九卷-第二章语音系统">第二章语音系统</h3>'
SOURCE_START = "第一章方言差别"
SOURCE_END = "第二章语音系统"
SOURCE_NOTE = "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:13411-13675"

HEADINGS = {
    "第一节语音差别": '<h4 id="第五十九卷-第一章方言差别-第一节语音差别">第一节语音差别</h4>',
    "第二节词汇语法差别": '<h4 id="第五十九卷-第一章方言差别-第二节词汇语法差别">第二节词汇语法差别</h4>',
    "一、声母": "<h5>一、声母</h5>",
    "二、韵母": "<h5>二、韵母</h5>",
    "三、声调": "<h5>三、声调</h5>",
}


def source_lines() -> list[str]:
    source = SOURCE.read_text(encoding="utf-8")
    start = source.index(SOURCE_START)
    end = source.index(SOURCE_END, start + len(SOURCE_START))
    lines = [line.strip() for line in source[start:end].splitlines() if line.strip()]
    if lines[0] != SOURCE_START:
        raise RuntimeError("unexpected chapter 1 source start")
    if len(lines) < 200:
        raise RuntimeError(f"chapter 1 source looks truncated: {len(lines)} lines")
    return lines


def make_html(lines: list[str]) -> str:
    html = [HTML_START]
    for line in lines[1:]:
        if line in HEADINGS:
            html.append(HEADINGS[line])
        else:
            html.append(f"<p>{escape(line, quote=False)}</p>")
    return "\n" + "\n".join(html) + "\n"


def patch_reader() -> dict[str, object]:
    lines = source_lines()
    html = HTML.read_text(encoding="utf-8")
    start = html.index(HTML_START)
    end = html.index(HTML_END, start)
    old = html[start:end]
    new = make_html(lines)
    changed = old != new
    if changed:
        HTML.write_text(html[:start] + new + html[end:], encoding="utf-8")
    return {
        "changed": changed,
        "source_lines": len(lines),
        "body_paragraphs": new.count("<p>"),
        "h4_count": new.count("<h4"),
        "h5_count": new.count("<h5"),
    }


def write_reports(result: dict[str, object]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十九卷方言 / 第一章方言差别",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "principle": "依据源稿行界重建第一章，保留示例表行，不改写文字、音值和例字。",
        "result": result,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第五十九卷方言第一章行界修复

- 时间：{now}
- 范围：`第五十九卷方言 / 第一章方言差别`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 用源稿 `第一章方言差别` 到 `第二章语音系统` 之间的有效行重建阅读器第一章。
- 恢复 `第一节语音差别`、`第二节词汇语法差别`、`一、声母`、`二、韵母`、`三、声调` 标题边界。
- 示例表、音值行、词汇对照行按源稿行界保留为独立段落。
- 不改写文字、音值和例字。

## 结果

- 阅读版发生改写：{result['changed']}
- 源稿有效行：{result['source_lines']}
- 输出正文小段落：{result['body_paragraphs']}
- H4：{result['h4_count']}
- H5：{result['h5_count']}
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(result: dict[str, object]) -> None:
    marker = "## 2026-07-09 第五十九卷方言第一章行界修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 用源稿行界重建第五十九卷方言第一章 `方言差别`，保留语音示例表和词汇对照行。
- 输出正文小段落 {result['body_paragraphs']} 段；不改写文字、音值和例字。
- 报告：`output/reports/dialect_volume59_chapter1_lines_20260709.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    result = patch_reader()
    write_reports(result)
    update_memory(result)
    print("dialect chapter1 lines rebuilt")
    print(f"changed={int(result['changed'])}")
    print(f"paragraphs={result['body_paragraphs']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

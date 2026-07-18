# -*- coding: utf-8 -*-
"""Repair and audit 第六十卷 人物 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第六十卷人物_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第六十卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="附录">|</main>)', re.S)
SOURCE_RE = re.compile(r'(^第六十卷.*?)(?=^附录|\Z)', re.S | re.M)

CHAPTERS = ["第一章传略", "第二章简介", "第三章名录"]
EXPECTED_H3 = len(CHAPTERS)
EXPECTED_H4 = 0


def h3(title: str) -> str:
    return f'<h3 id="第六十卷-{title}">{title}</h3>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section
    replacements = {
        "第六十卷\n第一章传　略": "第六十卷 人物\n\n第一章传略",
        "第一章传略：2633·\n": "",
        "第二章　简介": "第二章简介",
        "第三章名录\n、连云港市市区革命烈士简况表": "第三章名录\n连云港市市区革命烈士简况表",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[:m.start(1)] + section + text[m.end(1):]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第六十卷卷题、三章标题及名录表题断裂。"]
    return []


def sub_once(section: str, pattern: str, repl: str) -> str:
    section, _ = re.subn(pattern, repl, section, count=1, flags=re.S)
    return section


def apply_replacements(section: str) -> str:
    section = re.sub(r'<h2 id="第六十卷-[^"]+">.*?</h2>', '<h2 id="第六十卷-人物">第六十卷人物</h2>', section, count=1, flags=re.S)
    if h3("第一章传略") not in section:
        section = section.replace('<h2 id="第六十卷-人物">第六十卷人物</h2>\n<p>', '<h2 id="第六十卷-人物">第六十卷人物</h2>\n' + h3("第一章传略") + '\n<p>', 1)
    if h3("第二章简介") not in section:
        section = section.replace('<p>王谟（？～？）', h3("第二章简介") + '\n<p>王谟（？～？）', 1)
    if h3("第三章名录") not in section:
        section = section.replace('<p>、连云港市市区革命烈士简况表', h3("第三章名录") + '\n<p>连云港市市区革命烈士简况表', 1)
    return section


def cleanup(section: str) -> str:
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'<p>\s*(<h3 id="第六十卷-[^"]+">)', r'\1', section)
    section = re.sub(r'(</h3>)\s*</p>', r'\1', section)
    section = re.sub(r'(<p>[^<]*)(<h3 id="第六十卷-[^"]+">)', r'\1</p>\n\2', section)
    section = re.sub(r'(<h3 id="第六十卷-[^"]+">[^<]+</h3>)\s*([^<\s])', r'\1\n<p>\2', section)
    seen: set[str] = set()

    def keep(match: re.Match[str]) -> str:
        ident = match.group(1)
        if ident in seen:
            return ''
        seen.add(ident)
        return match.group(0)

    return re.sub(r'<h3 id="([^"]+)">[^<]+</h3>\s*', keep, section)


def restore_html() -> dict[str, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第六十卷 HTML range")
    section = cleanup(apply_replacements(cleanup(m.group(0))))
    HTML_PATH.write_text(html[:m.start()] + section + html[m.end():], encoding="utf-8")
    return audit_section()


def audit_section() -> dict[str, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    block = SECTION_RE.search(html).group(0)
    return {
        "bytes": len(block.encode("utf-8")),
        "h2_count": block.count("<h2 "),
        "h3_count": block.count("<h3 "),
        "h4_count": block.count("<h4 "),
        "table_placeholders": block.count('class="table-placeholder"'),
        "structured_tables": block.count('<table class="structured-table"'),
        "generic_heading_anchors": len(re.findall(r'<h[234] id="anchor">', block)),
        "embedded_h3_in_p": len(re.findall(r'<p[^>]*>[^<]*<h3', block)),
        "embedded_h4_in_p": len(re.findall(r'<p[^>]*>[^<]*<h4', block)),
        "malformed_heading_ids": len(re.findall(r'<h[34] id="[^"]*<h[34]', block)),
    }


def write_progress(stats: dict[str, int], changes: list[str]) -> None:
    status = "通过" if stats["h3_count"] == EXPECTED_H3 and stats["h4_count"] == EXPECTED_H4 and stats["generic_heading_anchors"] == 0 and stats["embedded_h3_in_p"] == 0 else "需复核"
    content = f"""# 2026-06-29 第六十卷《人物》修复核对进度

## 本轮范围
- 范围：`第六十卷 人物`。
- 目标：按交付标准修复卷题、3 个章级标题，并保留人物名录表格对象。
- 源文件：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已完成规范化，脚本复跑保持幂等'}。
- 将最终阅读页卷题统一为 `第六十卷人物`。
- 恢复 `第一章传略`、`第二章简介`、`第三章名录` 三个 H3 层级。
- 修正第三章名录起始表题前的残留顿号。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}，H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本轮保留现有结构化表格，不重建烈士名录等长表；后续需结合 PDF 原图进行表格专项核对。
- 本卷人物条目 OCR 字词仍需后续文字专项核对，本轮只处理卷章结构与表题边界。

## 遇到的问题与处理
- HTML 卷题只显示 `第六十卷`，源 MD 卷题缺 `人物`，已统一补足。
- 转换后章题被吞入正文，最终页无法直接检索 `第一章传略`、`第二章简介`、`第三章名录`，已按源 MD 与章节骨架定位恢复。
- 第三章名录起始处原为 `、连云港市市区革命烈士简况表`，已在章节标题后改为正常表题。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 进入附录、跋、编纂始末的收尾结构核对，并开始汇总剩余表格专项清单。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第六十卷人物章节核对完成

已完成 `第六十卷 人物` 章节格式核对：

- 新增脚本：`scripts/repair_sixtieth_volume_people.py`。
- 修复第六十卷卷题缺名、最终阅读页无 H3 导航层级、章题被正文吞并和第三章表题前残留顿号。
- 第六十卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（第一章传略、第二章简介、第三章名录），H4={stats['h4_count']}。
- 第六十卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，段落内嵌标题问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处。
- 已写入进度文档：`output/reports/progress/20260629_第六十卷人物_修复核对进度.md`。

验收：第六十卷 HTML 字节数 {stats['bytes']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：附录、跋、编纂始末结构收尾与表格专项清单。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第六十卷人物章节核对完成"
    if marker in memory:
        memory = memory[: memory.find(marker)].rstrip() + "\n" + entry
    else:
        memory = memory.rstrip() + "\n" + entry
    MEMORY_PATH.write_text(memory, encoding="utf-8")


def main() -> None:
    changes = repair_source_md()
    stats = restore_html()
    write_progress(stats, changes)
    update_memory(stats)
    print("Repair complete")
    for change in changes:
        print(f"- {change}")
    print(f"stats={stats}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()

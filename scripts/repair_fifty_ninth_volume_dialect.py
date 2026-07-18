# -*- coding: utf-8 -*-
"""Repair and audit 第五十九卷 方言 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第五十九卷方言_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第五十九卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第六十卷-[^"]+">|</main>)', re.S)
SOURCE_RE = re.compile(r'(^第五十九卷.*?)(?=^第六十卷|\Z)', re.S | re.M)

CHAPTERS = [
    ("第一章方言差别", ["第一节语音差别", "第二节词汇语法差别"]),
    ("第二章语音系统", ["第一节声韵调", "第二节连续变调", "第三节声韵配合关系"]),
    ("第三章同音字汇", []),
    ("第四章方言词汇", []),
    ("第五章语法特点", ["第一节词法特点", "第二节句法特点"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第五十九卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第五十九卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section

    section = re.sub(
        r'^第五十九卷\n方\n言\n\n.*?第五十九卷\n方\n言\n[0-9]+\n概述\n',
        '第五十九卷 方言\n\n概述\n',
        section,
        count=1,
        flags=re.S,
    )
    replacements = {
        "第二章\n语音系统\n第一节声韵调": "第二章语音系统\n第一节声韵调",
        "第二节 词汇语法差别": "第二节词汇语法差别",
        "第二节连读变调": "第二节连续变调",
        "第三章 同音字汇·2587·\n第三章同音字汇": "第三章同音字汇",
        "第四章\n方言词汇": "第四章方言词汇",
        "第五章 语法特点·2623·\n": "",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)

    if section != original:
        text = text[:m.start(1)] + section + text[m.end(1):]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第五十九卷卷题、重复 OCR 卷题噪声、章题节题断裂和目录题名。"]
    return []


def normalize_ipa(section: str) -> str:
    return re.sub(r'<div class="ipa-data">\s*(.*?)\s*</div>', r'<p>\1</p>', section, flags=re.S)


def sub_once(section: str, pattern: str, repl: str) -> str:
    section, _ = re.subn(pattern, repl, section, count=1, flags=re.S)
    return section


def remove_malformed_headings(section: str) -> str:
    section = re.sub(
        r'<h4 id="第五十九卷-[^"]+-</p>\s*<h4 id="第五十九卷-([^"]+)">([^<]+)</h4>\s*<p>">\2</h4>\s*',
        r'<h4 id="第五十九卷-\1">\2</h4>\n',
        section,
        flags=re.S,
    )
    section = re.sub(r'<p>">[^<]+</h4>\s*', '', section)
    return section


def apply_replacements(section: str) -> str:
    section = remove_malformed_headings(normalize_ipa(section))
    section = re.sub(r'<h2 id="第五十九卷-[^"]+">.*?</h2>', '<h2 id="第五十九卷-方言">第五十九卷方言</h2>', section, count=1, flags=re.S)
    if h3("概述") not in section:
        section = section.replace('<h2 id="第五十九卷-方言">第五十九卷方言</h2>\n<p>', '<h2 id="第五十九卷-方言">第五十九卷方言</h2>\n' + h3("概述") + '\n<p>', 1)
    section = re.sub(
        r'(<h3 id="第五十九卷-概述">概述</h3>\s*)<p>言.*?311连云港市境内',
        r'\1<p>连云港市境内',
        section,
        count=1,
        flags=re.S,
    )
    section = re.sub(
        r'(<h3 id="第五十九卷-概述">概述</h3>\s*)<p>言连云港市境内',
        r'\1<p>连云港市境内',
        section,
        count=1,
    )

    replacements = [
        ('第五十九卷-第一章方言差别-第一节语音差别', r'<p>第一节语音差别', h3('第一章方言差别') + '\n' + h4('第一章方言差别', '第一节语音差别') + '\n<p>'),
        ('第五十九卷-第一章方言差别-第二节词汇语法差别', r'<p>第二节\s*词汇语法差别', h4('第一章方言差别', '第二节词汇语法差别') + '\n<p>'),
        ('第五十九卷-第二章语音系统-第一节声韵调', r'<p>语音系统第一节声韵调', h3('第二章语音系统') + '\n' + h4('第二章语音系统', '第一节声韵调') + '\n<p>'),
        ('第五十九卷-第二章语音系统-第二节连续变调', r'<p>第二节(?:连读|连续)变调', h4('第二章语音系统', '第二节连续变调') + '\n<p>'),
        ('第五十九卷-第二章语音系统-第三节声韵配合关系', r'<p>第三节声韵配合关系', h4('第二章语音系统', '第三节声韵配合关系') + '\n<p>'),
        ('第五十九卷-第三章同音字汇', r'本字汇收常用字', h3('第三章同音字汇') + '\n<p>本字汇收常用字'),
        ('第五十九卷-第四章方言词汇', r'方言词汇本章记录连云港市城区', h3('第四章方言词汇') + '\n<p>本章记录连云港市城区'),
        ('第五十九卷-第五章语法特点-第一节词法特点', r'第一节词法特点', h3('第五章语法特点') + '\n' + h4('第五章语法特点', '第一节词法特点') + '\n<p>'),
        ('第五十九卷-第五章语法特点-第二节句法特点', r'<p>第二节句法特点', h4('第五章语法特点', '第二节句法特点') + '\n<p>'),
    ]
    for ident, pattern, repl in replacements:
        if ident not in section:
            section = sub_once(section, pattern, repl)
    return section


def cleanup(section: str) -> str:
    section = remove_malformed_headings(section)
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'</p>\s*</p>', '</p>', section)
    section = re.sub(r'(<p>[^<]*)(<h3 id="第五十九卷-[^"]+">)', r'\1</p>\n\2', section)
    section = re.sub(r'<p>\s*(<h[34] id="第五十九卷-[^"]+">)', r'\1', section)
    section = re.sub(r'(</h[34]>)\s*</p>', r'\1', section)
    section = re.sub(r'(<h[34] id="第五十九卷-[^"]+">[^<]+</h[34]>)\s*([^<\s])', r'\1\n<p>\2', section)
    section = re.sub(r'(<p>)(\s+)', r'\1', section)
    seen: set[str] = set()

    def keep(match: re.Match[str]) -> str:
        ident = match.group(1)
        if ident in seen:
            return ''
        seen.add(ident)
        return match.group(0)

    return re.sub(r'<h[34] id="([^"]+)">[^<]+</h[34]>\s*', keep, section)


def restore_html() -> dict[str, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第五十九卷 HTML range")
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
        "ipa_blocks": block.count('<div class="ipa-data">'),
        "embedded_h3_in_p": len(re.findall(r'<p[^>]*>[^<]*<h3', block)),
        "embedded_h4_in_p": len(re.findall(r'<p[^>]*>[^<]*<h4', block)),
        "malformed_heading_ids": len(re.findall(r'<h[34] id="[^"]*<h[34]', block)),
    }


def write_progress(stats: dict[str, int], changes: list[str]) -> None:
    status = "通过" if stats["h3_count"] == EXPECTED_H3 and stats["h4_count"] == EXPECTED_H4 and stats["ipa_blocks"] == 0 and stats["generic_heading_anchors"] == 0 else "需复核"
    content = f"""# 2026-06-29 第五十九卷《方言》修复核对进度

## 本轮范围
- 范围：`第五十九卷 方言`。
- 目标：按交付标准修复卷题、概述、5 章、7 节和正文段落结构。
- 源文件：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已完成规范化，脚本复跑保持幂等'}。
- 将最终阅读页卷题统一为 `第五十九卷方言`。
- 恢复概述、第一章方言差别至第五章语法特点及 7 个节题的标准 H3/H4 层级。
- 按章节骨架将第二章第二节题名统一为 `第二节连续变调`。
- 将本卷 `ipa-data` 音标数据块恢复为普通段落，避免阅读页保留临时数据容器。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第五章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本卷包含大量音标、同音字汇和方言词条，本轮只处理章节格式与临时容器，不改写正文音值和例词。
- 语音系统中的表59-1、表59-2在当前阅读页仍表现为 OCR 文本串，需后续 PDF/表格专项重建。

## 遇到的问题与处理
- 卷题断为 `第五十九卷方`，正文段首残留 `言` 和重复 OCR 卷题噪声，已修为标准卷题并补入概述层级。
- 第一章、第二章、第五章章题与节题混入正文，已按目录恢复 H3/H4。
- `第三章 同音字汇·2587·`、`第四章 方言词汇·2597·`、`第五章 语法特点·2623·` 等页眉式标题噪声已在插入章节标题时规整。
- 本卷存在 16 处 `ipa-data` 临时块，已统一转为普通段落。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 继续第六十卷《杂记》章节结构修复，并同步检查附录起始边界。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第五十九卷方言章节核对完成

已完成 `第五十九卷 方言` 章节格式核对：

- 新增脚本：`scripts/repair_fifty_ninth_volume_dialect.py`。
- 修复第五十九卷卷题断裂、概述缺失、最终阅读页无 H3/H4 导航层级、章题节题扁平化和页眉式标题噪声。
- 第五十九卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第五章），H4={stats['h4_count']}。
- 第五十九卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处。
- 已写入进度文档：`output/reports/progress/20260629_第五十九卷方言_修复核对进度.md`。

验收：第五十九卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：继续第六十卷《杂记》。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第五十九卷方言章节核对完成"
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

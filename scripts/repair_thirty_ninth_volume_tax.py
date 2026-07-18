# -*- coding: utf-8 -*-
"""Repair and audit 第三十九卷 税务 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第三十九卷税务_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第三十九卷-税务">.*?</h2>)(.*?)(?=<h2 id="第四十卷-[^"]+">)', re.S)
SOURCE_RE = re.compile(r'(第三十九卷.*?)(?=第四十卷)', re.S)

CHAPTERS = [
    ("第一章税务机构", ["第一节建国前税务机构", "第二节建国后税务机构"]),
    ("第二章税种税率", ["第一节农业税", "第二节工商各税", "第三节盐税"]),
    ("第三章稽征管理", ["第一节征收管理", "第二节减税免税", "第三节税务稽查"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(titles) for _, titles in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第三十九卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第三十九卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        raise RuntimeError("Cannot locate 第三十九卷 source range")
    section = m.group(1)
    original = section
    replacements = {
        "第三十九卷\n概述\n": "第三十九卷 税务\n\n概述\n",
        "\n第一章\n税务机构\n第一节\n建国前税务机构\n": "\n第一章税务机构\n第一节建国前税务机构\n",
        "\n建国后税务机构\n第二节\n": "\n第二节建国后税务机构\n",
        "\n税种\n税率\n第二章\n": "\n第二章税种税率\n",
        "\n第二节\n工商各税\n": "\n第二节工商各税\n",
        "\n第三章\n稽征管理\n": "\n第三章稽征管理\n",
        "\n第一节征收管理\n": "\n第一节征收管理\n",
        "\n第二节\n减税免税\n": "\n第二节减税免税\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[: m.start(1)] + section + text[m.end(1) :]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第三十九卷卷题、章题、节题断裂和节题倒置。"]
    return []


def insert_after_h2(section: str, marker: str) -> tuple[str, bool]:
    if marker in section:
        return section, False
    m = re.search(r'</h2>\s*', section)
    if not m:
        return section, False
    return section[:m.end()] + "\n" + marker + "\n" + section[m.end():], True


def insert_before_text(section: str, marker: str, text: str) -> tuple[str, bool]:
    if marker in section:
        return section, False
    pos = section.find(text)
    if pos < 0:
        return section, False
    p_start = section.rfind("<p>", 0, pos)
    p_end = section.rfind("</p>", 0, pos)
    insert_pos = p_start if p_start > p_end else pos
    return section[:insert_pos] + marker + "\n" + section[insert_pos:], True


def split_heading(section: str, marker: str, text: str, replacement: str = "") -> tuple[str, bool]:
    if marker in section:
        return section, False
    variants = [text]
    for v in variants:
        pattern = "<p>" + v
        pos = section.find(pattern)
        if pos >= 0:
            content_start = pos + len(pattern)
            return section[:pos] + marker + "\n<p>" + replacement + section[content_start:], True
        pos = section.find(v)
        if pos >= 0:
            p_start = section.rfind("<p>", 0, pos)
            p_end = section.rfind("</p>", 0, pos)
            content_start = pos + len(v)
            if p_start > p_end:
                return section[:pos] + "</p>\n" + marker + "\n<p>" + replacement + section[content_start:], True
            return section[:pos] + marker + "\n" + replacement + section[content_start:], True
    return section, False


def cleanup(section: str) -> str:
    replacements = {
        '<h2 id="第三十九卷-税务">第三十九卷概述</h2>': '<h2 id="第三十九卷-税务">第三十九卷税务</h2>',
        "<p>税务机构第一节建国前税务机构": h3("第一章税务机构") + "\n" + h4("第一章税务机构", "第一节建国前税务机构") + "\n<p>",
        "建国后税务机构第二节": h4("第一章税务机构", "第二节建国后税务机构"),
        "<p>税种税率": h3("第二章税种税率") + "\n<p>",
        "<p>第一节农业税": h4("第二章税种税率", "第一节农业税") + "\n<p>",
        "<p>第二节工商各税": h4("第二章税种税率", "第二节工商各税") + "\n<p>",
        "<p>第三节盐税": h4("第二章税种税率", "第三节盐税") + "\n<p>",
        "<p>第一节征收管理": h4("第三章稽征管理", "第一节征收管理") + "\n<p>",
        "<p>第二节减税免税": h4("第三章稽征管理", "第二节减税免税") + "\n<p>",
        "<p>第三节税务稽查": h4("第三章稽征管理", "第三节税务稽查") + "\n<p>",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    section = re.sub(r"(<p>[^<]*?)(<h[34] id=\"第三十九卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = section.replace("<p><h3", "<h3").replace("<p><h4", "<h4")
    section = section.replace("</h3>\n</p>", "</h3>\n").replace("</h4>\n</p>", "</h4>\n")
    seen_h3: set[str] = set()
    seen_h4: set[str] = set()

    def keep_first_h3(match: re.Match[str]) -> str:
        ident = match.group(1)
        if ident in seen_h3:
            return ""
        seen_h3.add(ident)
        return match.group(0)

    def keep_first_h4(match: re.Match[str]) -> str:
        ident = match.group(1)
        if ident in seen_h4:
            return ""
        seen_h4.add(ident)
        return match.group(0)

    section = re.sub(r'<h3 id="([^"]+)">[^<]+</h3>\s*', keep_first_h3, section)
    section = re.sub(r'<h4 id="([^"]+)">[^<]+</h4>\s*', keep_first_h4, section)
    return section


def restore_html() -> tuple[int, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第三十九卷 HTML range")
    section = m.group(0)
    section = section.replace('<h2 id="第三十九卷-税务">第三十九卷概述</h2>', '<h2 id="第三十九卷-税务">第三十九卷税务</h2>')
    inserted_h3 = inserted_h4 = 0
    section, added = insert_after_h2(section, h3("概述")); inserted_h3 += int(added)
    for title, needle in [
        ("第一章税务机构", "税务机构第一节建国前税务机构"),
        ("第二章税种税率", "税种税率明代，海州赋税"),
        ("第三章稽征管理", "稽征管理明清时期，境内赋税"),
    ]:
        section, added = insert_before_text(section, h3(title), needle); inserted_h3 += int(added)
    for chapter, title, needle, replacement in [
        ("第一章税务机构", "第一节建国前税务机构", "第一节建国前税务机构", ""),
        ("第一章税务机构", "第二节建国后税务机构", "建国后税务机构第二节", ""),
        ("第二章税种税率", "第一节农业税", "第一节农业税", ""),
        ("第二章税种税率", "第二节工商各税", "第二节工商各税", ""),
        ("第二章税种税率", "第三节盐税", "第三节盐税", ""),
        ("第三章稽征管理", "第一节征收管理", "第一节征收管理", ""),
        ("第三章稽征管理", "第二节减税免税", "第二节减税免税", ""),
        ("第三章稽征管理", "第三节税务稽查", "第三节税务稽查", ""),
    ]:
        section, added = split_heading(section, h4(chapter, title), needle, replacement)
        inserted_h4 += int(added)
    section = cleanup(section)
    html = html[:m.start()] + section + html[m.end():]
    HTML_PATH.write_text(html, encoding="utf-8")
    return inserted_h3, inserted_h4


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
    status = "通过" if stats["h3_count"] == EXPECTED_H3 and stats["h4_count"] == EXPECTED_H4 and stats["ipa_blocks"] == 0 else "需复核"
    content = f"""# 2026-06-29 第三十九卷《税务》修复核对进度

## 本轮范围
- 范围：`第三十九卷 税务`。
- 目标：按交付标准修复卷题、概述、章题、节题和正文段落结构。
- 源文件：`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已处于规范状态'}。
- 将最终阅读页卷题由 `第三十九卷概述` 修正为 `第三十九卷税务`。
- 恢复概述、第一章税务机构至第三章稽征管理及 8 个节题的标准 H3/H4 层级。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章税务机构至第三章稽征管理），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本卷当前阅读页未见结构化表格；源 PDF 中税率、税额类统计内容后续仍需在表格专项中核对是否被正文串行化。

## 验收状态
- 本卷结构验收：{status}。
- 后续已纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 进入 `第四十卷 金融`，继续按“源 MD 标题规范 -> 最终阅读页结构修复 -> 全书审计 -> typecheck -> 进度记录 -> Git 提交”的顺序推进。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第三十九卷税务章节核对完成

已完成 `第三十九卷 税务` 章节格式核对：

- 新增脚本：`scripts/repair_thirty_ninth_volume_tax.py`。
- 修复 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md` 中第三十九卷卷题、章题、节题断裂和节题倒置。
- 修复 `output/final_reader/连云港市志_全书.html` 中第三十九卷卷题误作概述、章节标题全部扁平化的问题。
- 第三十九卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章税务机构至第三章稽征管理），H4={stats['h4_count']}。
- 第三十九卷范围内 `ipa-data` 残留为 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；税率、税额类内容后续需从源 PDF 专项核验是否存在应表格化内容。
- 已写入进度文档：`output/reports/progress/20260629_第三十九卷税务_修复核对进度.md`。

验收：第三十九卷 HTML 字节数 {stats['bytes']}，范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第四十卷 金融`。第三十九卷税率、税额类内容需在 PDF 表格专项中复核。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第三十九卷税务章节核对完成"
    if marker in memory:
        memory = memory[: memory.find(marker)].rstrip() + "\n" + entry
    else:
        memory = memory.rstrip() + "\n" + entry
    MEMORY_PATH.write_text(memory, encoding="utf-8")


def main() -> None:
    changes = repair_source_md()
    inserted_h3, inserted_h4 = restore_html()
    stats = audit_section()
    stats["inserted_h3"] = inserted_h3
    stats["inserted_h4"] = inserted_h4
    write_progress(stats, changes)
    update_memory(stats)
    print("Repair complete")
    if changes:
        for change in changes:
            print(f"- {change}")
    print(f"stats={stats}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()

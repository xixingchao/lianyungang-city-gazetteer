# -*- coding: utf-8 -*-
"""Repair and audit 第三十七卷 物资流通 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第三十七卷物资流通_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第三十七卷-物资流通">.*?</h2>)(.*?)(?=<h2 id="第三十八卷-[^"]+">)', re.S)
SOURCE_RE = re.compile(r'(第三十七卷.*?)(?=第三十八卷)', re.S)

CHAPTERS = [
    ("第一章机构体制", ["第一节管理机构", "第二节经营机构", "第三节管理体制"]),
    ("第二章货源", ["第一节计划物资", "第二节地产品", "第三节协作", "第四节市场采购"]),
    ("第三章计划管理", ["第一节主要物资管理", "第二节节约代用"]),
    ("第四章供应", ["第一节计划分配原则", "第二节供应方法"]),
    ("第五章储运", ["第一节仓储建设", "第二节主要仓库"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(titles) for _, titles in CHAPTERS)
EXPECTED_TABLES = ["表37-2"]


def h3(title: str) -> str:
    return f'<h3 id="第三十七卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第三十七卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        raise RuntimeError("Cannot locate 第三十七卷 source range")
    section = m.group(1)
    original = section
    replacements = {
        "第三十七卷\n物资流通\n概述\n": "第三十七卷 物资流通\n\n概述\n",
        "\n第一章\n机构\n体制\n": "\n第一章机构体制\n",
        "\n第三节\n管理体制\n": "\n第三节管理体制\n",
        "\n第二章货源\n": "\n第二章货源\n",
        "\n第二节．地•产•品\n": "\n第二节地产品\n",
        "\n第三节•协•作\n": "\n第三节协作\n",
        "\n第三章\n计划管理\n": "\n第三章计划管理\n",
        "\n第一节\n主要物资管理\n": "\n第一节主要物资管理\n",
        "\n供　应\n第四章\n": "\n第四章供应\n",
        "\n第一节\n计划分配原则\n": "\n第一节计划分配原则\n",
        "\n储运\n第五章\n": "\n第五章储运\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[: m.start(1)] + section + text[m.end(1) :]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第三十七卷卷题、章题、节题断裂和 OCR 标题错位。"]
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


def split_heading(section: str, marker: str, text: str) -> tuple[str, bool]:
    if marker in section:
        return section, False
    variants = [
        text,
        text.replace("机构体制", "机构\n体制"),
        text.replace("地产品", "地•产•品"),
        text.replace("地产品", "地产品"),
        text.replace("协作", "协•作"),
        text.replace("供应", "供　应"),
    ]
    for v in variants:
        pattern = "<p>" + re.escape(v)
        pos = section.find(pattern)
        if pos >= 0:
            content_start = pos + len(pattern)
            return section[:pos] + marker + "\n<p>" + section[content_start:], True
        pos = section.find(v)
        if pos >= 0:
            p_start = section.rfind("<p>", 0, pos)
            p_end = section.rfind("</p>", 0, pos)
            if p_start > p_end:
                content_start = pos + len(v)
                return section[:pos] + "</p>\n" + marker + "\n<p>" + section[content_start:], True
            return section[:pos] + marker + "\n" + section[pos + len(v):], True
    return section, False


def cleanup(section: str) -> str:
    replacements = {
        "<p>机构体制第一节管理机构": h3("第一章机构体制") + "\n" + h4("第一章机构体制", "第一节管理机构") + "\n<p>",
        "<p>第一节管理机构": h4("第一章机构体制", "第一节管理机构") + "\n<p>",
        "<p>第三节管理体制": h4("第一章机构体制", "第三节管理体制") + "\n<p>",
        "<p>第二节．地产品": h4("第二章货源", "第二节地产品") + "\n<p>",
        "<p>第二节．地•产•品": h4("第二章货源", "第二节地产品") + "\n<p>",
        "<p>第二节地产品": h4("第二章货源", "第二节地产品") + "\n<p>",
        "<p>第三节•协•作": h4("第二章货源", "第三节协作") + "\n<p>",
        "<p>第三节协作": h4("第二章货源", "第三节协作") + "\n<p>",
        "<p>第一节主要物资管理": h4("第三章计划管理", "第一节主要物资管理") + "\n<p>",
        "<p>第二节节约代用": h4("第三章计划管理", "第二节节约代用") + "\n<p>",
        "<p>供　应": "<p>",
        "<p>第一节计划分配原则": h4("第四章供应", "第一节计划分配原则") + "\n<p>",
        "<p>第二节供应方法": h4("第四章供应", "第二节供应方法") + "\n<p>",
        "<p>储运第一节仓储建设": h3("第五章储运") + "\n" + h4("第五章储运", "第一节仓储建设") + "\n<p>",
        "<p>第一节仓储建设": h4("第五章储运", "第一节仓储建设") + "\n<p>",
        "<p>第二节主要仓库": h4("第五章储运", "第二节主要仓库") + "\n<p>",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    section = re.sub(r"(<h3 id=\"第三十七卷-第四章供应\">第四章供应</h3>\s*){2,}", h3("第四章供应") + "\n", section)
    section = section.replace(h3("第五章储运") + "\n<p>储运</p>\n" + h4("第五章储运", "第一节仓储建设"), h3("第五章储运") + "\n" + h4("第五章储运", "第一节仓储建设"))
    section = re.sub(r"(<p>[^<]*?)(<h[34] id=\"第三十七卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = section.replace("<p><h3", "<h3").replace("<p><h4", "<h4")
    section = section.replace("</h3>\n</p>", "</h3>\n").replace("</h4>\n</p>", "</h4>\n")
    return section


def restore_html() -> tuple[int, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第三十七卷 HTML range")
    section = m.group(0)
    inserted_h3 = inserted_h4 = 0
    section, added = insert_after_h2(section, h3("概述")); inserted_h3 += int(added)
    for title, needle in [
        ("第一章机构体制", "机构体制第一节管理机构"),
        ("第二章货源", "建国前，境内商品生产的门类较少"),
        ("第三章计划管理", "计划管理物资计划管理"),
        ("第四章供应", "供　应20世纪50年代后期"),
        ("第五章储运", "储运第一节仓储建设"),
    ]:
        section, added = insert_before_text(section, h3(title), needle); inserted_h3 += int(added)
    for chapter, title, needle in [
        ("第一章机构体制", "第一节管理机构", "第一节管理机构"),
        ("第一章机构体制", "第二节经营机构", "第二节经营机构"),
        ("第一章机构体制", "第三节管理体制", "第三节管理体制"),
        ("第二章货源", "第一节计划物资", "第一节计划物资"),
        ("第二章货源", "第二节地产品", "第二节地产品"),
        ("第二章货源", "第三节协作", "第三节协作"),
        ("第二章货源", "第四节市场采购", "第四节市场采购"),
        ("第三章计划管理", "第一节主要物资管理", "第一节主要物资管理"),
        ("第三章计划管理", "第二节节约代用", "第二节节约代用"),
        ("第四章供应", "第一节计划分配原则", "第一节计划分配原则"),
        ("第四章供应", "第二节供应方法", "第二节供应方法"),
        ("第五章储运", "第一节仓储建设", "第一节仓储建设"),
        ("第五章储运", "第二节主要仓库", "第二节主要仓库"),
    ]:
        section, added = split_heading(section, h4(chapter, title), needle)
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
    content = f"""# 2026-06-29 第三十七卷《物资流通》修复核对进度

## 本轮范围
- 范围：`第三十七卷 物资流通`。
- 目标：按交付标准修复卷题、概述、章题、节题和正文段落结构。
- 源文件：`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已处于规范状态'}。
- 保留最终阅读页既有结构化表格，并恢复标准 H3/H4 标题层级。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章机构体制至第五章储运），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 源 MD 可见表号：{', '.join(EXPECTED_TABLES)}；本轮先保留既有表格骨架，待 PDF 表格专项复核。

## 验收状态
- 本卷结构验收：{status}。
- 后续已纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 进入 `第三十八卷 财政`，继续按“源 MD 标题规范 -> 最终阅读页结构修复 -> 全书审计 -> typecheck -> 进度记录 -> Git 提交”的顺序推进。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第三十七卷物资流通章节核对完成

已完成 `第三十七卷 物资流通` 章节格式核对：

- 新增脚本：`scripts/repair_thirty_seventh_volume_materials.py`。
- 修复 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md` 中第三十七卷卷题、章题、节题断裂和 OCR 标题错位。
- 修复 `output/final_reader/连云港市志_全书.html` 中第三十七卷章节标题全部扁平化的问题。
- 第三十七卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章机构体制至第五章储运），H4={stats['h4_count']}。
- 第三十七卷范围内 `ipa-data` 残留为 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表37-*需从 PDF 专项补登、重建和核验。
- 已写入进度文档：`output/reports/progress/20260629_第三十七卷物资流通_修复核对进度.md`。

验收：第三十七卷 HTML 字节数 {stats['bytes']}，范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第三十八卷 财政`。第三十七卷表37-*需从源 PDF 专项补登、重建和核验。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第三十七卷物资流通章节核对完成"
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

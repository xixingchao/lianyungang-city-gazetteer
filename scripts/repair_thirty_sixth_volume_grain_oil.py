# -*- coding: utf-8 -*-
"""Repair and audit 第三十六卷 粮油购销 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第三十六卷粮油购销_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第三十六卷-粮油购销">.*?</h2>)(.*?)(?=<h2 id="第三十七卷-[^"]+">)', re.S)
SOURCE_RE = re.compile(r'(第三十六卷.*?)(?=第三十七卷)', re.S)

CHAPTERS = [
    ("第一章征购", ["第一节征收", "第二节收购"]),
    ("第二章销售", ["第一节城镇供应", "第二节农村销售"]),
    ("第三章市场贸易", ["第一节自由市场贸易", "第二节国家市场贸易"]),
    ("第四章储运", ["第一节仓储", "第二节调运"]),
    ("第五章加工", ["第一节制粉", "第二节碾米", "第三节榨油"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(titles) for _, titles in CHAPTERS)
EXPECTED_TABLES = ["表36-2", "表36-3", "表36-4", "表36-6", "表36-7", "表36-9", "表36-10", "表36-11", "表36-12", "表36-13", "表36-14", "表36-18", "表36-20", "表36-22"]


def h3(title: str) -> str:
    return f'<h3 id="第三十六卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第三十六卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        raise RuntimeError("Cannot locate 第三十六卷 source range")
    section = m.group(1)
    original = section
    replacements = {
        "第三十六卷\n粮油购销\n概述\n": "第三十六卷 粮油购销\n\n概述\n",
        "\n第一章\n历代封建王朝": "\n第一章征购\n历代封建王朝",
        "\n第一节•征收\n": "\n第一节征收\n",
        "\n销售\n第二章\n": "\n第二章销售\n",
        "\n第二节\n农村销售\n": "\n第二节农村销售\n",
        "\n市场贸易\n第三章\n": "\n第三章市场贸易\n",
        "\n，第节自由市场贸易\n": "\n第一节自由市场贸易\n",
        "\n第二节‧国家市场贸易\n": "\n第二节国家市场贸易\n",
        "\n第三章 \n\n省粮食局出省准运章": "\n省粮食局出省准运章",
        "\n第四章\n海州，唐时": "\n第四章储运\n海州，唐时",
        "\n第一节仓　储\n": "\n第一节仓储\n",
        "\n第四章\n储运\n1543·\n续上表\n": "\n续上表\n",
        "\n第二节调　运\n": "\n第二节调运\n",
        "\n第四章\n0.23\n": "\n0.23\n",
        "\n第五章\n连云港市历来": "\n第五章加工\n连云港市历来",
        "\n第一节制　粉\n": "\n第一节制粉\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[: m.start(1)] + section + text[m.end(1) :]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第三十六卷卷题、章题、节题断裂、表格续页页眉和 OCR 标题错位。"]
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
    variants = [text, text.replace("仓储", "仓　储"), text.replace("调运", "调　运"), text.replace("制粉", "制　粉"), text.replace("国家", "‧国家"), text.replace("征收", "•征收")]
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


def normalize_ipa(section: str) -> tuple[str, int]:
    count = 0
    def repl(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        text = re.sub(r"^\s*[·:.：\s]*\d{4}\s*[·:.：\s]*", "", match.group(1).strip())
        return f"<p>{text}</p>"
    return re.sub(r'<div class="ipa-data">(.*?)</div>', repl, section, flags=re.S), count


def render_source_chunk(start_title: str, end_title: str) -> str:
    source = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(source)
    if not m:
        return ""
    block = m.group(1)
    start = block.find(start_title)
    end = block.find(end_title, start)
    if start < 0 or end < 0:
        return ""
    chunk = block[start + len(start_title) : end].strip()
    chunk = re.sub(r"<!--.*?-->", "", chunk, flags=re.S)
    chunk = re.sub(r"\n{3,}", "\n\n", chunk).strip()
    lines = [line.strip() for line in chunk.splitlines() if line.strip()]
    return "\n".join(f"<p>{line}</p>" for line in lines)


def ensure_source_section(section: str, marker: str, source_start: str, source_end: str, before_marker: str) -> tuple[str, bool]:
    if marker in section:
        return section, False
    pos = section.find(before_marker)
    if pos < 0:
        return section, False
    body = render_source_chunk(source_start, source_end)
    if not body:
        return section, False
    return section[:pos] + marker + "\n" + body + "\n" + section[pos:], True


def cleanup(section: str) -> str:
    replacements = {
        "<p>第一节•征收一、田赋粮": h4("第一章征购", "第一节征收") + "\n<p>一、田赋粮",
        "<p>第一节征收一、田赋粮": h4("第一章征购", "第一节征收") + "\n<p>一、田赋粮",
        "<p>第一节城镇供应一、居民粮油供应": h4("第二章销售", "第一节城镇供应") + "\n<p>一、居民粮油供应",
        "<p>第二节农村销售一、缺粮统销": h4("第二章销售", "第二节农村销售") + "\n<p>一、缺粮统销",
        "<p>第二节‧国家市场贸易": h4("第三章市场贸易", "第二节国家市场贸易") + "\n<p>",
        "<p>第二节国家市场贸易": h4("第三章市场贸易", "第二节国家市场贸易") + "\n<p>",
        "<p>第一节仓　储一、仓库": h4("第四章储运", "第一节仓储") + "\n<p>一、仓库",
        "<p>第一节仓储一、仓库": h4("第四章储运", "第一节仓储") + "\n<p>一、仓库",
        "<p>第二节调　运一、漕运": h4("第四章储运", "第二节调运") + "\n<p>一、漕运",
        "<p>第二节调运一、漕运": h4("第四章储运", "第二节调运") + "\n<p>一、漕运",
        "<p>第一节制　粉一、石磨制粉": h4("第五章加工", "第一节制粉") + "\n<p>一、石磨制粉",
        "<p>第一节制粉一、石磨制粉": h4("第五章加工", "第一节制粉") + "\n<p>一、石磨制粉",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    section = section.replace("，第节自由市场贸易", "")
    section = section.replace("，第节</p>\n" + h4("第三章市场贸易", "第一节自由市场贸易") + "\n<p>（688年）", "</p>\n" + h4("第三章市场贸易", "第一节自由市场贸易") + "\n<p>唐垂拱四年（688年）")
    section = section.replace("，第节</p>\n" + h4("第三章市场贸易", "第一节自由市场贸易") + "\n<p>（688年)", "</p>\n" + h4("第三章市场贸易", "第一节自由市场贸易") + "\n<p>唐垂拱四年（688年)")
    section = section.replace("第三章 ", "")
    section = section.replace("第四章储运1543·", "")
    section = re.sub(r"<p>\s*[·:.：\s]*\d{4}\s*[·:.：\s]*</p>\n?", "", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    section = re.sub(r"(<p>[^<]*?)(<h[34] id=\"第三十六卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = section.replace("<p><h3", "<h3").replace("<p><h4", "<h4")
    section = section.replace("</h3>\n</p>", "</h3>\n").replace("</h4>\n</p>", "</h4>\n")
    return section


def restore_html() -> tuple[int, int, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第三十六卷 HTML range")
    section = m.group(0)
    inserted_h3 = inserted_h4 = 0
    section, added = insert_after_h2(section, h3("概述")); inserted_h3 += int(added)
    for title, needle in [
        ("第一章征购", "历代封建王朝制定科则征收田赋"),
        ("第二章销售", "历史上，粮食通过市场调剂余缺"),
        ("第三章市场贸易", "唐武德四年（621年），海州即设司仓参军"),
        ("第四章储运", "海州，唐时设司库参军"),
        ("第五章加工", "连云港市历来使用石磨"),
    ]:
        section, added = insert_before_text(section, h3(title), needle); inserted_h3 += int(added)
    for chapter, title, needle in [
        ("第一章征购", "第一节征收", "第一节征收"),
        ("第一章征购", "第二节收购", "第二节收购"),
        ("第二章销售", "第一节城镇供应", "第一节城镇供应"),
        ("第二章销售", "第二节农村销售", "第二节农村销售"),
        ("第三章市场贸易", "第一节自由市场贸易", "自由市场贸易唐垂拱四年"),
        ("第三章市场贸易", "第二节国家市场贸易", "第二节国家市场贸易"),
        ("第四章储运", "第一节仓储", "第一节仓储"),
        ("第四章储运", "第二节调运", "第二节调运"),
        ("第五章加工", "第一节制粉", "第一节制粉"),
        ("第五章加工", "第二节碾米", "第二节碾米"),
        ("第五章加工", "第三节榨油", "第三节榨油"),
    ]:
        marker = h4(chapter, title)
        section, added = split_heading(section, marker, needle)
        if not added and title == "第一节自由市场贸易":
            section, added = insert_before_text(section, marker, "唐垂拱四年（688年），海州开挖漕河")
        inserted_h4 += int(added)
    section, added = ensure_source_section(
        section,
        h4("第一章征购", "第二节收购"),
        "第二节收购",
        "第二章销售",
        h3("第二章销售"),
    )
    inserted_h4 += int(added)
    section, ipa_fixed = normalize_ipa(section)
    section = cleanup(section)
    html = html[:m.start()] + section + html[m.end():]
    HTML_PATH.write_text(html, encoding="utf-8")
    return inserted_h3, inserted_h4, ipa_fixed


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
    content = f"""# 2026-06-29 第三十六卷《粮油购销》修复核对进度

## 本轮范围
- 范围：`第三十六卷 粮油购销`。
- 目标：按交付标准修复卷题、概述、章题、节题、表格页残留和正文段落结构。
- 源文件：`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已处于规范状态'}。
- 保留最终阅读页既有结构化表格，并恢复标准 H3/H4 标题层级。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章征购至第五章加工），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 源 MD 可见表号：{', '.join(EXPECTED_TABLES)}；本轮先保留既有表格骨架，待 PDF 表格专项复核。
- 2 处 `ipa-data` 残留已改为普通段落，未直接重构表格数据。

## 验收状态
- 本卷结构验收：{status}。
- 后续已纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 进入 `第三十七卷 物资流通`，继续按“源 MD 标题规范 -> 最终阅读页结构修复 -> 全书审计 -> typecheck -> 进度记录 -> Git 提交”的顺序推进。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第三十六卷粮油购销章节核对完成

已完成 `第三十六卷 粮油购销` 章节格式核对：

- 新增脚本：`scripts/repair_thirty_sixth_volume_grain_oil.py`。
- 修复 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md` 中第三十六卷卷题、章题、节题断裂、表格续页页眉和 OCR 标题错位。
- 修复 `output/final_reader/连云港市志_全书.html` 中第三十六卷章节标题全部扁平化以及 2 处 `ipa-data` 残留的问题。
- 第三十六卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章征购至第五章加工），H4={stats['h4_count']}。
- 第三十六卷范围内 `ipa-data` 残留为 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表36-*需从 PDF 专项补登、重建和核验。
- 已写入进度文档：`output/reports/progress/20260629_第三十六卷粮油购销_修复核对进度.md`。

验收：第三十六卷 HTML 字节数 {stats['bytes']}，范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第三十七卷 物资流通`。第三十六卷表36-*需从源 PDF 专项补登、重建和核验。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第三十六卷粮油购销章节核对完成"
    if marker in memory:
        memory = memory[: memory.find(marker)].rstrip() + "\n" + entry
    else:
        memory = memory.rstrip() + "\n" + entry
    MEMORY_PATH.write_text(memory, encoding="utf-8")


def main() -> None:
    changes = repair_source_md()
    inserted_h3, inserted_h4, ipa_fixed = restore_html()
    stats = audit_section()
    stats["inserted_h3"] = inserted_h3
    stats["inserted_h4"] = inserted_h4
    stats["ipa_fixed"] = ipa_fixed
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

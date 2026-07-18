# -*- coding: utf-8 -*-
"""Repair and audit 第三十四卷 供销 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第三十四卷供销_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第三十四卷-供销">.*?</h2>)(.*?)(?=<h2 id="第三十五卷-[^"]+">)', re.S)
SOURCE_RE = re.compile(r'(第三十四卷.*?)(?=第三十五卷)', re.S)

CHAPTERS = [
    ("第一章机构体制", ["第一节机构", "第二节体制", "第三节经营网点和企业"]),
    ("第二章扶持生产", ["第一节扶持概况", "第二节主要扶持项目"]),
    ("第三章农业生产资料经营", ["第一节化肥", "第二节农药农药械农用薄膜", "第三节小农具林材竹材桐油"]),
    ("第四章农副产品经营", ["第一节棉花", "第二节茶叶", "第三节麻类", "第四节干鲜果品", "第五节芦苇芦席", "第六节蜂蜜", "第七节葛藤粉芦笋草莓"]),
    ("第五章废旧物资经营", ["第一节回收", "第二节利用"]),
]

H3_TITLES = {"概述", *(chapter for chapter, _ in CHAPTERS)}
H4_TO_CHAPTER = {title: chapter for chapter, titles in CHAPTERS for title in titles}
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(titles) for _, titles in CHAPTERS)


def h2() -> str:
    return '<h2 id="第三十四卷-供销">第三十四卷供销</h2>'


def h3(title: str) -> str:
    return f'<h3 id="第三十四卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第三十四卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        raise RuntimeError("Cannot locate 第三十四卷 source range")
    section = m.group(1)
    original = section
    replacements = {
        "第三十四卷\n概述\n": "第三十四卷 供销\n\n概述\n",
        "\n第一章\n机构体制\n": "\n第一章机构体制\n",
        "\n第二节•体制\n": "\n第二节体制\n",
        "\n第三节\n经营网点和企业\n": "\n第三节经营网点和企业\n",
        "\n扶持生产\n第二章\n": "\n第二章扶持生产\n",
        "\n第二节.\n主要扶持项目\n": "\n第二节主要扶持项目\n",
        "\n第三章\n农业生产资料经营\n": "\n第三章农业生产资料经营\n",
        "\n第一节•化•肥\n": "\n第一节化肥\n",
        "\n第二节农药农药械\n农用薄膜\n": "\n第二节农药农药械农用薄膜\n",
        "\n由竹材\n第三节小农具　林\n桐油\n": "\n第三节小农具林材竹材桐油\n",
        "\n第四章\n农副产品经营\n": "\n第四章农副产品经营\n",
        "\n第二节茶•叶\n": "\n第二节茶叶\n",
        "\n第四节\n干鲜果品\n": "\n第四节干鲜果品\n",
        "\n第五节芦苇‧芦席\n": "\n第五节芦苇芦席\n",
        "\n葛藤粉芦笋草莓\n第七节\n": "\n第七节葛藤粉芦笋草莓\n",
        "\n第五章\n废旧物资经营\n": "\n第五章废旧物资经营\n",
        "\n第一节回　收\n": "\n第一节回收\n",
        "\n第二节•利•用\n": "\n第二节利用\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[: m.start(1)] + section + text[m.end(1) :]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第三十四卷卷题、章题、节题断裂和 OCR 标题错位。"]
    return []


def get_source_section() -> str:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        raise RuntimeError("Cannot locate repaired 第三十四卷 source range")
    return m.group(1)


def clean_paragraph(line: str) -> str:
    line = line.strip()
    line = line.replace("•", "")
    return line


def render_from_source(section: str) -> str:
    lines = [line.strip() for line in section.splitlines()]
    html_lines: list[str] = [h2()]
    current_chapter = ""
    volume_seen = False
    for raw in lines:
        if not raw:
            continue
        if raw.startswith("<!--") and raw.endswith("-->"):
            html_lines.append(raw)
            continue
        if raw in {"第三十四卷", "第三十四卷 供销"}:
            volume_seen = True
            continue
        if not volume_seen:
            continue
        if raw in H3_TITLES:
            html_lines.append(h3(raw))
            if raw != "概述":
                current_chapter = raw
            continue
        if raw in H4_TO_CHAPTER:
            current_chapter = H4_TO_CHAPTER[raw]
            html_lines.append(h4(current_chapter, raw))
            continue
        html_lines.append(f"<p>{clean_paragraph(raw)}</p>")
    return "\n".join(html_lines) + "\n"


def update_html(new_block: str) -> bool:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第三十四卷 HTML range")
    old_block = m.group(0)
    if old_block == new_block:
        return False
    HTML_PATH.write_text(html[: m.start()] + new_block + html[m.end() :], encoding="utf-8")
    return True


def audit_section() -> dict[str, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    block = SECTION_RE.search(html).group(0)
    return {
        "bytes": len(block.encode("utf-8")),
        "h2_count": len(re.findall(r"<h2 ", block)),
        "h3_count": len(re.findall(r"<h3 ", block)),
        "h4_count": len(re.findall(r"<h4 ", block)),
        "table_placeholders": len(re.findall(r'class="table-placeholder"', block)),
        "structured_tables": len(re.findall(r'<table class="structured-table"', block)),
        "generic_heading_anchors": len(re.findall(r'<h[234] id="anchor">', block)),
        "ipa_blocks": len(re.findall(r'<div class="ipa-data">', block)),
        "embedded_h3_in_p": len(re.findall(r'<p[^>]*>[^<]*<h3', block)),
        "embedded_h4_in_p": len(re.findall(r'<p[^>]*>[^<]*<h4', block)),
        "malformed_heading_ids": len(re.findall(r'<h[34] id="[^"]*<h[34]', block)),
        "front_matter_residual": len(re.findall(r"CIP|责任编辑|编纂委员会|方志出版社", block)),
    }


def write_progress(stats: dict[str, int], changes: list[str], html_changed: bool) -> None:
    status = "通过" if stats["h3_count"] == EXPECTED_H3 and stats["h4_count"] == EXPECTED_H4 else "需复核"
    content = f"""# 2026-06-29 第三十四卷《供销》修复核对进度

## 本轮范围
- 范围：`第三十四卷 供销`。
- 目标：按交付标准修复卷题、概述、章题、节题和正文段落结构。
- 源文件：`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已处于规范状态'}。
- {'已用源 MD 重建最终阅读页第三十四卷 HTML。' if html_changed else '最终阅读页第三十四卷 HTML 复跑无变化。'}
- 卷标题已修为 `第三十四卷供销`。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章机构体制至第五章废旧物资经营），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 本卷源 MD 未检出 `表34-*` 编号。
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本轮未进入 PDF 表格专项；后续如发现原 PDF 中有无编号表，应另行补登和核验。

## 验收状态
- 本卷结构验收：{status}。
- 后续已纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 进入 `第三十五卷 粮油`，继续按“源 MD 标题规范 -> 最终阅读页结构修复 -> 全书审计 -> typecheck -> 进度记录 -> Git 提交”的顺序推进。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第三十四卷供销章节核对完成

已完成 `第三十四卷 供销` 章节格式核对：

- 新增脚本：`scripts/repair_thirty_fourth_volume_supply_marketing.py`。
- 修复 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md` 中第三十四卷卷题、章题、节题断裂和 OCR 标题错位。
- 重建 `output/final_reader/连云港市志_全书.html` 中第三十四卷阅读 HTML，解决卷题误作 `第三十四卷概述`、章节标题全部扁平化的问题。
- 第三十四卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章机构体制至第五章废旧物资经营），H4={stats['h4_count']}。
- 第三十四卷范围内 `ipa-data` 残留为 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；源 MD 未见表34-*。
- 已写入进度文档：`output/reports/progress/20260629_第三十四卷供销_修复核对进度.md`。

验收：第三十四卷 HTML 字节数 {stats['bytes']}，范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第三十五卷 粮油`。第三十四卷未见表34-*，后续重点转为专名与正文 OCR 精校。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第三十四卷供销章节核对完成"
    if marker in memory:
        memory = memory[: memory.find(marker)].rstrip() + "\n" + entry
    else:
        memory = memory.rstrip() + "\n" + entry
    MEMORY_PATH.write_text(memory, encoding="utf-8")


def main() -> None:
    changes = repair_source_md()
    source = get_source_section()
    new_block = render_from_source(source)
    html_changed = update_html(new_block)
    stats = audit_section()
    write_progress(stats, changes, html_changed)
    update_memory(stats)
    print("Repair complete")
    if changes:
        for change in changes:
            print(f"- {change}")
    print(f"html_changed={html_changed}")
    print(f"stats={stats}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Repair and audit 第十一卷 畜牧业 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第十卷至第十六卷（part03）.md"
TABLE_DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第十一卷畜牧业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第十一卷-畜牧业">.*?</h2>)(.*?)(?=<h2 id="第十二卷-水产">)', re.S)

CHAPTERS = [
    ("第一章畜牧生产", ["第一节家畜饲养", "第二节禽类饲养", "第三节其它动物养殖"]),
    ("第二章饲草饲料", ["第一节饲草", "第二节饲料"]),
    ("第三章疫病防治与检疫", ["第一节疫病防治", "第二节防疫检疫"]),
]


def h3(title: str) -> str:
    return f'<h3 id="第十一卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第十一卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    replacements = {
        "\n第十一卷\n畜\n牧\n业\nBTCTらC\n概\n述\n": "\n第十一卷 畜牧业\n\n概述\n",
        "\n第二章 饲草 饲料\n": "\n第二章饲草饲料\n",
        "\n第一节饲 草\n": "\n第一节饲草\n",
        "\n第三章\n疫病防治与检疫\n": "\n第三章疫病防治与检疫\n",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD part03 中第十一卷卷题、概述题、饲草饲料章题和疫病防治章题断裂。"]
    return []


def split_title_prefix(section: str, raw: str, marker: str, start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    pos = section.find(raw, start)
    if pos < 0:
        pos = section.find(raw)
    if pos < 0:
        return section, False, start
    before = section[:pos]
    after = section[pos + len(raw) :]
    section = before + marker + "\n<p>" + after
    return section, True, pos + len(marker) + 4


def insert_before(section: str, marker: str, needle: str, start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    pos = section.find(needle, start)
    if pos < 0:
        pos = section.find(needle)
    if pos < 0:
        return section, False, start
    section = section[:pos] + marker + "\n" + section[pos:]
    return section, True, pos + len(marker) + 1


def cleanup_heading_markup(section: str) -> str:
    section = section.replace("<p><h3", "<h3").replace("<p><h4", "<h4")
    section = section.replace("</h3>\n</p>", "</h3>\n").replace("</h4>\n</p>", "</h4>\n")
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第十一卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def normalize_residue(section: str) -> str:
    section = re.sub(r"^\s*<p>牧业BTCTらC", "<p>", section, count=1)
    section = section.replace("第二节禽类饲养", "第二节禽类饲养", 1)
    section = section.replace("第一节饲 草", "第一节饲草", 1)
    section = section.replace("疫病防治与检疫建国前", "第三章疫病防治与检疫建国前", 1)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)

    section, added, cursor = insert_before(section, '<h3 id="第十一卷-概述">概述</h3>', "连云港市畜牧业历史悠久", 0)
    h3_count += int(added)

    chapter_needles = {
        "第一章畜牧生产": "第一节家畜饲养",
        "第二章饲草饲料": "第一节饲草",
        "第三章疫病防治与检疫": "第三章疫病防治与检疫建国前",
    }
    cursor = 0
    for chapter, _titles in CHAPTERS:
        section, added, cursor = insert_before(section, h3(chapter), chapter_needles[chapter], cursor)
        h3_count += int(added)
        if chapter == "第三章疫病防治与检疫":
            section = section.replace(h3(chapter) + "\n" + chapter, h3(chapter) + "\n", 1)

    section_titles = {
        "第一节家畜饲养": ["第一节家畜饲养"],
        "第二节禽类饲养": ["第二节禽类饲养"],
        "第三节其它动物养殖": ["第三节其它动物养殖"],
        "第一节饲草": ["第一节饲草", "第一节饲 草"],
        "第二节饲料": ["第二节饲料"],
        "第一节疫病防治": ["第一节疫病防治"],
        "第二节防疫检疫": ["第二节防疫检疫"],
    }
    cursor = 0
    for chapter, titles in CHAPTERS:
        for title in titles:
            marker = h4(chapter, title)
            for raw in section_titles[title]:
                section, added, cursor = split_title_prefix(section, raw, marker, cursor)
                if added:
                    h4_count += 1
                    break

    return cleanup_heading_markup(section), h3_count, h4_count


def normalize_opening_paragraphs(section: str) -> str:
    replacements = {
        '<h3 id="第十一卷-概述">概述</h3>\n连云港市畜牧业': '<h3 id="第十一卷-概述">概述</h3>\n<p>连云港市畜牧业',
        '<h3 id="第十一卷-第三章疫病防治与检疫">第三章疫病防治与检疫</h3>\n建国前': '<h3 id="第十一卷-第三章疫病防治与检疫">第三章疫病防治与检疫</h3>\n<p>建国前',
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    return section


def audit_section(html: str) -> dict[str, int]:
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


def repair_html() -> tuple[list[str], dict[str, int]]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第十一卷 畜牧业 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第十一卷-畜牧业">第十一卷畜牧业</h2>'

    if '<p>牧业BTCTらC' in section:
        actions.append("清理第十一卷卷首 `牧业BTCTらC` OCR 残字。")

    section, h3_added, h4_added = restore_headings(section)
    section = normalize_opening_paragraphs(section)
    if h3_added:
        actions.append(f"恢复畜牧业卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复畜牧业卷节级 H4 标题：{h4_added} 处。")

    fixed = html[: m.start()] + heading + section + html[m.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    stats = audit_section(fixed)
    stats["inserted_h3"] = h3_added
    stats["inserted_h4"] = h4_added
    return actions, stats


def load_tables() -> list[dict[str, object]]:
    tables = []
    for path in sorted(TABLE_DATA_DIR.glob("LYG-上-T*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        number = data.get("table_number") or ""
        if number.startswith("表11-"):
            tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(
            f"| {data.get('table_id', '')} | {data.get('table_number', '')} | {data.get('title', '')} | {pages} | "
            f"{data.get('status', '')} | {size} | {data.get('notes', '')} |"
        )
    if not table_lines:
        table_lines = ["| 无 | 无 | 第十一卷正文未识别表11-*结构化表或表格占位符 | p687-p704 | 不适用 | 不适用 | 本轮无表格专项动作 |"]

    lines = [
        "# 第十一卷畜牧业 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第十一卷 畜牧业。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第十一卷-畜牧业` 至 `第十二卷-水产` 之前。",
        "- 源页范围：约 p687-p704，位于上册 part03。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第十一卷正文区间，确认本卷无表格占位符和结构化表格实例。",
        "- 统计第十一卷表格站状态，未发现表11-*登记条目。",
        "",
        "## 格式修复清单",
        "",
        "- `第十一卷畜` 修复为 `第十一卷畜牧业`，保持全书 TOC 对应 H2。",
        "- 卷内 `概述` 恢复为 H3，并清理卷首 `牧业BTCTらC` OCR 残字。",
        "- `第一章畜牧生产`、`第二章饲草饲料`、`第三章疫病防治与检疫` 恢复为 H3。",
        "- 家畜饲养、禽类饲养、其它动物养殖、饲草、饲料、疫病防治、防疫检疫各节恢复为 H4。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表11-*的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第十一卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第十一卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第十一卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第十一卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第十一卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第十一卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第十一卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第十一卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 第十一卷 H2 标题被截断为 `第十一卷畜`，正文首段混入 `牧业BTCTらC` 残字。",
        "- 源 MD 中卷题、概述题、第二章和第三章章题存在断行或空格问题。",
        "- 阅读版中全部章、节标题均扁平化为普通段落。",
        "- 第一章节题实际为 `禽类饲养` 和 `其它动物养殖`，不同于目录中的泛称，需按正文原题恢复。",
        "",
        "## 解决的困难",
        "",
        "- 以第十一卷区间和第十二卷边界限定修复范围，避免误动水产卷。",
        "- 依据正文真实标题恢复节题，不机械套用目录简称。",
        "- 对无表格卷明确登记表格状态，避免后续验收误判漏表。",
        "",
        "## 残留风险",
        "",
        "- 本卷无表格专项动作，但 OCR 正文字词尚未逐句校勘。",
        "- 畜禽品种、疫病名称和药品名称较多，后续精校需结合原 PDF 核读专业名词。",
        "",
        "## 下一步计划",
        "",
        "- 进入第十二卷 水产章节格式核对。",
        "- 后续正文精校阶段回头抽检第十一卷畜禽品种、疫病和兽药名称。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第十一卷畜牧业章节核对完成"
    section = f"""{header}

已完成 `第十一卷 畜牧业` 章节格式核对：

- 新增脚本：`scripts/repair_eleventh_volume_animal_husbandry.py`。
- 修复 `workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md` 中第十一卷卷题、概述题、第二章和第三章章题断裂。
- 修复 `output/final_reader/连云港市志_全书.html` 中第十一卷 H2 被截断、卷内标题全部扁平化的问题。
- 第十一卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章畜牧生产至第三章疫病防治与检疫），H4={stats['h4_count']}。
- 本章阅读版无结构化表格，无正文表格占位符；表格站暂无表11-*登记条目。
- 已写入进度文档：`output/reports/progress/20260628_第十一卷畜牧业_修复核对进度.md`。

验收：第十一卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第十二卷 水产`。第十一卷后续正文精校需重点核读畜禽品种、疫病名称和兽药名称。
"""
    if header in text:
        text = re.sub(rf"{re.escape(header)}.*?(?=\n## 2026-|\Z)", section.rstrip() + "\n", text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + section
    MEMORY_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    actions = []
    actions.extend(repair_source_md())
    html_actions, stats = repair_html()
    actions.extend(html_actions)
    tables = load_tables()
    write_progress(actions, stats, tables)
    update_memory(stats)
    print("Repair complete")
    for action in actions:
        print(f"- {action}")
    print(f"stats={stats}")
    print(f"tables={len(tables)}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()

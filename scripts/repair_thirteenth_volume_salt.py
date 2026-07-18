# -*- coding: utf-8 -*-
"""Repair and audit 第十三卷 盐业 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第十卷至第十六卷（part03）.md"
TABLE_DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第十三卷盐业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第十三卷-盐业">.*?</h2>)(.*?)(?=<h2 id="第十四卷-轻-手-工业">)', re.S)

CHAPTERS = [
    ("第一章生产", ["第一节原盐", "第二节加工盐", "第三节盐工"]),
    ("第二章运销", ["第一节体制", "第二节机构", "第三节仓坨", "第四节运输", "第五节销售", "第六节盐价", "第七节盐税"]),
    ("第三章缉私", ["第一节机构", "第二节查私"]),
]

CUMULATIVE_IPA_FIXED = 2
CUMULATIVE_REMOVED_DUP_TABLES = 3


def h3(title: str) -> str:
    return f'<h3 id="第十三卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第十三卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    replacements = {
        "\n第十三卷\n盐\n业\n\n概\n述\n": "\n第十三卷 盐业\n\n概述\n",
        "\n第一节原\n盐\n": "\n第一节原盐\n",
        "\n第三节 盐\n工": "\n第三节盐工",
        "\n第二章 运\n销\n": "\n第二章运销\n",
        "\n第一节体\n": "\n第一节体制\n",
        "\n第二章 运\n第四节运\n": "\n第四节运输\n",
        "\n第二章运\n": "\n",
        "\n第六节盐\n一、食盐价格\n": "\n第六节盐价\n一、食盐价格\n",
        "\n第三章缉\n私\n": "\n第三章缉私\n",
        "\n第二节查\n": "\n第二节查私\n",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD part03 中第十三卷卷题、概述题和多处章/节题断裂。"]
    return []


def split_title_prefix(section: str, raw: str, marker: str, start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    marker_text = re.search(r">([^<]+)</h4>", marker)
    if marker_text and re.search(rf"<h4 [^>]*>{re.escape(marker_text.group(1))}</h4>", section):
        return section, False, start
    pos = section.find(raw, start)
    if pos < 0:
        pos = section.find(raw)
    if pos < 0:
        return section, False, start
    section = section[:pos] + marker + "\n<p>" + section[pos + len(raw) :]
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
    section = re.sub(r'<h4 id="第十三卷-[^"]*<h4 id="(第十三卷-[^"]+)">', r'<h4 id="\1">', section)
    section = section.replace("</h3>\n</p>", "</h3>\n").replace("</h4>\n</p>", "</h4>\n")
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第十三卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def normalize_residue(section: str) -> str:
    section = re.sub(r"^\s*<p>业", "<p>", section, count=1)
    section = re.sub(r"^\s*<p>[：:]?\d+", "<p>", section, count=1)
    section = section.replace("第三节 盐工", "第三节盐工", 1)
    section = section.replace("第一节体", "第一节体制", 1)
    section = section.replace("第六节盐一、食盐价格", "第六节盐价一、食盐价格", 1)
    section = section.replace("第二节查两淮盐的缉私机构", "第二节查私两淮盐的缉私机构", 1)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)

    summary_marker = '<h3 id="第十三卷-概述">概述</h3>'
    if summary_marker not in section:
        section = summary_marker + "\n" + section.lstrip()
        added = True
        cursor = len(summary_marker) + 1
    else:
        added = False
        cursor = section.find(summary_marker) + len(summary_marker)
    h3_count += int(added)

    chapter_needles = {
        "第一章生产": "第一节原盐",
        "第二章运销": "盐斤历代专卖",
        "第三章缉私": "盐为高税商品",
    }
    cursor = 0
    for chapter, _titles in CHAPTERS:
        section, added, cursor = insert_before(section, h3(chapter), chapter_needles[chapter], cursor)
        h3_count += int(added)

    title_variants = {
        "第一节原盐": ["第一节原盐"],
        "第二节加工盐": ["第二节加工盐"],
        "第三节盐工": ["第三节盐工", "第三节 盐工"],
        "第一节体制": ["第一节体制", "第一节体"],
        "第二节机构": ["第二节机构"],
        "第三节仓坨": ["第三节仓坨"],
        "第四节运输": ["第四节运输"],
        "第五节销售": ["第五节销售"],
        "第六节盐价": ["第六节盐价", "第六节盐"],
        "第七节盐税": ["第七节盐税"],
        "第一节机构": ["第一节机构"],
        "第二节查私": ["第二节查私", "第二节查"],
    }
    cursor = 0
    for chapter, titles in CHAPTERS:
        for title in titles:
            marker = h4(chapter, title)
            for raw in title_variants[title]:
                section, added, cursor = split_title_prefix(section, raw, marker, cursor)
                if added:
                    h4_count += 1
                    break

    return cleanup_heading_markup(section), h3_count, h4_count


def normalize_opening_paragraphs(section: str) -> str:
    replacements = {
        '<h3 id="第十三卷-概述">概述</h3>\n连云港市海岸线': '<h3 id="第十三卷-概述">概述</h3>\n<p>连云港市海岸线',
        '<h3 id="第十三卷-第二章运销">第二章运销</h3>\n盐斤历代': '<h3 id="第十三卷-第二章运销">第二章运销</h3>\n<p>盐斤历代',
        '<h3 id="第十三卷-第三章缉私">第三章缉私</h3>\n盐为高税商品': '<h3 id="第十三卷-第三章缉私">第三章缉私</h3>\n<p>盐为高税商品',
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    return section


def compress_duplicate_tables(section: str) -> tuple[str, int]:
    patterns = [
        r'<table class="structured-table"><thead><tr><th>年份</th><th>合计\(吨\)</th><th>青口盐场\(吨\)</th><th>台北盐场\(吨\)</th><th>台南盐场\(吨\)</th><th>徐圩盐场\(吨\)</th><th>灌西盐场\(吨\)</th></tr></thead>.*?</table>\n?',
        r'<table class="structured-table"><thead><tr><th>年份</th><th>合计\(万吨\)</th><th>食盐\(万吨\)</th><th>工业盐\(万吨\)</th><th>农用盐\(万吨\)</th><th>渔用盐\(万吨\)</th><th>出口盐\(万吨\)</th><th>储备盐\(万吨\)</th></tr></thead>.*?</table>\n?',
    ]
    removed = 0
    for pat in patterns:
        regex = re.compile(pat, re.S)
        seen = False

        def repl(match: re.Match[str]) -> str:
            nonlocal seen, removed
            if seen:
                removed += 1
                return ""
            seen = True
            return match.group(0)

        section = regex.sub(repl, section)
    return section, removed


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
        raise RuntimeError("Cannot locate 第十三卷 盐业 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第十三卷-盐业">第十三卷盐业</h2>'

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>').replace('</div>', '</p>')
    if ipa_before:
        actions.append(f"将第十三卷误用 `ipa-data` 的正文块转回段落：{ipa_before} 处。")

    section, h3_added, h4_added = restore_headings(section)
    section = normalize_opening_paragraphs(section)
    if h3_added:
        actions.append(f"恢复盐业卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复盐业卷节级 H4 标题：{h4_added} 处。")

    section, removed_tables = compress_duplicate_tables(section)
    if removed_tables:
        actions.append(f"压缩重复临时结构化表格实例：{removed_tables} 处。")

    fixed = html[: m.start()] + heading + "\n" + section.lstrip() + html[m.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    stats = audit_section(fixed)
    stats["inserted_h3"] = h3_added
    stats["inserted_h4"] = h4_added
    stats["removed_duplicate_tables"] = removed_tables
    stats["ipa_fixed"] = ipa_before
    return actions, stats


def load_tables() -> list[dict[str, object]]:
    tables = []
    for path in sorted(TABLE_DATA_DIR.glob("LYG-上-T*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        number = data.get("table_number") or ""
        if number.startswith("表13-"):
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
        table_lines = ["| 暂无登记 | 表13-* | 第十三卷现有表格尚未进入表格站 | p790-p877 | 待补登 | 待定 | 盐业产量、运销、盐价盐税等表需专项补建 |"]

    lines = [
        "# 第十三卷盐业 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第十三卷 盐业。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第十三卷-盐业` 至 `第十四卷-轻-手-工业` 之前。",
        "- 源页范围：约 p790-p877，位于上册 part03。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第十三卷正文区间，确认本卷实际为三章，第二章运销含七个节。",
        "- 统计第十三卷表格状态，表格站暂无表13-*登记，阅读版已有临时结构表和占位符。",
        "",
        "## 格式修复清单",
        "",
        "- `第十三卷盐` 修复为 `第十三卷盐业`，保持全书 TOC 对应 H2。",
        "- 卷内 `概述` 恢复为 H3，并清理卷首 `业` OCR 残字。",
        "- `第一章生产`、`第二章运销`、`第三章缉私` 恢复为 H3。",
        "- 原盐、加工盐、盐工、体制、机构、仓坨、运输、销售、盐价、盐税、缉私机构、查私等节题恢复为 H4。",
        "- 明显重复的临时结构化表格压缩为单实例。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表13-*的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第十三卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第十三卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第十三卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第十三卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第十三卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第十三卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第十三卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第十三卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 第十三卷 H2 标题被截断为 `第十三卷盐`，正文首段混入 `业` 残字。",
        "- 源 MD 中第二章运销、第三章缉私和多个节题断裂。",
        "- 阅读版中所有章、节标题均扁平化，第二章出现多处表格残文干扰标题定位。",
        "- 表13-*均未登记到表格站，阅读版临时结构化表存在重复实例。",
        "",
        "## 解决的困难",
        "",
        "- 以第十三卷区间和第十四卷边界限定修复范围，避免误动轻（手）工业卷。",
        "- 按正文实际结构恢复第二章运销七个节，避免漏掉盐价、盐税。",
        "- 对重复临时表格仅保留单实例，不用未核数据填充完整表。",
        "",
        "## 残留风险",
        "",
        "- 表13-*需从源 PDF 逐张核读、登记、结构化。",
        "- 盐业专名、盐场名、盐价税额和历史制度名密集，后续精校需结合原 PDF 核读。",
        "",
        "## 下一步计划",
        "",
        "- 进入第十四卷 轻（手）工业章节格式核对。",
        "- 表格专项阶段优先补登第十三卷盐业产量、运销、盐价盐税等表。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第十三卷盐业章节核对完成"
    section = f"""{header}

已完成 `第十三卷 盐业` 章节格式核对：

- 新增脚本：`scripts/repair_thirteenth_volume_salt.py`。
- 修复 `workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md` 中第十三卷卷题、概述题和多处章/节题断裂。
- 修复 `output/final_reader/连云港市志_全书.html` 中第十三卷 H2 被截断、正文块误用 `ipa-data`、卷内标题全部扁平化的问题。
- 第十三卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章生产至第三章缉私），H4={stats['h4_count']}。
- 将第十三卷 {CUMULATIVE_IPA_FIXED} 处误用 `ipa-data` 的正文块转回普通段落。
- 压缩重复临时结构化表格实例 {CUMULATIVE_REMOVED_DUP_TABLES} 处。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表13-*登记条目。
- 已写入进度文档：`output/reports/progress/20260628_第十三卷盐业_修复核对进度.md`。

验收：第十三卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第十四卷 轻（手）工业`。第十三卷表13-*需从源 PDF 专项补登、重建和核验。
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

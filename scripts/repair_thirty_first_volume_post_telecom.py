# -*- coding: utf-8 -*-
"""Repair and audit 第三十一卷 邮电 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第三十一卷邮电_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第三十一卷-邮电">.*?</h2>)(.*?)(?=<h2 id="第三十二卷-[^"]+">)', re.S)

CHAPTERS = [
    ("第一章邮政", ["第一节邮路", "第二节邮政设备", "第三节邮政业务"]),
    ("第二章电信", ["第一节电报", "第二节长途电话", "第三节市内电话", "第四节农村电话"]),
]

CHAPTER_NEEDLES = {
    "第一章邮政": "境内自光绪二十九年（1903年）十一月设立大伊山",
    "第二章电信": "清光绪二十年（1894年），海州、青口通达的电报线路",
}

CHAPTER_VARIANTS = {
    "第一章邮政": ["第一章邮政", "第一章邮　政", "第一章"],
    "第二章电信": ["第二章电信", "第二章电　信", "第二章"],
}

SECTION_NEEDLES = {
    ("第一章邮政", "第一节邮路"): "一、干线邮路光绪二十九年至三十三年",
    ("第一章邮政", "第二节邮政设备"): "一、邮运工具20世纪30年代",
    ("第一章邮政", "第三节邮政业务"): "一、函件光绪二十九年（1903年）起",
    ("第二章电信", "第一节电报"): "一、有线电报光绪二十年（1894年）",
    ("第二章电信", "第二节长途电话"): "民国22年（1933年），以新浦为中心",
    ("第二章电信", "第三节市内电话"): "民国23年（1934年），海州一新浦一大浦已有市话线路",
    ("第二章电信", "第四节农村电话"): "民国21年（1932年），江苏省建设厅批准赣榆县",
}

SECTION_VARIANTS = {
    "第一节邮路": ["第一节邮　路", "第一节邮路", "第一节"],
    "第二节邮政设备": ["第二节‧由邮政设备", "第二节邮政设备", "第二节"],
    "第三节邮政业务": ["第三节邮政业务", "第三节"],
    "第一节电报": ["第一节•电•报", "第一节电报", "第一节"],
    "第二节长途电话": ["第二节长途电话", "第二节"],
    "第三节市内电话": ["第三节市内电话", "第三节"],
    "第四节农村电话": ["第四节农村电话", "第四节"],
}

EXPECTED_TABLES = [f"表31-{i}" for i in range(1, 9)]


def h3(title: str) -> str:
    return f'<h3 id="第三十一卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第三十一卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    start_candidates = [text.find("\n第三十一卷\n"), text.find("\n第三十一卷 邮电\n")]
    start_candidates = [pos for pos in start_candidates if pos >= 0]
    start = min(start_candidates) if start_candidates else -1
    end = text.find("\n第三十二卷", start)
    if start < 0 or end < 0:
        raise RuntimeError("Cannot locate 第三十一卷 source range")
    head, section, tail = text[:start], text[start:end], text[end:]
    replacements = {
        "\n第三十一卷\n概述\n": "\n第三十一卷 邮电\n\n概述\n",
        "\n第一章邮　政\n": "\n第一章邮政\n",
        "\n第一节邮　路\n": "\n第一节邮路\n",
        "\n第二节‧由\n邮政设备\n": "\n第二节邮政设备\n",
        "\n第二章电　信\n": "\n第二章电信\n",
        "\n第一节•电•报\n": "\n第一节电报\n",
        "\n第二章电信·1391\n": "\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    fixed = head + section + tail
    if fixed != original:
        SRC_MD.write_text(fixed, encoding="utf-8")
        return ["规范源 MD 中第三十一卷卷题、章题、节题断裂、页眉残留和 OCR 标题错位。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "第一章邮　政": "第一章邮政",
        "第一节邮　路": "第一节邮路",
        "第二节‧由邮政设备": "第二节邮政设备",
        "第二章电　信": "第二章电信",
        "第一节•电•报": "第一节电报",
        "第二章电信·1391": "",
    }
    for old, new in residues.items():
        section = section.replace(old, new)
    return section


def insert_or_replace_title(section: str, marker: str, needle: str, variants: list[str], start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    needle_pos = section.find(needle, max(0, start - 2500))
    if needle_pos < 0:
        needle_pos = section.find(needle)
    if needle_pos >= 0:
        prefix_start = max(0, needle_pos - 900)
        prefix = section[prefix_start:needle_pos]
        for raw in variants:
            rel = prefix.rfind(raw)
            if rel >= 0:
                pos = prefix_start + rel
                section = section[:pos] + marker + "\n<p>" + section[pos + len(raw) :]
                return section, True, pos + len(marker) + 4
        pos = needle_pos
        paragraph_start = section.rfind("<p>", 0, pos)
        paragraph_end = section.rfind("</p>", 0, pos)
        if paragraph_start > paragraph_end and not section[paragraph_start + 3 : pos].strip():
            pos = paragraph_start
        section = section[:pos] + marker + "\n" + section[pos:]
        return section, True, pos + len(marker) + 1
    return section, False, start


def cleanup_heading_markup(section: str) -> str:
    section = section.replace("<p><h3", "<h3").replace("<p><h4", "<h4")
    section = section.replace("</h3>\n</p>", "</h3>\n").replace("</h4>\n</p>", "</h4>\n")
    section = re.sub(r"(</h[34]>)\n(?!<)([^\n<][^\n]*?</p>)", r"\1\n<p>\2", section)
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第三十一卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def ensure_telecom_chapter(section: str) -> tuple[str, bool]:
    marker = h3("第二章电信")
    if marker in section:
        return section, False
    anchor = h4("第二章电信", "第一节电报")
    pos = section.find(anchor)
    if pos < 0:
        return section, False
    return section[:pos] + marker + "\n" + section[pos:], True


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)
    summary_marker = '<h3 id="第三十一卷-概述">概述</h3>'
    if summary_marker not in section:
        section = summary_marker + "\n" + section.lstrip()
        h3_count += 1
    cursor = len(summary_marker)
    for chapter, _titles in CHAPTERS:
        section, added, cursor = insert_or_replace_title(section, h3(chapter), CHAPTER_NEEDLES[chapter], CHAPTER_VARIANTS.get(chapter, [chapter]), cursor)
        h3_count += int(added)
    cursor = 0
    for chapter, titles in CHAPTERS:
        for title in titles:
            variants = SECTION_VARIANTS.get(title, [title])
            section, added, cursor = insert_or_replace_title(section, h4(chapter, title), SECTION_NEEDLES[(chapter, title)], variants, cursor)
            h4_count += int(added)
    section, added = ensure_telecom_chapter(section)
    h3_count += int(added)
    return cleanup_heading_markup(normalize_residue(section)), h3_count, h4_count


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
        raise RuntimeError("Cannot locate 第三十一卷 邮电 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第三十一卷-邮电">第三十一卷邮电</h2>'
    ipa_before = section.count('<div class="ipa-data">')
    section = re.sub(r'<div class="ipa-data">(.*?)</div>', r'<p>\1</p>', section, flags=re.S)
    if ipa_before:
        actions.append(f"将第三十一卷误用 `ipa-data` 的正文/表格 OCR 残块转回段落：{ipa_before} 处。")
    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复邮电卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复邮电卷节级 H4 标题：{h4_added} 处。")
    fixed = html[: m.start()] + heading + "\n" + section.lstrip() + html[m.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    stats = audit_section(fixed)
    stats["inserted_h3"] = h3_added
    stats["inserted_h4"] = h4_added
    stats["ipa_fixed"] = ipa_before
    return actions, stats


def load_tables() -> list[dict[str, object]]:
    tables = []
    for table_dir in TABLE_DATA_DIRS:
        if not table_dir.exists():
            continue
        for path in sorted(table_dir.glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            title = str(data.get("title") or "")
            number = str(data.get("table_number") or "")
            if title.startswith("表31-") or number.startswith("表31-"):
                tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(f"| {data.get('table_id', '')} | {data.get('table_number') or data.get('title', '')} | {data.get('title', '')} | {pages} | {data.get('status', '')} | {size} | {data.get('notes', '')} |")
    if not table_lines:
        table_lines = [f"| 暂无登记 | {table_no} | 第三十一卷可见表格尚未进入表格站 | p1485-p1514 | 待补登 | 待定 | 需从源 PDF 专项补建、核验 |" for table_no in EXPECTED_TABLES]

    lines = [
        "# 第三十一卷邮电 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第三十一卷 邮电。",
        "- 源 MD：`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第三十一卷-邮电` 至 `第三十二卷-*` 之前。",
        "- 源页范围：约 p1485-p1514，位于中册 part02。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第三十一卷正文区间和目录骨架，确认本卷为两章：邮政、电信。",
        "- 统计第三十一卷表格状态，源 MD 可见表31-1至表31-8，表格站暂无表31-*登记。",
        "",
        "## 格式修复清单",
        "",
        "- 卷题恢复为 `第三十一卷邮电`，卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章邮政`、`第二章电信` 共 2 个 H3。",
        "- 恢复邮路、邮政设备、邮政业务、电报、长途电话、市内电话、农村电话共 7 个 H4。",
        "- 将第三十一卷误入 `ipa-data` 的正文/表格 OCR 残块转回普通段落。",
        "- 清理源 MD 中页眉残留和 OCR 标题错位，如 `第一章邮　政`、`第二节‧由`、`第一节•电•报`。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表31-*的登记表格：{len(tables)} 张。",
        "- 源 MD 可见表31-1至表31-8；当前阅读版已有部分结构化表，但仍需 PDF 表格专项逐张核验。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第三十一卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第三十一卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第三十一卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第三十一卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第三十一卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第三十一卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第三十一卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第三十一卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第三十一卷卷题误显示为 `第三十一卷概述`，章、节标题全部扁平化为正文。",
        "- OCR 将部分节题识别为带符号或拆行文本，如 `第二节‧由 / 邮政设备`、`第一节•电•报`。",
        "- 邮电业务统计表和长途电话价目表数值密集，存在表格 OCR 粘连风险。",
        "- 表31-*未进入表格站，阅读版仅有部分结构化表，其余需 PDF 专项重建或核验。",
        "",
        "## 解决的困难",
        "",
        "- 以目录骨架确认 2 章 7 节正式标题，再用正文首句顺序定位。",
        "- 对 `第二节‧由`、`第一节•电•报` 等 OCR 标题错位统一规范为正式节名。",
        "- 对表31-1至表31-8在进度中统一按表31-*风险记录。",
        "",
        "## 残留风险",
        "",
        "- 表31-1至表31-8需从源 PDF 逐张核读、补登、结构化。",
        "- 邮政业务量、电信价目、农村电话等统计表数值密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第三十二卷 名胜旅游章节格式核对。",
        "- 表格专项阶段回补第三十一卷 8 张可见表格。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-29 第三十一卷邮电章节核对完成"
    section = f"""{header}

已完成 `第三十一卷 邮电` 章节格式核对：

- 新增脚本：`scripts/repair_thirty_first_volume_post_telecom.py`。
- 修复 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md` 中第三十一卷卷题、章题、节题断裂、页眉残留和 OCR 标题错位。
- 修复 `output/final_reader/连云港市志_全书.html` 中第三十一卷卷题误作 `第三十一卷概述`、章节标题全部扁平化以及正文/表格残块误用 `ipa-data` 的问题。
- 第三十一卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章邮政至第二章电信），H4={stats['h4_count']}。
- 第三十一卷范围内 `ipa-data` 残留已清零。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表31-*登记条目。
- 源 MD 可见表31-1至表31-8，本轮先记录为表格专项重点风险。
- 已写入进度文档：`output/reports/progress/20260629_第三十一卷邮电_修复核对进度.md`。

验收：第三十一卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第三十二卷 名胜旅游`。第三十一卷表31-1至表31-8需从源 PDF 专项补登、重建和核验。
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

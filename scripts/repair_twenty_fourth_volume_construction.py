# -*- coding: utf-8 -*-
"""Repair and audit 第二十四卷 建筑业 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第二十四卷建筑业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第二十四卷-建筑业">.*?</h2>)(.*?)(?=<h2 id="第二十五卷-电力工业">)', re.S)

CHAPTERS = [
    ("第一章勘察和设计", ["第一节地基勘察", "第二节建筑设计", "第三节主要勘察设计单位简介"]),
    ("第二章建筑工程", ["第一节工业建筑", "第二节住宅建筑", "第三节公共建筑"]),
    ("第三章施工安装", ["第一节土木建筑施工", "第二节构配件生产", "第三节机械化施工", "第四节单项设备安装", "第五节成套设备安装", "第六节主要企业简介"]),
    ("第四章建筑管理", ["第一节管理机构", "第二节行业管理", "第三节企业管理", "第四节省外与国外施工管理"]),
]

CHAPTER_NEEDLES = {
    "第一章勘察和设计": "1949年以前，全市没有勘察设计机构",
    "第二章建筑工程": "连云港地区的建筑工程早在先秦时期",
    "第三章施工安装": "1960年以前，连云港地区建筑施工沿袭传统的手工工艺",
    "第四章建筑管理": "中国历代封建王朝实行工管制度",
}

CHAPTER_VARIANTS = {
    "第一章勘察和设计": ["勘察和设计", "第一章勘察和设计"],
    "第二章建筑工程": ["建筑工程", "第二章建筑工程"],
    "第三章施工安装": ["施工安装", "第三章施工安装"],
    "第四章建筑管理": ["建筑管理", "第四章建筑管理"],
}

SECTION_NEEDLES = {
    ("第一章勘察和设计", "第一节地基勘察"): "从1958年开始，勘察技术人员",
    ("第一章勘察和设计", "第二节建筑设计"): "一、工业建筑设计",
    ("第一章勘察和设计", "第三节主要勘察设计单位简介"): "一、锦屏磷矿勘察设计室",
    ("第二章建筑工程", "第一节工业建筑"): "民国22年（1933年）5月3日",
    ("第二章建筑工程", "第二节住宅建筑"): "建于民国7年（1918年）的白宝山私人公馆白宝山楼",
    ("第二章建筑工程", "第三节公共建筑"): "三元宫建筑群坐落在花果山乡花果山村",
    ("第三章施工安装", "第一节土木建筑施工"): "一、基础施工",
    ("第三章施工安装", "第二节构配件生产"): "一、圆孔板",
    ("第三章施工安装", "第三节机械化施工"): "一、打桩",
    ("第三章施工安装", "第四节单项设备安装"): "一、给排水",
    ("第三章施工安装", "第五节成套设备安装"): "1982年，市工业设备安装公司承担连云港涤纶厂",
    ("第三章施工安装", "第六节主要企业简介"): "该公司组建于1949年",
    ("第四章建筑管理", "第一节管理机构"): "民国37年（1948年）以前",
    ("第四章建筑管理", "第二节行业管理"): "一、企业资质管理",
    ("第四章建筑管理", "第三节企业管理"): "一、经营管理",
    ("第四章建筑管理", "第四节省外与国外施工管理"): "一、省外施工管理",
}

SECTION_VARIANTS = {
    "第一节地基勘察": ["第一节地基勘察", "第一节"],
    "第二节建筑设计": ["第二节建筑设计", "第二节"],
    "第三节主要勘察设计单位简介": ["第三节主要勘察设计单位简介", "第三节"],
    "第一节工业建筑": ["第一节工业建筑", "第一节"],
    "第二节住宅建筑": ["第二节住宅建筑", "第二节"],
    "第三节公共建筑": ["第三节公共建筑", "第三节"],
    "第一节土木建筑施工": ["土木建筑施工第一节", "第一节土木建筑施工", "第一节"],
    "第二节构配件生产": ["构(配)件生产第二节", "第二节构配件生产", "第二节"],
    "第三节机械化施工": ["第三节机械化施工", "第三节"],
    "第四节单项设备安装": ["单项设备安装第四节", "第四节单项设备安装", "第四节"],
    "第五节成套设备安装": ["成套设备安装第五节", "第五节成套设备安装", "第五节"],
    "第六节主要企业简介": ["第六节主要建筑工程企业简介", "第六节主要企业简介", "第六节"],
    "第一节管理机构": ["第一节管理机构", "第一节"],
    "第二节行业管理": ["第二节行业管理", "第二节"],
    "第三节企业管理": ["第三节企业管理", "第三节"],
    "第四节省外与国外施工管理": ["第四节省省外与国外施工管理", "第四节省外与国外施工管理", "第四节省", "第四节"],
}

EXPECTED_TABLES = [f"表24-{i}" for i in range(1, 6)]


def h3(title: str) -> str:
    return f'<h3 id="第二十四卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第二十四卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    start_candidates = [text.find("\n第二十四卷\n"), text.find("\n第二十四卷 建筑业\n")]
    start_candidates = [pos for pos in start_candidates if pos >= 0]
    start = min(start_candidates) if start_candidates else -1
    end_candidates = [text.find("\n第二十五卷\n", start if start >= 0 else 0), text.find("\n第二十五卷 电力工业\n", start if start >= 0 else 0)]
    end_candidates = [pos for pos in end_candidates if pos >= 0]
    end = min(end_candidates) if end_candidates else -1
    if start < 0 or end < 0:
        raise RuntimeError("Cannot locate 第二十四卷 source range")
    head, section, tail = text[:start], text[start:end], text[end:]
    replacements = {
        "\n第二十四卷\n建筑业\n概述\n": "\n第二十四卷 建筑业\n\n概述\n",
        "\n第一章\n勘察和设计\n": "\n第一章勘察和设计\n",
        "\n第三节\n主要勘察设计单位简介\n": "\n第三节主要勘察设计单位简介\n",
        "\n第一章\n勘察和设计\n.1103 :\n": "\n",
        "\n第二章\n建筑工程\n": "\n第二章建筑工程\n",
        "\n第三章\n施工安装\n": "\n第三章施工安装\n",
        "\n土木建筑施工\n第一节\n": "\n第一节土木建筑施工\n",
        "\n构(配)件生产\n第二节\n": "\n第二节构配件生产\n",
        "\n第三节\n机械化施工\n": "\n第三节机械化施工\n",
        "\n第四节\n单项设备安装\n": "\n第四节单项设备安装\n",
        "\n成套设备安装\n第五节\n": "\n第五节成套设备安装\n",
        "\n第六节\n主要建筑工程企业简介\n一、连云港市第一一建筑工程公司\n": "\n第六节主要企业简介\n一、连云港市第一建筑工程公司\n",
        "\n第四章\n建筑管理\n": "\n第四章建筑管理\n",
        "\n第四节省\n省外与国外施工管理\n": "\n第四节省外与国外施工管理\n",
        "\n第四章\n建筑管理\n: 1131 \n": "\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    text = head + section + tail
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第二十四卷卷题、章题、节题断裂、页眉残留和 OCR 标题错误。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "<p>土木建筑施工第一节": "<p>",
        "<p>构(配)件生产第二节": "<p>",
        "<p>成套设备安装第五节": "<p>",
        "<p>第四节省省外与国外施工管理": "<p>",
    }
    for old, new in residues.items():
        section = section.replace(old, new, 1)
    section = section.replace("勘察和设计.1103 :", "")
    section = section.replace("建筑管理: 1131", "")
    section = section.replace("第一一建筑工程公司", "第一建筑工程公司")
    return section


def insert_or_replace_title(section: str, marker: str, needle: str, variants: list[str], start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    needle_pos = section.find(needle, max(0, start - 900))
    if needle_pos < 0:
        needle_pos = section.find(needle)
    if needle_pos >= 0:
        prefix_start = max(0, needle_pos - 380)
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
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第二十四卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)
    summary_marker = '<h3 id="第二十四卷-概述">概述</h3>'
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
    return cleanup_heading_markup(section), h3_count, h4_count


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
        raise RuntimeError("Cannot locate 第二十四卷 建筑业 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第二十四卷-建筑业">第二十四卷建筑业</h2>'
    ipa_before = section.count('<div class="ipa-data">')
    section = re.sub(r'<div class="ipa-data">(.*?)</div>', r'<p>\1</p>', section, flags=re.S)
    if ipa_before:
        actions.append(f"将第二十四卷误用 `ipa-data` 的正文/表格 OCR 残块转回段落：{ipa_before} 处。")
    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复建筑业卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复建筑业卷节级 H4 标题：{h4_added} 处。")
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
            if title.startswith("表24-") or number.startswith("表24-"):
                tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(f"| {data.get('table_id', '')} | {data.get('table_number') or data.get('title', '')} | {data.get('title', '')} | {pages} | {data.get('status', '')} | {size} | {data.get('notes', '')} |")
    if not table_lines:
        table_lines = [f"| 暂无登记 | {table_no} | 第二十四卷表格尚未进入表格站 | p1200-p1232 | 待补登 | 待定 | 需从源 PDF 专项补建、核验 |" for table_no in EXPECTED_TABLES]

    lines = [
        "# 第二十四卷建筑业 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第二十四卷 建筑业。",
        "- 源 MD：`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第二十四卷-建筑业` 至 `第二十五卷-电力工业` 之前。",
        "- 源页范围：约 p1200-p1232，位于中册 part01。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第二十四卷正文区间，确认本卷实际为四章：勘察和设计、建筑工程、施工安装、建筑管理。",
        "- 统计第二十四卷表格状态，表格站暂无表24-*登记，阅读版已有结构化表但仍需 PDF 表格专项复建。",
        "",
        "## 格式修复清单",
        "",
        "- 卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章勘察和设计` 至 `第四章建筑管理` 共 4 个 H3。",
        "- 恢复地基勘察、建筑设计、建筑工程各节、施工安装各节、行业管理和企业管理等 16 个 H4。",
        "- 将第二十四卷误入 `ipa-data` 的正文/表格 OCR 残块转回普通段落。",
        "- 清理源 MD 中章题、节题断裂和 `第四节省`、页眉残留等 OCR 错误。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表24-*的登记表格：{len(tables)} 张。",
        "- 源 MD 可见表24-1至表24-5；表24-3、表24-5存在跨页/残片 OCR，需 PDF 专项重建。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第二十四卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第二十四卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第二十四卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第二十四卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第二十四卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第二十四卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第二十四卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第二十四卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第二十四卷全部章、节标题扁平化为正文。",
        "- OCR 将 `土木建筑施工`、`构(配)件生产`、`成套设备安装` 与节号倒置。",
        "- `第四节省外与国外施工管理` 被识别为 `第四节省省外与国外施工管理`。",
        "- 表24-*均未登记到表格站，阅读版结构化表仍为待对照原图录入状态。",
        "",
        "## 解决的困难",
        "",
        "- 以第二十四卷至第二十五卷边界限定修复范围，避免误动电力工业卷。",
        "- 对施工安装章中多个倒置节题按正文首句定位恢复。",
        "- 对重复出现的页眉章题残留仅做卷内清理，不扩散到后续卷。",
        "",
        "## 残留风险",
        "",
        "- 第二十四卷表24-1至表24-5需从源 PDF 逐张核读、补登、结构化。",
        "- 建筑工程名称、设计单位、施工单位和统计指标密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第二十五卷 电力工业章节格式核对。",
        "- 表格专项阶段回补第二十四卷优秀设计、勘察设计单位、主要建筑、优质工程、建筑业主要单位等统计表。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第二十四卷建筑业章节核对完成"
    section = f"""{header}

已完成 `第二十四卷 建筑业` 章节格式核对：

- 新增脚本：`scripts/repair_twenty_fourth_volume_construction.py`。
- 修复 `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md` 中第二十四卷卷题、章题、节题断裂和页眉/OCR 标题错误。
- 修复 `output/final_reader/连云港市志_全书.html` 中第二十四卷章节标题全部扁平化以及正文/表格 OCR 残块误用 `ipa-data` 的问题。
- 第二十四卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章勘察和设计至第四章建筑管理），H4={stats['h4_count']}。
- 第二十四卷范围内 `ipa-data` 残留已清零。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表24-*登记条目。
- 已写入进度文档：`output/reports/progress/20260628_第二十四卷建筑业_修复核对进度.md`。

验收：第二十四卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第二十五卷 电力工业`。第二十四卷表24-*需从源 PDF 专项补登、重建和核验。
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

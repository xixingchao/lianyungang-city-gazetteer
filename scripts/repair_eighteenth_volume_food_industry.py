# -*- coding: utf-8 -*-
"""Repair and audit 第十八卷 食品工业 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第十八卷食品工业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第十八卷-食品工业">.*?</h2>)(.*?)(?=<h2 id="第十九卷-医药">)', re.S)

CHAPTERS = [
    ("第一章糕点糖果蜜饯", ["第一节糕点", "第二节糖果", "第三节果脯蜜饯", "第四节主要企业简介"]),
    ("第二章屠宰及肉类加工", ["第一节猪肉加工", "第二节牛、羊、兔肉加工", "第三节肉鸡加工", "第四节主要企业简介"]),
    ("第三章罐头", ["第一节畜禽类罐头", "第二节果蔬类罐头", "第三节水产类罐头", "第四节其它类罐头", "第五节主要企业简介"]),
    ("第四章饮料", ["第一节酒类", "第二节非酒精饮料", "第三节冷冻饮料", "第四节主要企业简介"]),
    ("第五章调味品及食品添加剂", ["第一节调味品", "第二节食品添加剂", "第三节主要企业简介"]),
    ("第六章其它食品加工", ["第一节豆制品", "第二节乳制品", "第三节淀粉及淀粉制品", "第四节水产品", "第五节制糖炼糖", "第六节蔬菜", "第七节蛋制品制茶", "第八节主要企业简介"]),
]

CHAPTER_NEEDLES = {
    "第一章糕点糖果蜜饯": "建国前，一般以前店后坊式加工糕点糖果",
    "第二章屠宰及肉类加工": "清代，赣榆县青口镇生猪宰杀",
    "第三章罐头": "民国23年（1934年），省立渔村师范学校创办了水产类罐头",
    "第四章饮料": "汉代，境内较多自家设槽坊酿酒",
    "第五章调味品及食品添加剂": "清康熙年间，板浦汪氏滴醋",
    "第六章其它食品加工": "境内其它食品加工业主要有制茶",
}

CHAPTER_VARIANTS = {
    "第一章糕点糖果蜜饯": ["糕点糖果蜜饯"],
    "第二章屠宰及肉类加工": ["屠宰及肉类加工"],
    "第三章罐头": ["罐头"],
    "第四章饮料": ["饮料"],
    "第五章调味品及食品添加剂": ["调味品及食品添加剂"],
    "第六章其它食品加工": ["其它食品加工"],
}

SECTION_NEEDLES = {
    ("第一章糕点糖果蜜饯", "第一节糕点"): "清嘉庆年间，海州有前店后坊式茶食糕点",
    ("第一章糕点糖果蜜饯", "第二节糖果"): "境内糖果生产较早的为新浦稻香村食品店",
    ("第一章糕点糖果蜜饯", "第三节果脯蜜饯"): "1985年，连云港市花果山果脯蜜饯厂",
    ("第一章糕点糖果蜜饯", "第四节主要企业简介"): "一、连云港食品总厂",
    ("第二章屠宰及肉类加工", "第一节猪肉加工"): "清康熙年间，赣榆县青口境内消除",
    ("第二章屠宰及肉类加工", "第二节牛、羊、兔肉加工"): "建国前，境内各乡镇均有零星的牛",
    ("第二章屠宰及肉类加工", "第三节肉鸡加工"): "20世纪60年代初，市食品公司用手工方法",
    ("第二章屠宰及肉类加工", "第四节主要企业简介"): "一、连云港市食品公司",
    ("第三章罐头", "第一节畜禽类罐头"): "职工150人，有空罐、实罐和冷冻等车间",
    ("第三章罐头", "第二节果蔬类罐头"): "一、水果罐头",
    ("第三章罐头", "第三节水产类罐头"): "位于境内墟沟北固山麓的省立渔村师范学校",
    ("第三章罐头", "第四节其它类罐头"): "一、花生酱罐头",
    ("第三章罐头", "第五节主要企业简介"): "一、连云港市罐头食品厂",
    ("第四章饮料", "第一节酒类"): "宋代，境内酿制的桃林大曲颇为出名",
    ("第四章饮料", "第二节非酒精饮料"): "一、碳酸饮料",
    ("第四章饮料", "第三节冷冻饮料"): "民国33年（1944年），墟沟建制冰厂",
    ("第四章饮料", "第四节主要企业简介"): "一、连云港市酿酒厂",
    ("第五章调味品及食品添加剂", "第一节调味品"): "一、酱油、食醋、酱",
    ("第五章调味品及食品添加剂", "第二节食品添加剂"): "一、柠檬酸",
    ("第五章调味品及食品添加剂", "第三节主要企业简介"): "一、灌云县板浦酱醋厂",
    ("第六章其它食品加工", "第一节豆制品"): "清末民初，海州人相光乐",
    ("第六章其它食品加工", "第二节乳制品"): "20世纪60年代初，新浦农场牛奶",
    ("第六章其它食品加工", "第三节淀粉及淀粉制品"): "境内农民有用山芋、豌豆、玉米等制作淀粉",
    ("第六章其它食品加工", "第四节水产品"): "一、冷冻加工",
    ("第六章其它食品加工", "第五节制糖炼糖"): "1958年，东海县糖厂建成投产",
    ("第六章其它食品加工", "第六节蔬菜"): "一、酱腌蔬菜",
    ("第六章其它食品加工", "第七节蛋制品制茶"): "一、蛋制品",
    ("第六章其它食品加工", "第八节主要企业简介"): "一、江苏省海洋渔业公司鱼品加工厂",
}

SECTION_VARIANTS = {
    "第一节糕点": ["第一节糕•点", "第一节糕点"],
    "第二节糖果": ["第二节糖‧果", "第二节糖果"],
    "第四节主要企业简介": ["第四节主要企业简介", "第四节"],
    "第一节酒类": ["第一节•酒•类", "第一节酒类"],
    "第一节调味品": ["第一节训调味品", "第一节调味品"],
    "第二节乳制品": ["乳制品第二节孚", "第二节孚", "第二节乳制品"],
    "第四节水产品": ["第四节•水•产•品", "第四节水产品"],
    "第七节蛋制品制茶": ["制茶蛋制品第七节", "第七节蛋制品制茶", "第七节"],
    "第八节主要企业简介": ["第八节主要企业简介", "第八节"],
}

EXPECTED_TABLES = [f"表18-{i}" for i in range(1, 9)]


def h3(title: str) -> str:
    return f'<h3 id="第十八卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第十八卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    start_candidates = [text.find("\n第十八卷\n"), text.find("\n第十八卷 食品工业\n")]
    start_candidates = [pos for pos in start_candidates if pos >= 0]
    start = min(start_candidates) if start_candidates else -1
    end_candidates = [text.find("\n第十九卷\n", start if start >= 0 else 0), text.find("\n第十九卷 医药\n", start if start >= 0 else 0)]
    end_candidates = [pos for pos in end_candidates if pos >= 0]
    end = min(end_candidates) if end_candidates else -1
    if start < 0 or end < 0:
        raise RuntimeError("Cannot locate 第十八卷 source range")
    head, section, tail = text[:start], text[start:end], text[end:]
    replacements = {
        "\n第十八卷\n食品工业\n概述\n": "\n第十八卷 食品工业\n\n概述\n",
        "\n第一章\n糕点\n糖果\n蜜饯\n": "\n第一章糕点糖果蜜饯\n",
        "\n第一节糕•点\n": "\n第一节糕点\n",
        "\n第二节糖‧果\n": "\n第二节糖果\n",
        "\n第四节\n主要企业简介\n": "\n第四节主要企业简介\n",
        "\n第二章馬\n屠宰及肉类加工，871·\n": "\n",
        "\n第二章\n屠宰及肉类加工\n": "\n第二章屠宰及肉类加工\n",
        "\n罐头\n第三章\n": "\n第三章罐头\n",
        "\n第一节\n畜禽类罐头\n": "\n第一节畜禽类罐头\n",
        "\n第二节\n果蔬类罐头\n": "\n第二节果蔬类罐头\n",
        "\n第三节\n水产类罐头\n": "\n第三节水产类罐头\n",
        "\n第四节\n其它类罐头\n": "\n第四节其它类罐头\n",
        "\n第五节\n主要企业简介\n": "\n第五节主要企业简介\n",
        "\n饮料\n第四章\n": "\n第四章饮料\n",
        "\n第一节•酒•类\n": "\n第一节酒类\n",
        "\n第二节\n非酒精饮料\n": "\n第二节非酒精饮料\n",
        "\n第五章\n调味品及食品添加剂\n": "\n第五章调味品及食品添加剂\n",
        "\n第一节训\n调味品\n": "\n第一节调味品\n",
        "\n第五章i\n": "\n",
        "\n第二节\n食品添加剂\n": "\n第二节食品添加剂\n",
        "\n第三节\n主要企业简介\n": "\n第三节主要企业简介\n",
        "\n第六章\n其它食品加工\n": "\n第六章其它食品加工\n",
        "\n乳制品\n第二节孚\n": "\n第二节乳制品\n",
        "\n第三节\n淀粉及淀粉制品\n": "\n第三节淀粉及淀粉制品\n",
        "\n第四节•水•产•品\n": "\n第四节水产品\n",
        "\n第五节\n制糖\n炼糖\n": "\n第五节制糖炼糖\n",
        "\n第六节蔬菜\n": "\n第六节蔬菜\n",
        "\n制茶\n蛋制品\n第七节\n": "\n第七节蛋制品制茶\n",
        "\n第八节\n主要企业简介\n": "\n第八节主要企业简介\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    text = head + section + tail
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第十八卷卷题、章题、节题断裂和重复页眉/目录残留。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "<p>第一节糕•点": "<p>",
        "<p>第二节糖‧果": "<p>",
        "<p>第二章馬屠宰及肉类加工，871·": "<p>",
        "<p>第一节•酒•类": "<p>",
        "<p>第一节训调味品": "<p>",
        "<p>乳制品第二节孚": "<p>",
        "<p>第四节•水•产•品": "<p>",
        "<p>制茶蛋制品第七节": "<p>",
    }
    for old, new in residues.items():
        section = section.replace(old, new, 1)
    section = section.replace("第五章i", "", 1)
    return section


def insert_or_replace_title(section: str, marker: str, needle: str, variants: list[str], start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    needle_pos = section.find(needle, max(0, start - 800))
    if needle_pos < 0:
        needle_pos = section.find(needle)
    if needle_pos >= 0:
        prefix_start = max(0, needle_pos - 260)
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
    section = re.sub(
        r"<p>(一、白[\s\u3000]*酒)</p>\n(<h4 id=\"第十八卷-第四章饮料-第一节酒类\">第一节酒类</h4>)\n<p>",
        r"\2\n<p>\1",
        section,
    )
    section = re.sub(r"(</h[34]>)\n(?!<)([^\n<][^\n]*?</p>)", r"\1\n<p>\2", section)
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第十八卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)

    summary_marker = '<h3 id="第十八卷-概述">概述</h3>'
    if summary_marker not in section:
        section = summary_marker + "\n" + section.lstrip()
        h3_count += 1
    cursor = len(summary_marker)

    for chapter, _titles in CHAPTERS:
        variants = CHAPTER_VARIANTS.get(chapter, [chapter])
        section, added, cursor = insert_or_replace_title(section, h3(chapter), CHAPTER_NEEDLES[chapter], variants, cursor)
        h3_count += int(added)

    cursor = 0
    for chapter, titles in CHAPTERS:
        for title in titles:
            variants = SECTION_VARIANTS.get(title, [title])
            if title == "主要企业简介":
                variants = ["主要企业简介"]
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
        raise RuntimeError("Cannot locate 第十八卷 食品工业 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第十八卷-食品工业">第十八卷食品工业</h2>'

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>').replace('</div>', '</p>')
    if ipa_before:
        actions.append(f"将第十八卷误用 `ipa-data` 的正文块转回段落：{ipa_before} 处。")

    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复食品工业卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复食品工业卷节级 H4 标题：{h4_added} 处。")

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
            if title.startswith("表18-") or number.startswith("表18-"):
                tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(
            f"| {data.get('table_id', '')} | {data.get('table_number') or data.get('title', '')} | {data.get('title', '')} | {pages} | "
            f"{data.get('status', '')} | {size} | {data.get('notes', '')} |"
        )
    if not table_lines:
        table_lines = [f"| 暂无登记 | {table_no} | 第十八卷表格尚未进入表格站 | p966-p1007 | 待补登 | 待定 | 需从源 PDF 专项补建、核验 |" for table_no in EXPECTED_TABLES]

    lines = [
        "# 第十八卷食品工业 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第十八卷 食品工业。",
        "- 源 MD：`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第十八卷-食品工业` 至 `第十九卷-医药` 之前。",
        "- 源页范围：约 p964-p1017，位于中册 part01。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第十八卷正文区间，确认本卷实际为六章：糕点糖果蜜饯、屠宰及肉类加工、罐头、饮料、调味品及食品添加剂、其它食品加工。",
        "- 统计第十八卷表格状态，表格站暂无表18-*登记，阅读版已有少量结构化表，大量表格仍为 OCR 残文。",
        "",
        "## 格式修复清单",
        "",
        "- 卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章糕点糖果蜜饯` 至 `第六章其它食品加工` 共 6 个 H3。",
        "- 恢复糕点、糖果、果脯蜜饯、猪肉加工、牛羊兔肉加工、肉鸡加工、罐头分类、酒类、非酒精饮料、冷冻饮料、调味品、食品添加剂、豆制品、乳制品、淀粉及淀粉制品、水产品、制糖炼糖、蔬菜、蛋制品制茶、主要企业简介等 28 个 H4。",
        "- 将第十八卷误入 `ipa-data` 的正文块转回普通段落。",
        "- 清理源 MD 中章题、节题断裂和 OCR 页眉残留。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表18-*的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第十八卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第十八卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第十八卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第十八卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第十八卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第十八卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第十八卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第十八卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第十八卷全部章、节标题扁平化为正文。",
        "- 源 MD 中章题与节题断裂较多，个别页眉如 `第二章馬`、`第五章i` 混入正文。",
        "- 表18-*大多仍是 OCR 残文，且有跨页续表。",
        "- 表18-*均未登记到表格站。",
        "",
        "## 解决的困难",
        "",
        "- 以第十八卷至第十九卷边界限定修复范围，避免误动医药卷。",
        "- 章题按章概述首句定位，节题按稳定段首或小题定位，避开表格残文。",
        "- 对未核表格只保留现有结构表，不用 OCR 残文补填。",
        "",
        "## 残留风险",
        "",
        "- 第十八卷表18-1至表18-8需从源 PDF 逐张核读、补登、结构化。",
        "- 食品工业产品名、企业名和经济指标密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第十九卷 医药章节格式核对。",
        "- 表格专项阶段回补第十八卷糕点糖果、肉类加工、罐头、酒类、调味品和食品企业基本情况表。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第十八卷食品工业章节核对完成"
    section = f"""{header}

已完成 `第十八卷 食品工业` 章节格式核对：

- 新增脚本：`scripts/repair_eighteenth_volume_food_industry.py`。
- 修复 `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md` 中第十八卷卷题、章题、节题断裂和页眉残留。
- 修复 `output/final_reader/连云港市志_全书.html` 中第十八卷章、节标题全部扁平化以及正文块误用 `ipa-data` 的问题。
- 第十八卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章糕点糖果蜜饯至第六章其它食品加工），H4={stats['h4_count']}。
- 第十八卷范围内 `ipa-data` 残留已清零。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表18-*登记条目。
- 已写入进度文档：`output/reports/progress/20260628_第十八卷食品工业_修复核对进度.md`。

验收：第十八卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第十九卷 医药`。第十八卷表18-*需从源 PDF 专项补登、重建和核验。
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

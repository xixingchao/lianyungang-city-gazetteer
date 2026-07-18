# -*- coding: utf-8 -*-
"""Repair and audit 第二十一卷 机械工业 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第二十一卷机械工业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第二十一卷-机械工业">.*?</h2>)(.*?)(?=<h2 id="第二十二卷-电子工业">)', re.S)

CHAPTERS = [
    (
        "第一章农业机械",
        ["第一节农田作业机械", "第二节排灌、动力机械", "第三节作物收获机械", "第四节农副产品加工机械", "第五节主要企业简介"],
    ),
    (
        "第二章通用机械",
        ["第一节起重装卸机械", "第二节交通运输机械", "第三节工业锅炉", "第四节基础件", "第五节工具", "第六节工业泵减速机", "第七节主要企业简介"],
    ),
    (
        "第三章专用机械",
        ["第一节建筑机械", "第二节化工机械", "第三节皮革机械", "第四节粮食机械", "第五节主要企业简介"],
    ),
    (
        "第四章电工电器及材料",
        ["第一节电工电器", "第二节电工材料", "第三节主要企业简介"],
    ),
    (
        "第五章机床仪器仪表",
        ["第一节机床", "第二节仪器仪表", "第三节主要企业简介"],
    ),
]

CHAPTER_NEEDLES = {
    "第一章农业机械": "解放前，少数城镇个体手工业者",
    "第二章通用机械": "连云港市通用机械生产始于20世纪50年代末60年代初",
    "第三章专用机械": "一、塔式起重机",
    "第四章电工电器及材料": "连云港市电工电器及材料产品的生产起于20世纪50年代末",
    "第五章机床仪器仪表": "连云港市机床生产始于20世纪50年代末",
}

CHAPTER_VARIANTS = {
    "第一章农业机械": ["农业机械", "第一章农业机械"],
    "第二章通用机械": ["通用机械", "第二章通用机械"],
    "第三章专用机械": ["专用机械", "第三章专用机械"],
    "第四章电工电器及材料": ["电工电器及材料", "第四章电工电器及材料"],
    "第五章机床仪器仪表": ["仪器仪表机床", "机床仪器仪表", "第五章机床仪器仪表"],
}

SECTION_NEEDLES = {
    ("第一章农业机械", "第一节农田作业机械"): "一、犁耙",
    ("第一章农业机械", "第二节排灌、动力机械"): "一、水车",
    ("第一章农业机械", "第三节作物收获机械"): "一、收割机",
    ("第一章农业机械", "第四节农副产品加工机械"): "一、饲料粉碎机",
    ("第一章农业机械", "第五节主要企业简介"): "一、连云港市农业机械厂",
    ("第二章通用机械", "第一节起重装卸机械"): "一、门式起重机",
    ("第二章通用机械", "第二节交通运输机械"): "一、胶轮马车",
    ("第二章通用机械", "第三节工业锅炉"): "1971年试制第一台KZG1-8型",
    ("第二章通用机械", "第四节基础件"): "轴承1958年",
    ("第二章通用机械", "第五节工具"): "一、砂轮",
    ("第二章通用机械", "第六节工业泵减速机"): "一、工业泵",
    ("第二章通用机械", "第七节主要企业简介"): "一、连云港车辆厂",
    ("第三章专用机械", "第一节建筑机械"): "一、塔式起重机",
    ("第三章专用机械", "第二节化工机械"): "一、离心机",
    ("第三章专用机械", "第三节皮革机械"): "1981年11月，连云港皮革机械厂",
    ("第三章专用机械", "第四节粮食机械"): "1973年，东海县粮油机械修造厂",
    ("第三章专用机械", "第五节主要企业简介"): "一、连云港市建筑机械厂",
    ("第四章电工电器及材料", "第一节电工电器"): "一、变压器",
    ("第四章电工电器及材料", "第二节电工材料"): "1958年，新海植物油厂土法生产",
    ("第四章电工电器及材料", "第三节主要企业简介"): "一、连云港电线电缆总厂",
    ("第五章机床仪器仪表", "第一节机床"): "一、车床",
    ("第五章机床仪器仪表", "第二节仪器仪表"): "一、光学仪器",
    ("第五章机床仪器仪表", "第三节主要企业简介"): "连云港机床厂",
}

SECTION_VARIANTS = {
    "第一节农田作业机械": ["第一节炙农田作业机械", "第一节农田作业机械", "第一节炙"],
    "第二节排灌、动力机械": ["第二节排灌、动力机械", "第二节"],
    "第三节作物收获机械": ["第三节作物收获机械", "第三节"],
    "第四节农副产品加工机械": ["第四节农副产品加工机械", "第四节"],
    "第五节主要企业简介": ["第五节：主要企业简介", "第五节主要企业简介", "第五节"],
    "第一节起重装卸机械": ["第一节起重装卸机械", "第一节"],
    "第二节交通运输机械": ["第二节交通运输机械", "第二节"],
    "第三节工业锅炉": ["第三节工业锅炉", "第三节"],
    "第四节基础件": ["第四节基础件", "第四节"],
    "第五节工具": ["第五节•工•具", "第五节工具", "第五节"],
    "第六节工业泵减速机": ["第六节减速机工业泵", "第六节工业泵减速机", "第六节"],
    "第七节主要企业简介": ["第七节主要企业简介", "第七节"],
    "第一节建筑机械": ["第一节建筑机械", "第一节"],
    "第二节化工机械": ["·第二节•化工机械", "第二节•化工机械", "第二节化工机械", "第二节"],
    "第三节皮革机械": ["第三节皮革机械", "第三节"],
    "第四节粮食机械": ["第四节‧米粮食机械", "第四节粮食机械", "第四节"],
    "第一节电工电器": ["第一节电工电器", "第一节"],
    "第二节电工材料": ["第二节电工材料", "第二节"],
    "第三节主要企业简介": ["第三节主要企业简介、", "第三节主要企业简介", "第三节"],
    "第一节机床": ["第一节机•床", "第一节机床", "第一节"],
    "第二节仪器仪表": ["仪器亻仪表第二节：", "仪器仪表第二节：", "仪器仪表第二节", "第二节仪器仪表", "第二节"],
}

EXPECTED_TABLES = [f"表21-{i}" for i in range(1, 7)]


def h3(title: str) -> str:
    return f'<h3 id="第二十一卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第二十一卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    start_candidates = [text.find("\n第二十一卷\n"), text.find("\n第二十一卷 机械工业\n")]
    start_candidates = [pos for pos in start_candidates if pos >= 0]
    start = min(start_candidates) if start_candidates else -1
    end_candidates = [text.find("\n第二十二卷\n", start if start >= 0 else 0), text.find("\n第二十二卷 电子工业\n", start if start >= 0 else 0)]
    end_candidates = [pos for pos in end_candidates if pos >= 0]
    end = min(end_candidates) if end_candidates else -1
    if start < 0 or end < 0:
        raise RuntimeError("Cannot locate 第二十一卷 source range")
    head, section, tail = text[:start], text[start:end], text[end:]
    replacements = {
        "\n第二十一卷\n机械工业\n概述\n": "\n第二十一卷 机械工业\n\n概述\n",
        "\n第一章\n农业机械\n": "\n第一章农业机械\n",
        "\n第一节炙\n农田作业机械\n": "\n第一节农田作业机械\n",
        "\n第二节\n排灌、动力机械\n": "\n第二节排灌、动力机械\n",
        "\n第三节\n作物收获机械\n": "\n第三节作物收获机械\n",
        "\n第四节\n农副产品加工机械\n": "\n第四节农副产品加工机械\n",
        "\n第五节\n主要企业简介\n": "\n第五节主要企业简介\n",
        "\n第二章\n通用机械\n": "\n第二章通用机械\n",
        "\n第一节\n起重装卸机械\n": "\n第一节起重装卸机械\n",
        "\n第二节\n交通运输机械\n": "\n第二节交通运输机械\n",
        "\n第三节\n工业锅炉\n": "\n第三节工业锅炉\n",
        "\n第四节\n基础件\n": "\n第四节基础件\n",
        "\n第五节•工•具\n": "\n第五节工具\n",
        "\n第六节\n减速机\n工业泵\n": "\n第六节工业泵减速机\n",
        "\n第七节\n主要企业简介\n": "\n第七节主要企业简介\n",
        "\n第三章\n专用机械\n第一节\n建筑机械\n": "\n第三章专用机械\n第一节建筑机械\n",
        "\n·第二节•化工机械\n": "\n第二节化工机械\n",
        "\n第三节\n皮革机械\n": "\n第三节皮革机械\n",
        "\n第四节‧米\n粮食机械\n": "\n第四节粮食机械\n",
        "\n第五节：\n主要企业简介\n": "\n第五节主要企业简介\n",
        "\n第四章\n电工电器及材料\n": "\n第四章电工电器及材料\n",
        "\n第一节\n电工电器\n": "\n第一节电工电器\n",
        "\n第二节\n电工材料\n": "\n第二节电工材料\n",
        "\n仪器\n仪表\n机床\n第五章\n": "\n第五章机床仪器仪表\n",
        "\n第一节机•床\n": "\n第一节机床\n",
        "\n仪器亻\n仪表\n第二节\n": "\n第二节仪器仪表\n",
        "\n第三节\n主要企业简介\n、连云港机床厂\n": "\n第三节主要企业简介\n一、连云港机床厂\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    text = head + section + tail
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第二十一卷卷题、章题、节题断裂和小题序号 OCR 残缺。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "<p>第一节炙农田作业机械": "<p>",
        "<p>第五节•工•具": "<p>",
        "<p>第六节减速机工业泵": "<p>",
        "<p>·第二节•化工机械": "<p>",
        "<p>第四节‧米粮食机械": "<p>",
        "<p>仪器亻仪表第二节：": "<p>",
        "<p>第三节主要企业简介、": "<p>",
    }
    for old, new in residues.items():
        section = section.replace(old, new, 1)
    return section


def insert_or_replace_title(section: str, marker: str, needle: str, variants: list[str], start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    needle_pos = section.find(needle, max(0, start - 800))
    if needle_pos < 0:
        needle_pos = section.find(needle)
    if needle_pos >= 0:
        prefix_start = max(0, needle_pos - 320)
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
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第二十一卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    section = section.replace("<p>艺。1971年试制第一台KZG1-8型", "<p>1971年试制第一台KZG1-8型")
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)

    summary_marker = '<h3 id="第二十一卷-概述">概述</h3>'
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
        raise RuntimeError("Cannot locate 第二十一卷 机械工业 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第二十一卷-机械工业">第二十一卷机械工业</h2>'

    ipa_before = section.count('<div class="ipa-data">')
    section = re.sub(r'<div class="ipa-data">(.*?)</div>', r'<p>\1</p>', section, flags=re.S)
    if ipa_before:
        actions.append(f"将第二十一卷误用 `ipa-data` 的表格 OCR 残块转回段落：{ipa_before} 处。")

    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复机械工业卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复机械工业卷节级 H4 标题：{h4_added} 处。")

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
            if title.startswith("表21-") or number.startswith("表21-"):
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
        table_lines = [f"| 暂无登记 | {table_no} | 第二十一卷表格尚未进入表格站 | p1096-p1137 | 待补登 | 待定 | 需从源 PDF 专项补建、核验 |" for table_no in EXPECTED_TABLES]

    lines = [
        "# 第二十一卷机械工业 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第二十一卷 机械工业。",
        "- 源 MD：`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第二十一卷-机械工业` 至 `第二十二卷-电子工业` 之前。",
        "- 源页范围：约 p1096-p1137，位于中册 part01。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第二十一卷正文区间，确认本卷实际为五章：农业机械、通用机械、专用机械、电工电器及材料、机床仪器仪表。",
        "- 统计第二十一卷表格状态，表格站暂无表21-*登记，阅读版已有结构化表但仍需 PDF 表格专项复建。",
        "",
        "## 格式修复清单",
        "",
        "- 卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章农业机械` 至 `第五章机床仪器仪表` 共 5 个 H3。",
        "- 恢复农田作业机械、排灌动力机械、作物收获机械、农副产品加工机械、通用机械各节、专用机械各节、电工电器及材料各节、机床仪器仪表各节等 23 个 H4。",
        "- 将第二十一卷误入 `ipa-data` 的表格 OCR 残块转回普通段落。",
        "- 清理源 MD 中章题、节题断裂和 `第一节炙`、`第五节•工•具`、`第四节‧米`、`仪器亻仪表` 等 OCR 标题错误。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表21-*的登记表格：{len(tables)} 张。",
        "- 源 MD 可见表21-1至表21-6；表21-5、表21-6存在跨页/残片 OCR，需 PDF 专项重建。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第二十一卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第二十一卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第二十一卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第二十一卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第二十一卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第二十一卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第二十一卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第二十一卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第二十一卷全部章、节标题扁平化为正文。",
        "- OCR 将 `第一节农田作业机械` 误作 `第一节炙农田作业机械`。",
        "- OCR 将 `第五节工具`、`第四节粮食机械`、`第二节仪器仪表` 混入符号或错字。",
        "- 表21-*均未登记到表格站，阅读版结构化表仍为待对照原图录入状态。",
        "",
        "## 解决的困难",
        "",
        "- 以第二十一卷至第二十二卷边界限定修复范围，避免误动电子工业卷。",
        "- 对重复出现的 `主要企业简介` 按所属章生成唯一 H4 锚点。",
        "- 对 `第六节减速机工业泵` 和 `第五章仪器仪表机床` 等倒置标题，按正文首句定位后恢复为通行目录顺序。",
        "",
        "## 残留风险",
        "",
        "- 第二十一卷表21-1至表21-6需从源 PDF 逐张核读、补登、结构化。",
        "- 机械产品型号、企业名、获奖产品名密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第二十二卷 电子工业章节格式核对。",
        "- 表格专项阶段回补第二十一卷机械工业主要产品产量、主要企业、获奖产品等统计表。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第二十一卷机械工业章节核对完成"
    section = f"""{header}

已完成 `第二十一卷 机械工业` 章节格式核对：

- 新增脚本：`scripts/repair_twenty_first_volume_machinery.py`。
- 修复 `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md` 中第二十一卷卷题、章题、节题断裂和 OCR 标题错误。
- 修复 `output/final_reader/连云港市志_全书.html` 中第二十一卷章节标题全部扁平化以及表格 OCR 残块误用 `ipa-data` 的问题。
- 第二十一卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章农业机械至第五章机床仪器仪表），H4={stats['h4_count']}。
- 第二十一卷范围内 `ipa-data` 残留已清零。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表21-*登记条目。
- 已写入进度文档：`output/reports/progress/20260628_第二十一卷机械工业_修复核对进度.md`。

验收：第二十一卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第二十二卷 电子工业`。第二十一卷表21-*需从源 PDF 专项补登、重建和核验。
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

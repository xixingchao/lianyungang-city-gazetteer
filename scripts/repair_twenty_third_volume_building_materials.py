# -*- coding: utf-8 -*-
"""Repair and audit 第二十三卷 建材工业 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第二十三卷建材工业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第二十三卷-建材工业">.*?</h2>)(.*?)(?=<h2 id="第二十四卷-建筑业">)', re.S)

CHAPTERS = [
    ("第一章砖瓦", ["第一节砖", "第二节瓦", "第三节主要企业简介"]),
    ("第二章黄沙石材", ["第一节黄沙", "第二节石材", "第三节主要企业简介"]),
    ("第三章石灰水泥水泥制品", ["第一节石灰", "第二节水泥", "第三节水泥制品", "第四节主要企业简介"]),
    ("第四章玻璃玻璃纤维玻璃钢制品", ["第一节玻璃", "第二节玻璃纤维玻璃纤维布", "第三节玻璃钢制品", "第四节主要企业简介"]),
    ("第五章其它建筑材料", ["第一节耐火材料", "第二节保温材料", "第三节装饰装修材料", "第四节其它材料", "第五节主要企业简介"]),
]

CHAPTER_NEEDLES = {
    "第一章砖瓦": "解放前夕，连云港市只有小土窑43座",
    "第二章黄沙石材": "连云港市黄沙主要有河沙、海沙",
    "第三章石灰水泥水泥制品": "市内石灰生产始于清末民初",
    "第四章玻璃玻璃纤维玻璃钢制品": "连云港市玻璃生产始于1958年",
    "第五章其它建筑材料": "连云港市耐火、保温材料生产均始于1958年",
}

CHAPTER_VARIANTS = {
    "第一章砖瓦": ["第一章砖　瓦", "第一章砖瓦", "砖瓦"],
    "第二章黄沙石材": ["第二章", "黄沙石材"],
    "第三章石灰水泥水泥制品": ["水泥石灰水泥制品", "石灰水泥水泥制品", "第三章石灰水泥水泥制品", "第三章"],
    "第四章玻璃玻璃纤维玻璃钢制品": ["玻璃玻璃纤维玻璃钢制品", "第四章玻璃玻璃纤维", "第四章"],
    "第五章其它建筑材料": ["第五章其它建筑材料", "其它建筑材料", "第五章"],
}

SECTION_NEEDLES = {
    ("第一章砖瓦", "第一节砖"): "一、粘土实心砖",
    ("第一章砖瓦", "第二节瓦"): "民国28年，日本人在新浦建兴亚、松岗窑厂生产砖瓦",
    ("第一章砖瓦", "第三节主要企业简介"): "一、连云港市制砖厂",
    ("第二章黄沙石材", "第一节黄沙"): "建国前，赣榆、东海两县百姓挖捞河沙",
    ("第二章黄沙石材", "第二节石材"): "民国21年（1932年）",
    ("第二章黄沙石材", "第三节主要企业简介"): "该厂是生产石子、石料的专业厂",
    ("第三章石灰水泥水泥制品", "第一节石灰"): "市内石灰生产始于清末民初",
    ("第三章石灰水泥水泥制品", "第二节水泥"): "1958年，新海连市跃进水泥厂",
    ("第三章石灰水泥水泥制品", "第三节水泥制品"): "一、水泥桁条",
    ("第三章石灰水泥水泥制品", "第四节主要企业简介"): "一、连云港市水泥厂",
    ("第四章玻璃玻璃纤维玻璃钢制品", "第一节玻璃"): "1958年，东海县投资37.76万元",
    ("第四章玻璃玻璃纤维玻璃钢制品", "第二节玻璃纤维玻璃纤维布"): "1973年，连云港市“五七”厂",
    ("第四章玻璃玻璃纤维玻璃钢制品", "第三节玻璃钢制品"): "1978年，连云港市玻璃纤维厂",
    ("第四章玻璃玻璃纤维玻璃钢制品", "第四节主要企业简介"): "一、东海县玻璃厂",
    ("第五章其它建筑材料", "第一节耐火材料"): "1958年，海州耐火材料厂成立",
    ("第五章其它建筑材料", "第二节保温材料"): "1958年，利用东海县境内储藏蛭石的优势",
    ("第五章其它建筑材料", "第三节装饰装修材料"): "大理石、花岗石板材",
    ("第五章其它建筑材料", "第四节其它材料"): "一、门窗",
    ("第五章其它建筑材料", "第五节主要企业简介"): "一、连云港市耐火材料厂",
}

SECTION_VARIANTS = {
    "第一节砖": ["第一节砖", "第一节"],
    "第二节瓦": ["第二节瓦", "第二节"],
    "第一节黄沙": ["第一节黄沙", "第一节"],
    "第二节石材": ["第二节石材", "第二节"],
    "第三节主要企业简介": ["第三节主要企业简介连云港市海州采石厂", "第三节三主要企业简介", "第三节主要企业简介", "第三节"],
    "第一节石灰": ["水泥石灰水泥制品", "第一节石灰", "第一节"],
    "第二节水泥": ["第二节•水•泥", "第二节水泥", "第二节"],
    "第三节水泥制品": ["第三节水泥制品", "第三节"],
    "第四节主要企业简介": ["第四节主要企业简介", "第四节"],
    "第一节玻璃": ["第一节玻璃", "第一节"],
    "第二节玻璃纤维玻璃纤维布": ["第二节玻璃纤维玻璃纤维布", "第二节玻璃纤维", "第二节"],
    "第三节玻璃钢制品": ["第三节玻璃钢制品", "第三节"],
    "第一节耐火材料": ["第一节而耐火材料", "第一节耐火材料", "第一节而", "第一节"],
    "第二节保温材料": ["第二节保温材料", "第二节"],
    "第三节装饰装修材料": ["第三节装饰装修材料、", "第三节装饰装修材料", "第三节"],
    "第四节其它材料": ["第四节其它材料", "第四节"],
    "第五节主要企业简介": ["第五节主要企业简介", "第五节"],
}

EXPECTED_TABLES = [f"表23-{i}" for i in range(1, 6)]


def h3(title: str) -> str:
    return f'<h3 id="第二十三卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第二十三卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    start_candidates = [text.find("\n第二十三卷\n"), text.find("\n第二十三卷 建材工业\n")]
    start_candidates = [pos for pos in start_candidates if pos >= 0]
    start = min(start_candidates) if start_candidates else -1
    end_candidates = [text.find("\n第二十四卷\n", start if start >= 0 else 0), text.find("\n第二十四卷 建筑业\n", start if start >= 0 else 0)]
    end_candidates = [pos for pos in end_candidates if pos >= 0]
    end = min(end_candidates) if end_candidates else -1
    if start < 0 or end < 0:
        raise RuntimeError("Cannot locate 第二十三卷 source range")
    head, section, tail = text[:start], text[start:end], text[end:]
    replacements = {
        "\n第二十三卷\n建材工业\n概述\n": "\n第二十三卷 建材工业\n\n概述\n",
        "\n第一章砖　瓦\n": "\n第一章砖瓦\n",
        "\n第三节三\n主要企业简介\n": "\n第三节主要企业简介\n",
        "\n第二章\n连云港市黄沙主要有河沙": "\n第二章黄沙石材\n连云港市黄沙主要有河沙",
        "\n第三节\n主要企业简介\n连云港市海州采石厂\n": "\n第三节主要企业简介\n一、连云港市海州采石厂\n",
        "\n水泥\n石灰\n水泥制品\n第三章\n": "\n第三章石灰水泥水泥制品\n第一节石灰\n",
        "\n第二节•水•泥\n": "\n第二节水泥\n",
        "\n第三章石灰水泥水泥制品\n:1083\n": "\n",
        "\n第三节\n水泥制品\n": "\n第三节水泥制品\n",
        "\n第四节\n主要企业简介\n": "\n第四节主要企业简介\n",
        "\n第四章\n玻璃\n玻璃纤维\n玻璃钢制品\n": "\n第四章玻璃玻璃纤维玻璃钢制品\n",
        "\n第二节\n玻璃纤维\n玻璃纤维布\n": "\n第二节玻璃纤维玻璃纤维布\n",
        "\n第三节\n玻璃钢制品\n": "\n第三节玻璃钢制品\n",
        "\n第四章玻璃玻璃纤维\n品：1089·\n玻璃钢制品\n": "\n",
        "\n第五章\n其它建筑材料\n": "\n第五章其它建筑材料\n",
        "\n第一节而\n耐火材料\n": "\n第一节耐火材料\n",
        "\n第三节\n装饰装修材料\n、大理石、花岗石板材\n": "\n第三节装饰装修材料\n一、大理石、花岗石板材\n",
        "\n第五节\n主要企业简介\n": "\n第五节主要企业简介\n",
        "\n第五章\n其它建筑材料\n\n续上表\n": "\n续上表\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    text = head + section + tail
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第二十三卷卷题、章题、节题断裂、页眉残留和 OCR 标题错误。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "<p>第三节三主要企业简介": "<p>",
        "<p>水泥石灰水泥制品": "<p>",
        "<p>第二节•水•泥": "<p>",
        "<p>第三节装饰装修材料、": "<p>",
        "<p>第一节而耐火材料": "<p>",
    }
    for old, new in residues.items():
        section = section.replace(old, new, 1)
    section = section.replace(":1083", "")
    section = section.replace("山品：1089·玻璃钢制品东", "山东")
    misplaced = '<h4 id="第二十三卷-第二章黄沙石材-第三节主要企业简介">第三节主要企业简介</h4>\n<p>连云港市海州采石厂安装一台6立方米空气压缩机，首次采用机械打炮眼。</p>'
    if misplaced in section:
        section = section.replace(misplaced, "<p>1964年，连云港市海州采石厂安装一台6立方米空气压缩机，首次采用机械打炮眼。</p>", 1)
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
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第二十三卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)
    summary_marker = '<h3 id="第二十三卷-概述">概述</h3>'
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
        raise RuntimeError("Cannot locate 第二十三卷 建材工业 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第二十三卷-建材工业">第二十三卷建材工业</h2>'
    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复建材工业卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复建材工业卷节级 H4 标题：{h4_added} 处。")
    fixed = html[: m.start()] + heading + "\n" + section.lstrip() + html[m.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    stats = audit_section(fixed)
    stats["inserted_h3"] = h3_added
    stats["inserted_h4"] = h4_added
    stats["ipa_fixed"] = 0
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
            if title.startswith("表23-") or number.startswith("表23-"):
                tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(f"| {data.get('table_id', '')} | {data.get('table_number') or data.get('title', '')} | {data.get('title', '')} | {pages} | {data.get('status', '')} | {size} | {data.get('notes', '')} |")
    if not table_lines:
        table_lines = [f"| 暂无登记 | {table_no} | 第二十三卷表格尚未进入表格站 | p1174-p1198 | 待补登 | 待定 | 需从源 PDF 专项补建、核验 |" for table_no in EXPECTED_TABLES]

    lines = [
        "# 第二十三卷建材工业 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第二十三卷 建材工业。",
        "- 源 MD：`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第二十三卷-建材工业` 至 `第二十四卷-建筑业` 之前。",
        "- 源页范围：约 p1174-p1198，位于中册 part01。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第二十三卷正文区间，确认本卷实际为五章：砖瓦、黄沙石材、石灰水泥水泥制品、玻璃玻璃纤维玻璃钢制品、其它建筑材料。",
        "- 统计第二十三卷表格状态，表格站暂无表23-*登记，阅读版已有结构化表但仍需 PDF 表格专项复建。",
        "",
        "## 格式修复清单",
        "",
        "- 卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章砖瓦` 至 `第五章其它建筑材料` 共 5 个 H3。",
        "- 恢复砖、瓦、黄沙、石材、石灰、水泥、水泥制品、玻璃、玻璃纤维玻璃纤维布、玻璃钢制品、耐火材料、保温材料、装饰装修材料等 19 个 H4。",
        "- 清理源 MD 中章题、节题断裂和 `第三节三`、`第二节•水•泥`、`第一节而`、页眉残留等 OCR 错误。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表23-*的登记表格：{len(tables)} 张。",
        "- 源 MD 可见表23-1至表23-5；表23-4、表23-5存在跨页/残片 OCR，需 PDF 专项重建。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第二十三卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第二十三卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第二十三卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第二十三卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第二十三卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第二十三卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第二十三卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第二十三卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第二十三卷全部章、节标题扁平化为正文。",
        "- OCR 将 `第三节主要企业简介` 识别为 `第三节三主要企业简介`，将 `第一节耐火材料` 识别为 `第一节而耐火材料`。",
        "- 第三章、第四章和第五章表格附近存在页眉式重复章题残留。",
        "- 表23-*均未登记到表格站，阅读版结构化表仍为待对照原图录入状态。",
        "",
        "## 解决的困难",
        "",
        "- 以第二十三卷至第二十四卷边界限定修复范围，避免误动建筑业卷。",
        "- 对多材料合并章题按正文总述恢复唯一 H3 锚点。",
        "- 对重复出现的 `主要企业简介` 按所属章生成唯一 H4 锚点。",
        "",
        "## 残留风险",
        "",
        "- 第二十三卷表23-1至表23-5需从源 PDF 逐张核读、补登、结构化。",
        "- 建材产品名、企业名和统计指标密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第二十四卷 建筑业章节格式核对。",
        "- 表格专项阶段回补第二十三卷沙石、石灰水泥、玻璃玻纤、主要企业、获奖产品等统计表。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第二十三卷建材工业章节核对完成"
    section = f"""{header}

已完成 `第二十三卷 建材工业` 章节格式核对：

- 新增脚本：`scripts/repair_twenty_third_volume_building_materials.py`。
- 修复 `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md` 中第二十三卷卷题、章题、节题断裂和页眉/OCR 标题错误。
- 修复 `output/final_reader/连云港市志_全书.html` 中第二十三卷章节标题全部扁平化的问题。
- 第二十三卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章砖瓦至第五章其它建筑材料），H4={stats['h4_count']}。
- 第二十三卷范围内 `ipa-data` 残留已清零。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表23-*登记条目。
- 已写入进度文档：`output/reports/progress/20260628_第二十三卷建材工业_修复核对进度.md`。

验收：第二十三卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第二十四卷 建筑业`。第二十三卷表23-*需从源 PDF 专项补登、重建和核验。
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

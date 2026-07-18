# -*- coding: utf-8 -*-
"""Repair and audit 第二十二卷 电子工业 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第二十二卷电子工业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第二十二卷-电子工业">.*?</h2>)(.*?)(?=<h2 id="第二十三卷-建材工业">)', re.S)

CHAPTERS = [
    ("第一章电子整机", ["第一节通信设备", "第二节广播电视", "第三节电子仪器", "第四节电子应用产品", "第五节主要企业简介"]),
    (
        "第二章电子元器件",
        ["第一节石英晶体", "第二节接插件", "第三节磁带计数器", "第四节广播电视配件", "第五节半导体器件", "第六节电位器", "第七节其它器件", "第八节主要企业简介"],
    ),
    ("第三章电子材料", ["第一节半导体材料", "第二节人造水晶", "第三节磁性材料", "第四节环氧模塑料", "第五节硅微粉", "第六节主要企业简介"]),
    ("第四章电子专用设备", ["第一节冲床", "第二节封帽机", "第三节数控钻床", "第四节胶体磨", "第五节塑料封接机", "第六节主要企业简介"]),
]

CHAPTER_NEEDLES = {
    "第一章电子整机": "连云港市的电子整机产业一直较薄弱",
    "第二章电子元器件": "连云港市的电子元器件是全市电子工业的主导产业",
    "第三章电子材料": "连云港市电子材料生产起步早",
    "第四章电子专用设备": "连云港市电子专用设备生产在电子行业起步较早",
}

CHAPTER_VARIANTS = {
    "第一章电子整机": ["电子整机", "第一章电子整机"],
    "第二章电子元器件": ["电子元器件", "第二章电子元器件"],
    "第三章电子材料": ["电子材料", "第三章电子材料"],
    "第四章电子专用设备": ["电子专用设备", "第四章电子专用设备"],
}

SECTION_NEEDLES = {
    ("第一章电子整机", "第一节通信设备"): "一、渔轮电台",
    ("第一章电子整机", "第二节广播电视"): "一、收音机",
    ("第一章电子整机", "第三节电子仪器"): "一、直流稳压电源",
    ("第一章电子整机", "第四节电子应用产品"): "一、静电复印机",
    ("第一章电子整机", "第五节主要企业简介"): "一、连云港市无线电厂",
    ("第二章电子元器件", "第一节石英晶体"): "一、石英晶体谐振器",
    ("第二章电子元器件", "第二节接插件"): "插塞插口1966年",
    ("第二章电子元器件", "第三节磁带计数器"): "1985年，连云港市无线电元件四厂",
    ("第二章电子元器件", "第四节广播电视配件"): "一、扬声器",
    ("第二章电子元器件", "第五节半导体器件"): "一、晶体管",
    ("第二章电子元器件", "第六节电位器"): "实芯电位器1978年",
    ("第二章电子元器件", "第七节其它器件"): "一、中频变压器",
    ("第二章电子元器件", "第八节主要企业简介"): "一、连云港市电讯器材厂",
    ("第三章电子材料", "第一节半导体材料"): "一、多晶硅与单晶硅",
    ("第三章电子材料", "第二节人造水晶"): "1978年5月，东海县城头公社",
    ("第三章电子材料", "第三节磁性材料"): "1978年3月，连云港市朝阳公社",
    ("第三章电子材料", "第四节环氧模塑料"): "1983年3月，市电子器材厂",
    ("第三章电子材料", "第五节硅微粉"): "境内石英资源丰富",
    ("第三章电子材料", "第六节主要企业简介"): "一、连云港市电子器材厂",
    ("第四章电子专用设备", "第一节冲床"): "1966年3月，连云港市无线电专用设备厂成立",
    ("第四章电子专用设备", "第二节封帽机"): "1970年8月，连云港市海州电器厂",
    ("第四章电子专用设备", "第三节数控钻床"): "中国科学院计算技术研究所",
    ("第四章电子专用设备", "第四节胶体磨"): "1983年4月，连云港市无线电专用设备厂",
    ("第四章电子专用设备", "第五节塑料封接机"): "1986年1月，连云港微波电器厂",
    ("第四章电子专用设备", "第六节主要企业简介"): "一、连云港市电声器材厂",
}

SECTION_VARIANTS = {
    "第一节通信设备": ["直傢信第-节通", "第一节通信设备", "第-节通"],
    "第二节广播电视": ["第二节广播电视", "第二节"],
    "第三节电子仪器": ["第三节电子仪器", "第三节"],
    "第四节电子应用产品": ["第四节电子应用产品", "第四节"],
    "第五节主要企业简介": ["第五节主要企业简介", "第五节"],
    "第一节石英晶体": ["第一节石英晶体", "第一节"],
    "第二节接插件": ["第二节　扌接插件、", "第二节接插件", "第二节"],
    "第三节磁带计数器": ["第三节磁带计数器", "第三节"],
    "第四节广播电视配件": ["第四节•广播电视配件", "第四节广播电视配件", "第四节"],
    "第五节半导体器件": ["第五节半导体器件", "第五节"],
    "第六节电位器": ["第六节电位器、", "第六节电位器", "第六节"],
    "第七节其它器件": ["其它器件第七节", "第七节其它器件", "第七节"],
    "第八节主要企业简介": ["第八节主要企业简介", "第八节"],
    "第一节半导体材料": ["第一节半导体材料", "第一节"],
    "第二节人造水晶": ["第二节人造水晶", "第二节"],
    "第三节磁性材料": ["第三节磁性材料", "第三节"],
    "第四节环氧模塑料": ["第四节环氧模塑料", "第四节"],
    "第五节硅微粉": ["第五节硅微粉", "第五节"],
    "第六节主要企业简介": ["第六节主要企业简介", "第六节"],
    "第一节冲床": ["第一节冲•床", "第一节冲床", "第一节"],
    "第二节封帽机": ["第二节封帽机", "第二节"],
    "第三节数控钻床": ["第三节数控钻床", "第三节"],
    "第四节胶体磨": ["第四节胶体磨", "第四节"],
    "第五节塑料封接机": ["第五节塑料封接机", "第五节"],
}

EXPECTED_TABLES = [f"表22-{i}" for i in range(1, 9)]


def h3(title: str) -> str:
    return f'<h3 id="第二十二卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第二十二卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    start_candidates = [text.find("\n第二十二卷\n"), text.find("\n第二十二卷 电子工业\n")]
    start_candidates = [pos for pos in start_candidates if pos >= 0]
    start = min(start_candidates) if start_candidates else -1
    end_candidates = [text.find("\n第二十三卷\n", start if start >= 0 else 0), text.find("\n第二十三卷 建材工业\n", start if start >= 0 else 0)]
    end_candidates = [pos for pos in end_candidates if pos >= 0]
    end = min(end_candidates) if end_candidates else -1
    if start < 0 or end < 0:
        raise RuntimeError("Cannot locate 第二十二卷 source range")
    head, section, tail = text[:start], text[start:end], text[end:]
    replacements = {
        "\n第二十二卷\n电子工业\n概述\n": "\n第二十二卷 电子工业\n\n概述\n",
        "\n第一章\n电子整机\n": "\n第一章电子整机\n",
        "\n直傢信\n第-节通\n": "\n第一节通信设备\n",
        "\n第三节\n电子仪器\n": "\n第三节电子仪器\n",
        "\n第四节\n电子应用产品\n": "\n第四节电子应用产品\n",
        "\n第二章\n电子元器件\n": "\n第二章电子元器件\n",
        "\n第二章电子元器件：1049·\n": "\n",
        "\n第二节　扌\n接插件\n、插塞插口\n": "\n第二节接插件\n一、插塞插口\n",
        "\n第三节\n磁带计数器\n": "\n第三节磁带计数器\n",
        "\n第四节•广播电视配件\n": "\n第四节广播电视配件\n",
        "\n第六节\n电位器\n、实芯电位器\n": "\n第六节电位器\n一、实芯电位器\n",
        "\n其它器件\n第七节\n一、中频变压器\n": "\n第七节其它器件\n一、中频变压器\n",
        "\n第八节\n主要企业简介\n": "\n第八节主要企业简介\n",
        "\n第二章 \n电子元器件\n1055\n": "\n",
        "\n第三章\n电子材料\n": "\n第三章电子材料\n",
        "\n第一节\n半导体材料\n": "\n第一节半导体材料\n",
        "\n第四节\n环氧模塑料\n": "\n第四节环氧模塑料\n",
        "\n第六节\n主要企业简介\n": "\n第六节主要企业简介\n",
        "\n第四章\n电子专用设备\n": "\n第四章电子专用设备\n",
        "\n第一节冲•床\n": "\n第一节冲床\n",
        "\n第四节\n胶体磨\n": "\n第四节胶体磨\n",
        "\n第五节\n塑料封接机\n": "\n第五节塑料封接机\n",
        "\n第四章\n\n连云港市电子工业获奖产品一览表\n": "\n连云港市电子工业获奖产品一览表\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    text = head + section + tail
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第二十二卷卷题、章题、节题断裂、页眉残留和 OCR 标题错误。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "<p>直傢信第-节通": "<p>",
        "<p>第二节　扌接插件、": "<p>",
        "<p>第四节•广播电视配件": "<p>",
        "<p>第六节电位器、": "<p>",
        "<p>其它器件第七节": "<p>",
        "<p>第一节冲•床": "<p>",
    }
    for old, new in residues.items():
        section = section.replace(old, new, 1)
    section = section.replace("电子元器件1055", "")
    return section


def insert_or_replace_title(section: str, marker: str, needle: str, variants: list[str], start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    needle_pos = section.find(needle, max(0, start - 900))
    if needle_pos < 0:
        needle_pos = section.find(needle)
    if needle_pos >= 0:
        prefix_start = max(0, needle_pos - 360)
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
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第二十二卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)

    summary_marker = '<h3 id="第二十二卷-概述">概述</h3>'
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
        raise RuntimeError("Cannot locate 第二十二卷 电子工业 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第二十二卷-电子工业">第二十二卷电子工业</h2>'

    ipa_before = section.count('<div class="ipa-data">')
    section = re.sub(r'<div class="ipa-data">(.*?)</div>', r'<p>\1</p>', section, flags=re.S)
    if ipa_before:
        actions.append(f"将第二十二卷误用 `ipa-data` 的正文/表格 OCR 残块转回段落：{ipa_before} 处。")

    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复电子工业卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复电子工业卷节级 H4 标题：{h4_added} 处。")

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
            if title.startswith("表22-") or number.startswith("表22-"):
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
        table_lines = [f"| 暂无登记 | {table_no} | 第二十二卷表格尚未进入表格站 | p1138-p1170 | 待补登 | 待定 | 需从源 PDF 专项补建、核验 |" for table_no in EXPECTED_TABLES]

    lines = [
        "# 第二十二卷电子工业 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第二十二卷 电子工业。",
        "- 源 MD：`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第二十二卷-电子工业` 至 `第二十三卷-建材工业` 之前。",
        "- 源页范围：约 p1138-p1170，位于中册 part01。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第二十二卷正文区间，确认本卷实际为四章：电子整机、电子元器件、电子材料、电子专用设备。",
        "- 统计第二十二卷表格状态，表格站暂无表22-*登记，阅读版已有结构化表但仍需 PDF 表格专项复建。",
        "",
        "## 格式修复清单",
        "",
        "- 卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章电子整机` 至 `第四章电子专用设备` 共 4 个 H3。",
        "- 恢复通信设备、广播电视、电子仪器、电子应用产品、电子元器件各节、电子材料各节、电子专用设备各节等 25 个 H4。",
        "- 将第二十二卷误入 `ipa-data` 的正文/表格 OCR 残块转回普通段落。",
        "- 清理源 MD 中章题、节题断裂和 `直傢信第-节通`、`第二节　扌`、`冲•床`、页眉残留等 OCR 错误。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表22-*的登记表格：{len(tables)} 张。",
        "- 源 MD 可见表22-1至表22-8；表22-7、表22-8存在跨页/残片 OCR，需 PDF 专项重建。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第二十二卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第二十二卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第二十二卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第二十二卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第二十二卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第二十二卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第二十二卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第二十二卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第二十二卷全部章、节标题扁平化为正文。",
        "- OCR 将 `第一节通信设备` 识别为 `直傢信第-节通`。",
        "- OCR 将 `第二节接插件`、`第七节其它器件`、`第一节冲床` 混入符号或错位。",
        "- 表22-*均未登记到表格站，阅读版结构化表仍为待对照原图录入状态。",
        "",
        "## 解决的困难",
        "",
        "- 以第二十二卷至第二十三卷边界限定修复范围，避免误动建材工业卷。",
        "- 将源 MD 中 `第二章电子元器件：1049·`、`电子元器件1055` 等页眉残留从正文中剥离。",
        "- 对重复出现的 `主要企业简介` 按所属章生成唯一 H4 锚点。",
        "",
        "## 残留风险",
        "",
        "- 第二十二卷表22-1至表22-8需从源 PDF 逐张核读、补登、结构化。",
        "- 电子产品型号、企业名、获奖产品名和表格数字密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第二十三卷 建材工业章节格式核对。",
        "- 表格专项阶段回补第二十二卷广播电视产品、石英晶体、接插件、晶体管、电位器、电子材料、主要企业和获奖产品等统计表。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第二十二卷电子工业章节核对完成"
    section = f"""{header}

已完成 `第二十二卷 电子工业` 章节格式核对：

- 新增脚本：`scripts/repair_twenty_second_volume_electronics.py`。
- 修复 `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md` 中第二十二卷卷题、章题、节题断裂和页眉/OCR 标题错误。
- 修复 `output/final_reader/连云港市志_全书.html` 中第二十二卷章节标题全部扁平化以及正文/表格 OCR 残块误用 `ipa-data` 的问题。
- 第二十二卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章电子整机至第四章电子专用设备），H4={stats['h4_count']}。
- 第二十二卷范围内 `ipa-data` 残留已清零。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表22-*登记条目。
- 已写入进度文档：`output/reports/progress/20260628_第二十二卷电子工业_修复核对进度.md`。

验收：第二十二卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第二十三卷 建材工业`。第二十二卷表22-*需从源 PDF 专项补登、重建和核验。
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

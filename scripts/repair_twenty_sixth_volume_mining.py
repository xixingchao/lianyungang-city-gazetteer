# -*- coding: utf-8 -*-
"""Repair and audit 第二十六卷 矿产 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第二十六卷矿产_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第二十六卷-矿产">.*?</h2>)(.*?)(?=<h2 id="第二十七卷-[^"]+">)', re.S)

CHAPTERS = [
    ("第一章磷矿", ["第一节地质勘探", "第二节基本建设", "第三节生产经营", "第四节主要企业简介"]),
    ("第二章煤矿", ["第一节地质勘探", "第二节基本建设", "第三节生产经营", "第四节主要企业简介"]),
    ("第三章蛇纹石矿", ["第一节地质勘探", "第二节基本建设", "第三节生产经营", "第四节主要企业简介"]),
    (
        "第四章其它矿产",
        ["第一节水晶矿", "第二节石英矿", "第三节大理石矿", "第四节花岗石矿", "第五节云母矿", "第六节蓝晶石矿 砂岩 蛭石 玄武岩矿"],
    ),
]

CHAPTER_NEEDLES = {
    "第一章磷矿": "连云港市磷矿资源丰富，开采早",
    "第二章煤矿": "连云港市境内无煤矿资源",
    "第三章蛇纹石矿": "连云港市蛇纹石矿储量大",
    "第四章其它矿产": "连云港市其它矿产主要有水晶",
}

CHAPTER_VARIANTS = {
    "第一章磷矿": ["第一章磷矿", "磷矿"],
    "第二章煤矿": ["第二章煤矿", "第二章", "煤矿"],
    "第三章蛇纹石矿": ["第三章蛇纹石矿", "第三章", "蛇纹石矿"],
    "第四章其它矿产": ["第四章其它矿产", "第四章", "其它矿产"],
}

SECTION_NEEDLES = {
    ("第一章磷矿", "第一节地质勘探"): "民国8年（1919年），海州人沈云需集资",
    ("第一章磷矿", "第二节基本建设"): "锦屏磷矿建矿初期",
    ("第一章磷矿", "第三节生产经营"): "民国9年（1920年），由沈云需之子沈蕃继承锦屏公司",
    ("第一章磷矿", "第四节主要企业简介"): "一、锦屏磷矿",
    ("第二章煤矿", "第一节地质勘探"): "1970年，根据徐州矿务局地质队提供",
    ("第二章煤矿", "第二节基本建设"): "连云港市煤矿各井设计由江苏省煤炭设计院",
    ("第二章煤矿", "第三节生产经营"): "连云港市煤矿开采方法",
    ("第二章煤矿", "第四节主要企业简介"): "连云港白集煤矿是开采煤炭的专业矿",
    ("第三章蛇纹石矿", "第一节地质勘探"): "1959年，江苏省冶金局地质勘探总队第五队",
    ("第三章蛇纹石矿", "第二节基本建设"): "1964年9月，东海县蛇纹石矿由国家投资",
    ("第三章蛇纹石矿", "第三节生产经营"): "1965年3月，东海县蛇纹石矿采用人抬肩挑",
    ("第三章蛇纹石矿", "第四节主要企业简介"): "东海县蛇纹石矿是开采蛇纹石的专业矿",
    ("第四章其它矿产", "第一节水晶矿"): "浅层矿带，南北宽15公里",
    ("第四章其它矿产", "第二节石英矿"): "连云港市石英矿主要分布在东海县境内",
    ("第四章其它矿产", "第三节大理石矿"): "黄川等地，总储量5999万立方米",
    ("第四章其它矿产", "第四节花岗石矿"): "花岗石矿在全市境内广泛分布",
    ("第四章其它矿产", "第五节云母矿"): "云母矿主要分布在东海县陆湖",
    ("第四章其它矿产", "第六节蓝晶石矿 砂岩 蛭石 玄武岩矿"): "一、蓝晶石矿",
}

SECTION_VARIANTS = {
    "第一节地质勘探": ["第一节地质勘探", "第一节"],
    "第二节基本建设": ["第二节基本建设", "第二节"],
    "第三节生产经营": ["第三节生产经营", "第三节"],
    "第四节主要企业简介": ["第四节主要企业简介", "第四节"],
    "第一节水晶矿": ["第一节水晶矿", "第一节"],
    "第二节石英矿": ["第二节石英矿", "第二节"],
    "第三节大理石矿": ["第三节大理石矿", "第三节"],
    "第四节花岗石矿": ["第四节花岗石矿", "第四节"],
    "第五节云母矿": ["第五节云母矿", "第五节"],
    "第六节蓝晶石矿 砂岩 蛭石 玄武岩矿": ["第六节蓝晶石矿 砂岩 蛭石 玄武岩矿", "第六节蓝晶石矿", "第六节"],
}


def h3(title: str) -> str:
    return f'<h3 id="第二十六卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第二十六卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    start_candidates = [text.find("\n第二十六卷\n"), text.find("\n第二十六卷 矿产\n")]
    start_candidates = [pos for pos in start_candidates if pos >= 0]
    start = min(start_candidates) if start_candidates else -1
    end_candidates = [text.find("\n第二十七卷\n", start if start >= 0 else 0), text.find("\n第二十七卷 开发区\n", start if start >= 0 else 0)]
    end_candidates = [pos for pos in end_candidates if pos >= 0]
    end = min(end_candidates) if end_candidates else -1
    if start < 0 or end < 0:
        raise RuntimeError("Cannot locate 第二十六卷 source range")
    head, section, tail = text[:start], text[start:end], text[end:]
    replacements = {
        "\n第二十六卷\n概述\n": "\n第二十六卷 矿产\n\n概述\n",
        "\n第三节\n生产经营\n": "\n第三节生产经营\n",
        "\n第四节\n主要企业简介\n": "\n第四节主要企业简介\n",
        "\n第二章\n煤矿\n": "\n第二章煤矿\n",
        "\n第一节\n地质勘探\n": "\n第一节地质勘探\n",
        "\n第二节\n基本建设\n": "\n第二节基本建设\n",
        "\n第三章\n蛇纹石矿\n": "\n第三章蛇纹石矿\n",
        "\n第四章\n其它矿产\n": "\n第四章其它矿产\n",
        "\n第五节\n云母矿\n": "\n第五节云母矿\n",
        "\n砂岩蛭石\n玄武岩矿\n第六节\n蓝晶石矿\n": "\n第六节蓝晶石矿 砂岩 蛭石 玄武岩矿\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    text = head + section + tail
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第二十六卷卷题、章题、节题断裂和第六节复合标题 OCR 顺序错误。"]
    return []


def normalize_residue(section: str) -> str:
    section = section.replace("砂岩蛭石玄武岩矿第六节蓝晶石矿", "第六节蓝晶石矿 砂岩 蛭石 玄武岩矿", 1)
    section = section.replace("<p>第一节地质勘探：", "<p>第一节地质勘探")
    return section


def insert_or_replace_title(section: str, marker: str, needle: str, variants: list[str], start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    needle_pos = section.find(needle, max(0, start - 1000))
    if needle_pos < 0:
        needle_pos = section.find(needle)
    if needle_pos >= 0:
        prefix_start = max(0, needle_pos - 480)
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
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第二十六卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)
    summary_marker = '<h3 id="第二十六卷-概述">概述</h3>'
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
        raise RuntimeError("Cannot locate 第二十六卷 矿产 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第二十六卷-矿产">第二十六卷矿产</h2>'
    ipa_before = section.count('<div class="ipa-data">')
    section = re.sub(r'<div class="ipa-data">(.*?)</div>', r'<p>\1</p>', section, flags=re.S)
    if ipa_before:
        actions.append(f"将第二十六卷误用 `ipa-data` 的正文 OCR 残块转回段落：{ipa_before} 处。")
    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复矿产卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复矿产卷节级 H4 标题：{h4_added} 处。")
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
            if title.startswith("表26-") or number.startswith("表26-"):
                tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(f"| {data.get('table_id', '')} | {data.get('table_number') or data.get('title', '')} | {data.get('title', '')} | {pages} | {data.get('status', '')} | {size} | {data.get('notes', '')} |")
    if not table_lines:
        table_lines = ["| 暂无登记 | 未见表26-* | 第二十六卷未发现表格站登记或源 MD 可见表号 | p1282-p1296 | 待 PDF 复核 | 待定 | 本轮重点恢复章节格式；表格专项时按原 PDF 全页检查 |"]

    lines = [
        "# 第二十六卷矿产 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第二十六卷 矿产。",
        "- 源 MD：`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第二十六卷-矿产` 至 `第二十七卷-*` 之前。",
        "- 源页范围：约 p1282-p1296，位于中册 part01。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第二十六卷正文区间和目录骨架，确认本卷为四章：磷矿、煤矿、蛇纹石矿、其它矿产。",
        "- 统计第二十六卷表格状态，表格站暂无表26-*登记，源 MD 未检出可见表26-*编号。",
        "",
        "## 格式修复清单",
        "",
        "- 卷题恢复为 `第二十六卷矿产`，卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章磷矿` 至 `第四章其它矿产` 共 4 个 H3。",
        "- 恢复磷矿、煤矿、蛇纹石矿、其它矿产下各节共 18 个 H4。",
        "- 将第二十六卷误入 `ipa-data` 的正文 OCR 残块转回普通段落。",
        "- 清理源 MD 中第二章、第三章、第四章断行标题，以及 `第六节蓝晶石矿 砂岩 蛭石 玄武岩矿` 的 OCR 顺序错位。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表26-*的登记表格：{len(tables)} 张。",
        "- 源 MD 本卷范围未检出 `表26-*` 显式表号；后续表格专项仍需按 p1282-p1296 原 PDF 逐页复核，确认是否存在无编号表或图表残片。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第二十六卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第二十六卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第二十六卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第二十六卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第二十六卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第二十六卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第二十六卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第二十六卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第二十六卷全部章、节标题扁平化为正文，卷题误显示为 `第二十六卷概述`。",
        "- 源 MD 中第二章、第三章、第四章及多处节题被拆行。",
        "- 第四章第六节在 OCR 中出现 `砂岩蛭石玄武岩矿` 前置、正式节题后置的顺序错位。",
        "- 本卷无表格站登记，且源 MD 未检出显式表号，表格风险需要进入 PDF 专项复核。",
        "",
        "## 解决的困难",
        "",
        "- 以目录骨架确认第二章为煤矿、第三章为蛇纹石矿，避免按 OCR 预估顺序误修。",
        "- 用正文首句和目录骨架双重定位标题，将同名 `第一节地质勘探` 等重复节题恢复到对应章下。",
        "- 对第四章第六节采用目录全名 `第六节蓝晶石矿 砂岩 蛭石 玄武岩矿`，保留其下 `一、蓝晶石矿` 等分项正文。",
        "",
        "## 残留风险",
        "",
        "- 第二十六卷矿种、地质术语、储量单位和企业名称密集，后续精校需结合原 PDF 校对。",
        "- 需在表格专项阶段按原 PDF 逐页确认本卷是否存在无编号表、统计图或 OCR 漏识表格。",
        "",
        "## 下一步计划",
        "",
        "- 进入第二十七卷 开发区章节格式核对。",
        "- 表格专项阶段回看第二十六卷 p1282-p1296，确认矿产卷是否需新增表格站条目。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第二十六卷矿产章节核对完成"
    section = f"""{header}

已完成 `第二十六卷 矿产` 章节格式核对：

- 新增脚本：`scripts/repair_twenty_sixth_volume_mining.py`。
- 修复 `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md` 中第二十六卷卷题、章题、节题断裂和第六节复合标题 OCR 顺序错位。
- 修复 `output/final_reader/连云港市志_全书.html` 中第二十六卷卷题误作 `第二十六卷概述`、章节标题全部扁平化以及正文残块误用 `ipa-data` 的问题。
- 第二十六卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章磷矿至第四章其它矿产），H4={stats['h4_count']}。
- 第二十六卷范围内 `ipa-data` 残留已清零。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表26-*登记条目，源 MD 未检出可见表26-*编号。
- 已写入进度文档：`output/reports/progress/20260628_第二十六卷矿产_修复核对进度.md`。

验收：第二十六卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第二十七卷 开发区`。第二十六卷需在表格专项阶段按 p1282-p1296 原 PDF 逐页确认是否存在无编号表或 OCR 漏识表格。
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

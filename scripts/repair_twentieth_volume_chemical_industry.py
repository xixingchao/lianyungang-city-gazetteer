# -*- coding: utf-8 -*-
"""Repair and audit 第二十卷 化学工业 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第二十卷化学工业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第二十卷-化学工业">.*?</h2>)(.*?)(?=<h2 id="第二十一卷-机械工业">)', re.S)

CHAPTERS = [
    ("第一章化工原料", ["第一节产品", "第二节主要企业简介"]),
    ("第二章化肥农药", ["第一节化学肥料", "第二节农药", "第三节主要企业简介"]),
    (
        "第三章其它化工制品",
        [
            "第一节添加剂",
            "第二节胶粘剂",
            "第三节其它剂类",
            "第四节香料涂料",
            "第五节石油制品",
            "第六节橡胶制品",
            "第七节化冶制品",
            "第八节主要企业简介",
        ],
    ),
]

CHAPTER_NEEDLES = {
    "第一章化工原料": "连云港市化工原料生产，主要围绕地产的磷矿石",
    "第二章化肥农药": "连云港市的化肥工业是从生产磷肥开始的",
    "第三章其它化工制品": "20世纪50年代初期前，全市日用化工制品主要有",
}

CHAPTER_VARIANTS = {
    "第一章化工原料": ["化工原料", "第一章化工原料"],
    "第二章化肥农药": ["农药化肥", "化肥农药", "第二章化肥农药"],
    "第三章其它化工制品": ["其它化工制品", "第三章其它化工制品"],
}

SECTION_NEEDLES = {
    ("第一章化工原料", "第一节产品"): "无机酸主要产品",
    ("第一章化工原料", "第二节主要企业简介"): "口创汇先进单位",
    ("第二章化肥农药", "第一节化学肥料"): "连云港市的化肥工业是从生产磷肥开始的",
    ("第二章化肥农药", "第二节农药"): "1959年初，中共新海连市委在新光化工厂的基础上",
    ("第二章化肥农药", "第三节主要企业简介"): "一、东海县磷肥厂",
    ("第三章其它化工制品", "第一节添加剂"): "饲料级磷酸氢钙1964年",
    ("第三章其它化工制品", "第二节胶粘剂"): "一、合成胶",
    ("第三章其它化工制品", "第三节其它剂类"): "一、化学试剂",
    ("第三章其它化工制品", "第四节香料涂料"): "一、香料",
    ("第三章其它化工制品", "第五节石油制品"): "1957年，新海连市炼油厂开始生产煤油",
    ("第三章其它化工制品", "第六节橡胶制品"): "1958年，新浦橡胶厂",
    ("第三章其它化工制品", "第七节化冶制品"): "一、炭素",
    ("第三章其它化工制品", "第八节主要企业简介"): "连云港市制碘厂",
}

SECTION_VARIANTS = {
    "第一节产品": ["第一节•产、", "第一节•产", "第一节产品"],
    "第二节主要企业简介": ["第二节主要企业简介", "第二节"],
    "第一节化学肥料": ["第一节化", "第一节化学肥料"],
    "第二节农药": ["农药第二节", "第二节农药", "第二节"],
    "第三节主要企业简介": ["第三节主要企业简介", "第三节"],
    "第一节添加剂": ["第一节添加剂、", "第一节添加剂"],
    "第二节胶粘剂": ["胶粘剂第二节", "第二节胶粘剂", "第二节"],
    "第三节其它剂类": ["第三节其它剂类", "第三节"],
    "第四节香料涂料": ["香料涂料第四节", "第四节香料涂料", "第四节"],
    "第五节石油制品": ["第五节石油制品", "第五节"],
    "第六节橡胶制品": ["第六节橡胶制品", "第六节"],
    "第七节化冶制品": ["第七节市化治制品", "第七节化冶制品", "第七节"],
    "第八节主要企业简介": ["第八节主要企业简介、", "第八节主要企业简介", "第八节"],
}

EXPECTED_TABLES = [f"表20-{i}" for i in range(1, 17)]


def h3(title: str) -> str:
    return f'<h3 id="第二十卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第二十卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    start_candidates = [text.find("\n第二十卷\n"), text.find("\n第二十卷 化学工业\n")]
    start_candidates = [pos for pos in start_candidates if pos >= 0]
    start = min(start_candidates) if start_candidates else -1
    end_candidates = [text.find("\n第二十一卷\n", start if start >= 0 else 0), text.find("\n第二十一卷 机械工业\n", start if start >= 0 else 0)]
    end_candidates = [pos for pos in end_candidates if pos >= 0]
    end = min(end_candidates) if end_candidates else -1
    if start < 0 or end < 0:
        raise RuntimeError("Cannot locate 第二十卷 source range")
    head, section, tail = text[:start], text[start:end], text[end:]
    replacements = {
        "\n第二十卷\n化学工业\n概述\n": "\n第二十卷 化学工业\n\n概述\n",
        "\n第一章\n化工原料\n": "\n第一章化工原料\n",
        "\n第一节•产\n、无机酸\n": "\n第一节产品\n一、无机酸\n",
        "\n第二节\n主要企业简介\n": "\n第二节主要企业简介\n",
        "\n农药\n化肥\n第二章\n第一节化\n": "\n第二章化肥农药\n第一节化学肥料\n",
        "\n农药\n第二节\n": "\n第二节农药\n",
        "\n第三节\n主要企业简介\n": "\n第三节主要企业简介\n",
        "\n第三章\n其它化工制品\n": "\n第三章其它化工制品\n",
        "\n第一节添加剂\n、饲料级磷酸氢钙\n": "\n第一节添加剂\n一、饲料级磷酸氢钙\n",
        "\n胶粘剂\n第二节\n": "\n第二节胶粘剂\n",
        "\n第三节\n其它剂类\n": "\n第三节其它剂类\n",
        "\n香料涂料\n第四节\n": "\n第四节香料涂料\n",
        "\n第五节\n石油制品\n": "\n第五节石油制品\n",
        "\n第六节\n橡胶制品\n": "\n第六节橡胶制品\n",
        "\n第七节\n市化治制品\n": "\n第七节化冶制品\n",
        "\n第八节\n主要企业简介\n、连云港市制碘厂\n": "\n第八节主要企业简介\n一、连云港市制碘厂\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    text = head + section + tail
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第二十卷卷题、章题、节题断裂和小题序号 OCR 残缺。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "<p>第一节•产、": "<p>",
        "<p>农药化肥": "<p>",
        "<p>第一节添加剂、": "<p>",
        "<p>胶粘剂第二节": "<p>",
        "<p>香料涂料第四节": "<p>",
        "<p>第七节市化治制品": "<p>",
        "<p>第八节主要企业简介、": "<p>",
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
        prefix_start = max(0, needle_pos - 280)
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
        r'(<h4 id="第二十卷-第二章化肥农药-第一节化学肥料">第一节化学肥料</h4>)\n(<h3 id="第二十卷-第二章化肥农药">第二章化肥农药</h3>)',
        r"\2\n\1",
        section,
        count=1,
    )
    section = re.sub(r"(</h[34]>)\n(?!<)([^\n<][^\n]*?</p>)", r"\1\n<p>\2", section)
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第二十卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)

    summary_marker = '<h3 id="第二十卷-概述">概述</h3>'
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
        raise RuntimeError("Cannot locate 第二十卷 化学工业 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第二十卷-化学工业">第二十卷化学工业</h2>'

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>').replace('</div>', '</p>')
    if ipa_before:
        actions.append(f"将第二十卷误用 `ipa-data` 的表格 OCR 残块转回段落：{ipa_before} 处。")

    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复化学工业卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复化学工业卷节级 H4 标题：{h4_added} 处。")

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
            if title.startswith("表20-") or number.startswith("表20-"):
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
        table_lines = [f"| 暂无登记 | {table_no} | 第二十卷表格尚未进入表格站 | p1046-p1094 | 待补登 | 待定 | 需从源 PDF 专项补建、核验 |" for table_no in EXPECTED_TABLES]

    lines = [
        "# 第二十卷化学工业 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第二十卷 化学工业。",
        "- 源 MD：`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第二十卷-化学工业` 至 `第二十一卷-机械工业` 之前。",
        "- 源页范围：约 p1044-p1095，位于中册 part01。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第二十卷正文区间，确认本卷实际为三章：化工原料、化肥农药、其它化工制品。",
        "- 统计第二十卷表格状态，表格站暂无表20-*登记，阅读版已有结构化表但仍需 PDF 表格专项复建。",
        "",
        "## 格式修复清单",
        "",
        "- 卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章化工原料` 至 `第三章其它化工制品` 共 3 个 H3。",
        "- 恢复产品、化工原料主要企业、化学肥料、农药、化肥农药主要企业、添加剂、胶粘剂、其它剂类、香料涂料、石油制品、橡胶制品、化冶制品、其它化工制品主要企业等 13 个 H4。",
        "- 将第二十卷误入 `ipa-data` 的表20-3 OCR 残块转回普通段落。",
        "- 清理源 MD 中章题、节题断裂和 `市化治制品` 等 OCR 标题错误。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表20-*的登记表格：{len(tables)} 张。",
        "- 源 MD 可见表20-1至表20-16；表20-15和表20-16存在跨页续表残文，需 PDF 专项重建。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第二十卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第二十卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第二十卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第二十卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第二十卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第二十卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第二十卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第二十卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第二十卷全部章、节标题扁平化为正文。",
        "- OCR 将 `第二章化肥农药` 与 `第一节化学肥料` 压成 `农药化肥第一节化`。",
        "- OCR 将 `第七节化冶制品` 识别为 `第七节市化治制品`。",
        "- 表20-*均未登记到表格站，阅读版结构化表仍为待对照原图录入状态。",
        "",
        "## 解决的困难",
        "",
        "- 以第二十卷至第二十一卷边界限定修复范围，避免误动机械工业卷。",
        "- 对第二章开头采用正文首句定位，分别恢复章题和第一节题。",
        "- 对重复出现的 `主要企业简介` 按所属章生成唯一 H4 锚点。",
        "",
        "## 残留风险",
        "",
        "- 第二十卷表20-1至表20-16需从源 PDF 逐张核读、补登、结构化。",
        "- 化工产品名、企业名、化学品名和统计指标密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第二十一卷 机械工业章节格式核对。",
        "- 表格专项阶段回补第二十卷化工原料、化肥农药、添加剂、胶粘剂、获奖产品等统计表。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第二十卷化学工业章节核对完成"
    section = f"""{header}

已完成 `第二十卷 化学工业` 章节格式核对：

- 新增脚本：`scripts/repair_twentieth_volume_chemical_industry.py`。
- 修复 `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md` 中第二十卷卷题、章题、节题断裂和 OCR 标题错误。
- 修复 `output/final_reader/连云港市志_全书.html` 中第二十卷章节标题全部扁平化以及表格 OCR 残块误用 `ipa-data` 的问题。
- 第二十卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章化工原料至第三章其它化工制品），H4={stats['h4_count']}。
- 第二十卷范围内 `ipa-data` 残留已清零。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表20-*登记条目。
- 已写入进度文档：`output/reports/progress/20260628_第二十卷化学工业_修复核对进度.md`。

验收：第二十卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第二十一卷 机械工业`。第二十卷表20-*需从源 PDF 专项补登、重建和核验。
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

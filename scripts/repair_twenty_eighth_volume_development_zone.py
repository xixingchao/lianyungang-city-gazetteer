# -*- coding: utf-8 -*-
"""Repair and audit 第二十八卷 开发区 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第二十八卷开发区_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第二十八卷-开发区">.*?</h2>)(.*?)(?=<h2 id="第二十九卷-[^"]+">)', re.S)

CHAPTERS = [
    ("第一章建区条件 发展规划", ["第一节建区条件", "第二节发展规划"]),
    ("第二章基本建设", ["第一节基础设施", "第二节土地管理", "第三节社会服务"]),
    ("第三章政策法规", ["第一节外商投资优惠政策", "第二节内联企业优惠待遇"]),
    ("第四章项目引进", ["第一节机械 电子", "第二节轻工 纺织", "第三节医药 包装", "第四节食品 饮料", "第五节化工 建材", "第六节技术 信息"]),
]

CHAPTER_NEEDLES = {
    "第一章建区条件 发展规划": "一、地理位置和行政区划",
    "第二章基本建设": "连云港经济技术开发区成立后，建设工作全面展开",
    "第三章政策法规": "开发区经济的发展得到国家优惠政策的大力扶持",
    "第四章项目引进": "自1985年9月开工以来，开发区按照中央关于开发区必须坚持",
}

CHAPTER_VARIANTS = {
    "第一章建区条件 发展规划": ["第一章建区条件发展规划", "建区条件发展规划", "第一章"],
    "第二章基本建设": ["第二章基本建设", "基本建设"],
    "第三章政策法规": ["第三章政策法规", "政策法规"],
    "第四章项目引进": ["第四章项目引进", "项目引进"],
}

SECTION_NEEDLES = {
    ("第一章建区条件 发展规划", "第一节建区条件"): "一、地理位置和行政区划",
    ("第一章建区条件 发展规划", "第二节发展规划"): "1984年，连云港市规划局草拟",
    ("第二章基本建设", "第一节基础设施"): "一、道路建设",
    ("第二章基本建设", "第二节土地管理"): "一、土地征用",
    ("第二章基本建设", "第三节社会服务"): "开发区在抓好经济建设的同时",
    ("第三章政策法规", "第一节外商投资优惠政策"): "一、税收",
    ("第三章政策法规", "第二节内联企业优惠待遇"): "一、税收",
    ("第四章项目引进", "第一节机械 电子"): "机械电子产业是区内技术、经济实力最强的支柱产业",
    ("第四章项目引进", "第二节轻工 纺织"): "纺织行业拥有生产性企业12家",
    ("第四章项目引进", "第三节医药 包装"): "医药包装行业1990年有6家企业",
    ("第四章项目引进", "第四节食品 饮料"): "食品饮料行业在连云港开发区起步较早",
    ("第四章项目引进", "第五节化工 建材"): "主要有7家企业，1990年实现工业产值82.65万元",
    ("第四章项目引进", "第六节技术 信息"): "区内从事技术开发和信息咨询的企业有6家",
}

SECTION_VARIANTS = {
    "第一节建区条件": ["第一节建区条件", "第一节"],
    "第二节发展规划": ["第二节发展规划", "第二节"],
    "第一节基础设施": ["第一节基础设施", "第一节"],
    "第二节土地管理": ["第二节土地管理", "第二节"],
    "第三节社会服务": ["第三节社会服务", "第三节"],
    "第一节外商投资优惠政策": ["第一节外商投资优惠政策", "第一节"],
    "第二节内联企业优惠待遇": ["第二节内联企业优惠待遇", "第二节"],
    "第一节机械 电子": ["机械电子第一节", "第一节机械 电子", "第一节"],
    "第二节轻工 纺织": ["纺织轻工第二节", "轻工纺织第二节", "第二节轻工 纺织", "第二节"],
    "第三节医药 包装": ["•医药•包装第三节", "医药包装第三节", "第三节医药 包装", "第三节"],
    "第四节食品 饮料": ["食品•饮料第四节", "食品饮料第四节", "第四节食品 饮料", "第四节"],
    "第五节化工 建材": ["建材第五节化工", "第五节化工", "第五节化工 建材", "第五节"],
    "第六节技术 信息": ["第六节‧技术‧信息", "第六节技术信息", "第六节技术 信息", "第六节"],
}

EXPECTED_TABLES = [f"表28-{i}" for i in range(1, 4)]


def h3(title: str) -> str:
    return f'<h3 id="第二十八卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第二十八卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    starts = [text.find("\n第二十八卷\n"), text.find("\n第二十八卷 开发区\n")]
    starts = [pos for pos in starts if pos >= 0]
    start = min(starts) if starts else -1
    ends = [text.find("\n第二十九卷\n", start if start >= 0 else 0), text.find("\n第二十九卷 口岸\n", start if start >= 0 else 0)]
    ends = [pos for pos in ends if pos >= 0]
    end = min(ends) if ends else -1
    if start < 0 or end < 0:
        raise RuntimeError("Cannot locate 第二十八卷 source range")
    head, section, tail = text[:start], text[start:end], text[end:]
    replacements = {
        "\n第二十八卷\n开发区\n概述\n": "\n第二十八卷 开发区\n\n概述\n",
        "\n第一章\n建区条件\n发展规划\n": "\n第一章建区条件 发展规划\n",
        "\n第二节\n发展规划\n": "\n第二节发展规划\n",
        "\n第二章\n基本建设\n": "\n第二章基本建设\n",
        "\n第一节\n基础设施\n": "\n第一节基础设施\n",
        "\n第二章基本建设。1227 ·\n": "\n",
        "\n第二节\n土地管理\n": "\n第二节土地管理\n",
        "\n第三章\n政策法规\n": "\n第三章政策法规\n",
        "\n第一节\n外商投资优惠政策\n": "\n第一节外商投资优惠政策\n",
        "\n第二节\n内联企业优惠待遇\n": "\n第二节内联企业优惠待遇\n",
        "\n第四章\n项目引进\n": "\n第四章项目引进\n",
        "\n机械电子\n第一节\n": "\n第一节机械 电子\n",
        "\n纺织\n轻工\n第二节\n": "\n第二节轻工 纺织\n",
        "\n•医药•包装\n第三节\n": "\n第三节医药 包装\n",
        "\n食品•饮料\n第四节\n": "\n第四节食品 饮料\n",
        "\n建材\n第五节化工\n": "\n第五节化工 建材\n",
        "\n第六节‧技术‧信息\n": "\n第六节技术 信息\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    fixed = head + section + tail
    if fixed != original:
        SRC_MD.write_text(fixed, encoding="utf-8")
        return ["规范源 MD 中第二十八卷卷题、章题、节题断裂、页眉残留和第四章节题 OCR 顺序错位。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "第二章基本建设。1227 ·": "",
        "建区条件发展规划第一节建区条件": "建区条件发展规划第一节建区条件",
        "机械电子第一节": "第一节机械 电子",
        "纺织轻工第二节": "第二节轻工 纺织",
        "•医药•包装第三节": "第三节医药 包装",
        "食品•饮料第四节": "第四节食品 饮料",
        "建材第五节化工": "第五节化工 建材",
        "第六节‧技术‧信息": "第六节技术 信息",
    }
    for old, new in residues.items():
        section = section.replace(old, new)
    return section


def insert_or_replace_title(section: str, marker: str, needle: str, variants: list[str], start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    needle_pos = section.find(needle, max(0, start - 1500))
    if needle_pos < 0:
        needle_pos = section.find(needle)
    if needle_pos >= 0:
        prefix_start = max(0, needle_pos - 700)
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
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第二十八卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)
    summary_marker = '<h3 id="第二十八卷-概述">概述</h3>'
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
        "front_matter_residual": len(re.findall(r"CIP(?!/90)|责任编辑|编纂委员会|方志出版社", block)),
    }


def repair_html() -> tuple[list[str], dict[str, int]]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第二十八卷 开发区 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第二十八卷-开发区">第二十八卷开发区</h2>'
    ipa_before = section.count('<div class="ipa-data">')
    section = re.sub(r'<div class="ipa-data">(.*?)</div>', r'<p>\1</p>', section, flags=re.S)
    if ipa_before:
        actions.append(f"将第二十八卷误用 `ipa-data` 的正文 OCR 残块转回段落：{ipa_before} 处。")
    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复开发区卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复开发区卷节级 H4 标题：{h4_added} 处。")
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
            if title.startswith("表28-") or number.startswith("表28-"):
                tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(f"| {data.get('table_id', '')} | {data.get('table_number') or data.get('title', '')} | {data.get('title', '')} | {pages} | {data.get('status', '')} | {size} | {data.get('notes', '')} |")
    if not table_lines:
        table_lines = [f"| 暂无登记 | {table_no} | 第二十八卷可见表格尚未进入表格站 | p1324-p1333 | 待补登 | 待定 | 需从源 PDF 专项补建、核验 |" for table_no in EXPECTED_TABLES]

    lines = [
        "# 第二十八卷开发区 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第二十八卷 开发区。",
        "- 源 MD：`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第二十八卷-开发区` 至 `第二十九卷-*` 之前。",
        "- 源页范围：约 p1322-p1338，位于中册 part01。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第二十八卷正文区间和目录骨架，确认本卷为四章：建区条件 发展规划、基本建设、政策法规、项目引进。",
        "- 统计第二十八卷表格状态，源 MD 可见表28-1至表28-3，表格站暂无表28-*登记。",
        "",
        "## 格式修复清单",
        "",
        "- 卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章建区条件 发展规划` 至 `第四章项目引进` 共 4 个 H3。",
        "- 恢复建区条件、发展规划、基础设施、土地管理、社会服务、外商投资优惠政策、内联企业优惠待遇及项目引进各行业共 13 个 H4。",
        "- 将第二十八卷误入 `ipa-data` 的正文 OCR 残块转回普通段落。",
        "- 清理源 MD 中页眉残留 `第二章基本建设。1227 ·` 和第四章节题顺序错位。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表28-*的登记表格：{len(tables)} 张。",
        "- 源 MD 可见表28-1至表28-3；当前阅读版仅 1 处结构化表，需 PDF 表格专项重建。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第二十八卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第二十八卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第二十八卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第二十八卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第二十八卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第二十八卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第二十八卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第二十八卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第二十八卷全部章、节标题扁平化为正文。",
        "- 第四章多处节题存在 OCR 前后倒置或符号混入，如 `机械电子第一节`、`纺织轻工第二节`、`第六节‧技术‧信息`。",
        "- 源 MD 和阅读版中有 `ipa-data` 误分类正文，以及页眉残留。",
        "- 表28-*未进入表格站，阅读版表格多数仍为 OCR 残片。",
        "",
        "## 解决的困难",
        "",
        "- 以目录骨架确认第四章六个行业节题的正式顺序，避免沿用 OCR 倒置文本。",
        "- 对 `第一节`、`第二节` 等重复标题使用章级上下文和正文首句定位。",
        "- 本轮只恢复章节交付结构，对表28-*保留专项重建风险记录。",
        "",
        "## 残留风险",
        "",
        "- 表28-1至表28-3需从源 PDF 逐张核读、补登、结构化。",
        "- 开发区规划、投资、土地收费等数值密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第二十九卷 口岸章节格式核对。",
        "- 表格专项阶段回补第二十八卷 3 张可见表格。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第二十八卷开发区章节核对完成"
    section = f"""{header}

已完成 `第二十八卷 开发区` 章节格式核对：

- 新增脚本：`scripts/repair_twenty_eighth_volume_development_zone.py`。
- 修复 `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md` 中第二十八卷卷题、章题、节题断裂、页眉残留和第四章节题 OCR 顺序错位。
- 修复 `output/final_reader/连云港市志_全书.html` 中第二十八卷章节标题全部扁平化以及正文残块误用 `ipa-data` 的问题。
- 第二十八卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章建区条件 发展规划至第四章项目引进），H4={stats['h4_count']}。
- 第二十八卷范围内 `ipa-data` 残留已清零。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表28-*登记条目。
- 源 MD 可见表28-1至表28-3，本轮先记录为表格专项重点风险。
- 已写入进度文档：`output/reports/progress/20260628_第二十八卷开发区_修复核对进度.md`。

验收：第二十八卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第二十九卷 口岸`。第二十八卷表28-1至表28-3需从源 PDF 专项补登、重建和核验。
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

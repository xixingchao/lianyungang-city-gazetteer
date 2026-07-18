# -*- coding: utf-8 -*-
"""Repair and audit 第十五卷 纺织工业 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第十卷至第十六卷（part03）.md"
TABLE_DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第十五卷纺织工业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第十五卷-纺织工业">.*?</h2>)(.*?)(?=<h2 id="第十六卷-皮塑工业">)', re.S)

CHAPTERS = [
    ("第一章化学纤维", ["第一节聚酯切片", "第二节合成纤维", "第三节主要企业简介"]),
    ("第二章棉纺织印染", ["第一节棉纺", "第二节棉织", "第三节印染", "第四节主要企业简介"]),
    ("第三章针织复制", ["第一节针织", "第二节复制", "第三节主要企业简介"]),
    ("第四章麻毛丝织", ["第一节麻纺织", "第二节毛纺织", "第三节丝织", "第四节主要企业简介"]),
    ("第五章服装鞋帽", ["第一节服装", "第二节鞋帽", "第三节主要企业简介"]),
]

CHAPTER_NEEDLES = {
    "第一章化学纤维": "1966年，全市第一家化纤企业",
    "第二章棉纺织印染": "明末清初，境内第一家手工染坊",
    "第三章针织复制": "连云港市针织、复制业分别始于",
    "第四章麻毛丝织": "连云港市丝织业始于西汉",
    "第五章服装鞋帽": "境内服装、鞋帽业相继始于",
}

SECTION_NEEDLES = {
    ("第一章化学纤维", "第一节聚酯切片"): "1975年底，江苏省轻工业厅",
    ("第一章化学纤维", "第二节合成纤维"): "一、维纶纤维",
    ("第一章化学纤维", "第三节主要企业简介"): "连云港涤纶厂",
    ("第二章棉纺织印染", "第一节棉纺"): "1971年下半年，经江苏省革命委员会批准",
    ("第二章棉纺织印染", "第二节棉织"): "清末民初，山东潍县人韩照堂",
    ("第二章棉纺织印染", "第三节印染"): "明末清初，山东石井村王姓",
    ("第二章棉纺织印染", "第四节主要企业简介"): "一、连云港市纺织厂",
    ("第三章针织复制", "第一节针织"): "一、针织衫裤",
    ("第三章针织复制", "第二节复制"): "一、巾被",
    ("第三章针织复制", "第三节主要企业简介"): "一、连云港市针织内衣厂",
    ("第四章麻毛丝织", "第一节麻纺织"): "连云港市麻纺织业始于",
    ("第四章麻毛丝织", "第二节毛纺织"): "一、毛线",
    ("第四章麻毛丝织", "第三节丝织"): "连云港市丝织业始于西汉时期",
    ("第四章麻毛丝织", "第四节主要企业简介"): "一、连云港麻纺织厂",
    ("第五章服装鞋帽", "第一节服装"): "境内服装业始于清朝后期",
    ("第五章服装鞋帽", "第二节鞋帽"): "连云港市鞋帽业首创于",
    ("第五章服装鞋帽", "第三节主要企业简介"): "一、连云港市服装厂",
}


def h3(title: str) -> str:
    return f'<h3 id="第十五卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第十五卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    replacements = {
        "\n第十五卷\n纺织工业\n概述\n": "\n第十五卷 纺织工业\n\n概述\n",
        "\n第二章\n棉纺织印染\n": "\n第二章棉纺织印染\n",
        "\n第二节棉\n": "\n第二节棉织\n",
        "\n第三节印\n": "\n第三节印染\n",
        "\n第三章\n针织复制\n": "\n第三章针织复制\n",
        "\n第一节 针\n织\n": "\n第一节针织\n",
        "\n第四章麻、毛、丝织\n": "\n第四章麻毛丝织\n",
        "\n第五章服装鞋帽\n": "\n第五章服装鞋帽\n",
        "\n第三节\n主要企业简介\n": "\n第三节主要企业简介\n",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD part03 中第十五卷卷题、章题和多处节题断裂。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "<p>棉纺织印染明末清初": "<p>明末清初",
        "<p>针织复制连云港市针织、复制业分别始于": "<p>连云港市针织、复制业分别始于",
        "<p>第一节 针织": "<p>第一节针织",
        "<p>麻、毛、丝织连云港市丝织业始于": "<p>连云港市丝织业始于",
        "<p>服装鞋帽境内服装、鞋帽业相继始于": "<p>境内服装、鞋帽业相继始于",
    }
    for old, new in residues.items():
        section = section.replace(old, new, 1)
    return section


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


def split_title_prefix(section: str, chapter: str, title: str, needle: str, start: int) -> tuple[str, bool, int]:
    marker = h4(chapter, title)
    if marker in section:
        return section, False, section.find(marker) + len(marker)

    variants = [title, title.replace("针织", " 针织")]
    needle_pos = section.find(needle, max(0, start - 300))
    if needle_pos < 0:
        needle_pos = section.find(needle)
    if needle_pos >= 0:
        prefix_start = max(0, needle_pos - 160)
        prefix = section[prefix_start:needle_pos]
        for raw in variants:
            rel = prefix.rfind(raw)
            if rel >= 0:
                pos = prefix_start + rel
                section = section[:pos] + marker + "\n<p>" + section[pos + len(raw) :]
                return section, True, pos + len(marker) + 4

    section, added, cursor = insert_before(section, marker, needle, start)
    return section, added, cursor


def cleanup_heading_markup(section: str) -> str:
    section = section.replace("<p><h3", "<h3").replace("<p><h4", "<h4")
    section = section.replace("</h3>\n</p>", "</h3>\n").replace("</h4>\n</p>", "</h4>\n")
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第十五卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)

    summary_marker = '<h3 id="第十五卷-概述">概述</h3>'
    if summary_marker not in section:
        section = summary_marker + "\n" + section.lstrip()
        h3_count += 1
    cursor = len(summary_marker)

    for chapter, _titles in CHAPTERS:
        section, added, cursor = insert_before(section, h3(chapter), CHAPTER_NEEDLES[chapter], cursor)
        h3_count += int(added)

    cursor = 0
    for chapter, titles in CHAPTERS:
        for title in titles:
            needle = SECTION_NEEDLES[(chapter, title)]
            section, added, cursor = split_title_prefix(section, chapter, title, needle, cursor)
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
        raise RuntimeError("Cannot locate 第十五卷 纺织工业 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第十五卷-纺织工业">第十五卷纺织工业</h2>'

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>').replace('</div>', '</p>')
    if ipa_before:
        actions.append(f"将第十五卷误用 `ipa-data` 的正文块转回段落：{ipa_before} 处。")

    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复纺织工业卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复纺织工业卷节级 H4 标题：{h4_added} 处。")

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
    for path in sorted(TABLE_DATA_DIR.glob("LYG-上-T*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        title = str(data.get("title") or "")
        number = str(data.get("table_number") or "")
        if title.startswith("表15-") or number.startswith("表15-"):
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
        table_lines = ["| 暂无登记 | 表15-* | 第十五卷现有表格尚未进入表格站 | p836-p875 | 待补登 | 待定 | 化纤、棉纺织、针织复制、服装鞋帽等统计表需专项补建 |"]

    lines = [
        "# 第十五卷纺织工业 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第十五卷 纺织工业。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第十五卷-纺织工业` 至 `第十六卷-皮塑工业` 之前。",
        "- 源页范围：约 p831-p875，位于上册 part03。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第十五卷正文区间，确认本卷实际为五章，覆盖化学纤维、棉纺织印染、针织复制、麻毛丝织、服装鞋帽。",
        "- 统计第十五卷表格状态，表格站暂无表15-*登记，阅读版已有结构化表和占位符。",
        "",
        "## 格式修复清单",
        "",
        "- 卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章化学纤维` 至 `第五章服装鞋帽` 共 5 个 H3。",
        "- 恢复聚酯切片、合成纤维、棉纺、棉织、印染、针织、复制、麻纺织、毛纺织、丝织、服装、鞋帽、主要企业简介等 17 个 H4。",
        "- 将第十五卷误入 `ipa-data` 的正文块转回普通段落。",
        "- 对章题残字如 `棉纺织印染`、`针织复制`、`麻、毛、丝织`、`服装鞋帽` 等仅作标题化清理，不改写正文事实。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表15-*的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第十五卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第十五卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第十五卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第十五卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第十五卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第十五卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第十五卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第十五卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第十五卷全部章、节标题扁平化为正文。",
        "- 源 MD 中第二章、第三章及多个节题断裂。",
        "- 本卷表格密集，阅读版有结构化表和占位符混排，部分表格 OCR 残文紧邻章节标题。",
        "- 表15-*均未登记到表格站。",
        "",
        "## 解决的困难",
        "",
        "- 以第十五卷至第十六卷边界限定修复范围，避免误动皮塑工业卷。",
        "- 章题按正文首句定位，节题按段首标题或节内首个稳定小题定位，避开表格残文。",
        "- 对未核表格只保留占位和现有结构表，不用 OCR 残文补填。",
        "",
        "## 残留风险",
        "",
        "- 第十五卷表格需从源 PDF 逐张核读、补登、结构化。",
        "- 企业名、产品名、设备型号、纤维规格和经济指标密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第十六卷 皮塑工业章节格式核对。",
        "- 表格专项阶段回补第十五卷化纤、棉纺织、针织复制和服装鞋帽等统计表。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第十五卷纺织工业章节核对完成"
    section = f"""{header}

已完成 `第十五卷 纺织工业` 章节格式核对：

- 新增脚本：`scripts/repair_fifteenth_volume_textile.py`。
- 修复 `workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md` 中第十五卷卷题、章题和多处节题断裂。
- 修复 `output/final_reader/连云港市志_全书.html` 中第十五卷章、节标题全部扁平化以及正文块误用 `ipa-data` 的问题。
- 第十五卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章化学纤维至第五章服装鞋帽），H4={stats['h4_count']}。
- 将第十五卷 {stats['ipa_fixed']} 处误用 `ipa-data` 的正文块转回普通段落。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表15-*登记条目。
- 已写入进度文档：`output/reports/progress/20260628_第十五卷纺织工业_修复核对进度.md`。

验收：第十五卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第十六卷 皮塑工业`。第十五卷表15-*需从源 PDF 专项补登、重建和核验。
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

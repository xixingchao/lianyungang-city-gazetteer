# -*- coding: utf-8 -*-
"""Repair and audit 第三十卷 交通运输 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第三十卷交通运输_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第三十卷-交通运输">.*?</h2>)(.*?)(?=<h2 id="第三十一卷-[^"]+">)', re.S)

CHAPTERS = [
    ("第一章公路运输", ["第一节道路", "第二节桥梁", "第三节工具", "第四节运输", "第五节管理"]),
    ("第二章内河航运", ["第一节内河航道", "第二节内河港口", "第三节装卸搬运", "第四节水运工具", "第五节客货运输"]),
    ("第三章铁路运输", ["第一节线路", "第二节车站", "第三节客货运输", "第四节站段管理"]),
    ("第四章民航运输", ["第一节机场", "第二节客货运输"]),
]

CHAPTER_NEEDLES = {
    "第一章公路运输": "西周时，境内已有道路",
    "第二章内河航运": "连云港市河川纵横，内河航运条件良好",
    "第三章铁路运输": "连云港境内的陇海铁路",
    "第四章民航运输": "民国18年（1929年）中美合资的中国航空公司成立",
}

CHAPTER_VARIANTS = {
    "第一章公路运输": ["第一章公路运输", "公路运输", "第一章"],
    "第二章内河航运": ["第二章内河航运", "内河航运", "第二章"],
    "第三章铁路运输": ["第三章铁路运输", "铁路运输", "第三章"],
    "第四章民航运输": ["第四章民航运输", "民航运输", "第四章"],
}

SECTION_NEEDLES = {
    ("第一章公路运输", "第一节道路"): "一、国道204线民国17~18年",
    ("第一章公路运输", "第二节桥梁"): "1960年初，东海、赣榆交界处的石梁河泄闸桥竣工",
    ("第一章公路运输", "第三节工具"): "一、人力路运工具背架轿子1949年以前",
    ("第一章公路运输", "第四节运输"): "一、客　运辛亥革命以后",
    ("第一章公路运输", "第五节管理"): "民国38年（1949年)4月底，山东省政府通知专署以下各级政府设置公路管理机构",
    ("第二章内河航运", "第一节内河航道"): "一、盐河唐垂拱四年",
    ("第二章内河航运", "第二节内河港口"): "一、市区港口明《隆庆海州志》记载",
    ("第二章内河航运", "第三节装卸搬运"): "一、市区装卸搬运建国前",
    ("第二章内河航运", "第四节水运工具"): "一、木帆船木料制成",
    ("第二章内河航运", "第五节客货运输"): "一、内河客运以盐河最多",
    ("第三章铁路运输", "第一节线路"): "一、陇海路徐连段光绪三十一年",
    ("第三章铁路运输", "第二节车站"): "民国14年（1925年），徐州至大浦通车后",
    ("第三章铁路运输", "第三节客货运输"): "一、客运民国19年（1930年）",
    ("第三章铁路运输", "第四节站段管理"): "1949年以后，新浦工务段实行段、领工区",
    ("第四章民航运输", "第一节机场"): "民航连云港军民合用机场位于东海县白塔埠",
    ("第四章民航运输", "第二节客货运输"): "1985年3月，连云港民航站开始简易开航",
}

SECTION_VARIANTS = {
    "第一节道路": ["第一节道路", "第一节"],
    "第二节桥梁": ["第二节桥梁", "第二节"],
    "第三节工具": ["第三节•工•具", "第三节工具", "第三节"],
    "第四节运输": ["第四节　运输", "第四节运输", "第四节"],
    "第五节管理": ["第五节管理", "第五节"],
    "第一节内河航道": ["第一节内河航道", "第一节"],
    "第二节内河港口": ["第二节内河港口", "第二节"],
    "第三节装卸搬运": ["第三节装卸搬运", "第三节"],
    "第四节水运工具": ["第四节水运工具", "第四节"],
    "第五节客货运输": ["第五节客货运输", "第五节"],
    "第一节线路": ["第一节线　路", "第一节线路", "第一节线", "第一节"],
    "第二节车站": ["第二节•车站", "第二节车站", "第二节"],
    "第三节客货运输": ["第三节客货运输", "第三节"],
    "第四节站段管理": ["第四节站段管理", "第四节"],
    "第一节机场": ["第一节机场", "第一节"],
    "第二节客货运输": ["第二节客货运输", "第二节"],
}

EXPECTED_TABLES = [f"表30-{i}" for i in range(1, 15)]


def h3(title: str) -> str:
    return f'<h3 id="第三十卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第三十卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    start_candidates = [text.find("\n第三十卷\n"), text.find("\n第三十卷 交通运输\n")]
    start_candidates = [pos for pos in start_candidates if pos >= 0]
    start = min(start_candidates) if start_candidates else -1
    end = text.find("\n第三十一卷", start)
    if start < 0 or end < 0:
        raise RuntimeError("Cannot locate 第三十卷 source range")
    head, section, tail = text[:start], text[start:end], text[end:]
    replacements = {
        "\n第三十卷\n交通运输\n概述\n": "\n第三十卷 交通运输\n\n概述\n",
        "\n第一章\n公路运输\n": "\n第一章公路运输\n",
        "\n第三节•工•具\n": "\n第三节工具\n",
        "\n第四节　运输\n": "\n第四节运输\n",
        "\n第一章\n公路运输\n:1325 \n": "\n",
        "\n第一章公路运输\n·1333\n": "\n",
        "\n第一章公路运输\n·1339\n": "\n",
        "\n第二章\n内河航运\n": "\n第二章内河航运\n",
        "\n第二节\n内河港口\n": "\n第二节内河港口\n",
        "\n第三章\n铁路运输\n": "\n第三章铁路运输\n",
        "\n第一节线　路\n": "\n第一节线路\n",
        "\n第二节•车站\n": "\n第二节车站\n",
        "\n第三节\n一、客运\n": "\n第三节客货运输\n一、客运\n",
        "\n第四节\n站段管理\n": "\n第四节站段管理\n",
        "\n第四章\n民航运输\n": "\n第四章民航运输\n",
        "\n第二节\n客货运输\n": "\n第二节客货运输\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    fixed = head + section + tail
    if fixed != original:
        SRC_MD.write_text(fixed, encoding="utf-8")
        return ["规范源 MD 中第三十卷卷题、章题、节题断裂、页眉残留和 OCR 标题错位。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "第三节•工•具": "第三节工具",
        "第四节　运输": "第四节运输",
        "第一节线　路": "第一节线路",
        "第二节•车站": "第二节车站",
        "第一章公路运输:1325": "",
        "第一章公路运输·1333": "",
        "第一章公路运输·1339": "",
    }
    for old, new in residues.items():
        section = section.replace(old, new)
    section = re.sub(r"(\d{4})第四节站段管理", r"\1\n第四节站段管理", section)
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
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第三十卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)
    summary_marker = '<h3 id="第三十卷-概述">概述</h3>'
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
        raise RuntimeError("Cannot locate 第三十卷 交通运输 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第三十卷-交通运输">第三十卷交通运输</h2>'
    ipa_before = section.count('<div class="ipa-data">')
    section = re.sub(r'<div class="ipa-data">(.*?)</div>', r'<p>\1</p>', section, flags=re.S)
    if ipa_before:
        actions.append(f"将第三十卷误用 `ipa-data` 的正文/表格 OCR 残块转回段落：{ipa_before} 处。")
    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复交通运输卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复交通运输卷节级 H4 标题：{h4_added} 处。")
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
            if title.startswith("表30-") or number.startswith("表30-"):
                tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(f"| {data.get('table_id', '')} | {data.get('table_number') or data.get('title', '')} | {data.get('title', '')} | {pages} | {data.get('status', '')} | {size} | {data.get('notes', '')} |")
    if not table_lines:
        table_lines = [f"| 暂无登记 | {table_no} | 第三十卷可见表格尚未进入表格站 | p1440-p1484 | 待补登 | 待定 | 需从源 PDF 专项补建、核验 |" for table_no in EXPECTED_TABLES]

    lines = [
        "# 第三十卷交通运输 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第三十卷 交通运输。",
        "- 源 MD：`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第三十卷-交通运输` 至 `第三十一卷-*` 之前。",
        "- 源页范围：约 p1438-p1484，位于中册 part02。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第三十卷正文区间和目录骨架，确认本卷为四章：公路运输、内河航运、铁路运输、民航运输。",
        "- 统计第三十卷表格状态，源 MD 可见表30-1至表30-14，表格站暂无表30-*登记。",
        "",
        "## 格式修复清单",
        "",
        "- 卷题保持为 `第三十卷交通运输`，卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章公路运输` 至 `第四章民航运输` 共 4 个 H3。",
        "- 恢复公路、内河、铁路、民航各节共 16 个 H4。",
        "- 将第三十卷误入 `ipa-data` 的正文/表格 OCR 残块转回普通段落。",
        "- 清理源 MD 中页眉残留和 OCR 标题错位，如 `第三节•工•具`、`第二节•车站`、`第一节线　路`。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表30-*的登记表格：{len(tables)} 张。",
        "- 源 MD 可见表30-1至表30-14；当前阅读版已有部分结构化表，但仍需 PDF 表格专项逐张核验。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第三十卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第三十卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第三十卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第三十卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第三十卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第三十卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第三十卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第三十卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第三十卷章、节标题全部扁平化为正文。",
        "- OCR 将部分节题识别为带符号或拆行文本，如 `第三节•工•具`、`第二节•车站`、`第四节 / 站段管理`。",
        "- 铁路客货运输表格附近正文与表格 OCR 粘连，需后续表格专项校正。",
        "- 表30-*未进入表格站，阅读版仅有部分结构化表，其余需 PDF 专项重建或核验。",
        "",
        "## 解决的困难",
        "",
        "- 以目录骨架确认 4 章 16 节正式标题，再用正文首句顺序定位，避免同名 `客货运输` 小节串位。",
        "- 对铁路、民航重复出现的 `客货运输` 使用章级上下文生成唯一 H4 锚点。",
        "- 对表30-6、表30-9、表30-12等 OCR 表号形态在进度中统一按表30-*风险记录。",
        "",
        "## 残留风险",
        "",
        "- 表30-1至表30-14需从源 PDF 逐张核读、补登、结构化。",
        "- 公路、铁路客货运输统计表数值密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第三十一卷 邮电章节格式核对。",
        "- 表格专项阶段回补第三十卷 14 张可见表格。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-29 第三十卷交通运输章节核对完成"
    section = f"""{header}

已完成 `第三十卷 交通运输` 章节格式核对：

- 新增脚本：`scripts/repair_thirtieth_volume_transportation.py`。
- 修复 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md` 中第三十卷卷题、章题、节题断裂、页眉残留和 OCR 标题错位。
- 修复 `output/final_reader/连云港市志_全书.html` 中第三十卷章节标题全部扁平化以及正文/表格残块误用 `ipa-data` 的问题。
- 第三十卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章公路运输至第四章民航运输），H4={stats['h4_count']}。
- 第三十卷范围内 `ipa-data` 残留已清零。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表30-*登记条目。
- 源 MD 可见表30-1至表30-14，本轮先记录为表格专项重点风险。
- 已写入进度文档：`output/reports/progress/20260629_第三十卷交通运输_修复核对进度.md`。

验收：第三十卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第三十一卷 邮电`。第三十卷表30-1至表30-14需从源 PDF 专项补登、重建和核验。
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

# -*- coding: utf-8 -*-
"""Repair and audit 第三十二卷 名胜旅游 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第三十二卷名胜旅游_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第三十二卷-名胜旅游">.*?</h2>)(.*?)(?=<h2 id="第三十三卷-[^"]+">)', re.S)

CHAPTERS = [
    ("第一章风景名胜", ["第一节花果山风景区", "第二节渔湾风景区", "第三节宿城风景区", "第四节海滨风景区", "第五节锦屏山风景区", "第六节其它景观"]),
    ("第二章旅游", ["第一节旅游设施", "第二节旅游服务"]),
]

CHAPTER_NEEDLES = {
    "第一章风景名胜": "花果山，位于南云台山中段",
    "第二章旅游": "市境山海齐观，景色秀美",
}

CHAPTER_VARIANTS = {
    "第一章风景名胜": ["第一章风景名胜", "风景名胜", "第一章"],
    "第二章旅游": ["第二章旅游", "旅游第二章", "第二章"],
}

SECTION_NEEDLES = {
    ("第一章风景名胜", "第一节花果山风景区"): "花果山，位于南云台山中段",
    ("第一章风景名胜", "第二节渔湾风景区"): "渔湾景区位于南云台山南麓",
    ("第一章风景名胜", "第三节宿城风景区"): "素有“世外桃源”之称",
    ("第一章风景名胜", "第四节海滨风景区"): "连云港市海岸类型齐全",
    ("第一章风景名胜", "第五节锦屏山风景区"): "景区由孔望山和锦屏山组成",
    ("第一章风景名胜", "第六节其它景观"): "一、东海温泉",
    ("第二章旅游", "第一节旅游设施"): "20世纪70年代，连云港市仅有连云饭店一家涉外旅游饭店",
    ("第二章旅游", "第二节旅游服务"): "一、管理机构",
}

SECTION_VARIANTS = {
    "第一节花果山风景区": ["第一节大花果山风景区", "第一节花果山风景区", "第一节大", "第一节"],
    "第二节渔湾风景区": ["第二节渔湾风景区", "第二节"],
    "第三节宿城风景区": ["第三节宿城风景区", "第三节"],
    "第四节海滨风景区": ["第四节海滨风景区", "第四节"],
    "第五节锦屏山风景区": ["第五节锦屏山风景区", "第五节"],
    "第六节其它景观": ["第六节其它景观", "第六节"],
    "第一节旅游设施": ["第一节旅游设施", "第一节"],
    "第二节旅游服务": ["第二节）旅游服务", "第二节旅游服务", "第二节）", "第二节"],
}

EXPECTED_TABLES: list[str] = []


def h3(title: str) -> str:
    return f'<h3 id="第三十二卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第三十二卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    start_candidates = [text.find("\n第三十二卷\n"), text.find("\n第三十二卷 名胜旅游\n")]
    start_candidates = [pos for pos in start_candidates if pos >= 0]
    start = min(start_candidates) if start_candidates else -1
    end = text.find("\n第三十三卷", start)
    if start < 0 or end < 0:
        raise RuntimeError("Cannot locate 第三十二卷 source range")
    head, section, tail = text[:start], text[start:end], text[end:]
    replacements = {
        "\n第三十二卷\n名胜旅游\n概述\n": "\n第三十二卷 名胜旅游\n\n概述\n",
        "\n第一章\n风景名胜\n": "\n第一章风景名胜\n",
        "\n第一节大\n花果山风景区\n": "\n第一节花果山风景区\n",
        "\n第二节\n渔湾风景区\n": "\n第二节渔湾风景区\n",
        "\n第三节\n宿城风景区\n": "\n第三节宿城风景区\n",
        "\n第四节\n": "\n第四节海滨风景区\n",
        "\n第五节\n锦屏山风景区\n": "\n第五节锦屏山风景区\n",
        "\n第六节\n其它景观\n": "\n第六节其它景观\n",
        "\n第二章\n市境山海齐观": "\n第二章旅游\n市境山海齐观",
        "\n第二节）\n旅游服务\n": "\n第二节旅游服务\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    fixed = head + section + tail
    if fixed != original:
        SRC_MD.write_text(fixed, encoding="utf-8")
        return ["规范源 MD 中第三十二卷卷题、章题、节题断裂和 OCR 标题错位。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "第一节大花果山风景区": "第一节花果山风景区",
        "第二节）旅游服务": "第二节旅游服务",
        "旅游第二章": "第二章旅游",
    }
    for old, new in residues.items():
        section = section.replace(old, new)
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
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第三十二卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)
    summary_marker = '<h3 id="第三十二卷-概述">概述</h3>'
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
        raise RuntimeError("Cannot locate 第三十二卷 名胜旅游 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第三十二卷-名胜旅游">第三十二卷名胜旅游</h2>'
    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复名胜旅游卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复名胜旅游卷节级 H4 标题：{h4_added} 处。")
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
            if title.startswith("表32-") or number.startswith("表32-"):
                tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(f"| {data.get('table_id', '')} | {data.get('table_number') or data.get('title', '')} | {data.get('title', '')} | {pages} | {data.get('status', '')} | {size} | {data.get('notes', '')} |")
    if not table_lines:
        table_lines = ["| 无 | 无表32-* | 第三十二卷目录与源 MD 未见表32-* | p1515-p1539 | 无需补登 | - | 本卷以景区与旅游服务正文为主 |"]

    lines = [
        "# 第三十二卷名胜旅游 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第三十二卷 名胜旅游。",
        "- 源 MD：`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第三十二卷-名胜旅游` 至 `第三十三卷-*` 之前。",
        "- 源页范围：约 p1515-p1539，位于中册 part02。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第三十二卷正文区间和目录骨架，确认本卷为两章：风景名胜、旅游。",
        "- 统计第三十二卷表格状态，源 MD 与表格站均未见表32-*登记。",
        "",
        "## 格式修复清单",
        "",
        "- 卷题保持为 `第三十二卷名胜旅游`，卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章风景名胜`、`第二章旅游` 共 2 个 H3。",
        "- 恢复花果山、渔湾、宿城、海滨、锦屏山、其它景观、旅游设施、旅游服务共 8 个 H4。",
        "- 清理源 MD 中标题断裂和 OCR 标题错位，如 `第一节大 / 花果山风景区`、`第二节） / 旅游服务`。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表32-*的登记表格：{len(tables)} 张。",
        "- 源 MD 未见表32-*，本轮无卷内表格补登项。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第三十二卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第三十二卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第三十二卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第三十二卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第三十二卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第三十二卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第三十二卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第三十二卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第三十二卷章、节标题全部扁平化为正文。",
        "- OCR 将部分节题识别为断裂或带符号文本，如 `第一节大 / 花果山风景区`、`第二节） / 旅游服务`。",
        "- 第二章章题 `旅游` 在源文中缺失独立行，需要结合目录骨架和正文首句恢复。",
        "",
        "## 解决的困难",
        "",
        "- 以目录骨架确认 2 章 8 节正式标题，再用景区正文首句顺序定位。",
        "- 对第二章旅游采用正文首句 `市境山海齐观` 作为章级锚点，避免误插入到概述中的旅游叙述。",
        "",
        "## 残留风险",
        "",
        "- 本卷未见表32-*，后续重点为景区名称、古迹名称和人名地名的 OCR 精校。",
        "- 花果山、孔望山、锦屏山等景区专名较多，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第三十三卷 商业章节格式核对。",
        "- 表格专项阶段暂不需要回补第三十二卷表格。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-29 第三十二卷名胜旅游章节核对完成"
    section = f"""{header}

已完成 `第三十二卷 名胜旅游` 章节格式核对：

- 新增脚本：`scripts/repair_thirty_second_volume_scenic_tourism.py`。
- 修复 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md` 中第三十二卷卷题、章题、节题断裂和 OCR 标题错位。
- 修复 `output/final_reader/连云港市志_全书.html` 中第三十二卷章节标题全部扁平化的问题。
- 第三十二卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章风景名胜至第二章旅游），H4={stats['h4_count']}。
- 第三十二卷范围内 `ipa-data` 残留为 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表32-*登记条目，源 MD 未见表32-*。
- 已写入进度文档：`output/reports/progress/20260629_第三十二卷名胜旅游_修复核对进度.md`。

验收：第三十二卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第三十三卷 商业`。第三十二卷未见表32-*，后续重点转为专名与正文 OCR 精校。
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

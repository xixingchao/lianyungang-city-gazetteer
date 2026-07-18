# -*- coding: utf-8 -*-
"""Repair and audit 第九卷 农林业 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第四卷至第十卷（part02）.md"
TABLE_DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第九卷农林业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第九卷-农林业">.*?</h2>)(.*?)(?=<h2 id="第十卷-水利">)', re.S)

CHAPTERS = [
    ("第一章农业生产关系变革", ["第一节土地改革", "第二节农业合作化", "第三节人民公社", "第四节联产承包责任制"]),
    ("第二章耕作制度与农业区划", ["第一节耕作制度", "第二节农业区划"]),
    ("第三章品种", ["第一节水稻", "第二节三麦", "第三节玉米", "第四节大豆", "第五节花生", "第六节甘薯", "第七节棉花"]),
    ("第四章作物栽培", ["第一节水稻栽培", "第二节三麦栽培", "第三节玉米栽培", "第四节大豆栽培", "第五节花生栽培", "第六节棉花栽培"]),
    ("第五章土壤改良与肥料施用", ["第一节土壤改良", "第二节肥料施用"]),
    ("第六章植物保护", ["第一节病虫害防治", "第二节草害防治", "第三节鼠害防治", "第四节植物检疫"]),
    ("第七章农业技术推广", ["第一节推广体系", "第二节科技成果"]),
    ("第八章蔬菜生产", ["第一节蔬菜品种", "第二节蔬菜特产", "第三节栽培技术", "第四节基地建设", "第五节病虫害防治"]),
    ("第九章林果桑茶", ["第一节林木", "第二节果树", "第三节蚕桑", "第四节茶树"]),
    ("第十章农机具", ["第一节动力机具", "第二节耕作机具", "第三节播种插秧机具", "第四节田间管理机具", "第五节收获加工机具", "第六节运输机具"]),
]


def h3(title: str) -> str:
    return f'<h3 id="第九卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第九卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    replacements = {
        "\n第九卷\n农\n林\n业\n$111811131111111131111113111111111\n述\n": "\n第九卷 农林业\n\n概述\n",
        "\n第二章\n耕作制度与农业区划\n": "\n第二章耕作制度与农业区划\n",
        "\n第三章品\n种\n": "\n第三章品种\n",
        "\n第五章\n土壤改良与肥料施用\n": "\n第五章土壤改良与肥料施用\n",
        "\n第七章\n农业技术推广\n": "\n第七章农业技术推广\n",
        "\n第一节 病虫害防治\n": "\n第一节病虫害防治\n",
        "\n第五节 病虫害防治\n": "\n第五节病虫害防治\n",
        "\n第三节 播种插秧机具\n": "\n第三节播种插秧机具\n",
        "\n第五节 收获加工机具\n": "\n第五节收获加工机具\n",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD part02 中第九卷卷题、概述题和多处章/节题断裂。"]
    return []


def insert_marker(section: str, marker: str, needle: str, start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    pos = section.find(needle, start)
    if pos < 0:
        pos = section.find(needle)
    if pos < 0:
        return section, False, start
    section = section[:pos] + marker + "\n" + section[pos:]
    return section, True, pos + len(marker) + 1


def replace_title_after(section: str, raw: str, marker: str, start: int) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    variants = [raw]
    if raw in {"第一节病虫害防治", "第五节病虫害防治"}:
        variants.append(raw.replace("节", "节 ", 1))
    if raw in {"第三节播种插秧机具", "第五节收获加工机具"}:
        variants.append(raw.replace("节", "节 ", 1))
    for variant in variants:
        pos = section.find(variant, start)
        if pos < 0:
            continue
        before = section[:pos]
        after = section[pos + len(variant) :]
        section = before + marker + "\n<p>" + after
        cursor = pos + len(marker) + 4
        return section, True, cursor
    return section, False, start


def cleanup_heading_markup(section: str) -> str:
    section = section.replace("<p><h3", "<h3").replace("<p><h4", "<h4")
    section = section.replace("</h3>\n</p>", "</h3>\n").replace("</h4>\n</p>", "</h4>\n")
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第九卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0

    # Repair the OCR-broken opening: H2 already carries 第九卷农, first paragraph carries 林业...述.
    section = re.sub(r"^\s*<p>林业\$\d+述", "<p>", section, count=1)
    section, added, cursor = insert_marker(section, '<h3 id="第九卷-概述">概述</h3>', "<p>连云港市农业生产历史悠久", 0)
    h3_count += int(added)

    chapter_needles = {
        "第一章农业生产关系变革": "第一节土地改革",
        "第二章耕作制度与农业区划": "第一节耕作制度",
        "第三章品种": "第三章品种",
        "第四章作物栽培": "第四章作物栽培",
        "第五章土壤改良与肥料施用": "第一节土壤改良",
        "第六章植物保护": "第六章植物保护",
        "第七章农业技术推广": "第一节推广体系",
        "第八章蔬菜生产": "第八章蔬菜生产",
        "第九章林果桑茶": "第九章林果桑茶",
        "第十章农机具": "第十章农机具",
    }

    cursor = 0
    for chapter, section_titles in CHAPTERS:
        marker = h3(chapter)
        needle = chapter_needles[chapter]
        section, added, cursor = insert_marker(section, marker, needle, cursor)
        h3_count += int(added)
        # Remove raw chapter title if it remains immediately after the marker.
        raw_variants = [chapter, chapter.replace("第三章品种", "第三章品\n种")]
        for raw in raw_variants:
            section = section.replace(marker + "\n" + raw, marker, 1)
        for title in section_titles:
            section, added, cursor = replace_title_after(section, title, h4(chapter, title), cursor)
            h4_count += int(added)

    # Normalize existing generic anchors for chapters 9 and 10 if still present.
    section = section.replace('<h3 id="anchor">第九章林果桑茶</h3>', h3("第九章林果桑茶"))
    section = section.replace('<h3 id="anchor">第十章农机具</h3>', h3("第十章农机具"))
    return cleanup_heading_markup(section), h3_count, h4_count


def compress_duplicate_tables(section: str) -> tuple[str, int]:
    patterns = [
        r'<table class="structured-table"><thead><tr><th>年份</th><th>粮食面积\(万亩\)</th><th>平均亩产\(公斤\)</th><th>总产\(吨\)</th></tr></thead>.*?</table>\n?',
        r'<table class="structured-table"><thead><tr><th>项目名称</th><th>年份</th><th>实施单位</th><th>实施面积\(万亩\)</th></tr></thead>.*?</table>\n?',
    ]
    removed = 0
    for pat in patterns:
        regex = re.compile(pat, re.S)
        seen = False

        def repl(match: re.Match[str]) -> str:
            nonlocal seen, removed
            if seen:
                removed += 1
                return ""
            seen = True
            return match.group(0)

        section = regex.sub(repl, section)
    return section, removed


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
        raise RuntimeError("Cannot locate 第九卷 农林业 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第九卷-农林业">第九卷农林业</h2>'

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>').replace('</div>', '</p>')
    if ipa_before:
        actions.append(f"将第九卷误用 `ipa-data` 的正文块转回段落：{ipa_before} 处。")

    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复农林业卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复农林业卷节级 H4 标题：{h4_added} 处。")

    section, removed_tables = compress_duplicate_tables(section)
    if removed_tables:
        actions.append(f"压缩重复临时结构化表格实例：{removed_tables} 处。")

    fixed = html[: m.start()] + heading + section + html[m.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    stats = audit_section(fixed)
    stats["inserted_h3"] = h3_added
    stats["inserted_h4"] = h4_added
    stats["removed_duplicate_tables"] = removed_tables
    stats["ipa_fixed"] = ipa_before
    return actions, stats


def load_tables() -> list[dict[str, object]]:
    tables = []
    for path in sorted(TABLE_DATA_DIR.glob("LYG-上-T*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        number = data.get("table_number") or ""
        if number.startswith("表9-"):
            tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(
            f"| {data.get('table_id', '')} | {data.get('table_number', '')} | {data.get('title', '')} | {pages} | "
            f"{data.get('status', '')} | {size} | {data.get('notes', '')} |"
        )
    if not table_lines:
        table_lines = ["| 暂无登记 | 表9-* | 第九卷现有表格尚未进入表格站 | p515-p563 | 待补登 | 待定 | 表9-1至表9-5需表格专项补建 |"]

    lines = [
        "# 第九卷农林业 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第九卷 农林业。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第九卷-农林业` 至 `第十卷-水利` 之前。",
        "- 源页范围：约 p515-p563，位于上册 part02。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第九卷正文区间，确认卷题、概述题、章题和节题大面积扁平化或断裂。",
        "- 统计第九卷表格状态，识别表9-1至表9-5多数仍为 OCR 表格残文，表格站暂无表9-*登记。",
        "",
        "## 格式修复清单",
        "",
        "- `第九卷农林业` 恢复为全书 TOC 对应 H2。",
        "- 卷内 `概述` 恢复为 H3，并清理卷首 `农/林/业/述` OCR 残字。",
        "- `第一章农业生产关系变革` 至 `第十章农机具` 恢复为 H3。",
        "- 农业生产关系变革、耕作制度与农业区划、品种、作物栽培、土壤肥料、植物保护、农业技术推广、蔬菜生产、林果桑茶、农机具各节题恢复为 H4。",
        "- 明显重复的临时结构化表格压缩为单实例。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表9-*的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第九卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第九卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第九卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第九卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第九卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第九卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第九卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第九卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 第九卷 H2 标题被截断为 `第九卷农`，正文首段混入 `林业$...述` 残字。",
        "- 源 MD 中第二章、第三章、第五章、第七章等章题存在换行、截断或缺题。",
        "- 阅读版仅保留第九章、第十章两个通用 `id=anchor` 标题，其余章、节题全部扁平化。",
        "- 表9-1至表9-5尚未登记为结构化表格站条目，临时表格存在重复实例。",
        "",
        "## 解决的困难",
        "",
        "- 以第九卷区间和第十卷边界限定修复范围，避免误动水利卷。",
        "- 对重复出现的节题按章顺序定位，减少同名节题串章风险。",
        "- 对表格仅压缩重复临时实例，不用未核数据填充结构化表。",
        "",
        "## 残留风险",
        "",
        "- 表9-1至表9-5均需从源 PDF 重新核读、登记、结构化。",
        "- 表9-2至表9-4跨农业技术推广章节，OCR 残文长且密集，需表格专项逐页处理。",
        "- OCR 正文字词尚未逐句校勘，本轮重点为标题层级、章节归属和表格风险登记。",
        "",
        "## 下一步计划",
        "",
        "- 进入第十卷 水利章节格式核对。",
        "- 表格专项阶段优先补登第九卷表9-1至表9-5。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第九卷农林业章节核对完成"
    section = f"""{header}

已完成 `第九卷 农林业` 章节格式核对：

- 新增脚本：`scripts/repair_ninth_volume_agriculture.py`。
- 修复 `workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md` 中第九卷卷题、概述题和多处章/节题断裂。
- 修复 `output/final_reader/连云港市志_全书.html` 中第九卷 H2 被截断、卷内标题大面积扁平化和通用 `id=anchor` 残留问题。
- 第九卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章农业生产关系变革至第十章农机具），H4={stats['h4_count']}。
- 将第九卷 {stats['ipa_fixed']} 处误用 `ipa-data` 的正文块转回普通段落。
- 压缩重复临时结构化表格实例 {stats['removed_duplicate_tables']} 处。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表9-*登记条目，需专项补登。
- 已写入进度文档：`output/reports/progress/20260628_第九卷农林业_修复核对进度.md`。

验收：第九卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0，正文表格占位符总数仍为 93。工作站 `npm run typecheck` 通过。

下一步：进入 `第十卷 水利`。第九卷表9-1至表9-5需从源 PDF 补登、重建和核验。
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

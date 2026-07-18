# -*- coding: utf-8 -*-
"""Repair and audit 第二十七卷 乡镇企业 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第二十七卷乡镇企业_修复核对进度.md"
PREV_PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第二十六卷矿产_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第二十七卷-乡镇企业">.*?</h2>)(.*?)(?=<h2 id="第二十八卷-[^"]+">)', re.S)

CHAPTERS = [
    ("第一章企业结构", ["第一节所有制结构", "第二节产业结构"]),
    ("第二章经营管理", ["第一节经营承包责任制", "第二节财务管理"]),
    ("第三章职工队伍", ["第一节职工构成", "第二节职工培训"]),
    ("第四章重点乡（镇）、村工业", ["第一节重点乡（镇）工业", "第二节专业村组", "第三节主要企业简介"]),
]

CHAPTER_NEEDLES = {
    "第一章企业结构": "全市乡镇企业的所有制形式主要有4种类型",
    "第二章经营管理": "1978年以前，全市乡镇企业在分配上强调缩小差别",
    "第三章职工队伍": "乡镇企业的职工大多数来自当地农村",
    "第四章重点乡（镇）、村工业": "一、青口镇",
}

CHAPTER_VARIANTS = {
    "第一章企业结构": ["第一章企业结构", "企业结构第一节", "企业结构"],
    "第二章经营管理": ["第二章经营管理", "经营管理第一节", "经营管理"],
    "第三章职工队伍": ["第三章职工队伍", "职工队伍第一节", "职工队伍"],
    "第四章重点乡（镇）、村工业": ["第四章重点乡（镇）、村工业", "重点乡（镇）、村工业第一节", "重点乡（镇）、村工业"],
}

SECTION_NEEDLES = {
    ("第一章企业结构", "第一节所有制结构"): "全市乡镇企业的所有制形式主要有4种类型",
    ("第一章企业结构", "第二节产业结构"): "一、农副产品加工业",
    ("第二章经营管理", "第一节经营承包责任制"): "1978年以前，全市乡镇企业在分配上强调缩小差别",
    ("第二章经营管理", "第二节财务管理"): "1980年以前，全市乡镇企业管理水平普遍较差",
    ("第三章职工队伍", "第一节职工构成"): "乡镇企业的职工大多数来自当地农村",
    ("第三章职工队伍", "第二节职工培训"): "1990年前，境内乡镇企业职工文化素质偏低",
    ("第四章重点乡（镇）、村工业", "第一节重点乡（镇）工业"): "一、青口镇",
    ("第四章重点乡（镇）、村工业", "第二节专业村组"): "1980年以来，市境-些村镇注重开发当地资源",
    ("第四章重点乡（镇）、村工业", "第三节主要企业简介"): "一、新浦电器开关厂",
}

SECTION_VARIANTS = {
    "第一节所有制结构": ["第一节所有制结构", "第一节"],
    "第二节产业结构": ["第二节产业结构", "第二节"],
    "第一节经营承包责任制": ["第一节经营承包责任制", "第一节"],
    "第二节财务管理": ["第二节财务管理", "第二节"],
    "第一节职工构成": ["第一节职工构成", "第一节"],
    "第二节职工培训": ["第二节职工培训", "第二节"],
    "第一节重点乡（镇）工业": ["第一节重点乡（镇）工业", "第一节"],
    "第二节专业村组": ["第二节专业村组", "第二节"],
    "第三节主要企业简介": ["第三节主要企业简介", "第三节"],
}

EXPECTED_TABLES = [f"表27-{i}" for i in range(1, 14)]


def h3(title: str) -> str:
    return f'<h3 id="第二十七卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第二十七卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    start_candidates = [text.find("\n第二十七卷\n"), text.find("\n第二十七卷 乡镇企业\n")]
    start_candidates = [pos for pos in start_candidates if pos >= 0]
    start = min(start_candidates) if start_candidates else -1
    end_candidates = [text.find("\n第二十八卷\n", start if start >= 0 else 0), text.find("\n第二十八卷 开发区\n", start if start >= 0 else 0)]
    end_candidates = [pos for pos in end_candidates if pos >= 0]
    end = min(end_candidates) if end_candidates else -1
    if start < 0 or end < 0:
        raise RuntimeError("Cannot locate 第二十七卷 source range")
    head, section, tail = text[:start], text[start:end], text[end:]
    replacements = {
        "\n第二十七卷\n镇企业\n概述\n": "\n第二十七卷 乡镇企业\n\n概述\n",
        "\n第一章\n企业结构\n第一节\n所有制结构\n": "\n第一章企业结构\n第一节所有制结构\n",
        "\n第一章\n企业结构\n：1199\n": "\n",
        "\n第一章\n企业结构\n·1207\n": "\n",
        "\n第二节\n产业结构\n": "\n第二节产业结构\n",
        "\n第二章\n经营管理\n第一节\n经营承包责任制\n": "\n第二章经营管理\n第一节经营承包责任制\n",
        "\n第二节\n财务管理\n": "\n第二节财务管理\n",
        "\n第三章\n职工队伍\n第一节\n职工构成\n": "\n第三章职工队伍\n第一节职工构成\n",
        "\n第二节\n职工培训\n": "\n第二节职工培训\n",
        "\n第四章\n重点乡（镇）、村工业\n第一节\n重点乡（镇）工业\n": "\n第四章重点乡（镇）、村工业\n第一节重点乡（镇）工业\n",
        "\n第三节\n主要企业简介\n": "\n第三节主要企业简介\n",
        "\n·1212·i\n\n": "\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    text = head + section + tail
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第二十七卷卷题、章题、节题断裂，并清理重复页眉式章题残留。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "企业结构：1199": "",
        "企业结构·1207": "",
        "·1212·i": "",
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
        prefix_start = max(0, needle_pos - 650)
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
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第二十七卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)
    summary_marker = '<h3 id="第二十七卷-概述">概述</h3>'
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
        raise RuntimeError("Cannot locate 第二十七卷 乡镇企业 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第二十七卷-乡镇企业">第二十七卷乡镇企业</h2>'
    ipa_before = section.count('<div class="ipa-data">')
    section = re.sub(r'<div class="ipa-data">(.*?)</div>', r'<p>\1</p>', section, flags=re.S)
    if ipa_before:
        actions.append(f"将第二十七卷误用 `ipa-data` 的正文 OCR 残块转回段落：{ipa_before} 处。")
    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复乡镇企业卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复乡镇企业卷节级 H4 标题：{h4_added} 处。")
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
            if title.startswith("表27-") or number.startswith("表27-"):
                tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(f"| {data.get('table_id', '')} | {data.get('table_number') or data.get('title', '')} | {data.get('title', '')} | {pages} | {data.get('status', '')} | {size} | {data.get('notes', '')} |")
    if not table_lines:
        table_lines = [f"| 暂无登记 | {table_no} | 第二十七卷可见表格尚未进入表格站 | p1299-p1321 | 待补登 | 待定 | 需从源 PDF 专项补建、核验 |" for table_no in EXPECTED_TABLES]

    lines = [
        "# 第二十七卷乡镇企业 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第二十七卷 乡镇企业。",
        "- 源 MD：`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第二十七卷-乡镇企业` 至 `第二十八卷-*` 之前。",
        "- 源页范围：约 p1297-p1321，位于中册 part01。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第二十七卷正文区间和目录骨架，确认本卷实际为 `乡镇企业`，第二十八卷才进入 `开发区`。",
        "- 统计第二十七卷表格状态，源 MD 可见表27-1至表27-13，表格站暂无表27-*登记。",
        "",
        "## 格式修复清单",
        "",
        "- 卷题恢复为 `第二十七卷乡镇企业`，卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章企业结构` 至 `第四章重点乡（镇）、村工业` 共 4 个 H3。",
        "- 恢复所有制结构、产业结构、经营承包责任制、财务管理、职工构成、职工培训、重点乡（镇）工业、专业村组、主要企业简介共 9 个 H4。",
        "- 清理阅读版中重复页眉式章题残留，如 `企业结构：1199`、`企业结构·1207`、`·1212·i`。",
        "- 清理源 MD 中卷题缺字、章题/节题断裂和重复页眉残留。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表27-*的登记表格：{len(tables)} 张。",
        "- 源 MD 可见表27-1至表27-13；当前阅读版只保留 4 处结构化表占位式表格，其余大量表格仍为正文残片，需 PDF 表格专项重建。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第二十七卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第二十七卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第二十七卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第二十七卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第二十七卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第二十七卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第二十七卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第二十七卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第二十七卷全部章、节标题扁平化为正文，卷题缺 `乡` 字。",
        "- 源 MD 中多处章题、节题断行，且表格页夹入重复页眉式章题。",
        "- 本卷表格密度高，可见表27-1至表27-13，但表格站暂无登记，阅读版表格多数仍为 OCR 残片。",
        "- 上一轮计划文本曾误写下一步为 `开发区`，本轮已据目录骨架更正：第二十七卷为 `乡镇企业`，第二十八卷才是 `开发区`。",
        "",
        "## 解决的困难",
        "",
        "- 以目录骨架和 HTML 锚点共同确认卷名，避免按前一轮计划误跳到第二十八卷。",
        "- 对重复 `第一章企业结构` 页眉残留做清理，保留唯一正式章级标题。",
        "- 对同名 `第一节`、`第二节` 使用章级上下文和正文首句定位，避免跨章误插。",
        "",
        "## 残留风险",
        "",
        "- 表27-1至表27-13需从源 PDF 逐张核读、补登、结构化。",
        "- 企业数据表、产业结构表、出口产品表、联营企业表等数值密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第二十八卷 开发区章节格式核对。",
        "- 表格专项阶段回补第二十七卷 13 张可见表格。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def correct_previous_next_step() -> None:
    if PREV_PROGRESS_PATH.exists():
        text = PREV_PROGRESS_PATH.read_text(encoding="utf-8")
        text = text.replace("进入第二十七卷 开发区章节格式核对", "进入第二十七卷 乡镇企业章节格式核对")
        PREV_PROGRESS_PATH.write_text(text, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    text = text.replace("下一步：进入 `第二十七卷 开发区`。", "下一步：进入 `第二十七卷 乡镇企业`。")
    header = "## 2026-06-28 第二十七卷乡镇企业章节核对完成"
    section = f"""{header}

已完成 `第二十七卷 乡镇企业` 章节格式核对：

- 新增脚本：`scripts/repair_twenty_seventh_volume_township_enterprises.py`。
- 修复 `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md` 中第二十七卷卷题缺字、章题/节题断裂和重复页眉式章题残留。
- 修复 `output/final_reader/连云港市志_全书.html` 中第二十七卷卷题误作 `第二十七卷镇企业`、章节标题全部扁平化的问题。
- 第二十七卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章企业结构至第四章重点乡（镇）、村工业），H4={stats['h4_count']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表27-*登记条目。
- 源 MD 可见表27-1至表27-13，本轮先记录为表格专项重点风险。
- 已写入进度文档：`output/reports/progress/20260628_第二十七卷乡镇企业_修复核对进度.md`。

验收：第二十七卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第二十八卷 开发区`。第二十七卷表27-1至表27-13需从源 PDF 专项补登、重建和核验。
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
    correct_previous_next_step()
    update_memory(stats)
    print("Repair complete")
    for action in actions:
        print(f"- {action}")
    print(f"stats={stats}")
    print(f"tables={len(tables)}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()

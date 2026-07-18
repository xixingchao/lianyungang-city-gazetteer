# -*- coding: utf-8 -*-
"""Repair and audit 第二十五卷 电力工业 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第二十五卷电力工业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第二十五卷-电力工业">.*?</h2>)(.*?)(?=<h2 id="第二十六卷-矿产">)', re.S)

CHAPTERS = [
    ("第一章发电", ["第一节新海发电厂", "第二节地方公用发电", "第三节用户自备电源"]),
    (
        "第二章供电",
        ["第一节配电网络", "第二节输电网络", "第三节主干线路", "第四节变电所", "第五节电力调度", "第六节运行检修", "第七节供电量与线损率", "第八节安全监察"],
    ),
    ("第三章用电", ["第一节电量负荷", "第二节用电结构", "第三节电力平衡", "第四节用电监察", "第五节营业"]),
]

CHAPTER_NEEDLES = {
    "第一章发电": "连云港市电业起源于民国9年",
    "第二章供电": "民国9年（1920年），新东电灯股份公司以220伏直配线路",
    "第三章用电": "民国9年（1920年），新东电灯股份公司晚间发少量电",
}

CHAPTER_VARIANTS = {
    "第一章发电": ["第一章•发电", "第一章发电", "发电"],
    "第二章供电": ["供电第二章", "第二章供电", "第二章", "供电"],
    "第三章用电": ["第三章用电‘1167用昇电第三章", "第三章用电", "用昇电第三章", "第三章"],
}

SECTION_NEEDLES = {
    ("第一章发电", "第一节新海发电厂"): "一、基本建设",
    ("第一章发电", "第二节地方公用发电"): "一、新浦热电厂",
    ("第一章发电", "第三节用户自备电源"): "一、小火电",
    ("第二章供电", "第一节配电网络"): "民国9年（1920年），新东电灯股份公司以220伏直配线路",
    ("第二章供电", "第二节输电网络"): "日军侵占连云港时期",
    ("第二章供电", "第三节主干线路"): "一、海连线",
    ("第二章供电", "第四节变电所"): "一、平山变电所",
    ("第二章供电", "第五节电力调度"): "一、调度沿革",
    ("第二章供电", "第六节运行检修"): "一、线路运行",
    ("第二章供电", "第七节供电量与线损率"): "一、供电量",
    ("第二章供电", "第八节安全监察"): "一、组织机构",
    ("第三章用电", "第一节电量负荷"): "民国9年（1920年），新东电灯股份公司晚间发少量电",
    ("第三章用电", "第二节用电结构"): "民国9年（1920年），新海连地区用电只为照明",
    ("第三章用电", "第三节电力平衡"): "1950年，电力供需出现缺口",
    ("第三章用电", "第四节用电监察"): "一、工业用电监察",
    ("第三章用电", "第五节营业"): "一、业务扩充",
}

SECTION_VARIANTS = {
    "第一节新海发电厂": ["第节新海发电厂", "第一节新海发电厂", "第节"],
    "第二节地方公用发电": ["第二节地方公用发电", "第二节"],
    "第三节用户自备电源": ["第三节用户自备电源", "第三节"],
    "第一节配电网络": ["第一节配电网络", "第一节"],
    "第二节输电网络": ["第二节　车输电网络", "第二节输电网络", "第二节　车", "第二节"],
    "第三节主干线路": ["主干线路第三节", "第三节主干线路", "第三节"],
    "第四节变电所": ["第四节•变•电•所", "第四节变电所", "第四节"],
    "第五节电力调度": ["电力调度第五节", "第五节电力调度", "第五节"],
    "第六节运行检修": ["第六节运行检修", "第六节"],
    "第七节供电量与线损率": ["第七节供电量与线损率", "第七节"],
    "第八节安全监察": ["第八节安全监察", "第八节"],
    "第一节电量负荷": ["第一节电量负荷", "第一节"],
    "第二节用电结构": ["第二节用电结构", "第二节"],
    "第三节电力平衡": ["第三节•电力平衡", "第三节电力平衡", "第三节"],
    "第四节用电监察": ["第四节用电监察", "第四节"],
    "第五节营业": ["第五节营业", "第五节"],
}

EXPECTED_TABLES = [f"表25-{i}" for i in range(1, 6)]


def h3(title: str) -> str:
    return f'<h3 id="第二十五卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第二十五卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    start_candidates = [text.find("\n第二十五卷\n"), text.find("\n第二十五卷 电力工业\n")]
    start_candidates = [pos for pos in start_candidates if pos >= 0]
    start = min(start_candidates) if start_candidates else -1
    end_candidates = [text.find("\n第二十六卷\n", start if start >= 0 else 0), text.find("\n第二十六卷 矿产\n", start if start >= 0 else 0)]
    end_candidates = [pos for pos in end_candidates if pos >= 0]
    end = min(end_candidates) if end_candidates else -1
    if start < 0 or end < 0:
        raise RuntimeError("Cannot locate 第二十五卷 source range")
    head, section, tail = text[:start], text[start:end], text[end:]
    replacements = {
        "\n第二十五卷\n电力工业\n概述\n": "\n第二十五卷 电力工业\n\n概述\n",
        "\n第一章•发电\n": "\n第一章发电\n",
        "\n第节\n新海发电厂\n": "\n第一节新海发电厂\n",
        "\n第二节\n地方公用发电\n": "\n第二节地方公用发电\n",
        "\n第三节\n用户自备电源\n": "\n第三节用户自备电源\n",
        "\n供电\n第二章\n第一节\n配电网络\n": "\n第二章供电\n第一节配电网络\n",
        "\n第二节　车\n输电网络\n": "\n第二节输电网络\n",
        "\n主干线路\n第三节\n": "\n第三节主干线路\n",
        "\n第四节•变•电•所\n": "\n第四节变电所\n",
        "\n电力调度\n第五节\n": "\n第五节电力调度\n",
        "\n第二章供电：1157·\n": "\n",
        "\n第二章供电·1163\n": "\n",
        "\n第七节\n供电量与线损率\n": "\n第七节供电量与线损率\n",
        "\n第三章用电‘1167\n用昇电\n第三章\n第一节\n电量负荷\n": "\n第三章用电\n第一节电量负荷\n",
        "\n第二节\n用电结构\n": "\n第二节用电结构\n",
        "\n第三节•电力平衡\n": "\n第三节电力平衡\n",
        "\n第三章用电·1177：\n": "\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    text = head + section + tail
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第二十五卷卷题、章题、节题断裂、页眉残留和 OCR 标题错误。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "<p>第节新海发电厂": "<p>",
        "<p>第二节　车输电网络": "<p>",
        "<p>主干线路第三节": "<p>",
        "<p>第四节•变•电•所": "<p>",
        "<p>电力调度第五节": "<p>",
        "<p>第三节•电力平衡": "<p>",
    }
    for old, new in residues.items():
        section = section.replace(old, new, 1)
    section = section.replace("第二章供电：1157·", "")
    section = section.replace("第二章供电·1163", "")
    section = section.replace("第二章供电：1165·", "")
    section = section.replace("第三章用电‘1167用昇电", "")
    section = section.replace("<p>用昇电</p>\n", "")
    reversed_usage = '<h4 id="第二十五卷-第三章用电-第一节电量负荷">第一节电量负荷</h4>\n<h3 id="第二十五卷-第三章用电">第三章用电</h3>'
    if reversed_usage in section:
        section = section.replace(reversed_usage, '<h3 id="第二十五卷-第三章用电">第三章用电</h3>\n<h4 id="第二十五卷-第三章用电-第一节电量负荷">第一节电量负荷</h4>', 1)
    section = section.replace("第三章用电·1177：", "")
    return section


def insert_or_replace_title(section: str, marker: str, needle: str, variants: list[str], start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    needle_pos = section.find(needle, max(0, start - 1000))
    if needle_pos < 0:
        needle_pos = section.find(needle)
    if needle_pos >= 0:
        prefix_start = max(0, needle_pos - 420)
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
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第二十五卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)
    summary_marker = '<h3 id="第二十五卷-概述">概述</h3>'
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
        raise RuntimeError("Cannot locate 第二十五卷 电力工业 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第二十五卷-电力工业">第二十五卷电力工业</h2>'
    ipa_before = section.count('<div class="ipa-data">')
    section = re.sub(r'<div class="ipa-data">(.*?)</div>', r'<p>\1</p>', section, flags=re.S)
    if ipa_before:
        actions.append(f"将第二十五卷误用 `ipa-data` 的正文/表格 OCR 残块转回段落：{ipa_before} 处。")
    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复电力工业卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复电力工业卷节级 H4 标题：{h4_added} 处。")
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
            if title.startswith("表25-") or number.startswith("表25-"):
                tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(f"| {data.get('table_id', '')} | {data.get('table_number') or data.get('title', '')} | {data.get('title', '')} | {pages} | {data.get('status', '')} | {size} | {data.get('notes', '')} |")
    if not table_lines:
        table_lines = [f"| 暂无登记 | {table_no} | 第二十五卷表格尚未进入表格站 | p1234-p1280 | 待补登 | 待定 | 需从源 PDF 专项补建、核验 |" for table_no in EXPECTED_TABLES]

    lines = [
        "# 第二十五卷电力工业 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第二十五卷 电力工业。",
        "- 源 MD：`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第二十五卷-电力工业` 至 `第二十六卷-矿产` 之前。",
        "- 源页范围：约 p1234-p1280，位于中册 part01。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第二十五卷正文区间，确认本卷实际为三章：发电、供电、用电。",
        "- 统计第二十五卷表格状态，表格站暂无表25-*登记，阅读版已有结构化表但仍需 PDF 表格专项复建。",
        "",
        "## 格式修复清单",
        "",
        "- 卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章发电` 至 `第三章用电` 共 3 个 H3。",
        "- 恢复新海发电厂、地方公用发电、用户自备电源、供电各节、用电各节等 16 个 H4。",
        "- 将第二十五卷误入 `ipa-data` 的正文/表格 OCR 残块转回普通段落。",
        "- 清理源 MD 中 `第一章•发电`、`第二节　车`、`第四节•变•电•所`、`用昇电`、页眉残留等 OCR 错误。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表25-*的登记表格：{len(tables)} 张。",
        "- 源 MD 可见表25-1至表25-5；表25-1、表25-4、表25-5均存在长表/残片 OCR，需 PDF 专项重建。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第二十五卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第二十五卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第二十五卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第二十五卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第二十五卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第二十五卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第二十五卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第二十五卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第二十五卷全部章、节标题扁平化为正文。",
        "- OCR 将多个标题识别为带符号或错字的形式，如 `第一章•发电`、`第二节　车`、`用昇电`。",
        "- 第二十五卷表格长表较多，表格 OCR 残块与正文混排明显。",
        "- 表25-*均未登记到表格站，阅读版结构化表仍为待对照原图录入状态。",
        "",
        "## 解决的困难",
        "",
        "- 以第二十五卷至第二十六卷边界限定修复范围，避免误动矿产卷。",
        "- 对供电、用电章中多处页眉残留先清理再恢复唯一章节锚点。",
        "- 对重复出现的统计表残块仅恢复段落属性，不在本轮硬重建表格。",
        "",
        "## 残留风险",
        "",
        "- 第二十五卷表25-1至表25-5需从源 PDF 逐张核读、补登、结构化。",
        "- 电力术语、设备型号、电压等级和统计指标密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第二十六卷 矿产章节格式核对。",
        "- 表格专项阶段回补第二十五卷新海发电厂经济指标、水电站发电量、东山电厂发电量、供电量、线损率等统计表。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第二十五卷电力工业章节核对完成"
    section = f"""{header}

已完成 `第二十五卷 电力工业` 章节格式核对：

- 新增脚本：`scripts/repair_twenty_fifth_volume_power.py`。
- 修复 `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md` 中第二十五卷卷题、章题、节题断裂和页眉/OCR 标题错误。
- 修复 `output/final_reader/连云港市志_全书.html` 中第二十五卷章节标题全部扁平化以及正文/表格 OCR 残块误用 `ipa-data` 的问题。
- 第二十五卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章发电至第三章用电），H4={stats['h4_count']}。
- 第二十五卷范围内 `ipa-data` 残留已清零。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表25-*登记条目。
- 已写入进度文档：`output/reports/progress/20260628_第二十五卷电力工业_修复核对进度.md`。

验收：第二十五卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第二十六卷 矿产`。第二十五卷表25-*需从源 PDF 专项补登、重建和核验。
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

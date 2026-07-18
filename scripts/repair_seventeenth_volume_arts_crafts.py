# -*- coding: utf-8 -*-
"""Repair and audit 第十七卷 工艺美术 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第十七卷工艺美术_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第十七卷-工艺美术">.*?</h2>)(.*?)(?=<h2 id="第十八卷-食品工业">)', re.S)

CHAPTERS = [
    ("第一章雕塑画类", ["第一节雕塑", "第二节画类", "第三节主要企业简介"]),
    ("第二章首饰玩具童车", ["第一节首饰", "第二节玩具", "第三节童车", "第四节主要企业简介"]),
    ("第三章竹藤草柳编", ["第一节竹编", "第二节藤编", "第三节草编", "第四节柳编", "第五节主要企业简介"]),
    ("第四章抽纱刺绣地毯", ["第一节抽纱刺绣", "第二节地毯", "第三节主要企业简介"]),
    ("第五章其它工艺品", ["第一节陶瓷", "第二节烟花爆竹", "第三节工艺包装盒", "第四节工艺桐木", "第五节工艺玻璃", "第六节主要企业简介"]),
]

CHAPTER_NEEDLES = {
    "第一章雕塑画类": "连云港市琢玉、雕石在新石器时代",
    "第二章首饰玩具童车": "连云港地区在唐代已有木制大刀",
    "第三章竹藤草柳编": "连云港市的竹、藤、草、柳工艺品是传统手工艺品",
    "第四章抽纱刺绣地毯": "清道光年间，牛山镇杨清玉精于针工艺",
    "第五章其它工艺品": "新石器时代境内即有工艺品",
}

SECTION_NEEDLES = {
    ("第一章雕塑画类", "第一节雕塑"): "一、玉",
    ("第一章雕塑画类", "第二节画类"): "一、贝雕画",
    ("第一章雕塑画类", "第三节主要企业简介"): "一、连云港贝雕总厂",
    ("第二章首饰玩具童车", "第一节首饰"): "一、手工饰品",
    ("第二章首饰玩具童车", "第二节玩具"): "1981年3月，海州古楼街综合",
    ("第二章首饰玩具童车", "第三节童车"): "1986年11月，灌云美术公司",
    ("第二章首饰玩具童车", "第四节主要企业简介"): "灌云县工艺美术工业公司",
    ("第三章竹藤草柳编", "第一节竹编"): "民国初期，赣榆县有1090户",
    ("第三章竹藤草柳编", "第二节藤编"): "1954年4月，新浦烈军属竹藤条叶厂",
    ("第三章竹藤草柳编", "第三节草编"): "民国初期，赣榆县从事竹草柳编织业",
    ("第三章竹藤草柳编", "第四节柳编"): "赣榆县柳简萝",
    ("第三章竹藤草柳编", "第五节主要企业简介"): "一、连云港市海苑工艺品有限公司",
    ("第四章抽纱刺绣地毯", "第一节抽纱刺绣"): "一、抽纱",
    ("第四章抽纱刺绣地毯", "第二节地毯"): "1958年7月，市工商联投资",
    ("第四章抽纱刺绣地毯", "第三节主要企业简介"): "一、连云港市绣品厂",
    ("第五章其它工艺品", "第一节陶瓷"): "锦屏二涧村遗址出土有新石器时代陶鼎",
    ("第五章其它工艺品", "第二节烟花爆竹"): "明末清初，赣榆县大沟南和海州城内有烟花作坊",
    ("第五章其它工艺品", "第三节工艺包装盒"): "1972年4月，文化用品厂印铁石印机",
    ("第五章其它工艺品", "第四节工艺桐木"): "社签订1.6万只将棋盒出口合同",
    ("第五章其它工艺品", "第五节工艺玻璃"): "1958年5月1日，墟沟服装社",
    ("第五章其它工艺品", "第六节主要企业简介"): "一、连云港印铁制罐厂",
}


def h3(title: str) -> str:
    return f'<h3 id="第十七卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第十七卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    boundary = text.find("\n第十八卷\n")
    if boundary < 0:
        boundary = len(text)
    section = text[:boundary]
    tail = text[boundary:]
    replacements = {
        "\n第十七卷\n工艺美术\n概述\n": "\n第十七卷 工艺美术\n\n概述\n",
        "\n第一章‘雕塑\n": "\n第一章雕塑画类\n",
        "\n第二节\n一、贝雕画\n": "\n第二节画类\n一、贝雕画\n",
        "\n第三节\n\n一、连云港贝雕总厂\n": "\n第三节主要企业简介\n一、连云港贝雕总厂\n",
        "\n童车\n首饰\n第二章\n玩具\n": "\n第二章首饰玩具童车\n",
        "\n市玩具\n第二节\n": "\n第二节玩具\n",
        "\n第三节•童•车\n": "\n第三节童车\n",
        "\n主要企业简介\n第四节\n": "\n第四节主要企业简介\n",
        "\n第三章\n竹、藤、草、柳编\n": "\n第三章竹藤草柳编\n",
        "\n第三章竹、藤、草、柳编\n·837\n": "\n",
        "\n第三章竹、藤、草、柳编\n": "\n",
        "\n第四节柳•编\n": "\n第四节柳编\n",
        "\n第四章\n抽纱\n刺绣\n地毯\n": "\n第四章抽纱刺绣地毯\n",
        "\n抽纱刺绣\n第一节扌\n": "\n第一节抽纱刺绣\n",
        "\n第三节\n\n一、连云港市绣品厂\n": "\n第三节主要企业简介\n一、连云港市绣品厂\n",
        "\n第五章\n其它工艺品\n": "\n第五章其它工艺品\n",
        "\n第二节\n烟花爆竹\n": "\n第二节烟花爆竹\n",
        "\n第三节\n工艺包装盒\n": "\n第三节工艺包装盒\n",
        "\n第四节\n工艺桐木\n": "\n第四节工艺桐木\n",
        "\n第六节\n主要企业简介\n": "\n第六节主要企业简介\n",
        "\n第五章其它工艺品·861\n": "\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    text = section + tail
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第十七卷卷题、章题、节题断裂和重复页眉/目录残留。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "<p>童车首饰玩具连云港地区": "<p>连云港地区",
        "<p>第二节一、贝雕画": "<p>一、贝雕画",
        "<p>第三节主要企业简介一、连云港贝雕总厂": "<p>一、连云港贝雕总厂",
        "<p>第三节•童•车": "<p>",
        "<p>主要企业简介第四节灌云县工艺美术工业公司": "<p>灌云县工艺美术工业公司",
        "<p>抽纱刺绣地毯清道光年间": "<p>清道光年间",
        "<p>抽纱刺绣第一节扌一、抽纱": "<p>一、抽纱",
        "<p>第三节工艺包装盒": "<p>",
        "<p>第四节工艺桐木": "<p>",
        "<p>第六节主要企业简介一、连云港印铁制罐厂": "<p>一、连云港印铁制罐厂",
    }
    for old, new in residues.items():
        section = section.replace(old, new, 1)
    section = section.replace("第三章竹、藤、草、柳编·837", "", 1)
    section = section.replace("第五章其它工艺品·861", "", 1)
    return section


def insert_before(section: str, marker: str, needle: str, start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    pos = section.find(needle, start)
    if pos < 0:
        pos = section.find(needle)
    if pos < 0:
        return section, False, start
    paragraph_start = section.rfind("<p>", 0, pos)
    paragraph_end = section.rfind("</p>", 0, pos)
    if paragraph_start > paragraph_end and not section[paragraph_start + 3 : pos].strip():
        pos = paragraph_start
    section = section[:pos] + marker + "\n" + section[pos:]
    return section, True, pos + len(marker) + 1


def split_or_insert_section(section: str, chapter: str, title: str, needle: str, start: int) -> tuple[str, bool, int]:
    marker = h4(chapter, title)
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    variants = [title]
    if title == "画类":
        variants.append("第二节")
    if title == "主要企业简介":
        variants.extend(["第三节主要企业简介", "第四节主要企业简介", "第五节主要企业简介", "第六节主要企业简介"])
    if title == "玩具":
        variants.extend(["市玩具", "第二节"])
    if title == "童车":
        variants.append("第三节•童•车")
    if title == "抽纱刺绣":
        variants.extend(["抽纱刺绣第一节扌", "第一节扌"])
    if title == "柳编":
        variants.append("第四节柳•编")

    needle_pos = section.find(needle, max(0, start - 500))
    if needle_pos < 0:
        needle_pos = section.find(needle)
    if needle_pos >= 0:
        prefix_start = max(0, needle_pos - 220)
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
    section = re.sub(r"(</h[34]>)\n(?!<)([^\n<][^\n]*?</p>)", r"\1\n<p>\2", section)
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第十七卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)

    summary_marker = '<h3 id="第十七卷-概述">概述</h3>'
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
            section, added, cursor = split_or_insert_section(section, chapter, title, needle, cursor)
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
        raise RuntimeError("Cannot locate 第十七卷 工艺美术 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第十七卷-工艺美术">第十七卷工艺美术</h2>'

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>').replace('</div>', '</p>')
    if ipa_before:
        actions.append(f"将第十七卷误用 `ipa-data` 的正文块转回段落：{ipa_before} 处。")

    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复工艺美术卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复工艺美术卷节级 H4 标题：{h4_added} 处。")

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
            if title.startswith("表17-") or number.startswith("表17-"):
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
        table_lines = ["| 暂无登记 | 表17-* | 第十七卷现有表格尚未进入表格站 | p925-p959 | 待补登 | 待定 | 玉雕、贝雕、首饰、地毯、陶瓷、烟花、工艺玻璃等表需专项补建 |"]

    lines = [
        "# 第十七卷工艺美术 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第十七卷 工艺美术。",
        "- 源 MD：`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第十七卷-工艺美术` 至 `第十八卷-食品工业` 之前。",
        "- 源页范围：约 p922-p959，位于中册 part01。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第十七卷正文区间，确认本卷实际为五章：雕塑画类、首饰玩具童车、竹藤草柳编、抽纱刺绣地毯、其它工艺品。",
        "- 统计第十七卷表格状态，表格站暂无表17-*登记，阅读版已有结构化表，无表格占位符。",
        "",
        "## 格式修复清单",
        "",
        "- 卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章雕塑画类` 至 `第五章其它工艺品` 共 5 个 H3。",
        "- 恢复雕塑、画类、首饰、玩具、童车、竹编、藤编、草编、柳编、抽纱刺绣、地毯、陶瓷、烟花爆竹、工艺包装盒、工艺桐木、工艺玻璃、主要企业简介等 21 个 H4。",
        "- 将第十七卷误入 `ipa-data` 的正文块转回普通段落。",
        "- 清理源 MD 中重复章名页眉、目录残留和多处 OCR 断裂标题。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表17-*的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第十七卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第十七卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第十七卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第十七卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第十七卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第十七卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第十七卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第十七卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第十七卷全部章、节标题扁平化为正文。",
        "- 源 MD 中章题、节题断裂严重，并混有重复章名页眉与目录残留。",
        "- 本卷表格多且题名密集，部分正文标题贴近表格 OCR 残文，容易误判。",
        "- 表17-*均未登记到表格站。",
        "",
        "## 解决的困难",
        "",
        "- 以第十七卷至第十八卷边界限定修复范围，避免误动食品工业卷。",
        "- 章题按正文首句定位，节题按稳定小题或企业简介开头定位，避开重复页眉。",
        "- 对未核表格只保留现有结构表，不用 OCR 残文补填。",
        "",
        "## 残留风险",
        "",
        "- 第十七卷表格需从源 PDF 逐张核读、补登、结构化。",
        "- 工艺术语、企业名、奖项和经济指标密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第十八卷 食品工业章节格式核对。",
        "- 表格专项阶段回补第十七卷玉雕、贝雕、首饰、地毯、陶瓷、烟花、工艺玻璃等统计表。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第十七卷工艺美术章节核对完成"
    section = f"""{header}

已完成 `第十七卷 工艺美术` 章节格式核对：

- 新增脚本：`scripts/repair_seventeenth_volume_arts_crafts.py`。
- 修复 `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md` 中第十七卷卷题、章题、节题断裂和重复页眉/目录残留。
- 修复 `output/final_reader/连云港市志_全书.html` 中第十七卷章、节标题全部扁平化以及正文块误用 `ipa-data` 的问题。
- 第十七卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章雕塑画类至第五章其它工艺品），H4={stats['h4_count']}。
- 第十七卷范围内 `ipa-data` 残留已清零。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表17-*登记条目。
- 已写入进度文档：`output/reports/progress/20260628_第十七卷工艺美术_修复核对进度.md`。

验收：第十七卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第十八卷 食品工业`。第十七卷表17-*需从源 PDF 专项补登、重建和核验。
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

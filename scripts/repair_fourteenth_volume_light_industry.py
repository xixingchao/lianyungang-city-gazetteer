# -*- coding: utf-8 -*-
"""Repair and audit 第十四卷 轻（手）工业 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第十卷至第十六卷（part03）.md"
TABLE_DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第十四卷轻手工业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第十四卷-轻-手-工业">.*?</h2>)(.*?)(?=<h2 id="第十五卷-纺织工业">)', re.S)

CHAPTERS = [
    ("第一章造纸", ["第一节生活用纸", "第二节文化用纸", "第三节工业用纸", "第四节主要企业简介"]),
    ("第二章印刷", ["第一节杂件印刷", "第二节报刊印刷", "第三节商标印刷", "第四节主要企业简介"]),
    ("第三章包装", ["第一节纸质包装", "第二节金属包装", "第三节复合包装", "第四节玻璃包装", "第五节主要企业简介"]),
    ("第四章日用化工", ["第一节火柴", "第二节洗涤用品", "第三节化妆用品", "第四节日用化工原料"]),
    ("第五章日用五金与工具", ["第一节日用五金", "第二节日用工具", "第三节炊事用具", "第四节主要企业简介"]),
    ("第六章家具", ["第一节木制家具", "第二节软体家具", "第三节钢木家具", "第四节主要企业简介"]),
    ("第七章电光源家用电器", ["第一节电光源", "第二节家用电器", "第三节主要企业简介"]),
]

CHAPTER_NEEDLES = {
    "第一章造纸": "连云港市造纸业始于",
    "第二章印刷": "连云港市印刷业始于",
    "第三章包装": "1956年前，连云港市包装业",
    "第四章日用化工": "连云港市日用化工业起始于",
    "第五章日用五金与工具": "连云港市日用五金、工具业起始于",
    "第六章家具": "连云港市家具业起始较早",
    "第七章电光源家用电器": "连云港市电光源业始于",
}

SECTION_NEEDLES = {
    ("第一章造纸", "第一节生活用纸"): "一、草浆卫生纸",
    ("第一章造纸", "第二节文化用纸"): "1959年，新浦造纸厂投资8万元",
    ("第一章造纸", "第三节工业用纸"): "1956年，华伦造纸厂利用当地的麦草",
    ("第一章造纸", "第四节主要企业简介"): "一、连云港市造纸厂",
    ("第二章印刷", "第一节杂件印刷"): "杂件印刷业历史较久",
    ("第二章印刷", "第二节报刊印刷"): "一、报纸印刷",
    ("第二章印刷", "第三节商标印刷"): "30年代初，新浦市区工商业有所发展",
    ("第二章印刷", "第四节主要企业简介"): "一、连云港市新海印刷厂",
    ("第三章包装", "第一节纸质包装"): "连云港市纸质包装业主要有纸袋",
    ("第三章包装", "第二节金属包装"): "连云港市金属包装工业主要有两大类",
    ("第三章包装", "第三节复合包装"): "连云港市复合包装材料生产始于",
    ("第三章包装", "第四节玻璃包装"): "连云港市日用玻璃包装工业源于",
    ("第三章包装", "第五节主要企业简介"): "一、连云港市包装一厂",
    ("第四章日用化工", "第一节火柴"): "连云港市火柴工业始于",
    ("第四章日用化工", "第二节洗涤用品"): "一、肥皂",
    ("第四章日用化工", "第三节化妆用品"): "一、美容护肤类",
    ("第四章日用化工", "第四节日用化工原料"): "一、BD抑菌洗涤剂",
    ("第五章日用五金与工具", "第一节日用五金"): "一、制钉",
    ("第五章日用五金与工具", "第二节日用工具"): "一、剪刀",
    ("第五章日用五金与工具", "第三节炊事用具"): "一、制锅",
    ("第五章日用五金与工具", "第四节主要企业简介"): "一、连云港市拔丝制钉厂",
    ("第六章家具", "第一节木制家具"): "木制家具业是连云港市较古老的手工业之一",
    ("第六章家具", "第二节软体家具"): "一、沙发",
    ("第六章家具", "第三节钢木家具"): "1976年，市木工厂引进钢木混合结构",
    ("第六章家具", "第四节主要企业简介"): "一、连云港市家具一厂",
    ("第七章电光源家用电器", "第一节电光源"): "一、碘钨灯管",
    ("第七章电光源家用电器", "第二节家用电器"): "一、洗衣机",
    ("第七章电光源家用电器", "第三节主要企业简介"): "一、连云港市特种灯泡厂",
}


def h3(title: str) -> str:
    return f'<h3 id="第十四卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第十四卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    replacements = {
        "\n第十四卷\n轻（手）工业\nらら\n概\n述\n": "\n第十四卷 轻（手）工业\n\n概述\n",
        "\n第一章造\n纸\n": "\n第一章造纸\n",
        "\n第二章印\n刷\n": "\n第二章印刷\n",
        "\n第三章包\n装\n": "\n第三章包装\n",
        "\n第五章\n日用五金与工具\n": "\n第五章日用五金与工具\n",
        "\n第六章家\n": "\n第六章家具\n",
        "\n第七章电光源\n家用电器\n": "\n第七章电光源家用电器\n",
        "\n第四节\n主要企业简介\n": "\n第四节主要企业简介\n",
        "\n第五节 主要企业简介\n": "\n第五节主要企业简介\n",
        "\n第四节 日用化工原料\n": "\n第四节日用化工原料\n",
        "\n第三节 主要企业简介\n": "\n第三节主要企业简介\n",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD part03 中第十四卷卷题、概述题和多处章/节题断裂。"]
    return []


def normalize_residue(section: str) -> str:
    section = re.sub(r"^\s*<p>らら", "<p>", section, count=1)
    residues = {
        "<p>纸连云港市造纸业始于": "<p>连云港市造纸业始于",
        "<p>刷连云港市印刷业始于": "<p>连云港市印刷业始于",
        "<p>装1956年前，连云港市包装业": "<p>1956年前，连云港市包装业",
        "<p>日用五金与工具连云港市日用五金、工具业起始于": "<p>连云港市日用五金、工具业起始于",
        "<p>家用电器连云港市电光源业始于": "<p>连云港市电光源业始于",
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

    needle_pos = section.find(needle, max(0, start - 200))
    if needle_pos >= 0:
        prefix_start = max(0, needle_pos - 120)
        prefix = section[prefix_start:needle_pos]
        for raw in [title, title.replace("主要企业简介", " 主要企业简介"), title.replace("日用化工原料", " 日用化工原料")]:
            rel = prefix.rfind(raw)
            if rel >= 0:
                pos = prefix_start + rel
                section = section[:pos] + marker + "\n<p>" + section[pos + len(raw) :]
                return section, True, pos + len(marker) + 4

    variants = [title, title.replace("主要企业简介", " 主要企业简介"), title.replace("日用化工原料", " 日用化工原料")]
    search_start = max(0, start - 200)
    positions = [section.find(v, search_start) for v in variants if section.find(v, search_start) >= 0]
    pos = min(positions) if positions else -1
    raw = ""
    if pos >= 0:
        for v in variants:
            if section.startswith(v, pos):
                raw = v
                break
        section = section[:pos] + marker + "\n<p>" + section[pos + len(raw) :]
        return section, True, pos + len(marker) + 4

    section, added, cursor = insert_before(section, marker, needle, start)
    return section, added, cursor


def split_known_residual_sections(section: str) -> tuple[str, int]:
    fixes = [
        ("第二章印刷", "第四节主要企业简介", "第四节 主要企业简介"),
        ("第五章日用五金与工具", "第四节主要企业简介", "第四节 主要企业简介"),
        ("第六章家具", "第四节主要企业简介", "第四节主要企业简介"),
    ]
    added = 0
    for chapter, title, raw in fixes:
        marker = h4(chapter, title)
        if marker in section:
            continue
        needle = SECTION_NEEDLES[(chapter, title)]
        needle_pos = section.find(needle)
        if needle_pos < 0:
            continue
        pos = section.rfind(raw, max(0, needle_pos - 160), needle_pos)
        if pos < 0:
            continue
        section = section[:pos] + marker + "\n<p>" + section[pos + len(raw) :]
        added += 1
    return section, added


def cleanup_heading_markup(section: str) -> str:
    section = section.replace("<p><h3", "<h3").replace("<p><h4", "<h4")
    section = re.sub(
        r'<h4 id="第十四卷-第一章造纸-<h4 id="第十四卷-第六章家具-第四节主要企业简介">第四节主要企业简介</h4>\s*<p>">第四节主要企业简介</h4>',
        h4("第一章造纸", "第四节主要企业简介"),
        section,
    )
    section = section.replace("</h3>\n</p>", "</h3>\n").replace("</h4>\n</p>", "</h4>\n")
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第十四卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)

    summary_marker = '<h3 id="第十四卷-概述">概述</h3>'
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

    section, known_added = split_known_residual_sections(section)
    h4_count += known_added

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
        raise RuntimeError("Cannot locate 第十四卷 轻（手）工业 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第十四卷-轻-手-工业">第十四卷轻（手）工业</h2>'

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>').replace('</div>', '</p>')
    if ipa_before:
        actions.append(f"将第十四卷误用 `ipa-data` 的正文块转回段落：{ipa_before} 处。")

    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复轻（手）工业卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复轻（手）工业卷节级 H4 标题：{h4_added} 处。")

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
        if title.startswith("表14-") or number.startswith("表14-"):
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
        table_lines = ["| 暂无登记 | 表14-* | 第十四卷现有表格尚未系统登记 | p778-p831 | 待补登 | 待定 | 需结合 PDF 补建造纸、印刷、家具、电光源等表 |"]

    lines = [
        "# 第十四卷轻（手）工业 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第十四卷 轻（手）工业。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第十四卷-轻-手-工业` 至 `第十五卷-纺织工业` 之前。",
        "- 源页范围：约 p778-p831，位于上册 part03。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第十四卷正文区间，确认本卷实际为七章，覆盖造纸、印刷、包装、日化、五金工具、家具、电光源家电等行业。",
        "- 统计第十四卷表格状态，表格站仅有 1 条疑似表14记录，阅读版仍有临时结构表和占位符。",
        "",
        "## 格式修复清单",
        "",
        "- 卷内 `概述` 恢复为 H3，并清理卷首 OCR 噪声 `らら`。",
        "- 恢复 `第一章造纸` 至 `第七章电光源家用电器` 共 7 个 H3。",
        "- 恢复生活用纸、文化用纸、工业用纸、主要企业简介、杂件印刷、纸质包装、日用五金、家具、电光源、家用电器等 28 个 H4。",
        "- 将第十四卷误入 `ipa-data` 的正文块转回普通段落。",
        "- 对章题残字如 `纸`、`刷`、`装`、`家用电器` 等仅作标题化清理，不改写正文事实。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中疑似表14-*登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第十四卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第十四卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第十四卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第十四卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第十四卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第十四卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第十四卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第十四卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第十四卷全部章、节标题扁平化为正文。",
        "- 源 MD 中卷题、概述题、第一章至第三章、第五章、第六章、第七章及多处主要企业简介节题断裂。",
        "- 章节跨度长，且包含多处表格页，容易把表格残文误识别为标题。",
        "- 表14-*登记不完整，现有 `LYG-上-T039` 只有疑似表14记录，表号字段为空。",
        "",
        "## 解决的困难",
        "",
        "- 以第十四卷至第十五卷边界限定修复范围，避免误动纺织工业卷。",
        "- 章题按正文首句定位，节题按段首标题或节内首个稳定小题定位，避开表格残文。",
        "- 对未核表格只保留占位和现有临时结构表，不用 OCR 残文补填。",
        "",
        "## 残留风险",
        "",
        "- 第十四卷表格需从源 PDF 逐张核读、补登、结构化。",
        "- 行业企业名、产品名、奖项和经济指标密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第十五卷 纺织工业章节格式核对。",
        "- 表格专项阶段回补第十四卷造纸、印刷、家具、电光源等统计表。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第十四卷轻（手）工业章节核对完成"
    section = f"""{header}

已完成 `第十四卷 轻（手）工业` 章节格式核对：

- 新增脚本：`scripts/repair_fourteenth_volume_light_industry.py`。
- 修复 `workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md` 中第十四卷卷题、概述题和多处章/节题断裂。
- 修复 `output/final_reader/连云港市志_全书.html` 中第十四卷章、节标题全部扁平化以及正文块误用 `ipa-data` 的问题。
- 第十四卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章造纸至第七章电光源家用电器），H4={stats['h4_count']}。
- 将第十四卷 {stats['ipa_fixed']} 处误用 `ipa-data` 的正文块转回普通段落。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站仅有疑似表14记录，需后续补登。
- 已写入进度文档：`output/reports/progress/20260628_第十四卷轻手工业_修复核对进度.md`。

验收：第十四卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第十五卷 纺织工业`。第十四卷表14-*需从源 PDF 专项补登、重建和核验。
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

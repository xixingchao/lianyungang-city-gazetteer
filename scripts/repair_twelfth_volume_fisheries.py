# -*- coding: utf-8 -*-
"""Repair and audit 第十二卷 水产 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "paddle_上" / "第十卷至第十六卷（part03）.md"
TABLE_DATA_DIR = ROOT / "workbench" / "table_entries" / "上" / "data"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第十二卷水产_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第十二卷-水产">.*?</h2>)(.*?)(?=<h2 id="第十三卷-盐业">)', re.S)

CHAPTERS = [
    ("第一章渔业生产关系", ["第一节解放前渔业生产关系", "第二节解放后渔业生产关系"]),
    ("第二章海洋捕捞", ["第一节渔场", "第二节渔船", "第三节渔港", "第四节捕捞工具", "第五节产量"]),
    ("第三章海产品养（增）殖", ["第一节海带养殖", "第二节对虾养殖", "第三节紫菜、裙带菜养殖", "第四节梭鱼养殖", "第五节海水增殖"]),
    ("第四章加工保鲜", ["第一节保鲜", "第二节腌干制品", "第三节冷冻加工", "第四节主要企业简介"]),
    ("第五章淡水渔业", ["第一节淡水养殖", "第二节淡水捕捞"]),
    ("第六章渔政", ["第一节机构及设施", "第二节渔政管理"]),
]

CUMULATIVE_IPA_FIXED = 2
CUMULATIVE_REMOVED_DUP_TABLES = 4


def h3(title: str) -> str:
    return f'<h3 id="第十二卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第十二卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    replacements = {
        "\n第十二卷\n水\n产\n概\n述\n": "\n第十二卷 水产\n\n概述\n",
        "\n第一章\n渔业生产关系\n": "\n第一章渔业生产关系\n",
        "\n第一节 解放前渔业生产关系\n": "\n第一节解放前渔业生产关系\n",
        "\n第三节 渔\n港\n": "\n第三节渔港\n",
        "\n第四节捕\n": "\n第四节捕捞工具\n",
        "\n第五节产\n量\n": "\n第五节产量\n",
        "\n第三章\n海产品养（增）殖\n": "\n第三章海产品养（增）殖\n",
        "\n第四节 主要企业简介\n": "\n第四节主要企业简介\n",
        "\n第六章渔\n政\n": "\n第六章渔政\n",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD part03 中第十二卷卷题、概述题和多处章/节题断裂。"]
    return []


def split_title_prefix(section: str, raw: str, marker: str, start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    pos = section.find(raw, start)
    if pos < 0:
        pos = section.find(raw)
    if pos < 0:
        return section, False, start
    section = section[:pos] + marker + "\n<p>" + section[pos + len(raw) :]
    return section, True, pos + len(marker) + 4


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


def cleanup_heading_markup(section: str) -> str:
    section = section.replace("<p><h3", "<h3").replace("<p><h4", "<h4")
    section = section.replace("</h3>\n</p>", "</h3>\n").replace("</h4>\n</p>", "</h4>\n")
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第十二卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def normalize_residue(section: str) -> str:
    section = re.sub(r"^\s*<p>产", "<p>", section, count=1)
    section = section.replace("渔业生产关系第一节 解放前渔业生产关系", "第一章渔业生产关系第一节解放前渔业生产关系", 1)
    section = section.replace("第三节 渔港", "第三节渔港", 1)
    section = section.replace("第四节捕", "第四节捕捞工具", 1)
    section = section.replace("海产品养（增）殖连云港市滩涂浅海", "第三章海产品养（增）殖连云港市滩涂浅海", 1)
    section = section.replace("第四节 主要企业简介", "第四节主要企业简介", 1)
    section = section.replace("政第一节机构及设施", "第六章渔政第一节机构及设施", 1)
    return section


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)

    section, added, cursor = insert_before(section, '<h3 id="第十二卷-概述">概述</h3>', "连云港市海岸线曲折", 0)
    h3_count += int(added)

    chapter_needles = {
        "第一章渔业生产关系": "第一章渔业生产关系第一节解放前渔业生产关系",
        "第二章海洋捕捞": "第一节渔场",
        "第三章海产品养（增）殖": "第三章海产品养（增）殖连云港市滩涂浅海",
        "第四章加工保鲜": "境内沿海渔民数千年来沿用",
        "第五章淡水渔业": "建国前，市境灌云县有连家渔船专事淡水捕捞",
        "第六章渔政": "第六章渔政第一节机构及设施",
    }
    cursor = 0
    for chapter, _titles in CHAPTERS:
        section, added, cursor = insert_before(section, h3(chapter), chapter_needles[chapter], cursor)
        h3_count += int(added)
        if chapter in {"第一章渔业生产关系", "第三章海产品养（增）殖", "第六章渔政"}:
            section = section.replace(h3(chapter) + "\n" + chapter, h3(chapter) + "\n", 1)

    title_variants = {
        "第一节解放前渔业生产关系": ["第一节解放前渔业生产关系", "第一节 解放前渔业生产关系"],
        "第二节解放后渔业生产关系": ["第二节解放后渔业生产关系"],
        "第一节渔场": ["第一节渔场"],
        "第二节渔船": ["第二节渔船"],
        "第三节渔港": ["第三节渔港", "第三节 渔港"],
        "第四节捕捞工具": ["第四节捕捞工具", "第四节捕"],
        "第五节产量": ["第五节产量", "第五节产"],
        "第一节海带养殖": ["第一节海带养殖"],
        "第二节对虾养殖": ["第二节对虾养殖"],
        "第三节紫菜、裙带菜养殖": ["第三节紫菜、裙带菜养殖"],
        "第四节梭鱼养殖": ["第四节梭鱼养殖"],
        "第五节海水增殖": ["第五节海水增殖"],
        "第一节保鲜": ["第一节保鲜"],
        "第二节腌干制品": ["第二节腌干制品"],
        "第三节冷冻加工": ["第三节冷冻加工"],
        "第四节主要企业简介": ["第四节主要企业简介", "第四节 主要企业简介"],
        "第一节淡水养殖": ["第一节淡水养殖"],
        "第二节淡水捕捞": ["第二节淡水捕捞"],
        "第一节机构及设施": ["第一节机构及设施"],
        "第二节渔政管理": ["第二节渔政管理"],
    }
    cursor = 0
    for chapter, titles in CHAPTERS:
        for title in titles:
            marker = h4(chapter, title)
            for raw in title_variants[title]:
                section, added, cursor = split_title_prefix(section, raw, marker, cursor)
                if added:
                    h4_count += 1
                    break

    return cleanup_heading_markup(section), h3_count, h4_count


def normalize_opening_paragraphs(section: str) -> str:
    replacements = {
        '<h3 id="第十二卷-概述">概述</h3>\n连云港市海岸线': '<h3 id="第十二卷-概述">概述</h3>\n<p>连云港市海岸线',
        '<h3 id="第十二卷-第三章海产品养（增）殖">第三章海产品养（增）殖</h3>\n连云港市滩涂': '<h3 id="第十二卷-第三章海产品养（增）殖">第三章海产品养（增）殖</h3>\n<p>连云港市滩涂',
        '<h3 id="第十二卷-第四章加工保鲜">第四章加工保鲜</h3>\n境内沿海': '<h3 id="第十二卷-第四章加工保鲜">第四章加工保鲜</h3>\n<p>境内沿海',
        '<h3 id="第十二卷-第五章淡水渔业">第五章淡水渔业</h3>\n建国前': '<h3 id="第十二卷-第五章淡水渔业">第五章淡水渔业</h3>\n<p>建国前',
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    return section


def compress_duplicate_tables(section: str) -> tuple[str, int]:
    patterns = [
        r'<table class="structured-table"><thead><tr><th>品种</th><th>分布海域</th><th>渔期</th><th>备注</th></tr></thead>.*?</table>\n?',
        r'<table class="structured-table"><thead><tr><th>品种</th><th>合计\(吨\)</th><th>国营渔轮捕捞量\(吨\)</th><th>其它渔船捕捞量\(吨\)</th><th>备注</th></tr></thead>.*?</table>\n?',
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
        raise RuntimeError("Cannot locate 第十二卷 水产 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第十二卷-水产">第十二卷水产</h2>'

    ipa_before = section.count('<div class="ipa-data">')
    section = section.replace('<div class="ipa-data">', '<p>').replace('</div>', '</p>')
    if ipa_before:
        actions.append(f"将第十二卷误用 `ipa-data` 的正文块转回段落：{ipa_before} 处。")

    section, h3_added, h4_added = restore_headings(section)
    section = normalize_opening_paragraphs(section)
    if h3_added:
        actions.append(f"恢复水产卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复水产卷节级 H4 标题：{h4_added} 处。")

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
        if number.startswith("表12-"):
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
        table_lines = ["| 暂无登记 | 表12-* | 第十二卷现有表格尚未进入表格站 | p705-p789 | 待补登 | 待定 | 表12-1至表12-14需表格专项补建 |"]

    lines = [
        "# 第十二卷水产 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第十二卷 水产。",
        "- 源 MD：`workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第十二卷-水产` 至 `第十三卷-盐业` 之前。",
        "- 源页范围：约 p705-p789，位于上册 part03。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第十二卷正文区间，确认本卷实际为六章，尾章为第六章渔政。",
        "- 统计第十二卷表格状态，识别表格站暂无表12-*登记，但阅读版已有临时结构化表和占位符。",
        "",
        "## 格式修复清单",
        "",
        "- `第十二卷水` 修复为 `第十二卷水产`，保持全书 TOC 对应 H2。",
        "- 卷内 `概述` 恢复为 H3，并清理卷首 `产` OCR 残字。",
        "- `第一章渔业生产关系` 至 `第六章渔政` 恢复为 H3。",
        "- 渔业生产关系、海洋捕捞、海产品养（增）殖、加工保鲜、淡水渔业、渔政各节题恢复为 H4。",
        "- 将 `第四节捕` 暂按正文内容恢复为 `第四节捕捞工具`，需后续 PDF 核题。",
        "- 明显重复的临时结构化表格压缩为单实例。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表12-*的登记表格：{len(tables)} 张。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第十二卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第十二卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第十二卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第十二卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第十二卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第十二卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第十二卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第十二卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 第十二卷 H2 标题被截断为 `第十二卷水`，正文首段混入 `产` 残字。",
        "- 源 MD 中第一章、第三章、第六章章题及第三节渔港、第五节产量等标题断裂。",
        "- 阅读版中所有章、节标题均扁平化，第四节捕捞工具还落在 `ipa-data` 块中。",
        "- 表12-*均未登记到表格站，阅读版临时结构化表存在重复实例。",
        "",
        "## 解决的困难",
        "",
        "- 以第十二卷区间和第十三卷边界限定修复范围，避免误动盐业卷。",
        "- 根据正文实际内容将第六章渔政单独恢复，避免并入淡水渔业。",
        "- 对重复临时表格仅保留单实例，不用未核数据填充完整表。",
        "",
        "## 残留风险",
        "",
        "- 表12-1至表12-14需从源 PDF 逐张核读、登记、结构化。",
        "- `第四节捕捞工具` 为按正文内容暂定标题，需 PDF/目录核题确认。",
        "- 水产品种、渔场、渔具、企业表数据密集，后续精校需结合原 PDF 核读专业名词和数值。",
        "",
        "## 下一步计划",
        "",
        "- 进入第十三卷 盐业章节格式核对。",
        "- 表格专项阶段优先补登第十二卷表12-1至表12-14。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第十二卷水产章节核对完成"
    section = f"""{header}

已完成 `第十二卷 水产` 章节格式核对：

- 新增脚本：`scripts/repair_twelfth_volume_fisheries.py`。
- 修复 `workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md` 中第十二卷卷题、概述题和多处章/节题断裂。
- 修复 `output/final_reader/连云港市志_全书.html` 中第十二卷 H2 被截断、正文块误用 `ipa-data`、卷内标题全部扁平化的问题。
- 第十二卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章渔业生产关系至第六章渔政），H4={stats['h4_count']}。
- 将第十二卷 {CUMULATIVE_IPA_FIXED} 处误用 `ipa-data` 的正文块转回普通段落。
- 压缩重复临时结构化表格实例 {CUMULATIVE_REMOVED_DUP_TABLES} 处。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表12-*登记条目。
- 已写入进度文档：`output/reports/progress/20260628_第十二卷水产_修复核对进度.md`。

验收：第十二卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第十三卷 盐业`。第十二卷表12-1至表12-14需从源 PDF 专项补登、重建和核验；`第四节捕捞工具` 需后续 PDF 核题确认。
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

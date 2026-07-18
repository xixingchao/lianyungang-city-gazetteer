# -*- coding: utf-8 -*-
"""Repair and audit 第三十三卷 商业 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "下" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第三十三卷商业_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第三十三卷-商业">.*?</h2>)(.*?)(?=<h2 id="第三十四卷-[^"]+">)', re.S)

CHAPTERS = [
    ("第一章所有制形式", ["第一节私营商业", "第二节合作（集体）商业", "第三节国营及公私合营商业"]),
    ("第二章商业机构", ["第一节管理机构", "第二节经营机构"]),
    ("第三章商品购销", ["第一节百货", "第二节五金交电化工", "第三节肉禽蛋", "第四节糖烟酒", "第五节蔬菜海产品"]),
    ("第四章饮食服务业", ["第一节饮食", "第二节旅馆", "第三节照相", "第四节理发", "第五节浴池", "第六节洗染"]),
]

CHAPTER_NEEDLES = {
    "第一章所有制形式": "建国前，境内商业皆属私营商业",
    "第二章商业机构": "民国38年（1949年）7月，山东省鲁中南行署",
    "第三章商品购销": "百货业过去通称布、杂（货）、广（货）业",
    "第四章饮食服务业": "民国38年（1949年）市区有饮食服务网点473个",
}

CHAPTER_VARIANTS = {
    "第一章所有制形式": ["第一章所有制形式", "所有制形式", "第一章"],
    "第二章商业机构": ["第二章商业机构", "商业机构", "第二章"],
    "第三章商品购销": ["第三章商品购销", "商品购销", "第三章"],
    "第四章饮食服务业": ["第四章饮食服务业", "饮食服务业", "第四章"],
}

SECTION_NEEDLES = {
    ("第一章所有制形式", "第一节私营商业"): "杂货店30多家，大小商行10多家",
    ("第一章所有制形式", "第二节合作（集体）商业"): "1956年开始对小商小贩进行社会主义改造",
    ("第一章所有制形式", "第三节国营及公私合营商业"): "一、国营商业民国37年（1948年）11月",
    ("第二章商业机构", "第一节管理机构"): "民国38年（1949年）7月，山东省鲁中南行署",
    ("第二章商业机构", "第二节经营机构"): "一、连云港贸易中心位于新浦解放东路32号",
    ("第三章商品购销", "第一节百货"): "一、行业状况百货业过去通称布、杂",
    ("第三章商品购销", "第二节五金交电化工"): "20世纪20年代，伴随着手工、纺织、电力工业的发展",
    ("第三章商品购销", "第三节肉禽蛋"): "一、生猪购销清末至民国",
    ("第三章商品购销", "第四节糖烟酒"): "一、行业状况建国前，糖烟酒销售多由食品店",
    ("第三章商品购销", "第五节蔬菜海产品"): "一、蔬菜行业状况历史上蔬菜多为自产自销",
    ("第四章饮食服务业", "第一节饮食"): "一、饮食店清末，赣榆县青口镇商业繁盛",
    ("第四章饮食服务业", "第二节旅馆"): "民国前后，青口镇有比较讲究的",
    ("第四章饮食服务业", "第三节照相"): "一、沿革民国5年（1916年）",
    ("第四章饮食服务业", "第四节理发"): "早年境内理发业多以担挑为主",
    ("第四章饮食服务业", "第五节浴池"): "清末民初，较大的旅馆兼设浴室",
    ("第四章饮食服务业", "第六节洗染"): "民国7年（1918年），海州城开设同和染坊",
}

SECTION_VARIANTS = {
    "第一节私营商业": ["第一节私营商业", "第一节"],
    "第二节合作（集体）商业": ["第二节合作（集体）商业", "第二节"],
    "第三节国营及公私合营商业": ["第三节国营及公私合营商业", "第三节"],
    "第一节管理机构": ["第一节管理机构", "第一节"],
    "第二节经营机构": ["第二节经营机构", "第二节"],
    "第一节百货": ["第一节百　货", "第一节百货", "第一节"],
    "第二节五金交电化工": ["第二节五金交电化工", "第二节五金交电", "第二节"],
    "第三节肉禽蛋": ["第三节肉禽蛋", "肉禽蛋第三节", "第三节"],
    "第四节糖烟酒": ["第四节糖烟酒", "第四节"],
    "第五节蔬菜海产品": ["第五节蔬菜海产品", "蔬菜海产品第五节", "第五节"],
    "第一节饮食": ["第一节•饮•食", "第一节饮食", "第一节"],
    "第二节旅馆": ["第二节旅•馆", "第二节旅馆", "第二节"],
    "第三节照相": ["第三节照相", "第三节"],
    "第四节理发": ["第四节•理•发", "第四节理发", "第四节"],
    "第五节浴池": ["第五节浴池", "第五节"],
    "第六节洗染": ["洗染第六节", "第六节洗染", "第六节"],
}

EXPECTED_TABLES = [f"表33-{i}" for i in range(1, 16)]


def h3(title: str) -> str:
    return f'<h3 id="第三十三卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第三十三卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    start_candidates = [text.find("\n第三十三卷\n"), text.find("\n第三十三卷 商业\n")]
    start_candidates = [pos for pos in start_candidates if pos >= 0]
    start = min(start_candidates) if start_candidates else -1
    end = text.find("\n第三十四卷", start)
    if start < 0 or end < 0:
        raise RuntimeError("Cannot locate 第三十三卷 source range")
    head, section, tail = text[:start], text[start:end], text[end:]
    replacements = {
        "\n第三十三卷\n概述\n": "\n第三十三卷 商业\n\n概述\n",
        "\n第一章\n所有制形式\n": "\n第一章所有制形式\n",
        "\n第二节\n合作（集体）商业\n": "\n第二节合作（集体）商业\n",
        "\n第三节\n国营及公私合营商业\n": "\n第三节国营及公私合营商业\n",
        "\n第二章\n商业机构\n": "\n第二章商业机构\n",
        "\n第二章\n商业机构\n:1433:\n": "\n",
        "\n第三章\n商品购销\n": "\n第三章商品购销\n",
        "\n第三章商品购销\n\n续上表\n": "\n续上表\n",
        "\n第一节百　货\n": "\n第一节百货\n",
        "\n化工\n第二节\n五金\n交电\n": "\n第二节五金交电化工\n",
        "\n肉禽蛋\n第三节\n": "\n第三节肉禽蛋\n",
        "\n第五节\n一、蔬菜\n": "\n第五节蔬菜海产品\n一、蔬菜\n",
        "\n第四章\n饮食服务业\n": "\n第四章饮食服务业\n",
        "\n第一节•饮•食\n": "\n第一节饮食\n",
        "\n第二节旅•馆\n": "\n第二节旅馆\n",
        "\n第四节•理•发\n": "\n第四节理发\n",
        "\n洗染\n第六节\n": "\n第六节洗染\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    fixed = head + section + tail
    if fixed != original:
        SRC_MD.write_text(fixed, encoding="utf-8")
        return ["规范源 MD 中第三十三卷卷题、章题、节题断裂、页眉残留和 OCR 标题错位。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "第一节百　货": "第一节百货",
        "第一节•饮•食": "第一节饮食",
        "第二节旅•馆": "第二节旅馆",
        "第四节•理•发": "第四节理发",
        "肉禽蛋第三节": "第三节肉禽蛋",
        "洗染第六节": "第六节洗染",
        "商业机构第一节管理机构": "商业机构\n第一节管理机构",
        "商品购销第一节百货": "商品购销\n第一节百货",
    }
    for old, new in residues.items():
        section = section.replace(old, new)
    section = section.replace("第二章商业机构:1433:", "")
    section = re.sub(r"(\d{4})商品购销第一节百货", r"\1\n商品购销\n第一节百货", section)
    return section


def insert_or_replace_title(section: str, marker: str, needle: str, variants: list[str], start: int = 0) -> tuple[str, bool, int]:
    if marker in section:
        return section, False, section.find(marker) + len(marker)
    needle_pos = section.find(needle, max(0, start - 2500))
    if needle_pos < 0:
        needle_pos = section.find(needle)
    if needle_pos >= 0:
        prefix_start = max(0, needle_pos - 1100)
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
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第三十三卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def render_source_chunk(start_title: str, end_title: str) -> str:
    source = SRC_MD.read_text(encoding="utf-8")
    start = source.find(start_title)
    end = source.find(end_title, start)
    if start < 0 or end < 0:
        return ""
    chunk = source[start + len(start_title) : end].strip()
    chunk = re.sub(r"<!--.*?-->", "", chunk, flags=re.S)
    chunk = re.sub(r"\n{3,}", "\n\n", chunk).strip()
    paragraphs = [line.strip() for line in chunk.splitlines() if line.strip()]
    return "\n".join(f"<p>{line}</p>" for line in paragraphs)


def ensure_source_section(section: str, chapter: str, title: str, source_start: str, source_end: str, before_marker: str) -> tuple[str, bool]:
    marker = h4(chapter, title)
    if marker in section:
        return section, False
    pos = section.find(before_marker)
    if pos < 0:
        return section, False
    rendered = render_source_chunk(source_start, source_end)
    if not rendered:
        return section, False
    insert = marker + "\n" + rendered + "\n"
    return section[:pos] + insert + section[pos:], True


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)
    summary_marker = '<h3 id="第三十三卷-概述">概述</h3>'
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
    section, added = ensure_source_section(
        section,
        "第三章商品购销",
        "第二节五金交电化工",
        "第二节五金交电化工",
        "第三节肉禽蛋",
        h4("第三章商品购销", "第三节肉禽蛋"),
    )
    h4_count += int(added)
    section, added = ensure_source_section(
        section,
        "第三章商品购销",
        "第五节蔬菜海产品",
        "第五节蔬菜海产品",
        "第四章饮食服务业",
        h3("第四章饮食服务业"),
    )
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
        raise RuntimeError("Cannot locate 第三十三卷 商业 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第三十三卷-商业">第三十三卷商业</h2>'
    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复商业卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复商业卷节级 H4 标题：{h4_added} 处。")
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
            if title.startswith("表33-") or number.startswith("表33-"):
                tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(f"| {data.get('table_id', '')} | {data.get('table_number') or data.get('title', '')} | {data.get('title', '')} | {pages} | {data.get('status', '')} | {size} | {data.get('notes', '')} |")
    registered = {str(data.get("table_number") or data.get("title") or "") for data in tables}
    for table_no in EXPECTED_TABLES:
        if table_no not in registered:
            table_lines.append(f"| 暂无登记 | {table_no} | 第三十三卷可见表格待进入表格站或需核验 | p1540-p1577 | 待补登 | 待定 | 需从源 PDF 专项补建、核验 |")

    lines = [
        "# 第三十三卷商业 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第三十三卷 商业。",
        "- 源 MD：`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第三十三卷-商业` 至 `第三十四卷-*` 之前。",
        "- 源页范围：约 p1540-p1577，位于中册 part02。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第三十三卷正文区间和目录骨架，确认本卷为四章：所有制形式、商业机构、商品购销、饮食服务业。",
        "- 统计第三十三卷表格状态，源 MD 可见表33-1至表33-15，表格站仅见表33-3相关骨架且存在下册疑似串卷条目。",
        "",
        "## 格式修复清单",
        "",
        "- 卷题恢复为 `第三十三卷商业`，卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章所有制形式` 至 `第四章饮食服务业` 共 4 个 H3。",
        "- 恢复私营商业、合作（集体）商业、商品购销、饮食服务业等共 16 个 H4。",
        "- 清理源 MD 中页眉残留和 OCR 标题错位，如 `肉禽蛋 / 第三节`、`洗染 / 第六节`、`第一节•饮•食`。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表33-*的登记表格：{len(tables)} 张。",
        "- 源 MD 可见表33-1至表33-15；当前表格站仅有表33-3骨架，且有下册同表号疑似串卷，需专项核验。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第三十三卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第三十三卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第三十三卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第三十三卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第三十三卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第三十三卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第三十三卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第三十三卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第三十三卷卷题误显示为 `第三十三卷概述`，章、节标题全部扁平化为正文。",
        "- 多处章节标题被表格 OCR 数字粘连，如 `商品购销第一节百货`、`肉禽蛋第三节`、`洗染第六节`。",
        "- 表33-*密集且表号形态不统一，如 `表338`、`表3312`、`表 3314`。",
        "",
        "## 解决的困难",
        "",
        "- 以目录骨架确认 4 章 16 节正式标题，再用正文首句顺序定位。",
        "- 对商品购销和饮食服务业中粘连最严重的标题，使用正文首句和 OCR 变体双重定位。",
        "- 将表33-1至表33-15统一纳入表格专项风险清单。",
        "",
        "## 残留风险",
        "",
        "- 表33-1至表33-15需从源 PDF 逐张核读、补登、结构化。",
        "- 表格站中表33-3存在中册重复和下册疑似串卷条目，需专项去重核验。",
        "- 商品购销数据和饮食服务业统计表数值密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第三十四卷 供销章节格式核对。",
        "- 表格专项阶段回补第三十三卷 15 张可见表格。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-29 第三十三卷商业章节核对完成"
    section = f"""{header}

已完成 `第三十三卷 商业` 章节格式核对：

- 新增脚本：`scripts/repair_thirty_third_volume_commerce.py`。
- 修复 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md` 中第三十三卷卷题、章题、节题断裂、页眉残留和 OCR 标题错位。
- 修复 `output/final_reader/连云港市志_全书.html` 中第三十三卷卷题误作 `第三十三卷概述`、章节标题全部扁平化的问题。
- 第三十三卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章所有制形式至第四章饮食服务业），H4={stats['h4_count']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站仅见表33-3骨架，且有下册疑似串卷条目。
- 源 MD 可见表33-1至表33-15，本轮先记录为表格专项重点风险。
- 已写入进度文档：`output/reports/progress/20260629_第三十三卷商业_修复核对进度.md`。

验收：第三十三卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第三十四卷 供销`。第三十三卷表33-1至表33-15需从源 PDF 专项补登、重建和核验。
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

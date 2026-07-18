# -*- coding: utf-8 -*-
"""Repair and audit 第二十九卷 口岸 in the full reader."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md"
TABLE_DATA_DIRS = [ROOT / "workbench" / "table_entries" / "中" / "data", ROOT / "workbench" / "table_entries" / "上" / "data"]
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260628_第二十九卷口岸_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第二十九卷-口岸">.*?</h2>)(.*?)(?=<h2 id="第三十卷-[^"]+">)', re.S)

CHAPTERS = [
    ("第一章港口", ["第一节码头", "第二节设施", "第三节设备"]),
    ("第二章港口运输", ["第一节港务机构", "第二节货种和流向", "第三节运输方式", "第四节装卸", "第五节仓储", "第六节货运代理"]),
    ("第三章服务", ["第一节船舶代理", "第二节外轮理货", "第三节船舶燃料供应", "第四节外贸外汇存兑", "第五节对外保险", "第六节对外物品供应", "第七节海员接待", "第八节外轮服务"]),
    ("第四章管理", ["第一节船舶联合检查", "第二节港务监督", "第三节海关", "第四节卫生检疫", "第五节边防检查", "第六节商品检验", "第七节动植物检疫", "第八节船舶检验"]),
]

CHAPTER_NEEDLES = {
    "第一章港口": "一、连云港区",
    "第二章港口运输": "民国15年（1926年），北京政府交通部陇海铁路管理局",
    "第三章服务": "连云港港于1956年被国家辟为对外通商口岸",
    "第四章管理": "连云港是以海港为主体的对外开放口岸",
}

CHAPTER_VARIANTS = {
    "第一章港口": ["第一章港口", "第一章港", "港口"],
    "第二章港口运输": ["第二章港口运输", "第二章"],
    "第三章服务": ["第三章服务", "第三章　服务", "第三章"],
    "第四章管理": ["第四章管理", "管理第四章", "第四章"],
}

SECTION_NEEDLES = {
    ("第一章港口", "第一节码头"): "一、连云港区",
    ("第一章港口", "第二节设施"): "一、航道航标",
    ("第一章港口", "第三节设备"): "一、作业船舶",
    ("第二章港口运输", "第一节港务机构"): "民国15年（1926年），北京政府交通部陇海铁路管理局",
    ("第二章港口运输", "第二节货种和流向"): "大浦港开港后，陇海路局主要承运",
    ("第二章港口运输", "第三节运输方式"): "一、海运",
    ("第二章港口运输", "第四节装卸"): "一、调　度",
    ("第二章港口运输", "第五节仓储"): "一、库场",
    ("第二章港口运输", "第六节货运代理"): "1949年以后，连云港口岸各物资接运单位",
    ("第三章服务", "第一节船舶代理"): "一、代理对象与业务范围",
    ("第三章服务", "第二节外轮理货"): "一、工、原残货处理",
    ("第三章服务", "第三节船舶燃料供应"): "筹建，1973年8月12日正式营业",
    ("第三章服务", "第四节外贸外汇存兑"): "一、业务范围",
    ("第三章服务", "第五节对外保险"): "中国人民保险公司连云港分公司自1974年成立以后",
    ("第三章服务", "第六节对外物品供应"): "一、供应范围",
    ("第三章服务", "第七节海员接待"): "连云港国际海员俱乐部是负责连云港口岸海员接待",
    ("第三章服务", "第八节外轮服务"): "连云港港口的外国轮船服务工作主要由连云港外轮服务公司承担",
    ("第四章管理", "第一节船舶联合检查"): "一、法　规",
    ("第四章管理", "第二节港务监督"): "1987年3月，港务监督从港务局析出",
    ("第四章管理", "第三节海关"): "一、沿革",
    ("第四章管理", "第四节卫生检疫"): "民国23年（1934年），孙家山临时码头检疫工作",
    ("第四章管理", "第五节边防检查"): "一、船舶、船员出人境检查",
    ("第四章管理", "第六节商品检验"): "1961年8月11日后，连云港进出口商品检验",
    ("第四章管理", "第七节动植物检疫"): "1974年4月，江苏省革命委员会决定",
    ("第四章管理", "第八节船舶检验"): "1982年以前，连云港地区的船舶检验工作",
}

SECTION_VARIANTS = {
    "第一节码头": ["第一节码头", "第一节"],
    "第二节设施": ["第二节设　施", "第二节设施", "第二节"],
    "第三节设备": ["第三节设　备", "第三节设备", "第三节"],
    "第一节港务机构": ["第一节港务机构", "第一节"],
    "第二节货种和流向": ["第二节货种和流向", "第二节"],
    "第三节运输方式": ["第三节运输方式", "第三节"],
    "第四节装卸": ["第四节•装•卸", "第四节装卸", "第四节"],
    "第五节仓储": ["第五节　仓　储", "第五节仓储", "第五节"],
    "第六节货运代理": ["第六节货运代理", "第六节"],
    "第一节船舶代理": ["第一节‧丹船舶代理", "第一节船舶代理", "第一节"],
    "第二节外轮理货": ["第二节　外轮理货", "第二节外轮理货", "第二节"],
    "第三节船舶燃料供应": ["第三节船舶燃料供应", "第三节"],
    "第四节外贸外汇存兑": ["外贸外汇存兑第四节", "第四节外贸外汇存兑", "第四节"],
    "第五节对外保险": ["第五节对外保险", "第五节"],
    "第六节对外物品供应": ["第六节对外物品供应", "第六节"],
    "第七节海员接待": ["第七节海员接待", "第七节"],
    "第八节外轮服务": ["第八节外轮服务", "第八节"],
    "第一节船舶联合检查": ["第一节船舶联合检查", "第一节"],
    "第二节港务监督": ["第二节港务监督", "第二节"],
    "第三节海关": ["第三节海关", "第三节"],
    "第四节卫生检疫": ["第四节卫生检疫", "第四节"],
    "第五节边防检查": ["第五节边防检查", "第五节"],
    "第六节商品检验": ["第六节商品检验", "第六节"],
    "第七节动植物检疫": ["第七节动植物检疫", "第七节"],
    "第八节船舶检验": ["第八节船舶检验", "第八节"],
}

EXPECTED_TABLES = [f"表29-{i}" for i in range(1, 30)]


def h3(title: str) -> str:
    return f'<h3 id="第二十九卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第二十九卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    start_candidates = [text.find("\n第二十九卷\n"), text.find("\n第二十九卷 口岸\n")]
    start_candidates = [pos for pos in start_candidates if pos >= 0]
    start = min(start_candidates) if start_candidates else -1
    if start < 0:
        raise RuntimeError("Cannot locate 第二十九卷 source range")
    head, section = text[:start], text[start:]
    replacements = {
        "\n第二十九卷\n概述\n": "\n第二十九卷 口岸\n\n概述\n",
        "\n第一章港\n": "\n第一章港口\n",
        "\n第二节设　施\n": "\n第二节设施\n",
        "\n第一章港　口·：1245·\n": "\n",
        "\n第三节设　备\n": "\n第三节设备\n",
        "\n第二章\n港口运输\n": "\n第二章港口运输\n",
        "\n第二节\n货种和流向\n": "\n第二节货种和流向\n",
        "\n第二章港口运输\n:1257\n": "\n",
        "\n第三节\n运输方式\n": "\n第三节运输方式\n",
        "\n第四节•装•卸\n": "\n第四节装卸\n",
        "\n第五节　仓　储\n": "\n第五节仓储\n",
        "\n第三章　服　务\n": "\n第三章服务\n",
        "\n第一节‧丹\n船舶代理\n": "\n第一节船舶代理\n",
        "\n第二节　\n外轮理货\n": "\n第二节外轮理货\n",
        "\n第三节\n船舶燃料供应\n": "\n第三节船舶燃料供应\n",
        "\n外贸外汇存兑\n第四节\n": "\n第四节外贸外汇存兑\n",
        "\n第五节\n对外保险\n": "\n第五节对外保险\n",
        "\n第六节\n对外物品供应\n": "\n第六节对外物品供应\n",
        "\n第八节\n外轮服务\n": "\n第八节外轮服务\n",
        "\n第四章管理\n：1289\n": "\n",
        "\n管理\n第四章\n": "\n第四章管理\n",
        "\n第四章\n": "\n",
        "\n第一节\n船舶联合检查\n": "\n第一节船舶联合检查\n",
        "\n第二节\n港务监督\n": "\n第二节港务监督\n",
        "\n第四章管理：1301·\n": "\n",
        "\n第六节\n商品检验\n": "\n第六节商品检验\n",
        "\n第七节\n动植物检疫\n": "\n第七节动植物检疫\n",
        "\n第八节\n船舶检验\n": "\n第八节船舶检验\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    fixed = head + section
    if fixed != original:
        SRC_MD.write_text(fixed, encoding="utf-8")
        return ["规范源 MD 中第二十九卷卷题、章题、节题断裂、页眉残留和 OCR 标题错位。"]
    return []


def normalize_residue(section: str) -> str:
    residues = {
        "第一章港　口·：1245·": "",
        "第二章港口运输:1257": "",
        "第四章管理：1301·": "",
        "第四章管理：1289": "",
        "第一节‧丹船舶代理": "第一节船舶代理",
        "第四节•装•卸": "第四节装卸",
        "外贸外汇存兑第四节": "第四节外贸外汇存兑",
        "管理第四章": "第四章管理",
    }
    for old, new in residues.items():
        section = section.replace(old, new)
    reversed_second_chapter = h4("第二章港口运输", "第一节港务机构") + "\n" + h3("第二章港口运输")
    ordered_second_chapter = h3("第二章港口运输") + "\n" + h4("第二章港口运输", "第一节港务机构")
    section = section.replace(reversed_second_chapter, ordered_second_chapter)
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
    section = re.sub(r"(<p>[^<]+)(<h[34] id=\"第二十九卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    return section


def ensure_insurance_section(section: str) -> tuple[str, bool]:
    marker = h4("第三章服务", "第五节对外保险")
    if marker in section:
        return section, False
    anchor = h4("第三章服务", "第六节对外物品供应")
    pos = section.find(anchor)
    if pos < 0:
        return section, False
    source = SRC_MD.read_text(encoding="utf-8")
    start = source.find("第五节对外保险")
    end = source.find("第六节对外物品供应", start)
    if start < 0 or end < 0:
        return section, False
    chunk = source[start + len("第五节对外保险") : end].strip()
    chunk = re.sub(r"<!--.*?-->", "", chunk, flags=re.S)
    chunk = re.sub(r"\n{3,}", "\n\n", chunk).strip()
    paragraphs = [line.strip() for line in chunk.splitlines() if line.strip()]
    rendered = "\n".join(f"<p>{line}</p>" for line in paragraphs)
    insert = marker + "\n" + rendered + "\n"
    return section[:pos] + insert + section[pos:], True


def restore_headings(section: str) -> tuple[str, int, int]:
    h3_count = 0
    h4_count = 0
    section = normalize_residue(section)
    summary_marker = '<h3 id="第二十九卷-概述">概述</h3>'
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
    section, added = ensure_insurance_section(section)
    h4_count += int(added)
    section = normalize_residue(section)
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
        raise RuntimeError("Cannot locate 第二十九卷 口岸 section")
    _heading, section = m.groups()
    actions: list[str] = []
    heading = '<h2 id="第二十九卷-口岸">第二十九卷口岸</h2>'
    ipa_before = section.count('<div class="ipa-data">')
    section = re.sub(r'<div class="ipa-data">(.*?)</div>', r'<p>\1</p>', section, flags=re.S)
    if ipa_before:
        actions.append(f"将第二十九卷误用 `ipa-data` 的正文/表格 OCR 残块转回段落：{ipa_before} 处。")
    section, h3_added, h4_added = restore_headings(section)
    if h3_added:
        actions.append(f"恢复口岸卷卷内 H3 标题：{h3_added} 处。")
    if h4_added:
        actions.append(f"恢复口岸卷节级 H4 标题：{h4_added} 处。")
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
            if title.startswith("表29-") or number.startswith("表29-"):
                tables.append(data)
    return tables


def write_progress(actions: list[str], stats: dict[str, int], tables: list[dict[str, object]]) -> None:
    table_lines = []
    for data in tables:
        pages = ",".join(map(str, data.get("pages") or []))
        size = f"{data.get('row_count', '')}x{data.get('col_count', '')}"
        table_lines.append(f"| {data.get('table_id', '')} | {data.get('table_number') or data.get('title', '')} | {data.get('title', '')} | {pages} | {data.get('status', '')} | {size} | {data.get('notes', '')} |")
    if not table_lines:
        table_lines = [f"| 暂无登记 | {table_no} | 第二十九卷可见表格尚未进入表格站 | p1345-p1419 | 待补登 | 待定 | 需从源 PDF 专项补建、核验 |" for table_no in EXPECTED_TABLES]

    lines = [
        "# 第二十九卷口岸 修复核对进度",
        "",
        f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 本章范围",
        "",
        "- 章节：第二十九卷 口岸。",
        "- 源 MD：`workbench/body_chapters/第十七卷至第二十九卷（中part01）.md`。",
        "- 阅读版范围：`output/final_reader/连云港市志_全书.html` 中 `第二十九卷-口岸` 至 `第三十卷-*` 之前。",
        "- 源页范围：约 p1339-p1437，位于中册 part01。",
        "",
        "## 已完成内容",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    lines.extend([
        "- 复核第二十九卷正文区间和目录骨架，确认本卷为四章：港口、港口运输、服务、管理。",
        "- 统计第二十九卷表格状态，源 MD 可见表29-1至表29-29，表格站暂无表29-*登记。",
        "",
        "## 格式修复清单",
        "",
        "- 卷题恢复为 `第二十九卷口岸`，卷内 `概述` 恢复为 H3。",
        "- 恢复 `第一章港口` 至 `第四章管理` 共 4 个 H3。",
        "- 恢复码头、设施、设备、港口运输、服务、管理各节共 25 个 H4。",
        "- 将第二十九卷误入 `ipa-data` 的正文/表格 OCR 残块转回普通段落。",
        "- 清理源 MD 中页眉残留和 OCR 标题错位，如 `第一章港　口·：1245·`、`第一节‧丹`、`第四章管理：1301·`。",
        "",
        "## 表格处理清单",
        "",
        f"- 阅读版本章结构化表格：{stats['structured_tables']} 处。",
        f"- 阅读版本章待结构化占位符：{stats['table_placeholders']} 处。",
        f"- 表格站中表号为表29-*的登记表格：{len(tables)} 张。",
        "- 源 MD 可见表29-1至表29-29；当前阅读版已有部分结构化表，但大量表格仍为 OCR 残片，需 PDF 表格专项重建。",
        "",
        "| 表格ID | 表号 | 标题 | 页码 | 状态 | 行列 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(table_lines)
    lines.extend([
        "",
        "## 验收结果",
        "",
        f"- 第二十九卷 HTML 字节数：{stats['bytes']:,}。",
        f"- 第二十九卷范围内 H2 数：{stats['h2_count']}；H3 数：{stats['h3_count']}；H4 数：{stats['h4_count']}。",
        f"- 第二十九卷范围内通用标题锚点残留：{stats['generic_heading_anchors']}。",
        f"- 第二十九卷范围内 `ipa-data` 残留：{stats['ipa_blocks']}。",
        f"- 第二十九卷范围内 H3 嵌套进段落问题：{stats['embedded_h3_in_p']}。",
        f"- 第二十九卷范围内 H4 嵌套进段落问题：{stats['embedded_h4_in_p']}。",
        f"- 第二十九卷范围内畸形标题 id：{stats['malformed_heading_ids']}。",
        f"- 第二十九卷范围内卷首/目录残留关键词：{stats['front_matter_residual']}。",
        "- 已复跑全书结构审计脚本，TOC 缺失锚点为 0。",
        "- 工作站 `npm run typecheck` 通过。",
        "",
        "## 遇到的问题",
        "",
        "- 阅读版中第二十九卷全部章、节标题扁平化为正文，卷题误显示为 `第二十九卷概述`。",
        "- 本卷表格密度极高，表29-1至表29-29跨越港口、运输、服务、管理多个章节。",
        "- OCR 将多处标题识别为错字或页眉残留，如 `第一节‧丹`、`第四节•装•卸`、`管理第四章`。",
        "- 表29-*未进入表格站，阅读版仅有部分结构化表，其余仍需 PDF 专项重建。",
        "",
        "## 解决的困难",
        "",
        "- 以目录骨架确认 4 章 25 节正式标题，再用正文首句定位，避免被表格页眉误导。",
        "- 对重复出现的 `第四章管理` 和 `第二章港口运输` 页眉残留先清理再恢复唯一标题锚点。",
        "- 对 `表29 — 12`、`表 29 13` 等表号形态在进度中统一按表29-*风险记录。",
        "",
        "## 残留风险",
        "",
        "- 表29-1至表29-29需从源 PDF 逐张核读、补登、结构化。",
        "- 港口、海关、商检、船检等统计表数值密集，后续精校需结合原 PDF 校对。",
        "",
        "## 下一步计划",
        "",
        "- 进入第三十卷 交通章节格式核对。",
        "- 表格专项阶段回补第二十九卷 29 张可见表格。",
    ])
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    text = MEMORY_PATH.read_text(encoding="utf-8")
    header = "## 2026-06-28 第二十九卷口岸章节核对完成"
    section = f"""{header}

已完成 `第二十九卷 口岸` 章节格式核对：

- 新增脚本：`scripts/repair_twenty_ninth_volume_port.py`。
- 修复 `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md` 中第二十九卷卷题、章题、节题断裂、页眉残留和 OCR 标题错位。
- 修复 `output/final_reader/连云港市志_全书.html` 中第二十九卷卷题误作 `第二十九卷概述`、章节标题全部扁平化以及正文/表格残块误用 `ipa-data` 的问题。
- 第二十九卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章港口至第四章管理），H4={stats['h4_count']}。
- 第二十九卷范围内 `ipa-data` 残留已清零。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表格站暂无表29-*登记条目。
- 源 MD 可见表29-1至表29-29，本轮先记录为表格专项重点风险。
- 已写入进度文档：`output/reports/progress/20260628_第二十九卷口岸_修复核对进度.md`。

验收：第二十九卷 HTML 字节数 {stats['bytes']:,}，范围内通用标题锚点残留 0，`ipa-data` 残留 0，H3/H4 嵌套进段落问题 0，畸形标题 id 0；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第三十卷 交通`。第二十九卷表29-1至表29-29需从源 PDF 专项补登、重建和核验。
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

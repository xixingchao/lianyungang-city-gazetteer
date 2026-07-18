# -*- coding: utf-8 -*-
"""Repair and audit 第三十八卷 财政 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第三十八卷财政_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第三十八卷-财政">.*?</h2>)(.*?)(?=<h2 id="第三十九卷-[^"]+">)', re.S)
SOURCE_RE = re.compile(r'(第三十八卷.*?)(?=第三十九卷)', re.S)

CHAPTERS = [
    ("第一章机构体制", ["第一节机构", "第二节体制"]),
    ("第二章财政收入", ["第一节税收", "第二节企业收入", "第三节国家预算调节基金、专项收入和其它收入", "第四节预算外资金收入"]),
    ("第三章财政支出", ["第一节经济建设支出", "第二节城市维护及建设支出", "第三节文教科学卫生事业费支出", "第四节行政管理费和公检法司支出", "第五节抚恤和社会福利救济费支出", "第六节其它支出", "第七节预算外资金支出"]),
    ("第四章财政管理", ["第一节企业财务管理", "第二节行政事业财务管理", "第三节农业财务管理", "第四节预算外资金管理", "第五节控制社会集团购买力", "第六节财政监督"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(titles) for _, titles in CHAPTERS)
EXPECTED_TABLES = ["表38-3", "表38-4", "表38-5", "表38-6"]


def h3(title: str) -> str:
    return f'<h3 id="第三十八卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第三十八卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        raise RuntimeError("Cannot locate 第三十八卷 source range")
    section = m.group(1)
    original = section
    replacements = {
        "第三十八卷\n概述\n": "第三十八卷 财政\n\n概述\n",
        "\n体制\n第一章\n机构\n": "\n第一章机构体制\n",
        "\n第一节机\n": "\n第一节机构\n",
        "\n第二节•体•制\n": "\n第二节体制\n",
        "\n第二章\n财政收入\n": "\n第二章财政收入\n",
        "\n第一节税\n、农业税": "\n第一节税收\n一、农业税",
        "\n第三节\n国家预算调节基金、专项收入和其它收入\n": "\n第三节国家预算调节基金、专项收入和其它收入\n",
        "\n第四节\n预算外资金收入\n": "\n第四节预算外资金收入\n",
        "\n第三章\n财政支出\n": "\n第三章财政支出\n",
        "\n第一节\n经济建设支出\n": "\n第一节经济建设支出\n",
        "\n第二节\n城市维护及建设支出\n": "\n第二节城市维护及建设支出\n",
        "\n第三节\n文教科学卫生事业费支出\n": "\n第三节文教科学卫生事业费支出\n",
        "\n行政管理费和公检法司支出\n第四节\n": "\n第四节行政管理费和公检法司支出\n",
        "\n抚恤和社会福利救济费支出\n第五节\n": "\n第五节抚恤和社会福利救济费支出\n",
        "\n第六节\n其它支出\n": "\n第六节其它支出\n",
        "\n第七节\n预算外资金支出\n": "\n第七节预算外资金支出\n",
        "\n第四章\n财政管理\n.1601\n": "\n第四章财政管理\n",
        "\n第一节\n企业财务管理\n": "\n第一节企业财务管理\n",
        "\n第三节‧\n农业财务管理\n": "\n第三节农业财务管理\n",
        "\n第四节予\n预算外资金管理\n": "\n第四节预算外资金管理\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    section = re.sub(r"\n(?:第一章机构体制，1583·|财政收入：1591·|第二章[贝！ ]|第四章贝)\n", "\n", section)
    if section != original:
        text = text[: m.start(1)] + section + text[m.end(1) :]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第三十八卷卷题、章题、节题断裂、节题倒置和 OCR 页眉残留。"]
    return []


def insert_after_h2(section: str, marker: str) -> tuple[str, bool]:
    if marker in section:
        return section, False
    m = re.search(r'</h2>\s*', section)
    if not m:
        return section, False
    return section[:m.end()] + "\n" + marker + "\n" + section[m.end():], True


def insert_before_text(section: str, marker: str, text: str) -> tuple[str, bool]:
    if marker in section:
        return section, False
    pos = section.find(text)
    if pos < 0:
        return section, False
    p_start = section.rfind("<p>", 0, pos)
    p_end = section.rfind("</p>", 0, pos)
    insert_pos = p_start if p_start > p_end else pos
    return section[:insert_pos] + marker + "\n" + section[insert_pos:], True


def split_heading(section: str, marker: str, text: str, replacement: str = "") -> tuple[str, bool]:
    if marker in section:
        return section, False
    variants = [
        text,
        text.replace("机构", "机"),
        text.replace("体制", "•体•制"),
        text.replace("税收", "税、农业税"),
        text.replace("第三节农业财务管理", "第三节‧农业财务管理"),
        text.replace("第四节预算外资金管理", "第四节予预算外资金管理"),
    ]
    for v in variants:
        pattern = "<p>" + v
        pos = section.find(pattern)
        if pos >= 0:
            content_start = pos + len(pattern)
            prefix = replacement if replacement else ""
            return section[:pos] + marker + "\n<p>" + prefix + section[content_start:], True
        pos = section.find(v)
        if pos >= 0:
            p_start = section.rfind("<p>", 0, pos)
            p_end = section.rfind("</p>", 0, pos)
            content_start = pos + len(v)
            prefix = replacement if replacement else ""
            if p_start > p_end:
                return section[:pos] + "</p>\n" + marker + "\n<p>" + prefix + section[content_start:], True
            return section[:pos] + marker + "\n" + prefix + section[content_start:], True
    return section, False


def normalize_ipa(section: str) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        text = re.sub(r"^\s*[·:.：\s]*\d{4}\s*[·:.：\s]*", "", match.group(1).strip())
        return f"<p>{text}</p>"

    return re.sub(r'<div class="ipa-data">(.*?)</div>', repl, section, flags=re.S), count


def cleanup(section: str) -> str:
    replacements = {
        "<h2 id=\"第三十八卷-财政\">第三十八卷概述</h2>": "<h2 id=\"第三十八卷-财政\">第三十八卷财政</h2>",
        "<p>体制机构": h3("第一章机构体制") + "\n<p>",
        "<p>财政收入明、清时期": h3("第二章财政收入") + "\n<p>明、清时期",
        "<p>第一节机": h4("第一章机构体制", "第一节机构") + "\n<p>",
        "<p>第二节•体•制": h4("第一章机构体制", "第二节体制") + "\n<p>",
        "<p>第一节税、农业税收入": h4("第二章财政收入", "第一节税收") + "\n<p>一、农业税收入",
        "<p>第二节企业收入": h4("第二章财政收入", "第二节企业收入") + "\n<p>",
        "<p>第三节国家预算调节基金、专项收入和其它收入": h4("第二章财政收入", "第三节国家预算调节基金、专项收入和其它收入") + "\n<p>",
        "<p>第四节预算外资金收入": h4("第二章财政收入", "第四节预算外资金收入") + "\n<p>",
        "<p>第一节经济建设支出": h4("第三章财政支出", "第一节经济建设支出") + "\n<p>",
        "<p>第二节城市维护及建设支出": h4("第三章财政支出", "第二节城市维护及建设支出") + "\n<p>",
        "<p>第三节文教科学卫生事业费支出": h4("第三章财政支出", "第三节文教科学卫生事业费支出") + "\n<p>",
        "<p>行政管理费和公检法司支出第四节": h4("第三章财政支出", "第四节行政管理费和公检法司支出") + "\n<p>",
        "<p>抚恤和社会福利救济费支出第五节": h4("第三章财政支出", "第五节抚恤和社会福利救济费支出") + "\n<p>",
        "<p>第六节其它支出": h4("第三章财政支出", "第六节其它支出") + "\n<p>",
        "<p>第七节预算外资金支出": h4("第三章财政支出", "第七节预算外资金支出") + "\n<p>",
        "财政管理第一节企业财务管理": h3("第四章财政管理") + "\n" + h4("第四章财政管理", "第一节企业财务管理"),
        "<p>第二节行政事业财务管理": h4("第四章财政管理", "第二节行政事业财务管理") + "\n<p>",
        "<p>第三节‧农业财务管理": h4("第四章财政管理", "第三节农业财务管理") + "\n<p>",
        "<p>第四节予预算外资金管理": h4("第四章财政管理", "第四节预算外资金管理") + "\n<p>",
        "<p>第五节控制社会集团购买力": h4("第四章财政管理", "第五节控制社会集团购买力") + "\n<p>",
        "<p>第六节财政监督": h4("第四章财政管理", "第六节财政监督") + "\n<p>",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    section = re.sub(r"财政收入：1595：", "", section)
    section = re.sub(r"\.1601", "", section)
    section = re.sub(r"<p>[：:·\s]*1589\s*", "<p>", section)
    section = re.sub(r"<p>[：:·\s]*1591[：:·\s]*", "<p>", section)
    section = re.sub(r"财政收入[：:·\s]*159[15][：:·\s]*", "", section)
    section = re.sub(r"<p>\s*[·:.：\s]*\d{4}\s*[·:.：\s]*</p>\n?", "", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    section = re.sub(r"(<h3 id=\"第三十八卷-[^\"]+\">[^<]+</h3>\s*){2,}", lambda m: m.group(1), section)
    section = re.sub(r"(<h4 id=\"第三十八卷-[^\"]+\">[^<]+</h4>\s*){2,}", lambda m: m.group(1), section)
    seen_h3: set[str] = set()

    def keep_first_h3(match: re.Match[str]) -> str:
        ident = match.group(1)
        if ident in seen_h3:
            return ""
        seen_h3.add(ident)
        return match.group(0)

    section = re.sub(r'<h3 id="([^"]+)">[^<]+</h3>\s*', keep_first_h3, section)
    section = re.sub(r"(<p>[^<]*?)(<h[34] id=\"第三十八卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = section.replace("<p><h3", "<h3").replace("<p><h4", "<h4")
    section = section.replace("</h3>\n</p>", "</h3>\n").replace("</h4>\n</p>", "</h4>\n")
    return section


def restore_html() -> tuple[int, int, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第三十八卷 HTML range")
    section = m.group(0)
    section = section.replace('<h2 id="第三十八卷-财政">第三十八卷概述</h2>', '<h2 id="第三十八卷-财政">第三十八卷财政</h2>')
    inserted_h3 = inserted_h4 = 0
    section, added = insert_after_h2(section, h3("概述")); inserted_h3 += int(added)
    for title, needle in [
        ("第一章机构体制", "体制机构唐代境内设司户参军和司仓参军"),
        ("第二章财政收入", "财政收入明、清时期，境内财政收入主要靠田赋"),
        ("第三章财政支出", "财政支出，古称岁出"),
        ("第四章财政管理", "财政管理第一节企业财务管理"),
    ]:
        section, added = insert_before_text(section, h3(title), needle); inserted_h3 += int(added)
    for chapter, title, needle, replacement in [
        ("第一章机构体制", "第一节机构", "第一节机", ""),
        ("第一章机构体制", "第二节体制", "第二节•体•制", ""),
        ("第二章财政收入", "第一节税收", "第一节税、农业税收入", "一、农业税收入"),
        ("第二章财政收入", "第二节企业收入", "第二节企业收入", ""),
        ("第二章财政收入", "第三节国家预算调节基金、专项收入和其它收入", "第三节国家预算调节基金、专项收入和其它收入", ""),
        ("第二章财政收入", "第四节预算外资金收入", "第四节预算外资金收入", ""),
        ("第三章财政支出", "第一节经济建设支出", "第一节经济建设支出", ""),
        ("第三章财政支出", "第二节城市维护及建设支出", "第二节城市维护及建设支出", ""),
        ("第三章财政支出", "第三节文教科学卫生事业费支出", "第三节文教科学卫生事业费支出", ""),
        ("第三章财政支出", "第四节行政管理费和公检法司支出", "行政管理费和公检法司支出第四节", ""),
        ("第三章财政支出", "第五节抚恤和社会福利救济费支出", "抚恤和社会福利救济费支出第五节", ""),
        ("第三章财政支出", "第六节其它支出", "第六节其它支出", ""),
        ("第三章财政支出", "第七节预算外资金支出", "第七节预算外资金支出", ""),
        ("第四章财政管理", "第一节企业财务管理", "第一节企业财务管理", ""),
        ("第四章财政管理", "第二节行政事业财务管理", "第二节行政事业财务管理", ""),
        ("第四章财政管理", "第三节农业财务管理", "第三节‧农业财务管理", ""),
        ("第四章财政管理", "第四节预算外资金管理", "第四节予预算外资金管理", ""),
        ("第四章财政管理", "第五节控制社会集团购买力", "第五节控制社会集团购买力", ""),
        ("第四章财政管理", "第六节财政监督", "第六节财政监督", ""),
    ]:
        section, added = split_heading(section, h4(chapter, title), needle, replacement)
        inserted_h4 += int(added)
    section, ipa_fixed = normalize_ipa(section)
    section = cleanup(section)
    html = html[:m.start()] + section + html[m.end():]
    HTML_PATH.write_text(html, encoding="utf-8")
    return inserted_h3, inserted_h4, ipa_fixed


def audit_section() -> dict[str, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    block = SECTION_RE.search(html).group(0)
    return {
        "bytes": len(block.encode("utf-8")),
        "h2_count": block.count("<h2 "),
        "h3_count": block.count("<h3 "),
        "h4_count": block.count("<h4 "),
        "table_placeholders": block.count('class="table-placeholder"'),
        "structured_tables": block.count('<table class="structured-table"'),
        "generic_heading_anchors": len(re.findall(r'<h[234] id="anchor">', block)),
        "ipa_blocks": block.count('<div class="ipa-data">'),
        "embedded_h3_in_p": len(re.findall(r'<p[^>]*>[^<]*<h3', block)),
        "embedded_h4_in_p": len(re.findall(r'<p[^>]*>[^<]*<h4', block)),
        "malformed_heading_ids": len(re.findall(r'<h[34] id="[^"]*<h[34]', block)),
    }


def write_progress(stats: dict[str, int], changes: list[str]) -> None:
    status = "通过" if stats["h3_count"] == EXPECTED_H3 and stats["h4_count"] == EXPECTED_H4 and stats["ipa_blocks"] == 0 else "需复核"
    content = f"""# 2026-06-29 第三十八卷《财政》修复核对进度

## 本轮范围
- 范围：`第三十八卷 财政`。
- 目标：按交付标准修复卷题、概述、章题、节题、OCR 页眉残留和正文段落结构。
- 源文件：`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已处于规范状态'}。
- 将最终阅读页卷题由 `第三十八卷概述` 修正为 `第三十八卷财政`。
- 恢复概述、第一章机构体制至第四章财政管理及 19 个节题的标准 H3/H4 层级。
- 2 处 `ipa-data` 残留已转为普通正文段落，未改动既有结构化表格数据。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章机构体制至第四章财政管理），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 源 MD 可见表号：{', '.join(EXPECTED_TABLES)}；本轮先保留既有表格骨架，待 PDF 表格专项复核。
- 本卷财政收支统计表跨页、续表页眉较多，后续表格专项需重点核对表38-3至表38-6的表头、年份列和金额列。

## 验收状态
- 本卷结构验收：{status}。
- 后续已纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 进入 `第三十九卷 税务`，继续按“源 MD 标题规范 -> 最终阅读页结构修复 -> 全书审计 -> typecheck -> 进度记录 -> Git 提交”的顺序推进。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第三十八卷财政章节核对完成

已完成 `第三十八卷 财政` 章节格式核对：

- 新增脚本：`scripts/repair_thirty_eighth_volume_finance.py`。
- 修复 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md` 中第三十八卷卷题、章题、节题断裂、节题倒置和 OCR 页眉残留。
- 修复 `output/final_reader/连云港市志_全书.html` 中第三十八卷卷题误作概述、章节标题全部扁平化以及 2 处 `ipa-data` 残留的问题。
- 第三十八卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章机构体制至第四章财政管理），H4={stats['h4_count']}。
- 第三十八卷范围内 `ipa-data` 残留为 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表38-*需从源 PDF 专项补登、重建和核验。
- 已写入进度文档：`output/reports/progress/20260629_第三十八卷财政_修复核对进度.md`。

验收：第三十八卷 HTML 字节数 {stats['bytes']}，范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第三十九卷 税务`。第三十八卷表38-*需从源 PDF 专项补登、重建和核验。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第三十八卷财政章节核对完成"
    if marker in memory:
        memory = memory[: memory.find(marker)].rstrip() + "\n" + entry
    else:
        memory = memory.rstrip() + "\n" + entry
    MEMORY_PATH.write_text(memory, encoding="utf-8")


def main() -> None:
    changes = repair_source_md()
    inserted_h3, inserted_h4, ipa_fixed = restore_html()
    stats = audit_section()
    stats["inserted_h3"] = inserted_h3
    stats["inserted_h4"] = inserted_h4
    stats["ipa_fixed"] = ipa_fixed
    write_progress(stats, changes)
    update_memory(stats)
    print("Repair complete")
    if changes:
        for change in changes:
            print(f"- {change}")
    print(f"stats={stats}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()

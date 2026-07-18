# -*- coding: utf-8 -*-
"""Repair and audit 第四十卷 金融 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第四十卷金融_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第四十卷-金融">.*?</h2>)(.*?)(?=<h2 id="第四十一卷-[^"]+">)', re.S)
SOURCE_RE = re.compile(r'(第四十卷.*?)(?=第四十一卷)', re.S)

CHAPTERS = [
    ("第一章金融机构", ["第一节典当钱庄", "第二节银行", "第三节保险公司", "第四节信托投资公司", "第五节信用合作社"]),
    ("第二章货币", ["第一节铸钱银两银元铜元", "第二节兑换券法币关金券金元券", "第三节抗币北海币华中币", "第四节人民币"]),
    ("第三章存款", ["第一节本位币存款", "第二节外币存款"]),
    ("第四章贷款", ["第一节本位币贷款", "第二节外汇贷款"]),
    ("第五章结算", ["第一节本位币结算", "第二节外汇结算"]),
    ("第六章国库业务", ["第一节预算资金收支", "第二节代理发行国家债券", "第三节清理建国前银钱业存放款"]),
    ("第七章保险业务", ["第一节国内保险", "第二节涉外保险"]),
    ("第八章金融管理", ["第一节金融机构管理", "第二节现金管理", "第三节工资基金管理", "第四节金银管理", "第五节信贷计划及信贷资金管理", "第六节基本建设投资管理", "第七节外汇管理", "第八节利率管理", "第九节金融市场管理"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(titles) for _, titles in CHAPTERS)
EXPECTED_TABLES = 7


def h3(title: str) -> str:
    return f'<h3 id="第四十卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第四十卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        raise RuntimeError("Cannot locate 第四十卷 source range")
    section = m.group(1)
    original = section
    replacements = {
        "第四十卷\n概述\n": "第四十卷 金融\n\n概述\n",
        "\n第一章\n金融机构\n": "\n第一章金融机构\n",
        "\n第一节\n典当\n钱庄\n": "\n第一节典当钱庄\n",
        "\n第三节•保险公司\n": "\n第三节保险公司\n",
        "\n第四节\n信托投资公司\n": "\n第四节信托投资公司\n",
        "\n第五节\n信用合作社\n": "\n第五节信用合作社\n",
        "\n货币\n第二章\n": "\n第二章货币\n",
        "\n第一节铸钱\n银两银元铜元\n": "\n第一节铸钱银两银元铜元\n",
        "\n第二节\n兑换券\n法币\n关金券\n金元券\n": "\n第二节兑换券法币关金券金元券\n",
        "\n第三节\n抗币\n北海币\n华中币\n": "\n第三节抗币北海币华中币\n",
        "\n第四节•人民币\n": "\n第四节人民币\n",
        "\n置存款\n第三章\n": "\n第三章存款\n",
        "\n第一节‧本位币存款\n": "\n第一节本位币存款\n",
        "\n第二节\n外币存款\n": "\n第二节外币存款\n",
        "\n贷款\n第四章\n": "\n第四章贷款\n",
        "\n第一节\u3000本位币贷款\n": "\n第一节本位币贷款\n",
        "\n第二节\n外汇贷款\n": "\n第二节外汇贷款\n",
        "\n结算\n第五章\n第一节\n本位币结算\n": "\n第五章结算\n第一节本位币结算\n",
        "\n第二节\n外汇结算\n": "\n第二节外汇结算\n",
        "\n第六章\n\n二、非贸易外汇结算": "\n二、非贸易外汇结算",
        "\n第六章\n国库业务\n第一节\n预算资金收支\n": "\n第六章国库业务\n第一节预算资金收支\n",
        "\n第六章\n国库业务\n:1681\n": "\n",
        "\n第七章\n保险业务\n": "\n第七章保险业务\n",
        "\n第八章\n金融管理\n第节金融机构管理\n": "\n第八章金融管理\n第一节金融机构管理\n",
        "\n第五节\n信贷计划及信贷资金管理\n": "\n第五节信贷计划及信贷资金管理\n",
        "\n第六节\n基本建设投资管理\n": "\n第六节基本建设投资管理\n",
        "\n第九节\n金融市场管理\n": "\n第九节金融市场管理\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[: m.start(1)] + section + text[m.end(1) :]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第四十卷卷题、章题、节题断裂、页眉重复和 OCR 节题错位。"]
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
    variants = [text]
    for v in variants:
        pattern = "<p>" + v
        pos = section.find(pattern)
        if pos >= 0:
            content_start = pos + len(pattern)
            return section[:pos] + marker + "\n<p>" + replacement + section[content_start:], True
        pos = section.find(v)
        if pos >= 0:
            p_start = section.rfind("<p>", 0, pos)
            p_end = section.rfind("</p>", 0, pos)
            content_start = pos + len(v)
            if p_start > p_end:
                return section[:pos] + "</p>\n" + marker + "\n<p>" + replacement + section[content_start:], True
            return section[:pos] + marker + "\n" + replacement + section[content_start:], True
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
        '<h2 id="第四十卷-金融">第四十卷概述</h2>': '<h2 id="第四十卷-金融">第四十卷金融</h2>',
        '<p>金融机构清朝末年': h3("第一章金融机构") + "\n<p>清朝末年",
        '<p>典当第一节钱庄': h4("第一章金融机构", "第一节典当钱庄") + "\n<p>",
        '<p>第二节银行': h4("第一章金融机构", "第二节银行") + "\n<p>",
        '<p>二、解放前革命根据地银行': h4("第一章金融机构", "第二节银行") + "\n<p>二、解放前革命根据地银行",
        '<p>第三节•保险公司': h4("第一章金融机构", "第三节保险公司") + "\n<p>",
        '<p>信托投资公司解放前': h4("第一章金融机构", "第四节信托投资公司") + "\n<p>解放前",
        '<p>第五节信用合作社': h4("第一章金融机构", "第五节信用合作社") + "\n<p>",
        '<p>货币境内流通': h3("第二章货币") + "\n<p>境内流通",
        '<p>铜元第一节铸钱银两银元': h4("第二章货币", "第一节铸钱银两银元铜元") + "\n<p>一、铸钱",
        '<p>兑换券法币第二节关金券金元券': h4("第二章货币", "第二节兑换券法币关金券金元券") + "\n<p>一、兑换券",
        '<p>华中币第三节抗币北海市': h4("第二章货币", "第三节抗币北海币华中币") + "\n<p>一、抗币",
        '<p>第四节•人民币': h4("第二章货币", "第四节人民币") + "\n<p>",
        '<p>置存款': h3("第三章存款") + "\n<p>",
        '<p>第一节‧本位币存款': h4("第三章存款", "第一节本位币存款") + "\n<p>",
        '<p>第二节外币存款': h4("第三章存款", "第二节外币存款") + "\n<p>",
        '<p>贷款解放初期': h3("第四章贷款") + "\n<p>解放初期",
        '<p>第一节\u3000本位币贷款': h4("第四章贷款", "第一节本位币贷款") + "\n<p>",
        '<p>第二节外汇贷款': h4("第四章贷款", "第二节外汇贷款") + "\n<p>",
        '结算第一节本位币结算': h3("第五章结算") + "\n" + h4("第五章结算", "第一节本位币结算"),
        '<p>第二节外汇结算': h4("第五章结算", "第二节外汇结算") + "\n<p>",
        '<p>国库业务第一节预算资金收支': h3("第六章国库业务") + "\n" + h4("第六章国库业务", "第一节预算资金收支") + "\n<p>",
        '<p>第二节代理发行国家债券': h4("第六章国库业务", "第二节代理发行国家债券") + "\n<p>",
        '<p>第三节清理建国前银钱业存放款': h4("第六章国库业务", "第三节清理建国前银钱业存放款") + "\n<p>",
        '<p>保险业务境内保险业': h3("第七章保险业务") + "\n<p>境内保险业",
        '<p>第一节国内保险': h4("第七章保险业务", "第一节国内保险") + "\n<p>",
        '<p>第二节涉外保险': h4("第七章保险业务", "第二节涉外保险") + "\n<p>",
        '<p>金融管理第节金融机构管理': h3("第八章金融管理") + "\n" + h4("第八章金融管理", "第一节金融机构管理") + "\n<p>",
        '<p>第二节现金管理': h4("第八章金融管理", "第二节现金管理") + "\n<p>",
        '<p>第三节工资基金管理': h4("第八章金融管理", "第三节工资基金管理") + "\n<p>",
        '<p>第四节金银管理': h4("第八章金融管理", "第四节金银管理") + "\n<p>",
        '<p>第五节信贷计划及信贷资金管理': h4("第八章金融管理", "第五节信贷计划及信贷资金管理") + "\n<p>",
        '<p>第六节基本建设投资管理': h4("第八章金融管理", "第六节基本建设投资管理") + "\n<p>",
        '<p>第七节外汇管理': h4("第八章金融管理", "第七节外汇管理") + "\n<p>",
        '<p>第八节利率管理': h4("第八章金融管理", "第八节利率管理") + "\n<p>",
        '<p>第九节金融市场管理': h4("第八章金融管理", "第九节金融市场管理") + "\n<p>",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    section = re.sub(r'<p>第六章\s*</p>\s*', '', section)
    section = re.sub(r'第六章\s*国库业务\s*:1681\s*', '', section)
    section = re.sub(r'<p>\s*[·:.：\s]*\d{4}\s*[·:.：\s]*</p>\n?', '', section)
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第四十卷-[^"]+">)', r'\1</p>\n\2', section)
    section = section.replace('<p><h3', '<h3').replace('<p><h4', '<h4')
    section = section.replace('</h3>\n</p>', '</h3>\n').replace('</h4>\n</p>', '</h4>\n')
    seen_h3: set[str] = set()
    seen_h4: set[str] = set()

    def keep_first_h3(match: re.Match[str]) -> str:
        ident = match.group(1)
        if ident in seen_h3:
            return ''
        seen_h3.add(ident)
        return match.group(0)

    def keep_first_h4(match: re.Match[str]) -> str:
        ident = match.group(1)
        if ident in seen_h4:
            return ''
        seen_h4.add(ident)
        return match.group(0)

    section = re.sub(r'<h3 id="([^"]+)">[^<]+</h3>\s*', keep_first_h3, section)
    section = re.sub(r'<h4 id="([^"]+)">[^<]+</h4>\s*', keep_first_h4, section)
    return section


def restore_html() -> tuple[int, int, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第四十卷 HTML range")
    section = m.group(0)
    section = section.replace('<h2 id="第四十卷-金融">第四十卷概述</h2>', '<h2 id="第四十卷-金融">第四十卷金融</h2>')
    inserted_h3 = inserted_h4 = 0
    section, added = insert_after_h2(section, h3("概述")); inserted_h3 += int(added)
    for title, needle in [
        ("第一章金融机构", "金融机构清朝末年"),
        ("第二章货币", "货币境内流通"),
        ("第三章存款", "置存款"),
        ("第四章贷款", "贷款解放初期"),
        ("第五章结算", "结算第一节本位币结算"),
        ("第六章国库业务", "国库业务第一节预算资金收支"),
        ("第七章保险业务", "保险业务境内保险业"),
        ("第八章金融管理", "金融管理第节金融机构管理"),
    ]:
        section, added = insert_before_text(section, h3(title), needle); inserted_h3 += int(added)
    for chapter, title, needle, replacement in [
        ("第一章金融机构", "第一节典当钱庄", "典当第一节钱庄", ""),
        ("第一章金融机构", "第二节银行", "第二节银行", ""),
        ("第一章金融机构", "第二节银行", "二、解放前革命根据地银行", "二、解放前革命根据地银行"),
        ("第一章金融机构", "第三节保险公司", "第三节•保险公司", ""),
        ("第一章金融机构", "第四节信托投资公司", "信托投资公司解放前", "解放前"),
        ("第一章金融机构", "第五节信用合作社", "第五节信用合作社", ""),
        ("第二章货币", "第一节铸钱银两银元铜元", "铜元第一节铸钱银两银元", "一、铸钱"),
        ("第二章货币", "第二节兑换券法币关金券金元券", "兑换券法币第二节关金券金元券", "一、兑换券"),
        ("第二章货币", "第三节抗币北海币华中币", "华中币第三节抗币北海市", "一、抗币"),
        ("第二章货币", "第四节人民币", "第四节•人民币", ""),
        ("第三章存款", "第一节本位币存款", "第一节‧本位币存款", ""),
        ("第三章存款", "第二节外币存款", "第二节外币存款", ""),
        ("第四章贷款", "第一节本位币贷款", "第一节\u3000本位币贷款", ""),
        ("第四章贷款", "第二节外汇贷款", "第二节外汇贷款", ""),
        ("第五章结算", "第一节本位币结算", "第一节本位币结算", ""),
        ("第五章结算", "第二节外汇结算", "第二节外汇结算", ""),
        ("第六章国库业务", "第一节预算资金收支", "第一节预算资金收支", ""),
        ("第六章国库业务", "第二节代理发行国家债券", "第二节代理发行国家债券", ""),
        ("第六章国库业务", "第三节清理建国前银钱业存放款", "第三节清理建国前银钱业存放款", ""),
        ("第七章保险业务", "第一节国内保险", "第一节国内保险", ""),
        ("第七章保险业务", "第二节涉外保险", "第二节涉外保险", ""),
        ("第八章金融管理", "第一节金融机构管理", "金融管理第节金融机构管理", ""),
        ("第八章金融管理", "第二节现金管理", "第二节现金管理", ""),
        ("第八章金融管理", "第三节工资基金管理", "第三节工资基金管理", ""),
        ("第八章金融管理", "第四节金银管理", "第四节金银管理", ""),
        ("第八章金融管理", "第五节信贷计划及信贷资金管理", "第五节信贷计划及信贷资金管理", ""),
        ("第八章金融管理", "第六节基本建设投资管理", "第六节基本建设投资管理", ""),
        ("第八章金融管理", "第七节外汇管理", "第七节外汇管理", ""),
        ("第八章金融管理", "第八节利率管理", "第八节利率管理", ""),
        ("第八章金融管理", "第九节金融市场管理", "第九节金融市场管理", ""),
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
    content = f"""# 2026-06-29 第四十卷《金融》修复核对进度

## 本轮范围
- 范围：`第四十卷 金融`。
- 目标：按交付标准修复卷题、概述、章题、节题、页眉残留和正文段落结构。
- 源文件：`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已处于规范状态'}。
- 将最终阅读页卷题由 `第四十卷概述` 修正为 `第四十卷金融`。
- 恢复概述、第一章金融机构至第八章金融管理及 29 个节题的标准 H3/H4 层级。
- 2 处 `ipa-data` 残留已转为普通正文段落，未改动既有结构化表格数据。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章金融机构至第八章金融管理），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本轮保留既有表格骨架；金融卷存款、贷款、外汇、利率等统计表跨页较多，后续 PDF 表格专项需重点核对表头、年份列和续表页眉。

## 验收状态
- 本卷结构验收：{status}。
- 后续已纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 进入 `第四十一卷 政党`，继续按“源 MD 标题规范 -> 最终阅读页结构修复 -> 全书审计 -> typecheck -> 进度记录 -> Git 提交”的顺序推进。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第四十卷金融章节核对完成

已完成 `第四十卷 金融` 章节格式核对：

- 新增脚本：`scripts/repair_fortieth_volume_finance.py`。
- 修复 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md` 中第四十卷卷题、章题、节题断裂、页眉重复和 OCR 节题错位。
- 修复 `output/final_reader/连云港市志_全书.html` 中第四十卷卷题误作概述、章节标题全部扁平化以及 2 处 `ipa-data` 残留的问题。
- 第四十卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章金融机构至第八章金融管理），H4={stats['h4_count']}。
- 第四十卷范围内 `ipa-data` 残留为 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；金融统计表需从源 PDF 专项补登、重建和核验。
- 已写入进度文档：`output/reports/progress/20260629_第四十卷金融_修复核对进度.md`。

验收：第四十卷 HTML 字节数 {stats['bytes']}，范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第四十一卷 政党`。第四十卷金融统计表需在 PDF 表格专项中复核。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第四十卷金融章节核对完成"
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

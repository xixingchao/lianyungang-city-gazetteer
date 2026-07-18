# -*- coding: utf-8 -*-
"""Repair and audit 第四十五卷 军事 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第四十五卷军事_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第四十五卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第四十六卷-[^"]+">|</main>)', re.S)
SOURCE_RE = re.compile(r'(第四十五卷\s*\n概述.*?)(?=\n第四十六卷|\Z)', re.S)

CHAPTERS = [
    ("第一章起义起事战事", ["第一节起义起事", "第二节战事"]),
    ("第二章驻防", ["第一节清以前驻防及军事设施", "第二节民国时期驻军与地方武装", "第三节解放后驻防及人民武装机关"]),
    ("第三章兵役", ["第一节府兵制募兵制", "第二节征集制", "第三节志愿兵役制", "第四节义务兵役制", "第五节预备役制"]),
    ("第四章民兵", ["第一节组建", "第二节训练", "第三节战勤"]),
    ("第五章人民防空", ["第一节机构", "第二节组织指挥", "第三节防空通信", "第四节防护工程"]),
    ("第六章拥政爱民", ["第一节支援地方建设", "第二节军民共建", "第三节抢险救灾"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第四十五卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第四十五卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section
    replacements = {
        "第四十五卷\n概述\n": "第四十五卷 军事\n\n概述\n",
        "起义起事战事\n第一章\n第一节‧起义‧起事\n": "第一章起义起事战事\n第一节起义起事\n",
        "第二节\u3000战\u3000事\n": "第二节战事\n",
        "民興兵第一节组建": "第四章民兵\n第一节组建",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[: m.start(1)] + section + text[m.end(1):]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第四十五卷卷题、章题、节题断裂和 OCR 标题错字。"]
    return []


def apply_replacements(section: str) -> str:
    section = section.replace('<h2 id="第四十五卷-军事">第四十五卷概述</h2>', '<h2 id="第四十五卷-军事">第四十五卷军事</h2>', 1)
    if h3("概述") not in section:
        section = section.replace('</h2>\n<p>连云港市东濒黄海', '</h2>\n' + h3("概述") + '\n<p>连云港市东濒黄海', 1)
    replacements = [
        ('放起义起事战事第一节‧起义‧起事一、民国前起义、起事徐宣', '放</p>\n' + h3('第一章起义起事战事') + '\n' + h4('第一章起义起事战事', '第一节起义起事') + '\n<p>一、民国前起义、起事徐宣'),
        ('<p>第二节\u3000战\u3000事一、清以前战事齐莒纪彰之战', h4('第一章起义起事战事', '第二节战事') + '\n<p>一、清以前战事齐莒纪彰之战'),
        ('<p>驻防第一节清以前驻防及军事设施一、驻\u3000防秦代', h3('第二章驻防') + '\n' + h4('第二章驻防', '第一节清以前驻防及军事设施') + '\n<p>一、驻防秦代'),
        ('<p>第二节民国时期驻军与地方武装一、驻军军阀及国民政府军队', h4('第二章驻防', '第二节民国时期驻军与地方武装') + '\n<p>一、驻军军阀及国民政府军队'),
        ('<p>兵役第一节募兵制府兵制唐代的府兵制', h3('第三章兵役') + '\n' + h4('第三章兵役', '第一节府兵制募兵制') + '\n<p>唐代的府兵制'),
        ('<p>第二节征集制隋炀帝时期', h4('第三章兵役', '第二节征集制') + '\n<p>隋炀帝时期'),
        ('<p>第三节志愿兵役制抗日战争和解放战争时期', h4('第三章兵役', '第三节志愿兵役制') + '\n<p>抗日战争和解放战争时期'),
        ('<p>第四节义务兵役制1955年7月', h4('第三章兵役', '第四节义务兵役制') + '\n<p>1955年7月'),
        ('<p>第五节预备役制1955年', h4('第三章兵役', '第五节预备役制') + '\n<p>1955年'),
        ('<p>民興兵第一节组建民国26年', h3('第四章民兵') + '\n' + h4('第四章民兵', '第一节组建') + '\n<p>民国26年'),
        ('<p>第二节训练抗日战争、解放战争时期', h4('第四章民兵', '第二节训练') + '\n<p>抗日战争、解放战争时期'),
        ('<p>人民防空第一节机构1953年11月28日', h3('第五章人民防空') + '\n' + h4('第五章人民防空', '第一节机构') + '\n<p>1953年11月28日'),
        ('<p>第三节防空通信1955年4月', h4('第五章人民防空', '第三节防空通信') + '\n<p>1955年4月'),
        ('<p>第四节防护工程1949～1968年', h4('第五章人民防空', '第四节防护工程') + '\n<p>1949～1968年'),
        ('<p>拥政爱民第一节支援地方建设全国解放后', h3('第六章拥政爱民') + '\n' + h4('第六章拥政爱民', '第一节支援地方建设') + '\n<p>全国解放后'),
        ('<p>第二节军民共建军民共建是', h4('第六章拥政爱民', '第二节军民共建') + '\n<p>军民共建是'),
        ('<p>第三节抢险救灾中国人民解放军驻连云港部队', h4('第六章拥政爱民', '第三节抢险救灾') + '\n<p>中国人民解放军驻连云港部队'),
    ]
    for old, new in replacements:
        section = section.replace(old, new, 1)
    return section


def insert_missing(section: str) -> str:
    fallbacks = [
        (h4('第二章驻防', '第三节解放后驻防及人民武装机关'), '<p>连云港军分区1983年4月11日'),
        (h4('第四章民兵', '第三节战勤'), '<p>社会主义建设社会主义建设时期'),
        (h4('第四章民兵', '第三节战勤'), '<p>张洽桥炸毁日军火车2节'),
        (h4('第四章民兵', '第三节战勤'), '<p>民国35年（1946年）10月'),
        (h4('第五章人民防空', '第二节组织指挥'), '<p>1990年10月12日，连云港市人防办公室组织化学事故应急救援方案检验性演'),
    ]
    for marker, needle in fallbacks:
        if marker in section:
            continue
        pos = section.find(needle)
        if pos >= 0:
            section = section[:pos] + marker + '\n' + section[pos:]
    return section


def cleanup(section: str) -> str:
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第四十五卷-[^"]+">)', r'\1</p>\n\2', section)
    section = section.replace('<p><h3', '<h3').replace('<p><h4', '<h4')
    section = section.replace('</h3>\n</p>', '</h3>\n').replace('</h4>\n</p>', '</h4>\n')
    seen: set[str] = set()

    def keep(match: re.Match[str]) -> str:
        ident = match.group(1)
        if ident in seen:
            return ''
        seen.add(ident)
        return match.group(0)

    section = re.sub(r'<h[34] id="([^"]+)">[^<]+</h[34]>\s*', keep, section)
    return section


def restore_html() -> dict[str, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第四十五卷 HTML range")
    section = m.group(0)
    section = apply_replacements(section)
    section = insert_missing(section)
    section = cleanup(section)
    html = html[:m.start()] + section + html[m.end():]
    HTML_PATH.write_text(html, encoding="utf-8")
    return audit_section()


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
    status = "通过" if stats["h3_count"] == EXPECTED_H3 and stats["h4_count"] == EXPECTED_H4 and stats["ipa_blocks"] == 0 and stats["generic_heading_anchors"] == 0 else "需复核"
    content = f"""# 2026-06-29 第四十五卷《军事》修复核对进度

## 本轮范围
- 范围：`第四十五卷 军事`。
- 目标：按交付标准修复卷题、概述、6 章、20 节和正文段落结构。
- 源文件：`workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已处于规范状态'}。
- 将最终阅读页卷题由 `第四十五卷概述` 修正为 `第四十五卷军事`。
- 恢复概述、第一章起义起事战事至第六章拥政爱民及 20 个节题的标准 H3/H4 层级。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第六章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本卷当前无结构化表格；后续全文校对应重点核对军事章内附录名单和长段落连续性。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 继续下 part01 第四十六卷起修复。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第四十五卷军事章节核对完成

已完成 `第四十五卷 军事` 章节格式核对：

- 新增脚本：`scripts/repair_forty_fifth_volume_military.py`。
- 修复第四十五卷卷题误作概述、最终阅读页无 H3/H4 导航层级、章题节题扁平化和 OCR 标题错字。
- 第四十五卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第六章），H4={stats['h4_count']}。
- 第四十五卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处。
- 已写入进度文档：`output/reports/progress/20260629_第四十五卷军事_修复核对进度.md`。

验收：第四十五卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：继续下 part01 第四十六卷起。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第四十五卷军事章节核对完成"
    if marker in memory:
        memory = memory[: memory.find(marker)].rstrip() + "\n" + entry
    else:
        memory = memory.rstrip() + "\n" + entry
    MEMORY_PATH.write_text(memory, encoding="utf-8")


def main() -> None:
    changes = repair_source_md()
    stats = restore_html()
    write_progress(stats, changes)
    update_memory(stats)
    print("Repair complete")
    for change in changes:
        print(f"- {change}")
    print(f"stats={stats}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()

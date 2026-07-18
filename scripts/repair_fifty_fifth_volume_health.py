# -*- coding: utf-8 -*-
"""Repair and audit 第五十五卷 卫生 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第五十五卷卫生_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第五十五卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第五十六卷-[^"]+">|</main>)', re.S)
SOURCE_RE = re.compile(r'(^第五十五卷.*?)(?=^第五十六卷|\Z)', re.S | re.M)

CHAPTERS = [
    ("第一章公共卫生", ["第一节爱国卫生", "第二节劳动卫生", "第三节食品卫生", "第四节学校卫生", "第五节环境卫生"]),
    ("第二章常见病防治", ["第一节传染病防治", "第二节寄生虫病防治", "第三节地方病防治", "第四节计划免疫"]),
    ("第三章医疗", ["第一节中医", "第二节西医", "第三节中西医结合", "第四节护理"]),
    ("第四章医政 药政", ["第一节个体行医管理", "第二节农村医疗管理", "第三节城市医院管理", "第四节药政管理", "第五节药品检验"]),
    ("第五章保健疗养", ["第一节妇女保健", "第二节儿童保健", "第三节干部保健", "第四节知识分子保健", "第五节疗养"]),
    ("第六章教育 科研", ["第一节教育", "第二节科研"]),
    ("第七章卫生机构", ["第一节连云港市卫生局", "第二节区、县卫生局", "第三节医疗单位选介"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第五十五卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第五十五卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section
    replacements = {
        "第五十五卷\n概述\n": "第五十五卷 卫生\n\n概述\n",
        "公共卫生\n第节爱国卫生": "第一章公共卫生\n第一节爱国卫生",
        "医疗\n第三章\n第一节中医": "第三章医疗\n第一节中医",
        "第二节西\n": "第二节西医\n",
        "医政\n药政\n第四章\n个体行医管理\n第节": "第四章医政 药政\n第一节个体行医管理",
        "第五章\n保健疗养\n第节妇女保健": "第五章保健疗养\n第一节妇女保健",
        "第二节·儿童保健": "第二节儿童保健",
        "第五节‘疗·养": "第五节疗养",
        "第六章\n教育\n科研\n第一节教•育": "第六章教育 科研\n第一节教育",
        "第七章\n卫生机构\n第一节\n连云港市卫生局": "第七章卫生机构\n第一节连云港市卫生局",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[:m.start(1)] + section + text[m.end(1):]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第五十五卷卷题、章题、节题断裂和 OCR 标题误字。"]
    return []


def sub_once(section: str, pattern: str, repl: str) -> str:
    section, _ = re.subn(pattern, repl, section, count=1, flags=re.S)
    return section


def normalize_ipa(section: str) -> str:
    return re.sub(r'<div class="ipa-data">\s*(.*?)\s*</div>', r'<p>\1</p>', section, flags=re.S)


def apply_replacements(section: str) -> str:
    section = normalize_ipa(section)
    section = re.sub(r'<h2 id="第五十五卷-[^"]+">.*?</h2>', '<h2 id="第五十五卷-卫生">第五十五卷卫生</h2>', section, count=1, flags=re.S)
    if h3("概述") not in section:
        section = section.replace('<h2 id="第五十五卷-卫生">第五十五卷卫生</h2>\n<p>', '<h2 id="第五十五卷-卫生">第五十五卷卫生</h2>\n' + h3("概述") + '\n<p>', 1)

    replacements = [
        (r'<p>公共卫生第节爱国卫生', h3('第一章公共卫生') + '\n' + h4('第一章公共卫生', '第一节爱国卫生') + '\n<p>'),
        (r'<p>第二节劳动卫生', h4('第一章公共卫生', '第二节劳动卫生') + '\n<p>'),
        (r'<p>第三节食品卫生', h4('第一章公共卫生', '第三节食品卫生') + '\n<p>'),
        (r'<p>第四节学校卫生', h4('第一章公共卫生', '第四节学校卫生') + '\n<p>'),
        (r'<p>第五节环境卫生', h4('第一章公共卫生', '第五节环境卫生') + '\n<p>'),
        (r'<p>常见病防治第一节传染病防治', h3('第二章常见病防治') + '\n' + h4('第二章常见病防治', '第一节传染病防治') + '\n<p>'),
        (r'<p>第二节寄生虫病防治', h4('第二章常见病防治', '第二节寄生虫病防治') + '\n<p>'),
        (r'<p>第三节地方病防治', h4('第二章常见病防治', '第三节地方病防治') + '\n<p>'),
        (r'<p>第四节计划免疫', h4('第二章常见病防治', '第四节计划免疫') + '\n<p>'),
        (r'<p>医疗第一节中医', h3('第三章医疗') + '\n' + h4('第三章医疗', '第一节中医') + '\n<p>'),
        (r'<p>第二节西一、起源和发展', h4('第三章医疗', '第二节西医') + '\n<p>一、起源和发展'),
        (r'<p>第三节中西医结合', h4('第三章医疗', '第三节中西医结合') + '\n<p>'),
        (r'<p>第四节护理', h4('第三章医疗', '第四节护理') + '\n<p>'),
        (r'<p>医政药政个体行医管理第节', h3('第四章医政 药政') + '\n' + h4('第四章医政 药政', '第一节个体行医管理') + '\n<p>'),
        (r'申请开业者第二节农村医疗管理', r'申请开业者</p>\n' + h4('第四章医政 药政', '第二节农村医疗管理') + '\n<p>'),
        (r'<p>第三节城市医院管理', h4('第四章医政 药政', '第三节城市医院管理') + '\n<p>'),
        (r'<p>第四节药政管理', h4('第四章医政 药政', '第四节药政管理') + '\n<p>'),
        (r'<p>第五节药品检验', h4('第四章医政 药政', '第五节药品检验') + '\n<p>'),
        (r'<p>保健疗养第节妇女保健', h3('第五章保健疗养') + '\n' + h4('第五章保健疗养', '第一节妇女保健') + '\n<p>'),
        (r'<p>第二节·儿童保健', h4('第五章保健疗养', '第二节儿童保健') + '\n<p>'),
        (r'<p>第三节干部保健', h4('第五章保健疗养', '第三节干部保健') + '\n<p>'),
        (r'<p>第四节知识分子保健', h4('第五章保健疗养', '第四节知识分子保健') + '\n<p>'),
        (r'<p>第五节‘疗·养', h4('第五章保健疗养', '第五节疗养') + '\n<p>'),
        (r'<p>教育科研第一节教•育', h3('第六章教育 科研') + '\n' + h4('第六章教育 科研', '第一节教育') + '\n<p>'),
        (r'<p>第二节科研', h4('第六章教育 科研', '第二节科研') + '\n<p>'),
        (r'(科研单位：南京医学院、东海县人民医院)卫生机构第一节连云港市卫生局', r'\1</p>\n' + h3('第七章卫生机构') + '\n' + h4('第七章卫生机构', '第一节连云港市卫生局') + '\n<p>'),
        (r'<p>第二节区、县卫生局', h4('第七章卫生机构', '第二节区、县卫生局') + '\n<p>'),
        (r'<p>第三节医疗单位选介', h4('第七章卫生机构', '第三节医疗单位选介') + '\n<p>'),
    ]
    for pattern, repl in replacements:
        section = sub_once(section, pattern, repl)
    return section


def cleanup(section: str) -> str:
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第五十五卷-[^"]+">)', r'\1</p>\n\2', section)
    section = section.replace('<p><h3', '<h3').replace('<p><h4', '<h4')
    section = re.sub(r'(</h[34]>)\s*</p>', r'\1', section)
    seen: set[str] = set()

    def keep(match: re.Match[str]) -> str:
        ident = match.group(1)
        if ident in seen:
            return ''
        seen.add(ident)
        return match.group(0)

    return re.sub(r'<h[34] id="([^"]+)">[^<]+</h[34]>\s*', keep, section)


def restore_html() -> dict[str, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第五十五卷 HTML range")
    section = cleanup(apply_replacements(m.group(0)))
    HTML_PATH.write_text(html[:m.start()] + section + html[m.end():], encoding="utf-8")
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
    content = f"""# 2026-06-29 第五十五卷《卫生》修复核对进度

## 本轮范围
- 范围：`第五十五卷 卫生`。
- 目标：按交付标准修复卷题、概述、7 章、28 节和正文段落结构。
- 源文件：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已完成规范化，脚本复跑保持幂等'}。
- 将最终阅读页卷题统一为 `第五十五卷卫生`。
- 恢复概述、第一章公共卫生至第七章卫生机构及 28 个节题的标准 H3/H4 层级。
- 将本卷 `ipa-data` 数据块转回普通段落。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第七章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 卫生机构统计表跨 p2645-p2647，仍需后续 PDF 表格专项逐格核对；本轮保留现有结构化表格，不做表格内容重录。

## 遇到的问题与处理
- 卷题误显示为 `第五十五卷概述`，已修为 `第五十五卷卫生` 并补入概述层级。
- 多处章题和节题被拼入正文，如 `公共卫生第节爱国卫生`、`保健疗养第节妇女保健`，已按目录拆回。
- `第二节西`、`教•育`、`第五节‘疗·养` 等 OCR 标题误字已按目录归一为 `西医`、`教育`、`疗养`。
- 第七章前接科研项目正文，已在 `科研单位：南京医学院、东海县人民医院` 后拆出 `第七章卫生机构`。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 继续第五十六卷起修复。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第五十五卷卫生章节核对完成

已完成 `第五十五卷 卫生` 章节格式核对：

- 新增脚本：`scripts/repair_fifty_fifth_volume_health.py`。
- 修复第五十五卷卷题误作概述、最终阅读页无 H3/H4 导航层级、章题节题扁平化、OCR 标题误字和 `ipa-data` 正文块。
- 第五十五卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第七章），H4={stats['h4_count']}。
- 第五十五卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处。
- 已写入进度文档：`output/reports/progress/20260629_第五十五卷卫生_修复核对进度.md`。

验收：第五十五卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：继续第五十六卷起。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第五十五卷卫生章节核对完成"
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

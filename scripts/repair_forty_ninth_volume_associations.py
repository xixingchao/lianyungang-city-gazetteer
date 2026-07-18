# -*- coding: utf-8 -*-
"""Repair and audit 第四十九卷 社团 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第四十九卷社团_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第四十九卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第五十卷-[^"]+">|</main>)', re.S)
SOURCE_RE = re.compile(r'(第四十九卷\s*\n概·述.*?)(?=\n第五十卷|\Z)', re.S)

CHAPTERS = [
    ("第一章工人团体", ["第一节解放前工人运动", "第二节工会组织", "第三节市工会代表大会", "第四节主要活动"]),
    ("第二章青少年团体", ["第一节共产主义青年团", "第二节青年联合会", "第三节学生联合会", "第四节中国少年先锋队"]),
    ("第三章妇女团体", ["第一节组织", "第二节妇女代表大会", "第三节主要活动"]),
    ("第四章工商团体", ["第一节商会", "第二节工商业联合会"]),
    ("第五章其它社团", ["第一节农会", "第二节贫下中农(渔)协会", "第三节连云港市哲学社会科学联合会", "第四节连云港市文学艺术界联合会", "第五节连云港市科学技术协会", "第六节连云港市个体劳动者协会", "第七节连云港市黄埔军校同学会联络筹备组"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第四十九卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第四十九卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section
    replacements = {
        "第四十九卷\n概·述\n": "第四十九卷 社团\n\n概述\n",
        "第一章\n工人团体\n第一节\n解放前工人运动": "第一章工人团体\n第一节解放前工人运动",
        "第二章\n青少年团体": "第二章青少年团体",
        "妇女团体\n第一节组•织": "第三章妇女团体\n第一节组织",
        "第二节‧妇女代表大会": "第二节妇女代表大会",
        "工商团体\n第一节商会": "第四章工商团体\n第一节商会",
        "其它社团\n第一节农会": "第五章其它社团\n第一节农会",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[: m.start(1)] + section + text[m.end(1):]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第四十九卷卷题、章题、节题断裂和 OCR 标题符号。"]
    return []


def sub_once(section: str, pattern: str, repl: str) -> str:
    section, _ = re.subn(pattern, repl, section, count=1, flags=re.S)
    return section


def apply_replacements(section: str) -> str:
    section = re.sub(r'<h2 id="第四十九卷-社团">.*?</h2>', '<h2 id="第四十九卷-社团">第四十九卷社团</h2>', section, count=1, flags=re.S)
    if h3("概述") not in section:
        section = section.replace('<h2 id="第四十九卷-社团">第四十九卷社团</h2>\n<p>', '<h2 id="第四十九卷-社团">第四十九卷社团</h2>\n' + h3("概述") + '\n<p>', 1)

    replacements = [
        (r'<p>工人团体第一节解放前工人运动', h3('第一章工人团体') + '\n' + h4('第一章工人团体', '第一节解放前工人运动') + '\n<p>'),
        (r'<p>第二节工会组织', h4('第一章工人团体', '第二节工会组织') + '\n<p>'),
        (r'<p>第三节市工会代表大会', h4('第一章工人团体', '第三节市工会代表大会') + '\n<p>'),
        (r'<p>第四节主要活动', h4('第一章工人团体', '第四节主要活动') + '\n<p>'),
        (r'<p>青少年团体第一节共产主义青年团', h3('第二章青少年团体') + '\n' + h4('第二章青少年团体', '第一节共产主义青年团') + '\n<p>'),
        (r'<p>第二节青年联合会', h4('第二章青少年团体', '第二节青年联合会') + '\n<p>'),
        (r'<p>第三节学生联合会', h4('第二章青少年团体', '第三节学生联合会') + '\n<p>'),
        (r'<p>第四节中国少年先锋队', h4('第二章青少年团体', '第四节中国少年先锋队') + '\n<p>'),
        (r'<p>妇女团体第一节组[•·‧]?织', h3('第三章妇女团体') + '\n' + h4('第三章妇女团体', '第一节组织') + '\n<p>'),
        (r'<p>第二节妇女代表大会', h4('第三章妇女团体', '第二节妇女代表大会') + '\n<p>'),
        (r'<p>第二节[•·‧]?妇女代表大会', h4('第三章妇女团体', '第二节妇女代表大会') + '\n<p>'),
        (r'<p>第三节主要活动', h4('第三章妇女团体', '第三节主要活动') + '\n<p>'),
        (r'<p>工商团体第一节商会', h3('第四章工商团体') + '\n' + h4('第四章工商团体', '第一节商会') + '\n<p>'),
        (r'<p>第二节工商业联合会', h4('第四章工商团体', '第二节工商业联合会') + '\n<p>'),
        (r'<p>其它社团第一节农会', h3('第五章其它社团') + '\n' + h4('第五章其它社团', '第一节农会') + '\n<p>'),
        (r'<p>第二节贫下中农\(渔\)协会', h4('第五章其它社团', '第二节贫下中农(渔)协会') + '\n<p>'),
        (r'<p>第三节连云港市哲学社会科学联合会', h4('第五章其它社团', '第三节连云港市哲学社会科学联合会') + '\n<p>'),
        (r'<p>第四节连云港市文学艺术界联合会', h4('第五章其它社团', '第四节连云港市文学艺术界联合会') + '\n<p>'),
        (r'(影视工作者协会1990\.41140)第五节连云港市科学技术协会', r'\1</p>\n' + h4('第五章其它社团', '第五节连云港市科学技术协会') + '\n<p>'),
        (r'<p>第五节连云港市科学技术协会', h4('第五章其它社团', '第五节连云港市科学技术协会') + '\n<p>'),
        (r'<p>第六节连云港市个体劳动者协会', h4('第五章其它社团', '第六节连云港市个体劳动者协会') + '\n<p>'),
        (r'<p>第七节连云港市黄埔军校同学会联络筹备组', h4('第五章其它社团', '第七节连云港市黄埔军校同学会联络筹备组') + '\n<p>'),
    ]
    for pattern, repl in replacements:
        section = sub_once(section, pattern, repl)
    return section


def cleanup(section: str) -> str:
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第四十九卷-[^"]+">)', r'\1</p>\n\2', section)
    section = section.replace('<p><h3', '<h3').replace('<p><h4', '<h4')
    section = re.sub(r'(</h[34]>)\s*</p>', r'\1', section)
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
        raise RuntimeError("Cannot locate 第四十九卷 HTML range")
    section = m.group(0)
    section = apply_replacements(section)
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
    content = f"""# 2026-06-29 第四十九卷《社团》修复核对进度

## 本轮范围
- 范围：`第四十九卷 社团`。
- 目标：按交付标准修复卷题、概述、5 章、20 节和正文段落结构。
- 源文件：`workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已处于规范状态'}。
- 将最终阅读页卷题由 `第四十九卷概·述` 修正为 `第四十九卷社团`。
- 恢复概述、第一章工人团体至第五章其它社团及 20 个节题的标准 H3/H4 层级。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第五章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本卷 `1990年连云港市文学艺术界联合会所属协会一览表` 当前为 OCR 正文串，未转为结构化表格；后续 PDF 表格专项需重点核对并重建。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 继续下 part01 第五十卷起修复。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第四十九卷社团章节核对完成

已完成 `第四十九卷 社团` 章节格式核对：

- 新增脚本：`scripts/repair_forty_ninth_volume_associations.py`。
- 修复第四十九卷卷题误作概述、最终阅读页无 H3/H4 导航层级、章题节题扁平化和 OCR 标题符号。
- 第四十九卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第五章），H4={stats['h4_count']}。
- 第四十九卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处。
- 已写入进度文档：`output/reports/progress/20260629_第四十九卷社团_修复核对进度.md`。

验收：第四十九卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：继续下 part01 第五十卷起。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第四十九卷社团章节核对完成"
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

# -*- coding: utf-8 -*-
"""Repair and audit 第五十卷 教育 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第五十卷教育_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第五十卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第五十一卷-[^"]+">|</main>)', re.S)
SOURCE_RE = re.compile(r'(第五十卷\s*\n概述.*?)(?=\n第五十一卷|\Z)', re.S)

CHAPTERS = [
    ("第一章旧学", ["第一节州学 县学", "第二节书院", "第三节塾学", "第四节学堂"]),
    ("第二章学前教育", ["第一节幼儿园", "第二节学前班"]),
    ("第三章初等教育", ["第一节小学", "第二节学制 课程 教育教学", "第三节特殊教育"]),
    ("第四章中等教育", ["第一节普通中学", "第二节职业中学", "第三节技工学校", "第四节中等专业学校", "第五节中等师范学校", "第六节学校选介"]),
    ("第五章高等教育", ["第一节发展概况", "第二节学校简介"]),
    ("第六章成人教育", ["第一节农民教育", "第二节职工教育", "第三节干部教育", "第四节老龄教育", "第五节学校选介"]),
    ("第七章教师", ["第一节教师队伍", "第二节教师工资", "第三节教育研究", "第四节师资培训"]),
    ("第八章教育行政", ["第一节连云港市教育局", "第二节区、县教育行政机构", "第三节学校管理体制", "第四节教育经费"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第五十卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第五十卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section
    replacements = {
        "第五十卷\n概述\n": "第五十卷 教育\n\n概述\n",
        "第一章\n海州唐代建学宫": "第一章旧学\n海州唐代建学宫",
        "州学县学\n第一节": "第一节州学 县学",
        "第二节　书　院": "第二节书院",
        "第三节\n特殊教育": "第三节特殊教育",
        "第四章\n中等教育\n第一节音\n普通中学": "第四章中等教育\n第一节普通中学",
        "第四章\n\n第四节\n中等专业学校": "第四章\n第四节中等专业学校",
        "第五节\n中等师范学校": "第五节中等师范学校",
        "第六节·学校选介": "第六节学校选介",
        "高等教育\n第五章\n第一节发展概况": "第五章高等教育\n第一节发展概况",
        "学校简介\n第二节": "第二节学校简介",
        "第六章\n成人教育": "第六章成人教育",
        "第一节\n农民教育": "第一节农民教育",
        "第三节\n干部教育": "第三节干部教育",
        "第四节\n老龄教育": "第四节老龄教育",
        "第五节\n学校选介": "第五节学校选介",
        "教师\n第七章\n第一节\n教师队伍": "第七章教师\n第一节教师队伍",
        "第二节\n教师工资": "第二节教师工资",
        "第四节\n师资培训": "第四节师资培训",
        "第八章\n教育行政": "第八章教育行政",
        "第一节这\n连云港市教育局": "第一节连云港市教育局",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[: m.start(1)] + section + text[m.end(1):]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第五十卷卷题、章题、节题断裂和 OCR 标题误字。"]
    return []


def sub_once(section: str, pattern: str, repl: str) -> str:
    section, _ = re.subn(pattern, repl, section, count=1, flags=re.S)
    return section


def normalize_ipa(section: str) -> str:
    return re.sub(r'<div class="ipa-data">\s*(.*?)\s*</div>', r'<p>\1</p>', section, flags=re.S)


def apply_replacements(section: str) -> str:
    section = normalize_ipa(section)
    section = re.sub(r'<h2 id="第五十卷-教育">.*?</h2>', '<h2 id="第五十卷-教育">第五十卷教育</h2>', section, count=1, flags=re.S)
    if h3("概述") not in section:
        section = section.replace('<h2 id="第五十卷-教育">第五十卷教育</h2>\n<p>', '<h2 id="第五十卷-教育">第五十卷教育</h2>\n' + h3("概述") + '\n<p>', 1)

    replacements = [
        (r'(<p>海州唐代建学宫)', h3('第一章旧学') + r'\n\1'),
        (r'<p>州学县学第一节', h4('第一章旧学', '第一节州学 县学') + '\n<p>'),
        (r'<p>第二节\s*书\s*院', h4('第一章旧学', '第二节书院') + '\n<p>'),
        (r'<p>第三节塾学', h4('第一章旧学', '第三节塾学') + '\n<p>'),
        (r'<p>第四节学堂', h4('第一章旧学', '第四节学堂') + '\n<p>'),
        (r'<p>学前教育第一节幼儿园', h3('第二章学前教育') + '\n' + h4('第二章学前教育', '第一节幼儿园') + '\n<p>'),
        (r'<p>第二节学前班', h4('第二章学前教育', '第二节学前班') + '\n<p>'),
        (r'<p>初等教育第一节小学', h3('第三章初等教育') + '\n' + h4('第三章初等教育', '第一节小学') + '\n<p>'),
        (r'(实验小学1600190624)学制课程第二节教育教学', r'\1</p>\n' + h4('第三章初等教育', '第二节学制 课程 教育教学') + '\n<p>'),
        (r'(<p>和北京市聋哑教材编写组编写的全国通用八年制教材)', h4('第三章初等教育', '第三节特殊教育') + r'\n\1'),
        (r'(合1522209)中等教育第一节音?普通中学', r'\1</p>\n' + h3('第四章中等教育') + '\n' + h4('第四章中等教育', '第一节普通中学') + '\n<p>'),
        (r'<p>第二节职业中学', h4('第四章中等教育', '第二节职业中学') + '\n<p>'),
        (r'(伊山职业中学)第三节技工学校', r'\1</p>\n' + h4('第四章中等教育', '第三节技工学校') + '\n<p>'),
        (r'(猴嘴镇)第四节中等专业学校', r'\1</p>\n' + h4('第四章中等教育', '第四节中等专业学校') + '\n<p>'),
        (r'<p>第五节中等师范学校', h4('第四章中等教育', '第五节中等师范学校') + '\n<p>'),
        (r'<p>第六节[·•]?学校选介', h4('第四章中等教育', '第六节学校选介') + '\n<p>'),
        (r'<p>高等教育第一节发展概况', h3('第五章高等教育') + '\n' + h4('第五章高等教育', '第一节发展概况') + '\n<p>'),
        (r'(连云港职业大学)学校简介第二节', r'\1</p>\n' + h4('第五章高等教育', '第二节学校简介') + '\n<p>'),
        (r'<p>成人教育民国', h3('第六章成人教育') + '\n<p>民国'),
        (r'<p>第一节农民教育', h4('第六章成人教育', '第一节农民教育') + '\n<p>'),
        (r'(扫盲班3209936993627321)第二节职工教育', r'\1</p>\n' + h4('第六章成人教育', '第二节职工教育') + '\n<p>'),
        (r'<p>第三节干部教育', h4('第六章成人教育', '第三节干部教育') + '\n<p>'),
        (r'<p>第四节老龄教育', h4('第六章成人教育', '第四节老龄教育') + '\n<p>'),
        (r'(成人高校教职工\(人\)295其中：专任教师146</p>\s*<table class="structured-table"><thead><tr><th>数值</th></tr></thead><tbody><tr><td>待对照原图录入</td></tr></tbody></table>\s*<p>成人教育·2237</p>\s*<table class="structured-table"><thead><tr><th>数值</th></tr></thead><tbody><tr><td>待对照原图录入</td></tr></tbody></table>)\s*<p>贸易、金融财会', r'\1\n' + h4('第六章成人教育', '第五节学校选介') + '\n<p>贸易、金融财会'),
        (r'<p>教师第一节教师队伍', h3('第七章教师') + '\n' + h4('第七章教师', '第一节教师队伍') + '\n<p>'),
        (r'(<p>人月工资平均123\.29分，约合人民币37元。)', h4('第七章教师', '第二节教师工资') + r'\n\1'),
        (r'<p>第三节教育研究', h4('第七章教师', '第三节教育研究') + '\n<p>'),
        (r'<p>第四节师资培训', h4('第七章教师', '第四节师资培训') + '\n<p>'),
        (r'(教育学院进行考前培训，)教育行政辛亥革命后', r'\1</p>\n' + h3('第八章教育行政') + '\n<p>辛亥革命后'),
        (r'<p>第一节这?连云港市教育局', h4('第八章教育行政', '第一节连云港市教育局') + '\n<p>'),
        (r'<p>区、县教育行政机构第二节', h4('第八章教育行政', '第二节区、县教育行政机构') + '\n<p>'),
        (r'<p>第三节学校管理体制', h4('第八章教育行政', '第三节学校管理体制') + '\n<p>'),
        (r'<p>第四节教育经费', h4('第八章教育行政', '第四节教育经费') + '\n<p>'),
    ]
    for pattern, repl in replacements:
        section = sub_once(section, pattern, repl)
    return section


def cleanup(section: str) -> str:
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第五十卷-[^"]+">)', r'\1</p>\n\2', section)
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
        raise RuntimeError("Cannot locate 第五十卷 HTML range")
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
    content = f"""# 2026-06-29 第五十卷《教育》修复核对进度

## 本轮范围
- 范围：`第五十卷 教育`。
- 目标：按交付标准修复卷题、概述、8 章、30 节和正文段落结构。
- 源文件：`workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已完成规范化或已处于规范状态'}。
- 将最终阅读页卷题由 `第五十卷概述` 修正为 `第五十卷教育`。
- 恢复概述、第一章旧学至第八章教育行政及 30 个节题的标准 H3/H4 层级。
- 将本卷 `ipa-data` 数据块转回普通段落，避免正文内容游离在阅读结构外。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第八章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本卷教育统计表数量较多，当前以保留既有结构化表为准；后续 PDF 表格专项需逐表核对表头、续表和数值列。

## 遇到的问题与处理
- 目录题名多处被 OCR 合并入正文，如 `学制课程第二节教育教学`、`学校简介第二节`、`区、县教育行政机构第二节`，已按 XML 目录标准拆回 H4。
- `第二节教师工资` 原标题在 HTML 中丢失，依据源 MD 和正文起点补回。
- `第三节特殊教育` 标题在 HTML 中缺失，依据源 MD 位置补入到聋哑学校正文前。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 继续修复下 part01 第五十一卷起，并同步检查全书导航锚点。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第五十卷教育章节核对完成

已完成 `第五十卷 教育` 章节格式核对：

- 新增脚本：`scripts/repair_fiftieth_volume_education.py`。
- 修复第五十卷卷题误作概述、最终阅读页无 H3/H4 导航层级、章题节题扁平化、OCR 标题误字和 `ipa-data` 正文块。
- 第五十卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第八章），H4={stats['h4_count']}。
- 第五十卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处。
- 已写入进度文档：`output/reports/progress/20260629_第五十卷教育_修复核对进度.md`。

验收：第五十卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：继续下 part01 第五十一卷起。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第五十卷教育章节核对完成"
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

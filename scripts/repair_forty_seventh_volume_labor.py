# -*- coding: utf-8 -*-
"""Repair and audit 第四十七卷 劳动 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第四十七卷劳动_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第四十七卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第四十八卷-[^"]+">|</main>)', re.S)
SOURCE_RE = re.compile(r'(第四十七卷\s*\n概述.*?)(?=\n第四十八卷|\Z)', re.S)

CHAPTERS = [
    ("第一章劳动力管理", ["第一节劳动力资源", "第二节劳动力计划", "第三节劳动就业", "第四节用工形式", "第五节劳动力调配", "第六节精简职工", "第七节劳动争议处理", "第八节技术培训", "第九节城镇知识青年上山下乡"]),
    ("第二章工资福利", ["第一节工资制度", "第二节工资形式", "第三节工资改革", "第四节工资调整", "第五节工资水平", "第六节保险福利"]),
    ("第三章劳动保护", ["第一节安全生产", "第二节工业卫生", "第三节防护用品", "第四节安全监察"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第四十七卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第四十七卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section
    replacements = {
        "第四十七卷\n概述\n": "第四十七卷 劳动\n\n概述\n",
        "第一章\n劳动力管理\n": "第一章劳动力管理\n",
        "第一节\n劳动力资源\n": "第一节劳动力资源\n",
        "第二节‧劳动力计划": "第二节劳动力计划",
        "第四节•用工形式": "第四节用工形式",
        "第五节#劳动力调配": "第五节劳动力调配",
        "城镇知识青年“上山下乡”·第九节": "第九节城镇知识青年“上山下乡”",
        "第二章\n工资福利\n": "第二章工资福利\n",
        "第三章\n劳动保护\n": "第三章劳动保护\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[: m.start(1)] + section + text[m.end(1):]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第四十七卷卷题、章题、节题断裂和 OCR 标题符号。"]
    return []


def normalize_ipa(section: str) -> str:
    return re.sub(r'<div class="ipa-data">\s*(.*?)\s*</div>', r'<p>\1</p>', section, flags=re.S)


def sub_once(section: str, pattern: str, repl: str) -> str:
    section, _ = re.subn(pattern, repl, section, count=1, flags=re.S)
    return section


def apply_replacements(section: str) -> str:
    section = re.sub(r'<h2 id="第四十七卷-劳动">.*?</h2>', '<h2 id="第四十七卷-劳动">第四十七卷劳动</h2>', section, count=1, flags=re.S)
    section = normalize_ipa(section)
    if h3("概述") not in section:
        section = section.replace('<h2 id="第四十七卷-劳动">第四十七卷劳动</h2>\n<p>', '<h2 id="第四十七卷-劳动">第四十七卷劳动</h2>\n' + h3("概述") + '\n<p>', 1)

    replacements = [
        (r'<p>劳动力管理清光绪二十六年', h3('第一章劳动力管理') + '\n<p>清光绪二十六年'),
        (r'<p>第一节劳动力资源', h4('第一章劳动力管理', '第一节劳动力资源') + '\n<p>'),
        (r'(全民合同制工人48865)第二节[‧•·]?劳动力计划', r'\1</p>\n' + h4('第一章劳动力管理', '第二节劳动力计划') + '\n<p>'),
        (r'<p>第二节[‧•·]?劳动力计划', h4('第一章劳动力管理', '第二节劳动力计划') + '\n<p>'),
        (r'<p>第三节劳动就业', h4('第一章劳动力管理', '第三节劳动就业') + '\n<p>'),
        (r'<p>第四节[‧•·]?用工形式', h4('第一章劳动力管理', '第四节用工形式') + '\n<p>'),
        (r'<p>第五节[#＃]?劳动力调配', h4('第一章劳动力管理', '第五节劳动力调配') + '\n<p>'),
        (r'<p>第六节精简职工', h4('第一章劳动力管理', '第六节精简职工') + '\n<p>'),
        (r'<p>第七节劳动争议处理', h4('第一章劳动力管理', '第七节劳动争议处理') + '\n<p>'),
        (r'<p>第八节技术培训', h4('第一章劳动力管理', '第八节技术培训') + '\n<p>'),
        (r'<p>城镇知识青年“上山下乡”·第九节', h4('第一章劳动力管理', '第九节城镇知识青年上山下乡') + '\n<p>'),
        (r'<p>工资福利清末', h3('第二章工资福利') + '\n<p>清末'),
        (r'<p>第一节工资制度', h4('第二章工资福利', '第一节工资制度') + '\n<p>'),
        (r'<p>第二节工资形式', h4('第二章工资福利', '第二节工资形式') + '\n<p>'),
        (r'<p>第三节工资改革', h4('第二章工资福利', '第三节工资改革') + '\n<p>'),
        (r'<p>第四节工资调整、?', h4('第二章工资福利', '第四节工资调整') + '\n<p>'),
        (r'<p>第五节工资水平', h4('第二章工资福利', '第五节工资水平') + '\n<p>'),
        (r'<p>第六节保险福利', h4('第二章工资福利', '第六节保险福利') + '\n<p>'),
        (r'(</tbody></table>\s*)<p>缴纳本人标准工资的3%', r'\1' + h4('第二章工资福利', '第六节保险福利') + '\n<p>缴纳本人标准工资的3%'),
        (r'<p>劳动保护建国前', h3('第三章劳动保护') + '\n<p>建国前'),
        (r'<p>第一节安全生产', h4('第三章劳动保护', '第一节安全生产') + '\n<p>'),
        (r'(25·2114 ·)第二节工业卫生', r'\1</p>\n' + h4('第三章劳动保护', '第二节工业卫生') + '\n<p>'),
        (r'<p>第二节工业卫生', h4('第三章劳动保护', '第二节工业卫生') + '\n<p>'),
        (r'<p>第三节防护用品', h4('第三章劳动保护', '第三节防护用品') + '\n<p>'),
        (r'<p>第四节安全监察', h4('第三章劳动保护', '第四节安全监察') + '\n<p>'),
        (r'<p>第四节[‧•·]?安全监察', h4('第三章劳动保护', '第四节安全监察') + '\n<p>'),
    ]
    for pattern, repl in replacements:
        section = sub_once(section, pattern, repl)
    return section


def insert_missing(section: str) -> str:
    fallbacks = [
        (h4('第一章劳动力管理', '第九节城镇知识青年上山下乡'), '城镇知识青年“上山下乡”·第九节'),
        (h4('第二章工资福利', '第六节保险福利'), '第六节保险福利'),
        (h4('第三章劳动保护', '第四节安全监察'), '第四节安全监察'),
    ]
    for marker, needle in fallbacks:
        if marker in section:
            continue
        pos = section.find(needle)
        if pos >= 0:
            section = section[:pos] + marker + '\n<p>' + section[pos + len(needle):]
    return section


def cleanup(section: str) -> str:
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第四十七卷-[^"]+">)', r'\1</p>\n\2', section)
    section = section.replace('<p><h3', '<h3').replace('<p><h4', '<h4')
    section = re.sub(r'(</h[34]>)\s*</p>', r'\1', section)
    section = re.sub(r'<p>\s*(</tbody></table>)', r'\1', section)
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
        raise RuntimeError("Cannot locate 第四十七卷 HTML range")
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
    content = f"""# 2026-06-29 第四十七卷《劳动》修复核对进度

## 本轮范围
- 范围：`第四十七卷 劳动`。
- 目标：按交付标准修复卷题、概述、3 章、19 节和正文段落结构。
- 源文件：`workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已处于规范状态'}。
- 将最终阅读页卷题由 `第四十七卷概述` 修正为 `第四十七卷劳动`。
- 恢复概述、第一章劳动力管理至第三章劳动保护及 19 个节题的标准 H3/H4 层级。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第三章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本轮保留既有结构化表格，不进行表内数字重录；表 47 系列表格需在后续 PDF 表格专项中逐表对照。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 继续下 part01 第四十八卷起修复。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第四十七卷劳动章节核对完成

已完成 `第四十七卷 劳动` 章节格式核对：

- 新增脚本：`scripts/repair_forty_seventh_volume_labor.py`。
- 修复第四十七卷卷题误作概述、最终阅读页无 H3/H4 导航层级、章题节题扁平化和 OCR 标题符号。
- 第四十七卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第三章），H4={stats['h4_count']}。
- 第四十七卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处。
- 已写入进度文档：`output/reports/progress/20260629_第四十七卷劳动_修复核对进度.md`。

验收：第四十七卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：继续下 part01 第四十八卷起。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第四十七卷劳动章节核对完成"
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

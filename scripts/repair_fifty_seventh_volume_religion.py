# -*- coding: utf-8 -*-
"""Repair and audit 第五十七卷 宗教 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第五十七卷宗教_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第五十七卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第五十八卷-[^"]+">|</main>)', re.S)
SOURCE_RE = re.compile(r'(^第五十七卷.*?)(?=^第五十八卷|\Z)', re.S | re.M)

CHAPTERS = [
    ("第一章佛教", ["第一节传布与活动", "第二节著名佛教建筑物"]),
    ("第二章道教", ["第一节活动", "第二节道教庙观"]),
    ("第三章伊斯兰教", ["第一节穆斯林", "第二节清真寺"]),
    ("第四章天主教", ["第一节传布与活动", "第二节活动范围"]),
    ("第五章基督教", ["第一节组织与活动", "第二节活动场所"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第五十七卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第五十七卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section
    replacements = {
        "第五十七卷\n概述\n": "第五十七卷 宗教\n\n概述\n",
        "第一章佛．教": "第一章佛教",
        "第一节‧↑\n传布与活动：": "第一节传布与活动",
        "第二节‧氵\n清真寺": "第二节清真寺",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[:m.start(1)] + section + text[m.end(1):]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第五十七卷卷题、章题、节题断裂和 OCR 标题误字。"]
    return []


def sub_once(section: str, pattern: str, repl: str) -> str:
    section, _ = re.subn(pattern, repl, section, count=1, flags=re.S)
    return section


def apply_replacements(section: str) -> str:
    section = re.sub(r'<h2 id="第五十七卷-[^"]+">.*?</h2>', '<h2 id="第五十七卷-宗教">第五十七卷宗教</h2>', section, count=1, flags=re.S)
    if h3("概述") not in section:
        section = section.replace('<h2 id="第五十七卷-宗教">第五十七卷宗教</h2>\n<p>', '<h2 id="第五十七卷-宗教">第五十七卷宗教</h2>\n' + h3("概述") + '\n<p>', 1)

    replacements = [
        (r'<p>自东汉佛教传入境内', h3('第一章佛教') + '\n<p>自东汉佛教传入境内'),
        (r'<p>第一节‧↑传布与活动：</p>\s*<p>一、传布', h4('第一章佛教', '第一节传布与活动') + '\n<p>一、传布'),
        (r'<p>第二节著名佛教建筑物', h4('第一章佛教', '第二节著名佛教建筑物') + '\n<p>'),
        (r'(中华民国六年十月东海县临洪市新浦阔行公立刘振殿撰东海刘允生书)道教境内方士、道士活动历史较久', r'\1</p>\n' + h3('第二章道教') + '\n<p>境内方士、道士活动历史较久'),
        (r'<p>第一节活动', h4('第二章道教', '第一节活动') + '\n<p>'),
        (r'<p>第二节道教庙观', h4('第二章道教', '第二节道教庙观') + '\n<p>'),
        (r'<p>伊斯兰教19世纪后期', h3('第三章伊斯兰教') + '\n<p>19世纪后期'),
        (r'<p>第一节穆斯林', h4('第三章伊斯兰教', '第一节穆斯林') + '\n<p>'),
        (r'<p>第二节‧氵清真寺', h4('第三章伊斯兰教', '第二节清真寺') + '\n<p>'),
        (r'<p>天主教第一节传布与活动', h3('第四章天主教') + '\n' + h4('第四章天主教', '第一节传布与活动') + '\n<p>'),
        (r'<p>第二节活动范围', h4('第四章天主教', '第二节活动范围') + '\n<p>'),
        (r'<p>基督教第一节组织与活动', h3('第五章基督教') + '\n' + h4('第五章基督教', '第一节组织与活动') + '\n<p>'),
        (r'<p>第二节活动场所', h4('第五章基督教', '第二节活动场所') + '\n<p>'),
    ]
    for pattern, repl in replacements:
        section = sub_once(section, pattern, repl)
    return section


def cleanup(section: str) -> str:
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第五十七卷-[^"]+">)', r'\1</p>\n\2', section)
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
        raise RuntimeError("Cannot locate 第五十七卷 HTML range")
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
    content = f"""# 2026-06-29 第五十七卷《宗教》修复核对进度

## 本轮范围
- 范围：`第五十七卷 宗教`。
- 目标：按交付标准修复卷题、概述、5 章、10 节和正文段落结构。
- 源文件：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已完成规范化，脚本复跑保持幂等'}。
- 将最终阅读页卷题统一为 `第五十七卷宗教`。
- 恢复概述、第一章佛教至第五章基督教及 10 个节题的标准 H3/H4 层级。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第五章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 天主教教职人员管辖范围等表格仍需后续 PDF 表格专项逐格核对；本轮保留现有结构化表格，不做表格内容重录。

## 遇到的问题与处理
- 卷题误显示为 `第五十七卷概述`，已修为 `第五十七卷宗教` 并补入概述层级。
- 佛教、道教、伊斯兰教、天主教、基督教章题均混入正文段落，已按目录恢复为 H3。
- `第一节‧↑传布与活动`、`第二节‧氵清真寺` 等 OCR 标题残符已按目录标准清理。
- 第二章道教前承接碑记正文，已在碑记末尾后拆出独立章题。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 继续第五十八卷起修复。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第五十七卷宗教章节核对完成

已完成 `第五十七卷 宗教` 章节格式核对：

- 新增脚本：`scripts/repair_fifty_seventh_volume_religion.py`。
- 修复第五十七卷卷题误作概述、最终阅读页无 H3/H4 导航层级、章题节题扁平化和 OCR 标题误字。
- 第五十七卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第五章），H4={stats['h4_count']}。
- 第五十七卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处。
- 已写入进度文档：`output/reports/progress/20260629_第五十七卷宗教_修复核对进度.md`。

验收：第五十七卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：继续第五十八卷起。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第五十七卷宗教章节核对完成"
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

# -*- coding: utf-8 -*-
"""Repair and audit 第四十八卷 外事侨务 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第四十八卷外事侨务_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第四十八卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第四十九卷-[^"]+">|</main>)', re.S)
SOURCE_RE = re.compile(r'(第四十八卷\s*\n外事侨务\s*\n概述.*?)(?=\n第四十九卷|\Z)', re.S)

CHAPTERS = [
    ("第一章外事", ["第一节外事往来", "第二节友好港口、城市", "第三节涉外管理"]),
    ("第二章侨务", ["第一节侨情", "第二节落实侨务政策", "第三节侨务活动"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第四十八卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第四十八卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section
    replacements = {
        "第四十八卷\n外事侨务\n概述\n": "第四十八卷 外事侨务\n\n概述\n",
        "外事\n第一章\n第一节外事往来": "第一章外事\n第一节外事往来",
        "置侨务\n第一章": "第二章侨务",
        "置侨务第一节•侨•情": "第二章侨务\n第一节侨情",
        "第一节•侨•情": "第一节侨情",
        "第三节佳侨务活动": "第三节侨务活动",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[: m.start(1)] + section + text[m.end(1):]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第四十八卷卷题、章题、节题断裂和 OCR 标题错字。"]
    return []


def sub_once(section: str, pattern: str, repl: str) -> str:
    section, _ = re.subn(pattern, repl, section, count=1, flags=re.S)
    return section


def apply_replacements(section: str) -> str:
    section = re.sub(r'<h2 id="第四十八卷-外事侨务">.*?</h2>', '<h2 id="第四十八卷-外事侨务">第四十八卷外事侨务</h2>', section, count=1, flags=re.S)
    if h3("概述") not in section:
        section = section.replace('<h2 id="第四十八卷-外事侨务">第四十八卷外事侨务</h2>\n<p>', '<h2 id="第四十八卷-外事侨务">第四十八卷外事侨务</h2>\n' + h3("概述") + '\n<p>', 1)

    replacements = [
        (r'<p>外事第一节外事往来', h3('第一章外事') + '\n' + h4('第一章外事', '第一节外事往来') + '\n<p>'),
        (r'<p>第二节友好港口、城市', h4('第一章外事', '第二节友好港口、城市') + '\n<p>'),
        (r'(\(1991年11月9日，两市政府代表在科雷奥郡签署缔结友好城市协议书\))第三节涉外管理', r'\1</p>\n' + h4('第一章外事', '第三节涉外管理') + '\n<p>'),
        (r'<p>第三节涉外管理', h4('第一章外事', '第三节涉外管理') + '\n<p>'),
        (r'<p>置?侨务第一节[•·‧]?侨[•·‧]?情', h3('第二章侨务') + '\n' + h4('第二章侨务', '第一节侨情') + '\n<p>'),
        (r'<p>第二节落实侨务政策', h4('第二章侨务', '第二节落实侨务政策') + '\n<p>'),
        (r'<p>第三节佳?侨务活动', h4('第二章侨务', '第三节侨务活动') + '\n<p>'),
    ]
    for pattern, repl in replacements:
        section = sub_once(section, pattern, repl)
    return section


def insert_missing(section: str) -> str:
    fallbacks = [
        (h4('第一章外事', '第三节涉外管理'), '第三节涉外管理'),
        (h3('第二章侨务') + '\n' + h4('第二章侨务', '第一节侨情'), '第一节•侨•情'),
        (h4('第二章侨务', '第三节侨务活动'), '第三节佳侨务活动'),
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
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第四十八卷-[^"]+">)', r'\1</p>\n\2', section)
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
        raise RuntimeError("Cannot locate 第四十八卷 HTML range")
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
    content = f"""# 2026-06-29 第四十八卷《外事侨务》修复核对进度

## 本轮范围
- 范围：`第四十八卷 外事侨务`。
- 目标：按交付标准修复概述、2 章、6 节和正文段落结构。
- 源文件：`workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已处于规范状态'}。
- 保持最终阅读页卷题 `第四十八卷外事侨务`，补齐概述 H3。
- 恢复第一章外事、第二章侨务及 6 个节题的标准 H3/H4 层级。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第二章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本卷当前无结构化表格；后续全文校对应重点核对长段落连续性和涉外人名 OCR。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 继续下 part01 第四十九卷起修复。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第四十八卷外事侨务章节核对完成

已完成 `第四十八卷 外事侨务` 章节格式核对：

- 新增脚本：`scripts/repair_forty_eighth_volume_foreign_affairs_overseas.py`。
- 修复第四十八卷最终阅读页无 H3/H4 导航层级、章题节题扁平化和 OCR 标题错字。
- 第四十八卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第二章），H4={stats['h4_count']}。
- 第四十八卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处。
- 已写入进度文档：`output/reports/progress/20260629_第四十八卷外事侨务_修复核对进度.md`。

验收：第四十八卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：继续下 part01 第四十九卷起。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第四十八卷外事侨务章节核对完成"
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

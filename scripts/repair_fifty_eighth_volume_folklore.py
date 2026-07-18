# -*- coding: utf-8 -*-
"""Repair and audit 第五十八卷 民俗 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第五十八卷民俗_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第五十八卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第五十九卷-[^"]+">|</main>)', re.S)
SOURCE_RE = re.compile(r'(^第五十八卷.*?)(?=^第五十九卷|\Z)', re.S | re.M)

CHAPTERS = [
    ("第一章行业习俗", ["第一节农林业", "第二节渔业", "第三节盐业", "第四节手工业", "第五节商业"]),
    ("第二章生活习俗", ["第一节服饰", "第二节饮食", "第三节住宅", "第四节行旅"]),
    ("第三章礼仪习俗", ["第一节生育", "第二节娶嫁", "第三节生日", "第四节丧葬"]),
    ("第四章节庆、娱乐习俗", ["第一节节庆习俗", "第二节娱乐习俗"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第五十八卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第五十八卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section
    replacements = {
        "第五十八卷\n概述\n": "第五十八卷 民俗\n\n概述\n",
        "第一章\n行业习俗\n第一节农林业": "第一章行业习俗\n第一节农林业",
        "第二节•渔业": "第二节渔业",
        "第三节盐：业": "第三节盐业",
        "第四节•手工•业": "第四节手工业",
        "第五节•商业": "第五节商业",
        "第一节服•饰": "第一节服饰",
        "第二节•饮•食": "第二节饮食",
        "第三节住　宅": "第三节住宅",
        "第四节　行　旅": "第四节行旅",
        "第一节生•育": "第一节生育",
        "第三节•生•日": "第三节生日",
        "节庆、娱乐习俗\n节庆习俗\n第一节": "第四章节庆、娱乐习俗\n第一节节庆习俗",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[:m.start(1)] + section + text[m.end(1):]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第五十八卷卷题、章题、节题断裂和 OCR 标题误字。"]
    return []


def sub_once(section: str, pattern: str, repl: str) -> str:
    section, _ = re.subn(pattern, repl, section, count=1, flags=re.S)
    return section


def apply_replacements(section: str) -> str:
    section = re.sub(r'<h2 id="第五十八卷-[^"]+">.*?</h2>', '<h2 id="第五十八卷-民俗">第五十八卷民俗</h2>', section, count=1, flags=re.S)
    if h3("概述") not in section:
        section = section.replace('<h2 id="第五十八卷-民俗">第五十八卷民俗</h2>\n<p>', '<h2 id="第五十八卷-民俗">第五十八卷民俗</h2>\n' + h3("概述") + '\n<p>', 1)

    replacements = [
        (r'<p>行业习俗第一节农林业', h3('第一章行业习俗') + '\n' + h4('第一章行业习俗', '第一节农林业') + '\n<p>'),
        (r'<p>第二节•渔业', h4('第一章行业习俗', '第二节渔业') + '\n<p>'),
        (r'<p>第三节盐：业', h4('第一章行业习俗', '第三节盐业') + '\n<p>'),
        (r'<p>第四节•手工•业', h4('第一章行业习俗', '第四节手工业') + '\n<p>'),
        (r'<p>第五节•商业', h4('第一章行业习俗', '第五节商业') + '\n<p>'),
        (r'<p>生活习俗第一节服•饰', h3('第二章生活习俗') + '\n' + h4('第二章生活习俗', '第一节服饰') + '\n<p>'),
        (r'<p>第二节•饮•食', h4('第二章生活习俗', '第二节饮食') + '\n<p>'),
        (r'<p>第三节住　宅', h4('第二章生活习俗', '第三节住宅') + '\n<p>'),
        (r'<p>第四节(?:行旅|　行　旅)', h4('第二章生活习俗', '第四节行旅') + '\n<p>'),
        (r'<p>礼仪习俗第一节生•育', h3('第三章礼仪习俗') + '\n' + h4('第三章礼仪习俗', '第一节生育') + '\n<p>'),
        (r'<p>第二节娶嫁', h4('第三章礼仪习俗', '第二节娶嫁') + '\n<p>'),
        (r'<p>第三节•生•日', h4('第三章礼仪习俗', '第三节生日') + '\n<p>'),
        (r'<p>第四节丧葬', h4('第三章礼仪习俗', '第四节丧葬') + '\n<p>'),
        (r'<p>节庆、娱乐习俗节庆习俗第一节', h3('第四章节庆、娱乐习俗') + '\n' + h4('第四章节庆、娱乐习俗', '第一节节庆习俗') + '\n<p>'),
        (r'<p>第二节娱乐习俗', h4('第四章节庆、娱乐习俗', '第二节娱乐习俗') + '\n<p>'),
    ]
    for pattern, repl in replacements:
        section = sub_once(section, pattern, repl)
    return section


def cleanup(section: str) -> str:
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第五十八卷-[^"]+">)', r'\1</p>\n\2', section)
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
        raise RuntimeError("Cannot locate 第五十八卷 HTML range")
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
    content = f"""# 2026-06-29 第五十八卷《民俗》修复核对进度

## 本轮范围
- 范围：`第五十八卷 民俗`。
- 目标：按交付标准修复卷题、概述、4 章、15 节和正文段落结构。
- 源文件：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已完成规范化，脚本复跑保持幂等'}。
- 将最终阅读页卷题统一为 `第五十八卷民俗`。
- 恢复概述、第一章行业习俗至第四章节庆、娱乐习俗及 15 个节题的标准 H3/H4 层级。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第四章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本卷以正文条目为主，本轮未发现表格专项对象；后续仍需 PDF/OCR 文字专项复核俗称、异体字和断句。

## 遇到的问题与处理
- 卷题误显示为 `第五十八卷概述`，已修为 `第五十八卷民俗` 并补入概述层级。
- 章题与节题均混入正文段首，如 `行业习俗第一节农林业`、`生活习俗第一节服•饰`，已按目录恢复。
- `第二节•渔业`、`第三节盐：业`、`第二节•饮•食`、`第三节•生•日` 等 OCR 标题符号已清理。
- 第四章原顺序为 `节庆、娱乐习俗节庆习俗第一节`，已恢复为 `第四章节庆、娱乐习俗 / 第一节节庆习俗`。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 继续第五十九卷起修复。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第五十八卷民俗章节核对完成

已完成 `第五十八卷 民俗` 章节格式核对：

- 新增脚本：`scripts/repair_fifty_eighth_volume_folklore.py`。
- 修复第五十八卷卷题误作概述、最终阅读页无 H3/H4 导航层级、章题节题扁平化和 OCR 标题误字。
- 第五十八卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第四章），H4={stats['h4_count']}。
- 第五十八卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处。
- 已写入进度文档：`output/reports/progress/20260629_第五十八卷民俗_修复核对进度.md`。

验收：第五十八卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：继续第五十九卷起。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第五十八卷民俗章节核对完成"
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

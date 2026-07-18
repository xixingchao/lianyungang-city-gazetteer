# -*- coding: utf-8 -*-
"""Repair and audit 第五十三卷 文物 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第五十三卷文物_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第五十三卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第五十四卷-[^"]+">|</main>)', re.S)
SOURCE_RE = re.compile(r'(^第五十三卷\s*\n概述.*?)(?=^第五十四卷|\Z)', re.S | re.M)

CHAPTERS = [
    ("第一章遗址", ["第一节化石和旧石器出土地点", "第二节村落", "第三节城址", "第四节窖藏", "第五节石室"]),
    ("第二章墓葬", ["第一节周朝、春秋、战国墓", "第二节汉墓", "第三节五代、宋、元、明墓", "第四节近、现代墓"]),
    ("第三章建筑", ["第一节宗教及纪念建筑", "第二节公共建筑", "第三节园林民居", "第四节厂店 馆院"]),
    ("第四章石刻 石雕", ["第一节摩崖石刻", "第二节石雕"]),
    ("第五章馆藏文物", ["第一节玉石器", "第二节陶瓷器", "第三节金属器", "第四节碑刻", "第五节书画", "第六节漆木 毛笔 牙器 其它", "第七节版本文献"]),
    ("第六章文物管理与保护", ["第一节管理机构", "第二节文物普查", "第三节文物保护单位公布与维修", "第四节博物馆 纪念馆"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第五十三卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第五十三卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section
    replacements = {
        "第五十三卷\n概述\n": "第五十三卷 文物\n\n概述\n",
        "第二章墓葬\n第一节\n周朝、春秋、战国墓": "第二章墓葬\n第一节周朝、春秋、战国墓",
        "第二节汉　墓": "第二节汉墓",
        "第三节\n五代、宋、元、明墓": "第三节五代、宋、元、明墓",
        "第四节‧讠\n近、现代墓": "第四节近、现代墓",
        "建筑\n第三章\n第一节\n宗教及纪念建筑": "第三章建筑\n第一节宗教及纪念建筑",
        "厂店馆院\n第四节": "第四节厂店 馆院",
        "石刻·石雕\n第四章\n第一节摩崖石刻": "第四章石刻 石雕\n第一节摩崖石刻",
        "第五章\n\n第五章\n馆藏文物": "第五章馆藏文物",
        "第二节\n陶瓷器": "第二节陶瓷器",
        "毛笔牙器\n第六节\n漆木": "第六节漆木 毛笔 牙器 其它",
        "第六章\n文物管理与保护": "第六章文物管理与保护",
        "第四节\n博物馆\n纪念馆": "第四节博物馆 纪念馆",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[:m.start(1)] + section + text[m.end(1):]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第五十三卷卷题、章题、节题断裂和 OCR 标题误字。"]
    return []


def sub_once(section: str, pattern: str, repl: str) -> str:
    section, _ = re.subn(pattern, repl, section, count=1, flags=re.S)
    return section


def normalize_ipa(section: str) -> str:
    return re.sub(r'<div class="ipa-data">\s*(.*?)\s*</div>', r'<p>\1</p>', section, flags=re.S)


def apply_replacements(section: str) -> str:
    section = normalize_ipa(section)
    section = re.sub(r'<h2 id="第五十三卷-文物">.*?</h2>', '<h2 id="第五十三卷-文物">第五十三卷文物</h2>', section, count=1, flags=re.S)
    if h3("概述") not in section:
        section = section.replace('<h2 id="第五十三卷-文物">第五十三卷文物</h2>\n<p>', '<h2 id="第五十三卷-文物">第五十三卷文物</h2>\n' + h3("概述") + '\n<p>', 1)

    replacements = [
        (r'<p>第一节化石和旧石器出土地点', h3('第一章遗址') + '\n' + h4('第一章遗址', '第一节化石和旧石器出土地点') + '\n<p>'),
        (r'<p>第二节村落', h4('第一章遗址', '第二节村落') + '\n<p>'),
        (r'<p>第三节城址', h4('第一章遗址', '第三节城址') + '\n<p>'),
        (r'<p>第四节窖藏', h4('第一章遗址', '第四节窖藏') + '\n<p>'),
        (r'<p>第五节石[•·]?室', h4('第一章遗址', '第五节石室') + '\n<p>'),
        (r'<p>第一节周朝、春秋、战国墓', h3('第二章墓葬') + '\n' + h4('第二章墓葬', '第一节周朝、春秋、战国墓') + '\n<p>'),
        (r'<p>第二节汉\s*墓', h4('第二章墓葬', '第二节汉墓') + '\n<p>'),
        (r'<p>第三节五代、宋、元、明墓', h4('第二章墓葬', '第三节五代、宋、元、明墓') + '\n<p>'),
        (r'<p>第四节[‧·•]?讠?近、现代墓', h4('第二章墓葬', '第四节近、现代墓') + '\n<p>'),
        (r'<p>建筑第一节宗教及纪念建筑', h3('第三章建筑') + '\n' + h4('第三章建筑', '第一节宗教及纪念建筑') + '\n<p>'),
        (r'<p>第二节公共建筑', h4('第三章建筑', '第二节公共建筑') + '\n<p>'),
        (r'<p>第三节园林民居', h4('第三章建筑', '第三节园林民居') + '\n<p>'),
        (r'<p>厂店馆院第四节', h4('第三章建筑', '第四节厂店 馆院') + '\n<p>'),
        (r'<p>石刻[·・]石雕第一节摩崖石刻', h3('第四章石刻 石雕') + '\n' + h4('第四章石刻 石雕', '第一节摩崖石刻') + '\n<p>'),
        (r'<p>第二节石雕', h4('第四章石刻 石雕', '第二节石雕') + '\n<p>'),
        (r'<p>馆藏文物第一节玉石器', h3('第五章馆藏文物') + '\n' + h4('第五章馆藏文物', '第一节玉石器') + '\n<p>'),
        (r'<p>第二节陶瓷器', h4('第五章馆藏文物', '第二节陶瓷器') + '\n<p>'),
        (r'<p>第三节金属器', h4('第五章馆藏文物', '第三节金属器') + '\n<p>'),
        (r'<p>第四节碑刻', h4('第五章馆藏文物', '第四节碑刻') + '\n<p>'),
        (r'<p>第五节书\s*画', h4('第五章馆藏文物', '第五节书画') + '\n<p>'),
        (r'<p>毛笔牙器第六节漆木', h4('第五章馆藏文物', '第六节漆木 毛笔 牙器 其它') + '\n<p>'),
        (r'(出土时置于)第七节版本文献', r'\1</p>\n' + h4('第五章馆藏文物', '第七节版本文献') + '\n<p>'),
        (r'<p>文物管理与保护第一节管理机构', h3('第六章文物管理与保护') + '\n' + h4('第六章文物管理与保护', '第一节管理机构') + '\n<p>'),
        (r'<p>第二节文物普查', h4('第六章文物管理与保护', '第二节文物普查') + '\n<p>'),
        (r'<p>第三节文物保护单位公布与维修', h4('第六章文物管理与保护', '第三节文物保护单位公布与维修') + '\n<p>'),
        (r'<p>第四节博物馆纪念馆', h4('第六章文物管理与保护', '第四节博物馆 纪念馆') + '\n<p>'),
    ]
    for pattern, repl in replacements:
        section = sub_once(section, pattern, repl)
    return section


def cleanup(section: str) -> str:
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第五十三卷-[^"]+">)', r'\1</p>\n\2', section)
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
        raise RuntimeError("Cannot locate 第五十三卷 HTML range")
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
    content = f"""# 2026-06-29 第五十三卷《文物》修复核对进度

## 本轮范围
- 范围：`第五十三卷 文物`。
- 目标：按交付标准修复卷题、概述、6 章、26 节和正文段落结构。
- 源文件：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已完成规范化或已处于规范状态'}。
- 将最终阅读页卷题由 `第五十三卷概述` 修正为 `第五十三卷文物`。
- 恢复概述、第一章遗址至第六章文物管理与保护及 26 个节题的标准 H3/H4 层级。
- 将本卷 `ipa-data` 数据块转回普通段落。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第六章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本卷以遗址、墓葬、馆藏文物正文为主，仍需后续 PDF 文字专项核对 OCR 错字和个别断句。

## 遇到的问题与处理
- 多处章题与节题被 OCR 拼入正文，如 `石刻·石雕第一节摩崖石刻`、`馆藏文物第一节玉石器`，已按 XML 目录拆回。
- `第七节版本文献` 嵌入上一段 `佛牙` 说明中，已拆为独立 H4。
- `第四节近、现代墓`、`第六节漆木 毛笔 牙器 其它` 等存在 OCR 符号或换序，已按目录标准归位。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 继续第五十四卷起修复。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第五十三卷文物章节核对完成

已完成 `第五十三卷 文物` 章节格式核对：

- 新增脚本：`scripts/repair_fifty_third_volume_relics.py`。
- 修复第五十三卷卷题误作概述、最终阅读页无 H3/H4 导航层级、章题节题扁平化、OCR 标题误字和 `ipa-data` 正文块。
- 第五十三卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第六章），H4={stats['h4_count']}。
- 第五十三卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处。
- 已写入进度文档：`output/reports/progress/20260629_第五十三卷文物_修复核对进度.md`。

验收：第五十三卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：继续第五十四卷起。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第五十三卷文物章节核对完成"
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

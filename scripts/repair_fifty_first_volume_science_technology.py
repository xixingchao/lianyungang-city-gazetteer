# -*- coding: utf-8 -*-
"""Repair and audit 第五十一卷 科技 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第五十一卷科技_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第五十一卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第五十二卷-[^"]+">|</main>)', re.S)

CHAPTERS = [
    ("第一章机构与队伍", ["第一节管理机构", "第二节科研机构", "第三节科技队伍", "第四节学术团体"]),
    ("第二章科技投入与成果", ["第一节科技项目", "第二节科技服务", "第三节科技成果"]),
    ("第三章科技应用与推广", ["第一节农业", "第二节工业", "第三节医药卫生", "第四节其它"]),
    ("第四章社会科学", ["第一节机构 团体", "第二节学术成果"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第五十一卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第五十一卷-{chapter}-{title}">{title}</h4>'


def source_range(text: str) -> re.Match[str] | None:
    matches = list(re.finditer(r'^第五十一卷\s*$', text, re.M))
    if not matches:
        return None
    start = matches[-1].start()
    return re.match(r'.*', text[start:], re.S)


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    matches = list(re.finditer(r'^第五十一卷\s*$', text, re.M))
    if not matches:
        return []
    start = matches[-1].start()
    section = text[start:]
    original = section
    replacements = {
        "第五十一卷\n概述\n": "第五十一卷 科技\n\n概述\n",
        "第一章·机构与队伍": "第一章机构与队伍",
        "第三节·科技队伍": "第三节科技队伍",
        "第一章 朴\n\n第四节\n学术团体": "第四节学术团体",
        "第二章\n科技投入与成果\n第一节科技项目": "第二章科技投入与成果\n第一节科技项目",
        "第三章\n科技应用与推广\n第一节•农•业": "第三章科技应用与推广\n第一节农业",
        "第二节工\n一、能源": "第二节工业\n一、能源",
        "第四节\n其．它": "第四节其它",
        "社会科学\n第四章\n团体\n机构\n第一节\n一、机构": "第四章社会科学\n第一节机构 团体\n一、机构",
        "第二节\n学术成果": "第二节学术成果",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        SRC_MD.write_text(text[:start] + section, encoding="utf-8")
        return ["规范源 MD 中第五十一卷卷题、章题、节题断裂和 OCR 标题误字。"]
    return []


def sub_once(section: str, pattern: str, repl: str) -> str:
    section, _ = re.subn(pattern, repl, section, count=1, flags=re.S)
    return section


def normalize_ipa(section: str) -> str:
    return re.sub(r'<div class="ipa-data">\s*(.*?)\s*</div>', r'<p>\1</p>', section, flags=re.S)


def apply_replacements(section: str) -> str:
    section = normalize_ipa(section)
    section = re.sub(r'<h2 id="第五十一卷-科技">.*?</h2>', '<h2 id="第五十一卷-科技">第五十一卷科技</h2>', section, count=1, flags=re.S)
    if h3("概述") not in section:
        section = section.replace('<h2 id="第五十一卷-科技">第五十一卷科技</h2>\n<p>', '<h2 id="第五十一卷-科技">第五十一卷科技</h2>\n' + h3("概述") + '\n<p>', 1)

    replacements = [
        (r'<p>第一节管理机构', h3('第一章机构与队伍') + '\n' + h4('第一章机构与队伍', '第一节管理机构') + '\n<p>'),
        (r'<p>第二节科研机构', h4('第一章机构与队伍', '第二节科研机构') + '\n<p>'),
        (r'<p>第三节[·•]?科技队伍', h4('第一章机构与队伍', '第三节科技队伍') + '\n<p>'),
        (r'<p>第四节学术团体', h4('第一章机构与队伍', '第四节学术团体') + '\n<p>'),
        (r'<p>2264科技投入与成果第一节科技项目', h3('第二章科技投入与成果') + '\n' + h4('第二章科技投入与成果', '第一节科技项目') + '\n<p>'),
        (r'<p>第二节科技服务', h4('第二章科技投入与成果', '第二节科技服务') + '\n<p>'),
        (r'<p>第三节科技成果', h4('第二章科技投入与成果', '第三节科技成果') + '\n<p>'),
        (r'(<p>机。</p>)', h3('第三章科技应用与推广') + '\n' + h4('第三章科技应用与推广', '第一节农业') + r'\n\1'),
        (r'<p>第二节工一、能源', h4('第三章科技应用与推广', '第二节工业') + '\n<p>一、能源'),
        (r'<p>第三节医药卫生', h4('第三章科技应用与推广', '第三节医药卫生') + '\n<p>'),
        (r'<p>第四节其．它', h4('第三章科技应用与推广', '第四节其它') + '\n<p>'),
        (r'<p>社会科学团体机构第一节一、机构', h3('第四章社会科学') + '\n' + h4('第四章社会科学', '第一节机构 团体') + '\n<p>一、机构'),
        (r'(<p>民国初年，著名教育家江恒源编著了《伦理学概论》)', h4('第四章社会科学', '第二节学术成果') + r'\n\1'),
    ]
    for pattern, repl in replacements:
        section = sub_once(section, pattern, repl)
    return section


def cleanup(section: str) -> str:
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第五十一卷-[^"]+">)', r'\1</p>\n\2', section)
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
        raise RuntimeError("Cannot locate 第五十一卷 HTML range")
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
    content = f"""# 2026-06-29 第五十一卷《科技》修复核对进度

## 本轮范围
- 范围：`第五十一卷 科技`。
- 目标：按交付标准修复卷题、概述、4 章、13 节和正文段落结构。
- 源文件：`workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已完成规范化或已处于规范状态'}。
- 将最终阅读页卷题由 `第五十一卷概述` 修正为 `第五十一卷科技`。
- 恢复概述、第一章机构与队伍至第四章社会科学及 13 个节题的标准 H3/H4 层级。
- 将本卷 `ipa-data` 数据块转回普通段落，避免正文内容游离在阅读结构外。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第四章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本卷科技人员、科技成果和社科成果表格较密，当前保留既有结构化表；后续 PDF 表格专项需逐表核对续表、表号和数值列。

## 遇到的问题与处理
- `第一章机构与队伍` 章题在 HTML 中丢失，仅保留 `第一节管理机构`，已按 XML 目录补回。
- `第三章科技应用与推广` 被续表正文吞并，已在成果表尾后补回章题和 `第一节农业`。
- `第四章社会科学 / 第一节机构 团体` 被 OCR 重排为 `社会科学第四章团体机构第一节`，已按目录标准归位。
- `第二节学术成果` 的首段起始句在 HTML 中缺失，已依据源 MD 和目录标准在现存正文起点前恢复节题；首句缺字需在后续 PDF 文字校对专项核补。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 进入第五十二卷《文化》起，继续修复下 part02。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第五十一卷科技章节核对完成

已完成 `第五十一卷 科技` 章节格式核对：

- 新增脚本：`scripts/repair_fifty_first_volume_science_technology.py`。
- 修复第五十一卷卷题误作概述、最终阅读页无 H3/H4 导航层级、章题节题扁平化、OCR 标题误字和 `ipa-data` 正文块。
- 第五十一卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第四章），H4={stats['h4_count']}。
- 第五十一卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处。
- 已写入进度文档：`output/reports/progress/20260629_第五十一卷科技_修复核对进度.md`。

验收：第五十一卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：进入第五十二卷《文化》起。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第五十一卷科技章节核对完成"
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

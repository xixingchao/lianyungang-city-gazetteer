# -*- coding: utf-8 -*-
"""Repair and audit 第五十四卷 报刊 广播 电视 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第五十四卷报刊广播电视_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第五十四卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第五十五卷-[^"]+">|</main>)', re.S)
SOURCE_RE = re.compile(r'(^第五十四卷.*?)(?=^第五十五卷|\Z)', re.S | re.M)

CHAPTERS = [
    ("第一章报纸", ["第一节综合报纸", "第二节行(专)业报纸"]),
    ("第二章刊物", ["第一节文艺刊物", "第二节专业刊物", "第三节校刊"]),
    ("第三章广播", ["第一节有线广播", "第二节无线广播", "第三节广播节目设置"]),
    ("第四章电视", ["第一节电视台站", "第二节电视节目设置", "第三节电视讯号传输"]),
    ("第五章其它新闻机构和团体", ["第一节新华通讯社支社", "第二节记者站", "第三节新闻工作者协会 新闻学会"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第五十四卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第五十四卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section
    replacements = {
        "第五十四卷\n广播电视\n报刊\n概述\n": "第五十四卷 报刊 广播 电视\n\n概述\n",
        "行(专)业报纸\n第二节": "第二节行(专)业报纸",
        "第二章\n连云港最早出版的刊物": "第二章刊物\n连云港最早出版的刊物",
        "第一节\n有线广播": "第一节有线广播",
        "第二节.无线广播": "第二节无线广播",
        "电昇视\n第四章\n": "第四章电视\n",
        "第一节亲\n新华通讯社支社": "第一节新华通讯社支社",
        "新闻学会\n第三节\n新闻工作者协会": "第三节新闻工作者协会 新闻学会",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[:m.start(1)] + section + text[m.end(1):]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第五十四卷卷题、章题、节题断裂和 OCR 标题误字。"]
    return []


def sub_once(section: str, pattern: str, repl: str) -> str:
    section, _ = re.subn(pattern, repl, section, count=1, flags=re.S)
    return section


def normalize_ipa(section: str) -> str:
    return re.sub(r'<div class="ipa-data">\s*(.*?)\s*</div>', r'<p>\1</p>', section, flags=re.S)


def apply_replacements(section: str) -> str:
    section = normalize_ipa(section)
    section = re.sub(
        r'<h2 id="第五十四卷-[^"]+">.*?</h2>',
        '<h2 id="第五十四卷-报刊广播-电视">第五十四卷报刊广播电视</h2>',
        section,
        count=1,
        flags=re.S,
    )
    if h3("概述") not in section:
        section = section.replace(
            '<h2 id="第五十四卷-报刊广播-电视">第五十四卷报刊广播电视</h2>\n<p>',
            '<h2 id="第五十四卷-报刊广播-电视">第五十四卷报刊广播电视</h2>\n' + h3("概述") + '\n<p>',
            1,
        )

    replacements = [
        (r'<p>第一节综合报纸', h3('第一章报纸') + '\n' + h4('第一章报纸', '第一节综合报纸') + '\n<p>'),
        (r'(连云港报1958\s*~陈天柱)行\(专\)业报纸第二节', r'\1</p>\n' + h4('第一章报纸', '第二节行(专)业报纸') + '\n<p>'),
        (r'(?<!>)连云港最早出版的刊物', h3('第二章刊物') + '\n<p>连云港最早出版的刊物'),
        (r'<p>第一节文艺刊物', h4('第二章刊物', '第一节文艺刊物') + '\n<p>'),
        (r'<p>第二节专业刊物', h4('第二章刊物', '第二节专业刊物') + '\n<p>'),
        (r'<p>第三节校刊', h4('第二章刊物', '第三节校刊') + '\n<p>'),
        (r'<p>第一节有线广播', h3('第三章广播') + '\n' + h4('第三章广播', '第一节有线广播') + '\n<p>'),
        (r'<p>第二节\.无线广播', h4('第三章广播', '第二节无线广播') + '\n<p>'),
        (r'<p>第三节广播节目设置', h4('第三章广播', '第三节广播节目设置') + '\n<p>'),
        (r'<p>电昇视1971年10月1日', h3('第四章电视') + '\n<p>1971年10月1日'),
        (r'<p>第一节电视台站', h4('第四章电视', '第一节电视台站') + '\n<p>'),
        (r'<p>第二节电视节目设置', h4('第四章电视', '第二节电视节目设置') + '\n<p>'),
        (r'<p>第三节电视讯号传输', h4('第四章电视', '第三节电视讯号传输') + '\n<p>'),
        (r'<p>其它新闻机构和团体建国前后', h3('第五章其它新闻机构和团体') + '\n<p>建国前后'),
        (r'<p>第一节亲新华通讯社支社', h4('第五章其它新闻机构和团体', '第一节新华通讯社支社') + '\n<p>'),
        (r'<p>第二节记者站', h4('第五章其它新闻机构和团体', '第二节记者站') + '\n<p>'),
        (r'新闻学会第三节新闻工作者协会', h4('第五章其它新闻机构和团体', '第三节新闻工作者协会 新闻学会') + '\n<p>'),
    ]
    for pattern, repl in replacements:
        section = sub_once(section, pattern, repl)
    return section


def cleanup(section: str) -> str:
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第五十四卷-[^"]+">)', r'\1</p>\n\2', section)
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
        raise RuntimeError("Cannot locate 第五十四卷 HTML range")
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
    content = f"""# 2026-06-29 第五十四卷《报刊 广播 电视》修复核对进度

## 本轮范围
- 范围：`第五十四卷 报刊 广播 电视`。
- 目标：按交付标准修复卷题、概述、5 章、14 节和正文段落结构。
- 源文件：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已完成规范化，脚本复跑保持幂等'}。
- 将最终阅读页卷题统一为 `第五十四卷报刊广播电视`。
- 恢复概述、第一章报纸至第五章其它新闻机构和团体及 14 个节题的标准 H3/H4 层级。
- 将本卷 `ipa-data` 数据块转回普通段落。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第五章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 报刊、广播、电视节目表仍需后续 PDF 表格专项逐格核对，本轮保留现有结构化表格，不做表格内容重录。

## 遇到的问题与处理
- 卷题 OCR 顺序不完整，HTML 显示为 `第五十四卷广播电视`，已按目录补为报刊、广播、电视三类。
- 多处章题和节题被拼入正文，如 `行(专)业报纸第二节`、`第一节亲新华通讯社支社`，已拆回标准标题。
- `电昇视` 属 OCR 残字并吞并第四章标题，已按源目录恢复为 `第四章电视`。
- `新闻学会第三节新闻工作者协会` 顺序错乱，已按目录归并为 `第三节新闻工作者协会 新闻学会`。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 继续第五十五卷起修复。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第五十四卷报刊广播电视章节核对完成

已完成 `第五十四卷 报刊 广播 电视` 章节格式核对：

- 新增脚本：`scripts/repair_fifty_fourth_volume_newspapers_broadcast_tv.py`。
- 修复第五十四卷卷题缺“报刊”、最终阅读页无 H3/H4 导航层级、章题节题扁平化、OCR 标题误字和 `ipa-data` 正文块。
- 第五十四卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第五章），H4={stats['h4_count']}。
- 第五十四卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处。
- 已写入进度文档：`output/reports/progress/20260629_第五十四卷报刊广播电视_修复核对进度.md`。

验收：第五十四卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：继续第五十五卷起。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第五十四卷报刊广播电视章节核对完成"
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

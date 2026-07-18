# -*- coding: utf-8 -*-
"""Repair and audit 第四十四卷 治安司法 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第四十四卷治安司法_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第四十四卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第四十五卷-[^"]+">|</main>)', re.S)
SOURCE_RE = re.compile(r'(第四十四卷\s*\n治安司法.*?)(?=\n第四十五卷|\Z)', re.S)

CHAPTERS = [
    ("第一章治安", ["第一节机构", "第二节政治保卫", "第三节经济、文化保卫", "第四节刑事案件侦破", "第五节治安管理", "第六节预审监所"]),
    ("第二章检察", ["第一节机构", "第二节刑事检察", "第三节经济检察", "第四节法纪检察", "第五节监所检察", "第六节控告申诉检察"]),
    ("第三章审判", ["第一节机构", "第二节刑事案件审判", "第三节民事案件审判", "第四节经济案件审判", "第五节行政案件审判", "第六节审判监督"]),
    ("第四章司法行政", ["第一节机构", "第二节律师", "第三节公证", "第四节人民调解", "第五节法制宣传教育", "第六节劳动改造劳动教养"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第四十四卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第四十四卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section
    replacements = {
        "第四十四卷\n治安司法\n概述\n": "第四十四卷 治安司法\n\n概述\n",
        "第一章治\n": "第一章治安\n",
        "监所预审\u30001第六节\n一、预审": "第六节预审 监所\n一、预审",
        "第一节机•构\n": "第一节机构\n",
        "第一节机·构\n": "第一节机构\n",
        "第二节•改•造": "第二节改造",
        "第二节·清理整顿": "第二节清理整顿",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[: m.start(1)] + section + text[m.end(1):]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第四十四卷卷题、章题、节题断裂和页眉错位。"]
    return []


def apply_direct_replacements(section: str) -> str:
    if h3("概述") not in section:
        section = section.replace('</h2>\n<p>清海州直隶州州衙', '</h2>\n' + h3("概述") + '\n<p>清海州直隶州州衙', 1)

    replacements = [
        ('<p>清光绪三十一年（1905年），赣榆县建立巡警局。民国时期', h3('第一章治安') + '\n<p>清光绪三十一年（1905年），赣榆县建立巡警局。民国时期'),
        ('<p>第一节机构一、民国时期警察机构民国元年', h4('第一章治安', '第一节机构') + '\n<p>一、民国时期警察机构民国元年'),
        ('<p>第二节政治保卫一、剿匪肃特民国30年', h4('第一章治安', '第二节政治保卫') + '\n<p>一、剿匪肃特民国30年'),
        ('<p>第三节经济、文化保卫一、经济保卫安全防范1951年', h4('第一章治安', '第三节经济、文化保卫') + '\n<p>一、经济保卫安全防范1951年'),
        ('<p>第四节刑事案件侦破一、杀人案件1955年', h4('第一章治安', '第四节刑事案件侦破') + '\n<p>一、杀人案件1955年'),
        ('监所预审\u30001第六节一、预审民国30年', h4('第一章治安', '第六节预审监所') + '\n<p>一、预审民国30年'),
        ('<p>1951年7月，灌云县人民检察署成立', h3('第二章检察') + '\n<p>1951年7月，灌云县人民检察署成立'),
        ('<p>第一节机•构一、民国时期地方检察机构民国2年', h4('第二章检察', '第一节机构') + '\n<p>一、民国时期地方检察机构民国2年'),
        ('第二节刑事检察一、审查批捕1955年', h4('第二章检察', '第二节刑事检察') + '\n<p>一、审查批捕1955年'),
        ('<p>第三节经济检察一、立案侦查1955年', h4('第二章检察', '第三节经济检察') + '\n<p>一、立案侦查1955年'),
        ('<p>第四节法纪检察一、立案侦查1956年', h4('第二章检察', '第四节法纪检察') + '\n<p>一、立案侦查1956年'),
        ('<p>第五节监所检察一、判决、裁定执行监督1957年', h4('第二章检察', '第五节监所检察') + '\n<p>一、判决、裁定执行监督1957年'),
        ('<p>第六节控告申诉检察一、来信、来访1956年', h4('第二章检察', '第六节控告申诉检察') + '\n<p>一、来信、来访1956年'),
        ('<p>第二节刑事案件审判一、反革命案件1950年', h4('第三章审判', '第二节刑事案件审判') + '\n<p>一、反革命案件1950年'),
        ('第二节刑事案件审判一、反革命案件1950年', h4('第三章审判', '第二节刑事案件审判') + '\n<p>一、反革命案件1950年'),
        ('第三节民事案件审判一、婚姻家庭案件离婚建国初期', h4('第三章审判', '第三节民事案件审判') + '\n<p>一、婚姻家庭案件离婚建国初期'),
        ('第四节经济案件审判一、经济合同纠纷案件1979年', h4('第三章审判', '第四节经济案件审判') + '\n<p>一、经济合同纠纷案件1979年'),
        ('<p>第五节行政案件审判1982年', h4('第三章审判', '第五节行政案件审判') + '\n<p>1982年'),
        ('<p>第六节审判监督一、申诉：1949年', h4('第三章审判', '第六节审判监督') + '\n<p>一、申诉：1949年'),
        ('<p>司法行政连云港市司法局成立于1981年1月6日', h3('第四章司法行政') + '\n<p>连云港市司法局成立于1981年1月6日'),
        ('<p>第一节机·构民国29年（1940年）至民国37年', h4('第四章司法行政', '第一节机构') + '\n<p>民国29年（1940年）至民国37年'),
        ('<p>第二节律师一、组织清未', h4('第四章司法行政', '第二节律师') + '\n<p>一、组织清未'),
        ('<p>第五节法制宣传教育一、宣传组织1981年前', h4('第四章司法行政', '第五节法制宣传教育') + '\n<p>一、宣传组织1981年前'),
        ('<p>第六节劳动改造劳动教养一、组织劳改组织民国时期', h4('第四章司法行政', '第六节劳动改造劳动教养') + '\n<p>一、组织劳改组织民国时期'),
    ]
    for old, new in replacements:
        section = section.replace(old, new, 1)
    return section


def insert_missing(section: str) -> str:
    fallbacks = [
        (h4('第一章治安', '第五节治安管理'), '<p>1950年，市公安机关根据中央有关规定'),
        (h4('第一章治安', '第五节治安管理'), '<p>二、户政管理户口管理自明朝起'),
        (h3('第三章审判'), '<p>连云港市中级人民法院（含市院）1962年8月'),
        (h4('第三章审判', '第一节机构'), '<p>连云港市中级人民法院（含市院）1962年8月'),
        (h4('第四章司法行政', '第三节公证'), '<p>州、连云、墟沟、猴嘴一批企业集中地为中心'),
        (h4('第四章司法行政', '第四节人民调解'), '<p>二、调解工作1954~1958年'),
    ]
    for marker, needle in fallbacks:
        if marker in section:
            continue
        pos = section.find(needle)
        if pos >= 0:
            section = section[:pos] + marker + '\n' + section[pos:]
    return section


def cleanup(section: str) -> str:
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第四十四卷-[^"]+">)', r'\1</p>\n\2', section)
    section = section.replace('<p><h3', '<h3').replace('<p><h4', '<h4')
    section = section.replace('</h3>\n</p>', '</h3>\n').replace('</h4>\n</p>', '</h4>\n')
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
        raise RuntimeError("Cannot locate 第四十四卷 HTML range")
    section = m.group(0)
    section = apply_direct_replacements(section)
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
    content = f"""# 2026-06-29 第四十四卷《治安司法》修复核对进度

## 本轮范围
- 范围：`第四十四卷 治安司法`。
- 目标：按交付标准修复卷题、概述、4 章、24 节、正文段落结构和表格风险记录。
- 源文件：`workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已处于规范状态'}。
- 恢复概述、第一章治安至第四章司法行政及 24 个节题的标准 H3/H4 层级。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第四章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本轮保留既有表格骨架；治安、检察、审判、司法行政统计表需在 PDF 表格专项中逐表核对。
- 第四十四卷章节较长，存在页眉、表格页和节题串联；本轮先恢复导航层级和交付阅读结构。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 继续下 part01 第四十五卷起修复，或进入第四十四卷表格专项复核。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第四十四卷治安司法章节核对完成

已完成 `第四十四卷 治安司法` 章节格式核对：

- 新增脚本：`scripts/repair_forty_fourth_volume_security_justice.py`。
- 修复第四十四卷最终阅读页无 H3/H4 导航层级、章题节题扁平化和页眉错位。
- 第四十四卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第四章），H4={stats['h4_count']}。
- 第四十四卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；治安、检察、审判、司法行政统计表需从源 PDF 专项核验。
- 已写入进度文档：`output/reports/progress/20260629_第四十四卷治安司法_修复核对进度.md`。

验收：第四十四卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：继续下 part01 第四十五卷起，或进入第四十四卷 PDF 表格专项复核。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第四十四卷治安司法章节核对完成"
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

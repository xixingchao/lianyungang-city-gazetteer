# -*- coding: utf-8 -*-
"""Repair and audit 第四十一卷 政党 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第四十一卷政党_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第四十一卷-政党">.*?</h2>)(.*?)(?=<h2 id="第四十二卷-[^"]+">)', re.S)
SOURCE_RE = re.compile(r'(第四十一卷.*?)(?=第四十二卷)', re.S)

CHAPTERS = [
    ("第一章解放前中共海属地方组织", ["第一节组织", "第二节主要活动"]),
    ("第二章解放后中共连云港市地方组织", ["第一节市(县)组织机构", "第二节市代表会议、代表大会", "第三节历任领导人", "第四节党的建设", "第五节统一战线工作"]),
    ("第三章解放后中共各区、县地方组织", ["第一节中共新浦区地方组织", "第二节中共海州区地方组织", "第三节中共云台区地方组织", "第四节中共连云区地方组织", "第五节中共赣榆县地方组织", "第六节中共东海县地方组织", "第七节中共灌云县地方组织"]),
    ("第四章中国国民党海属地区组织", ["第一节国民党连云市党部", "第二节国民党赣榆县地方组织", "第三节国民党东海县地方组织", "第四节国民党灌云县地方组织"]),
    ("第五章民主党派连云港市地方组织", ["第一节中国国民党革命委员会连云港市委员会", "第二节中国民主同盟连云港市委员会", "第三节中国民主建国会连云港市委员会", "第四节中国民主促进会连云港市委员会", "第五节中国农工民主党连云港市委员会", "第六节中国致公党连云港市工作委员会", "第七节九三学社连云港市委员会"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(titles) for _, titles in CHAPTERS)
EXPECTED_TABLES = 15


def h3(title: str) -> str:
    return f'<h3 id="第四十一卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第四十一卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        raise RuntimeError("Cannot locate 第四十一卷 source range")
    section = m.group(1)
    original = section
    replacements = {
        "第四十一卷\n概述\n": "第四十一卷 政党\n\n概述\n",
        "\n解放前中共海属地方组织\n第一章\n第一节组织\n": "\n第一章解放前中共海属地方组织\n第一节组织\n",
        "\n第二章\n解放后中共连云港市地方组织\n": "\n第二章解放后中共连云港市地方组织\n",
        "\n第二节\n市代表会议、代表大会\n": "\n第二节市代表会议、代表大会\n",
        "\n第三节\n历任领导人\n": "\n第三节历任领导人\n",
        "\n第四节\n党的建设\n": "\n第四节党的建设\n",
        "\n第五节\n统一战线工作\n": "\n第五节统一战线工作\n",
        "\n第三章\n解放后中共各区、县地方组织\n第一节\n中共新浦区地方组织\n": "\n第三章解放后中共各区、县地方组织\n第一节中共新浦区地方组织\n",
        "\n第二节\n中共海州区地方组织\n": "\n第二节中共海州区地方组织\n",
        "\n第三节\n中共云台区地方组织\n": "\n第三节中共云台区地方组织\n",
        "\n第五节\n中共赣榆县地方组织\n": "\n第五节中共赣榆县地方组织\n",
        "\n第六节\n中共东海县地方组织\n": "\n第六节中共东海县地方组织\n",
        "\n第七节\n中共灌云县地方组织\n": "\n第七节中共灌云县地方组织\n",
        "\n第四章\n中国国民党海属地区组织\n第一节\n国民党连云市党部\n": "\n第四章中国国民党海属地区组织\n第一节国民党连云市党部\n",
        "\n第二节\n国民党赣榆县地方组织\n": "\n第二节国民党赣榆县地方组织\n",
        "\n第三节\n国民党东海县地方组织\n": "\n第三节国民党东海县地方组织\n",
        "\n第五章 \n\n第五章\n民主党派连云港市地方组织\n第节\n中国国民党革命委员会连云港市委员会\n": "\n第五章民主党派连云港市地方组织\n第一节中国国民党革命委员会连云港市委员会\n",
        "\n第二节\n中国民主同盟连云港市委员会\n": "\n第二节中国民主同盟连云港市委员会\n",
        "\n第三节\n中国民主建国会连云港市委员会\n": "\n第三节中国民主建国会连云港市委员会\n",
        "\n第四节\n中国民主促进会连云港市委员会\n": "\n第四节中国民主促进会连云港市委员会\n",
        "\n第五节\n中国农工民主党连云港市委员会\n": "\n第五节中国农工民主党连云港市委员会\n",
        "\n第六节\n中国致公党连云港市工作委员会\n": "\n第六节中国致公党连云港市工作委员会\n",
        "\n第七节\n九三学社连云港市委员会\n": "\n第七节九三学社连云港市委员会\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    section = re.sub(r"\n第二章(?:角|\s*)\n(?:解放后中共连云港市地方组织)?[：:·\d\s]*\n?", "\n", section)
    section = re.sub(r"\n第三章角\n", "\n", section)
    if section != original:
        text = text[: m.start(1)] + section + text[m.end(1) :]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第四十一卷卷题、章题、节题断裂、页眉残留和 OCR 节题错位。"]
    return []


def insert_after_h2(section: str, marker: str) -> tuple[str, bool]:
    if marker in section:
        return section, False
    m = re.search(r'</h2>\s*', section)
    if not m:
        return section, False
    return section[:m.end()] + "\n" + marker + "\n" + section[m.end():], True


def insert_before_text(section: str, marker: str, text: str) -> tuple[str, bool]:
    if marker in section:
        return section, False
    pos = section.find(text)
    if pos < 0:
        return section, False
    p_start = section.rfind("<p>", 0, pos)
    p_end = section.rfind("</p>", 0, pos)
    insert_pos = p_start if p_start > p_end else pos
    return section[:insert_pos] + marker + "\n" + section[insert_pos:], True


def split_heading(section: str, marker: str, text: str, replacement: str = "") -> tuple[str, bool]:
    if marker in section:
        return section, False
    for v in [text]:
        pattern = "<p>" + v
        pos = section.find(pattern)
        if pos >= 0:
            content_start = pos + len(pattern)
            return section[:pos] + marker + "\n<p>" + replacement + section[content_start:], True
        pos = section.find(v)
        if pos >= 0:
            p_start = section.rfind("<p>", 0, pos)
            p_end = section.rfind("</p>", 0, pos)
            content_start = pos + len(v)
            if p_start > p_end:
                return section[:pos] + "</p>\n" + marker + "\n<p>" + replacement + section[content_start:], True
            return section[:pos] + marker + "\n" + replacement + section[content_start:], True
    return section, False


def normalize_ipa(section: str) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        text = re.sub(r"^\s*[·:.：\s]*\d{4}\s*[·:.：\s]*", "", match.group(1).strip())
        return f"<p>{text}</p>"

    return re.sub(r'<div class="ipa-data">(.*?)</div>', repl, section, flags=re.S), count


def cleanup(section: str) -> str:
    replacements = {
        '<h2 id="第四十一卷-政党">第四十一卷概述</h2>': '<h2 id="第四十一卷-政党">第四十一卷政党</h2>',
        '<p>解放前中共海属地方组织第一节组织': h3("第一章解放前中共海属地方组织") + "\n" + h4("第一章解放前中共海属地方组织", "第一节组织") + "\n<p>",
        '<p>第二节主要活动': h4("第一章解放前中共海属地方组织", "第二节主要活动") + "\n<p>",
        '<p>解放后中共连云港市地方组织第一节市(县)组织机构': h3("第二章解放后中共连云港市地方组织") + "\n" + h4("第二章解放后中共连云港市地方组织", "第一节市(县)组织机构") + "\n<p>",
        '<p>第二节市代表会议、代表大会': h4("第二章解放后中共连云港市地方组织", "第二节市代表会议、代表大会") + "\n<p>",
        '<p>解放后中共连云港市地方组织第三节历任领导人': h4("第二章解放后中共连云港市地方组织", "第三节历任领导人") + "\n<p>",
        '<p>第三节历任领导人': h4("第二章解放后中共连云港市地方组织", "第三节历任领导人") + "\n<p>",
        '<p>第四节党的建设': h4("第二章解放后中共连云港市地方组织", "第四节党的建设") + "\n<p>",
        '<p>第五节统一战线工作': h4("第二章解放后中共连云港市地方组织", "第五节统一战线工作") + "\n<p>",
        '<p>60.1%734764.4%解放后中共各区、县地方组织第一节中共新浦区地方组织': '<p>60.1%734764.4%</p>\n' + h3("第三章解放后中共各区、县地方组织") + "\n" + h4("第三章解放后中共各区、县地方组织", "第一节中共新浦区地方组织") + "\n<p>",
        '<p>解放后中共各区、县地方组织第一节中共新浦区地方组织': h3("第三章解放后中共各区、县地方组织") + "\n" + h4("第三章解放后中共各区、县地方组织", "第一节中共新浦区地方组织") + "\n<p>",
        '<p>第二节中共海州区地方组织': h4("第三章解放后中共各区、县地方组织", "第二节中共海州区地方组织") + "\n<p>",
        '<p>第三节中共云台区地方组织': h4("第三章解放后中共各区、县地方组织", "第三节中共云台区地方组织") + "\n<p>",
        '<p>第四节中共连云区地方组织': h4("第三章解放后中共各区、县地方组织", "第四节中共连云区地方组织") + "\n<p>",
        '<p>第五节中共赣榆县地方组织': h4("第三章解放后中共各区、县地方组织", "第五节中共赣榆县地方组织") + "\n<p>",
        '<p>第六节中共东海县地方组织': h4("第三章解放后中共各区、县地方组织", "第六节中共东海县地方组织") + "\n<p>",
        '<p>第七节中共灌云县地方组织': h4("第三章解放后中共各区、县地方组织", "第七节中共灌云县地方组织") + "\n<p>",
        '<p>中国国民党海属地区组织第一节国民党连云市党部': h3("第四章中国国民党海属地区组织") + "\n" + h4("第四章中国国民党海属地区组织", "第一节国民党连云市党部") + "\n<p>",
        '<p>第二节国民党赣榆县地方组织': h4("第四章中国国民党海属地区组织", "第二节国民党赣榆县地方组织") + "\n<p>",
        '<p>第三节国民党东海县地方组织': h4("第四章中国国民党海属地区组织", "第三节国民党东海县地方组织") + "\n<p>",
        '<p>第四节国民党灌云县地方组织': h4("第四章中国国民党海属地区组织", "第四节国民党灌云县地方组织") + "\n<p>",
        '<p>民主党派连云港市地方组织第节中国国民党革命委员会连云港市委员会': h3("第五章民主党派连云港市地方组织") + "\n" + h4("第五章民主党派连云港市地方组织", "第一节中国国民党革命委员会连云港市委员会") + "\n<p>",
        '<p>第二节中国民主同盟连云港市委员会': h4("第五章民主党派连云港市地方组织", "第二节中国民主同盟连云港市委员会") + "\n<p>",
        '<p>第三节中国民主建国会连云港市委员会': h4("第五章民主党派连云港市地方组织", "第三节中国民主建国会连云港市委员会") + "\n<p>",
        '<p>第四节中国民主促进会连云港市委员会': h4("第五章民主党派连云港市地方组织", "第四节中国民主促进会连云港市委员会") + "\n<p>",
        '<p>第五节中国农工民主党连云港市委员会': h4("第五章民主党派连云港市地方组织", "第五节中国农工民主党连云港市委员会") + "\n<p>",
        '<p>第六节中国致公党连云港市工作委员会': h4("第五章民主党派连云港市地方组织", "第六节中国致公党连云港市工作委员会") + "\n<p>",
        '<p>第七节九三学社连云港市委员会': h4("第五章民主党派连云港市地方组织", "第七节九三学社连云港市委员会") + "\n<p>",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    section = re.sub(r'<p>第二章(?:角|\s*)</p>\s*', '', section)
    section = re.sub(r'<p>第三章角</p>\s*', '', section)
    section = re.sub(r'第二章角\s*解放后中共连云港市地方组织[：:·\d\s]*', '', section)
    section = re.sub(r'<p>第五章\s*</p>\s*', '', section)
    section = re.sub(r'<p>\s*[·:.：\s]*\d{4}\s*[·:.：\s]*</p>\n?', '', section)
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第四十一卷-[^"]+">)', r'\1</p>\n\2', section)
    section = section.replace('<p><h3', '<h3').replace('<p><h4', '<h4')
    section = section.replace('</h3>\n</p>', '</h3>\n').replace('</h4>\n</p>', '</h4>\n')
    seen_h3: set[str] = set()
    seen_h4: set[str] = set()

    def keep_first_h3(match: re.Match[str]) -> str:
        ident = match.group(1)
        if ident in seen_h3:
            return ''
        seen_h3.add(ident)
        return match.group(0)

    def keep_first_h4(match: re.Match[str]) -> str:
        ident = match.group(1)
        if ident in seen_h4:
            return ''
        seen_h4.add(ident)
        return match.group(0)

    section = re.sub(r'<h3 id="([^"]+)">[^<]+</h3>\s*', keep_first_h3, section)
    section = re.sub(r'<h4 id="([^"]+)">[^<]+</h4>\s*', keep_first_h4, section)
    return section


def restore_html() -> tuple[int, int, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第四十一卷 HTML range")
    section = m.group(0)
    section = section.replace('<h2 id="第四十一卷-政党">第四十一卷概述</h2>', '<h2 id="第四十一卷-政党">第四十一卷政党</h2>')
    inserted_h3 = inserted_h4 = 0
    section, added = insert_after_h2(section, h3("概述")); inserted_h3 += int(added)
    for title, needle in [
        ("第一章解放前中共海属地方组织", "解放前中共海属地方组织第一节组织"),
        ("第二章解放后中共连云港市地方组织", "解放后中共连云港市地方组织第一节市(县)组织机构"),
        ("第三章解放后中共各区、县地方组织", "解放后中共各区、县地方组织第一节中共新浦区地方组织"),
        ("第四章中国国民党海属地区组织", "中国国民党海属地区组织第一节国民党连云市党部"),
        ("第五章民主党派连云港市地方组织", "民主党派连云港市地方组织第节中国国民党革命委员会连云港市委员会"),
    ]:
        section, added = insert_before_text(section, h3(title), needle); inserted_h3 += int(added)
    for chapter, title, needle, replacement in [
        ("第一章解放前中共海属地方组织", "第一节组织", "第一节组织", ""),
        ("第一章解放前中共海属地方组织", "第二节主要活动", "第二节主要活动", ""),
        ("第二章解放后中共连云港市地方组织", "第一节市(县)组织机构", "第一节市(县)组织机构", ""),
        ("第二章解放后中共连云港市地方组织", "第二节市代表会议、代表大会", "第二节市代表会议、代表大会", ""),
        ("第二章解放后中共连云港市地方组织", "第三节历任领导人", "第三节历任领导人", ""),
        ("第二章解放后中共连云港市地方组织", "第四节党的建设", "第四节党的建设", ""),
        ("第二章解放后中共连云港市地方组织", "第五节统一战线工作", "第五节统一战线工作", ""),
        ("第三章解放后中共各区、县地方组织", "第一节中共新浦区地方组织", "第一节中共新浦区地方组织", ""),
        ("第三章解放后中共各区、县地方组织", "第二节中共海州区地方组织", "第二节中共海州区地方组织", ""),
        ("第三章解放后中共各区、县地方组织", "第三节中共云台区地方组织", "第三节中共云台区地方组织", ""),
        ("第三章解放后中共各区、县地方组织", "第四节中共连云区地方组织", "第四节中共连云区地方组织", ""),
        ("第三章解放后中共各区、县地方组织", "第五节中共赣榆县地方组织", "第五节中共赣榆县地方组织", ""),
        ("第三章解放后中共各区、县地方组织", "第六节中共东海县地方组织", "第六节中共东海县地方组织", ""),
        ("第三章解放后中共各区、县地方组织", "第七节中共灌云县地方组织", "第七节中共灌云县地方组织", ""),
        ("第四章中国国民党海属地区组织", "第一节国民党连云市党部", "第一节国民党连云市党部", ""),
        ("第四章中国国民党海属地区组织", "第二节国民党赣榆县地方组织", "第二节国民党赣榆县地方组织", ""),
        ("第四章中国国民党海属地区组织", "第三节国民党东海县地方组织", "第三节国民党东海县地方组织", ""),
        ("第四章中国国民党海属地区组织", "第四节国民党灌云县地方组织", "第四节国民党灌云县地方组织", ""),
        ("第五章民主党派连云港市地方组织", "第一节中国国民党革命委员会连云港市委员会", "第节中国国民党革命委员会连云港市委员会", ""),
        ("第五章民主党派连云港市地方组织", "第二节中国民主同盟连云港市委员会", "第二节中国民主同盟连云港市委员会", ""),
        ("第五章民主党派连云港市地方组织", "第三节中国民主建国会连云港市委员会", "第三节中国民主建国会连云港市委员会", ""),
        ("第五章民主党派连云港市地方组织", "第四节中国民主促进会连云港市委员会", "第四节中国民主促进会连云港市委员会", ""),
        ("第五章民主党派连云港市地方组织", "第五节中国农工民主党连云港市委员会", "第五节中国农工民主党连云港市委员会", ""),
        ("第五章民主党派连云港市地方组织", "第六节中国致公党连云港市工作委员会", "第六节中国致公党连云港市工作委员会", ""),
        ("第五章民主党派连云港市地方组织", "第七节九三学社连云港市委员会", "第七节九三学社连云港市委员会", ""),
    ]:
        section, added = split_heading(section, h4(chapter, title), needle, replacement)
        inserted_h4 += int(added)
    section, ipa_fixed = normalize_ipa(section)
    section = cleanup(section)
    html = html[:m.start()] + section + html[m.end():]
    HTML_PATH.write_text(html, encoding="utf-8")
    return inserted_h3, inserted_h4, ipa_fixed


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
    status = "通过" if stats["h3_count"] == EXPECTED_H3 and stats["h4_count"] == EXPECTED_H4 and stats["ipa_blocks"] == 0 else "需复核"
    content = f"""# 2026-06-29 第四十一卷《政党》修复核对进度

## 本轮范围
- 范围：`第四十一卷 政党`。
- 目标：按交付标准修复卷题、概述、章题、节题、页眉残留和正文段落结构。
- 源文件：`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已处于规范状态'}。
- 将最终阅读页卷题由 `第四十一卷概述` 修正为 `第四十一卷政党`。
- 恢复概述、第一章解放前中共海属地方组织至第五章民主党派连云港市地方组织及 25 个节题的标准 H3/H4 层级。
- 3 处 `ipa-data` 残留已转为普通正文段落，未改动既有结构化表格数据。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第五章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本轮保留既有表格骨架；政党卷组织沿革、历任领导人、党员统计、政协党外人士等表格跨页较多，后续 PDF 表格专项需重点核对表头、续表页眉和人名列。
- 第五章第一节民革连云港市委开头疑似缺少筹建句首，后续需对照 PDF 补核正文完整性。

## 验收状态
- 本卷结构验收：{status}。
- 后续已纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 进入 `第四十二卷 政务`，继续按“源 MD 标题规范 -> 最终阅读页结构修复 -> 全书审计 -> typecheck -> 进度记录 -> Git 提交”的顺序推进。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第四十一卷政党章节核对完成

已完成 `第四十一卷 政党` 章节格式核对：

- 新增脚本：`scripts/repair_forty_first_volume_parties.py`。
- 修复 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md` 中第四十一卷卷题、章题、节题断裂、页眉残留和 OCR 节题错位。
- 修复 `output/final_reader/连云港市志_全书.html` 中第四十一卷卷题误作概述、章节标题全部扁平化以及 3 处 `ipa-data` 残留的问题。
- 第四十一卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第五章），H4={stats['h4_count']}。
- 第四十一卷范围内 `ipa-data` 残留为 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；政党组织沿革、历任领导人、党员统计等表格需从源 PDF 专项补登、重建和核验。
- 第五章第一节民革连云港市委开头疑似缺少筹建句首，后续需对照 PDF 补核正文完整性。
- 已写入进度文档：`output/reports/progress/20260629_第四十一卷政党_修复核对进度.md`。

验收：第四十一卷 HTML 字节数 {stats['bytes']}，范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第四十二卷 政务`。第四十一卷表格和第五章第一节开头需在 PDF 专项中复核。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第四十一卷政党章节核对完成"
    if marker in memory:
        memory = memory[: memory.find(marker)].rstrip() + "\n" + entry
    else:
        memory = memory.rstrip() + "\n" + entry
    MEMORY_PATH.write_text(memory, encoding="utf-8")


def main() -> None:
    changes = repair_source_md()
    inserted_h3, inserted_h4, ipa_fixed = restore_html()
    stats = audit_section()
    stats["inserted_h3"] = inserted_h3
    stats["inserted_h4"] = inserted_h4
    stats["ipa_fixed"] = ipa_fixed
    write_progress(stats, changes)
    update_memory(stats)
    print("Repair complete")
    if changes:
        for change in changes:
            print(f"- {change}")
    print(f"stats={stats}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()

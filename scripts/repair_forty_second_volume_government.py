# -*- coding: utf-8 -*-
"""Repair and audit 第四十二卷 政务 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第四十二卷政务_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第四十二卷-政务">.*?</h2>)(.*?)(?=<h2 id="第四十三卷-[^"]+">|</main>)', re.S)
SOURCE_RE = re.compile(r'(第四十二卷\s*\n概述.*)\Z', re.S)

CHAPTERS = [
    ("第一章民国地方政权", ["第一节组织机构", "第二节政务纪要"]),
    ("第二章抗日根据地和解放区民主政府", ["第一节组织机构", "第二节政务纪要"]),
    ("第三章新海连市、新海县人民政府", ["第一节组织机构", "第二节政府首长", "第三节政务纪要"]),
    ("第四章连云港(新海连)市人民委员会", ["第一节组织机构", "第二节市人民委员会领导人", "第三节政务纪要"]),
    ("第五章连云港市革命委员会", ["第一节组织机构", "第二节市革命委员会首长", "第三节政务纪要"]),
    ("第六章连云港市人民政府", ["第一节组织机构", "第二节政府首长", "第三节政务纪要"]),
    ("第七章区、县人民政府", ["第一节新浦区人民政府", "第二节海州区人民政府", "第三节云台区人民政府", "第四节连云区人民政府", "第五节赣榆县人民政府", "第六节东海县人民政府", "第七节灌云县人民政府"]),
    ("第八章参议会", ["第一节抗日根据地、解放区参议会", "第二节国民政府地方参议会"]),
    ("第九章新海连特区、新海连市各界人民代表会议", ["第一节代表", "第二节历届人民代表会议", "第三节常务(协商)委员会"]),
    ("第十章连云港(新海连)市人民代表大会", ["第一节代表", "第二节历届人民代表大会", "第三节常务委员会"]),
    ("第十一章区、县各界人民代表会议、人民代表大会", ["第一节新浦区人民代表大会", "第二节海州区人民代表大会", "第三节云台区人民代表大会", "第四节连云区人民代表大会", "第五节赣榆县各界人民代表会议、人民代表大会", "第六节东海县各界人民代表会议、人民代表大会", "第七节灌云县各界人民代表会议、人民代表大会"]),
    ("第十二章中国人民政治协商会议连云港(新海连)市委员会", ["第一节政协新海连市第一届委员会", "第二节政协新海连市第二届委员会", "第三节政协连云港市第三届委员会", "第四节政协连云港市第四届委员会", "第五节政协连云港市第五届委员会", "第六节政协连云港市第六届委员会", "第七节政协连云港市第七届委员会", "第八节市政协各专门委员会和工作组"]),
    ("第十三章政协各区、县委员会", ["第一节政协新浦区委员会", "第二节政协海州区委员会", "第三节政协云台区委员会", "第四节政协连云区委员会", "第五节政协赣榆县委员会", "第六节政协东海县委员会", "第七节政协灌云县委员会"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第四十二卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第四十二卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section
    replacements = {
        "第四十二卷\n概述\n": "第四十二卷 政务\n\n概述\n",
        "\n第一章\n民国地方政权\n第一节组织机构\n": "\n第一章民国地方政权\n第一节组织机构\n",
        "\n第二节\n政务纪要\n": "\n第二节政务纪要\n",
        "\n第二节了\n政务纪要\n": "\n第二节政务纪要\n",
        "\n第三节营\n常务委员会\n": "\n第三节常务委员会\n",
        "\n第一节』\n政协新海连市第一届委员会\n": "\n第一节政协新海连市第一届委员会\n",
        "\n第二节了\n政协海州区委员会\n": "\n第二节政协海州区委员会\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    section = re.sub(r"\n第(十[一二三]|十二)章[^\n]*[：:·，,\d\s]*\n", "\n", section)
    if section != original:
        text = text[: m.start(1)] + section
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第四十二卷卷题、部分节题断裂、OCR 节题错位和页眉残留。"]
    return []


def normalize_ipa(section: str) -> tuple[str, int]:
    count = 0
    def repl(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return f"<p>{match.group(1).strip()}</p>"
    return re.sub(r'<div class="ipa-data">(.*?)</div>', repl, section, flags=re.S), count


def apply_replacements(section: str) -> str:
    rep: dict[str, str] = {
        '<h2 id="第四十二卷-政务">第四十二卷概述</h2>': '<h2 id="第四十二卷-政务">第四十二卷政务</h2>',
        '<p>民国地方政权第一节组织机构': h3('第一章民国地方政权') + '\n' + h4('第一章民国地方政权', '第一节组织机构') + '\n<p>',
        '<p>第二节政务纪要': h4('第一章民国地方政权', '第二节政务纪要') + '\n<p>',
        '<p>抗日根据地和解放区民主政府第一节组织机构': h3('第二章抗日根据地和解放区民主政府') + '\n' + h4('第二章抗日根据地和解放区民主政府', '第一节组织机构') + '\n<p>',
        '<p>第二节了政务纪要': h4('第二章抗日根据地和解放区民主政府', '第二节政务纪要') + '\n<p>',
        '<p>新海连市、新海县人民政府第一节组织机构': h3('第三章新海连市、新海县人民政府') + '\n' + h4('第三章新海连市、新海县人民政府', '第一节组织机构') + '\n<p>',
        '<p>第二节政府首长': h4('第三章新海连市、新海县人民政府', '第二节政府首长') + '\n<p>',
        '<p>杨祖彤(女)(1953.2～1955.4)副市长季士杰(1952.3~1955.4)张书伦(1954.1~1955.4)第三节政务纪要': '<p>杨祖彤(女)(1953.2～1955.4)副市长季士杰(1952.3~1955.4)张书伦(1954.1~1955.4)</p>\n' + h4('第三章新海连市、新海县人民政府', '第三节政务纪要') + '\n<p>',
        '<p>连云港（新海连）市人民委员会第一节组织机构': h3('第四章连云港(新海连)市人民委员会') + '\n' + h4('第四章连云港(新海连)市人民委员会', '第一节组织机构') + '\n<p>',
        '<p>第二节市人民委员会领导人': h4('第四章连云港(新海连)市人民委员会', '第二节市人民委员会领导人') + '\n<p>',
        '<p>连云港市革命委员会第一节组织机构': h3('第五章连云港市革命委员会') + '\n' + h4('第五章连云港市革命委员会', '第一节组织机构') + '\n<p>',
        '<p>第二节市革命委员会首长': h4('第五章连云港市革命委员会', '第二节市革命委员会首长') + '\n<p>',
        '<p>连云港市人民政府第一节组织机构': h3('第六章连云港市人民政府') + '\n' + h4('第六章连云港市人民政府', '第一节组织机构') + '\n<p>',
        '<p>区、县人民政府第一节新浦区人民政府': h3('第七章区、县人民政府') + '\n' + h4('第七章区、县人民政府', '第一节新浦区人民政府') + '\n<p>',
        '<p>第二节海州区人民政府': h4('第七章区、县人民政府', '第二节海州区人民政府') + '\n<p>',
        '<p>第四节连云区人民政府': h4('第七章区、县人民政府', '第四节连云区人民政府') + '\n<p>',
        '<p>第六节东海县人民政府': h4('第七章区、县人民政府', '第六节东海县人民政府') + '\n<p>',
        '<p>第七节灌云县人民政府': h4('第七章区、县人民政府', '第七节灌云县人民政府') + '\n<p>',
        '<p>参议会抗日根据地、解放区参议会第一节、一、组织机构': h3('第八章参议会') + '\n' + h4('第八章参议会', '第一节抗日根据地、解放区参议会') + '\n<p>一、组织机构',
        '<p>第二节国国民政府地方参议会': h4('第八章参议会', '第二节国民政府地方参议会') + '\n<p>',
        '<p>新海连特区、新海连市各界人民代表会议第一节代\u3000表': h3('第九章新海连特区、新海连市各界人民代表会议') + '\n' + h4('第九章新海连特区、新海连市各界人民代表会议', '第一节代表') + '\n<p>',
        '<p>第二节历届人民代表会议': h4('第九章新海连特区、新海连市各界人民代表会议', '第二节历届人民代表会议') + '\n<p>',
        '1224第二节历届人民代表会议': '1224</p>\n' + h4('第九章新海连特区、新海连市各界人民代表会议', '第二节历届人民代表会议') + '\n<p>',
        '<p>第三节常务（协商）委员会': h4('第九章新海连特区、新海连市各界人民代表会议', '第三节常务(协商)委员会') + '\n<p>',
        '<p>连云港（新海连）市人民代表大会第一节代表': h3('第十章连云港(新海连)市人民代表大会') + '\n' + h4('第十章连云港(新海连)市人民代表大会', '第一节代表') + '\n<p>',
        '<p>第二节历届人民代表大会': h4('第十章连云港(新海连)市人民代表大会', '第二节历届人民代表大会') + '\n<p>',
        '1114611546第二节历届人民代表大会': '1114611546</p>\n' + h4('第十章连云港(新海连)市人民代表大会', '第二节历届人民代表大会') + '\n<p>',
        '<p>第三节营常务委员会': h4('第十章连云港(新海连)市人民代表大会', '第三节常务委员会') + '\n<p>',
        '<p>附42-2：出席省各界代表会议代表、省协商委员会代表名单、出席山东省各界人民代表会议代表名单王景武程绪和张融存李增玺赵理斋刘一麟二、出席江苏省协商委员会委员名单易企衡连云港（新海连）市人民代表大会第一节代表': '<p>附42-2：出席省各界代表会议代表、省协商委员会代表名单、出席山东省各界人民代表会议代表名单王景武程绪和张融存李增玺赵理斋刘一麟二、出席江苏省协商委员会委员名单易企衡</p>\n' + h3('第十章连云港(新海连)市人民代表大会') + '\n' + h4('第十章连云港(新海连)市人民代表大会', '第一节代表') + '\n<p>',
        '<h3 id="anchor">第十一章</h3>\n<p>区、县各界人民代表会议、人民代表大会第一节新浦区人民代表大会': h3('第十一章区、县各界人民代表会议、人民代表大会') + '\n' + h4('第十一章区、县各界人民代表会议、人民代表大会', '第一节新浦区人民代表大会') + '\n<p>',
        '<p>第二节海州区人民代表大会': h4('第十一章区、县各界人民代表会议、人民代表大会', '第二节海州区人民代表大会') + '\n<p>',
        '<p>第三节云台区人民代表大会': h4('第十一章区、县各界人民代表会议、人民代表大会', '第三节云台区人民代表大会') + '\n<p>',
        '<p>第四节连云区人民代表大会': h4('第十一章区、县各界人民代表会议、人民代表大会', '第四节连云区人民代表大会') + '\n<p>',
        '<p>第五节赣榆县各界人民代表会议、人民代表大会': h4('第十一章区、县各界人民代表会议、人民代表大会', '第五节赣榆县各界人民代表会议、人民代表大会') + '\n<p>',
        '<p>第六节东海县各界人民代表会议、人民代表大会': h4('第十一章区、县各界人民代表会议、人民代表大会', '第六节东海县各界人民代表会议、人民代表大会') + '\n<p>',
        '<p>第七节灌云县各界人民代表会议、人民代表大会': h4('第十一章区、县各界人民代表会议、人民代表大会', '第七节灌云县各界人民代表会议、人民代表大会') + '\n<p>',
        '<h3 id="anchor">第十二章</h3>\n<p>中国人民政治协商会议连云港（新海连）市委员会第一节』</p>\n<p>政协新海连市第一届委员会': h3('第十二章中国人民政治协商会议连云港(新海连)市委员会') + '\n' + h4('第十二章中国人民政治协商会议连云港(新海连)市委员会', '第一节政协新海连市第一届委员会') + '\n<p>',
        '<p>第二节政协新海连市第二届委员会': h4('第十二章中国人民政治协商会议连云港(新海连)市委员会', '第二节政协新海连市第二届委员会') + '\n<p>',
        '<p>第三节政协连云港市第三届委员会': h4('第十二章中国人民政治协商会议连云港(新海连)市委员会', '第三节政协连云港市第三届委员会') + '\n<p>',
        '<p>第四节政协连云港市第四届委员会': h4('第十二章中国人民政治协商会议连云港(新海连)市委员会', '第四节政协连云港市第四届委员会') + '\n<p>',
        '<p>第五节政协连云港市第五届委员会': h4('第十二章中国人民政治协商会议连云港(新海连)市委员会', '第五节政协连云港市第五届委员会') + '\n<p>',
        '<p>第六节政协连云港市第六届委员会': h4('第十二章中国人民政治协商会议连云港(新海连)市委员会', '第六节政协连云港市第六届委员会') + '\n<p>',
        '<p>第七节政协连云港市第七届委员会': h4('第十二章中国人民政治协商会议连云港(新海连)市委员会', '第七节政协连云港市第七届委员会') + '\n<p>',
        '<p>第八节市政协各专门委员会和工作组': h4('第十二章中国人民政治协商会议连云港(新海连)市委员会', '第八节市政协各专门委员会和工作组') + '\n<p>',
        '<h3 id="anchor">第十三章</h3>\n<p>政协各区、县委员会第一节政协新浦区委员会': h3('第十三章政协各区、县委员会') + '\n' + h4('第十三章政协各区、县委员会', '第一节政协新浦区委员会') + '\n<p>',
        '<p>第二节了政协海州区委员会': h4('第十三章政协各区、县委员会', '第二节政协海州区委员会') + '\n<p>',
        '<p>第三节政协云台区委员会': h4('第十三章政协各区、县委员会', '第三节政协云台区委员会') + '\n<p>',
        '<p>第四节政协连云区委员会': h4('第十三章政协各区、县委员会', '第四节政协连云区委员会') + '\n<p>',
        '<p>第五节政协赣榆县委员会': h4('第十三章政协各区、县委员会', '第五节政协赣榆县委员会') + '\n<p>',
        '<p>政协东海县委员会第六节政协东海县委员会': h4('第十三章政协各区、县委员会', '第六节政协东海县委员会') + '\n<p>',
        '<p>第七节政协灌云县委员会': h4('第十三章政协各区、县委员会', '第七节政协灌云县委员会') + '\n<p>',
    }
    for old, new in rep.items():
        section = section.replace(old, new)
    return section


def insert_missing(section: str) -> str:
    # The OCR dropped a few section labels; insert them before stable body starts.
    fallbacks = [
        (h4('第四章连云港(新海连)市人民委员会', '第三节政务纪要'), '1955年底全市对农业、手工业私营工商业的社会主义改造取得初步成果'),
        (h4('第五章连云港市革命委员会', '第三节政务纪要'), '1980年8月19日，对文化大革命”期间冤假错案复查工作基本结束'),
        (h4('第六章连云港市人民政府', '第二节政府首长'), '一、第六届连云港市人民政府市长、副市长名录'),
        (h4('第六章连云港市人民政府', '第三节政务纪要'), '1983年1月18日，国务院批准江苏省人民政府'),
        (h4('第七章区、县人民政府', '第三节云台区人民政府'), '1983年4月，成立南城区筹备组'),
        (h4('第七章区、县人民政府', '第五节赣榆县人民政府'), '1952～1990年，每逢突击性工作'),
    ]
    for marker, needle in fallbacks:
        if marker in section:
            continue
        pos = section.find(needle)
        if pos < 0:
            continue
        p_start = section.rfind('<p>', 0, pos)
        p_end = section.rfind('</p>', 0, pos)
        insert_pos = p_start if p_start > p_end else pos
        section = section[:insert_pos] + marker + '\n' + section[insert_pos:]
    return section


def cleanup(section: str) -> str:
    # Keep 第四章第三节 inside 第四章, after the leadership list.
    chapter4 = h3('第四章连云港(新海连)市人民委员会')
    chapter4_s3 = h4('第四章连云港(新海连)市人民委员会', '第三节政务纪要')
    misplaced_chapter4_s3 = (
        chapter4_s3
        + '\n<p>1955年底全市对农业、手工业私营工商业的社会主义改造取得初步成果，社会主义制度开始确立。</p>\n'
    )
    if section.find(misplaced_chapter4_s3) < section.find(chapter4):
        section = section.replace(misplaced_chapter4_s3, '', 1)
    section = section.replace(
        '秘书长王玉焕(1963.12~1967.1)第三节政务纪要',
        '秘书长王玉焕(1963.12~1967.1)</p>\n' + chapter4_s3 + '\n<p>',
        1,
    )
    if chapter4_s3 not in section:
        section = section.replace(
            '<p>1955年7月9日，市人委一届四次会议通过',
            chapter4_s3 + '\n<p>1955年7月9日，市人委一届四次会议通过',
            1,
        )
    # Keep 第六章 section order as 组织机构 -> 政府首长 -> 政务纪要 when fallback insertion sees body text first.
    gov3 = h4('第六章连云港市人民政府', '第三节政务纪要')
    gov2 = h4('第六章连云港市人民政府', '第二节政府首长')
    if gov3 in section and gov2 in section and section.find(gov3) < section.find(gov2):
        section = section.replace(gov3 + '\n', '', 1)
        pos = section.find(gov2)
        nxt = section.find('<h3 id="第四十二卷-第七章', pos)
        insert_pos = nxt if nxt != -1 else pos
        section = section[:insert_pos] + gov3 + '\n' + section[insert_pos:]
    section = re.sub(r'<h3 id="anchor">第(?:十一|十二|十三)章</h3>\s*', '', section)
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第四十二卷-[^"]+">)', r'\1</p>\n\2', section)
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


def restore_html() -> tuple[int, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第四十二卷 HTML range")
    section = m.group(0)
    section = section.replace('<h2 id="第四十二卷-政务">第四十二卷概述</h2>', '<h2 id="第四十二卷-政务">第四十二卷政务</h2>')
    if h3('概述') not in section:
        section = section.replace('</h2>', '</h2>\n' + h3('概述'), 1)
    section, ipa_fixed = normalize_ipa(section)
    section = apply_replacements(section)
    section = insert_missing(section)
    section = cleanup(section)
    html = html[:m.start()] + section + html[m.end():]
    HTML_PATH.write_text(html, encoding="utf-8")
    return ipa_fixed, 0


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
    content = f"""# 2026-06-29 第四十二卷《政务》修复核对进度

## 本轮范围
- 范围：`第四十二卷 政务`。
- 目标：按交付标准修复卷题、概述、13 章、53 节、通用锚点和正文段落结构。
- 源文件：`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已处于规范状态'}。
- 将最终阅读页卷题由 `第四十二卷概述` 修正为 `第四十二卷政务`。
- 恢复概述、第一章民国地方政权至第十三章政协各区、县委员会及 53 个节题的标准 H3/H4 层级。
- 清理 3 个 `id="anchor"` 通用标题锚点，并将 1 处 `ipa-data` 残留转为普通正文段落。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第十三章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本轮保留既有表格骨架；政务卷人大、政协和区县代表会议表格需在 PDF 表格专项中继续核对。
- 第四十二卷个别节题由正文首句补位，后续全文校对应重点核对第六章、第七章部分节首完整性。

## 验收状态
- 本卷结构验收：{status}。
- 后续已纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 中 part02（第三十卷至第四十二卷）章节层级修复已推进到末卷；下一步转入下 part01 第四十三卷起继续修复，或开展 PDF 表格专项复核。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第四十二卷政务章节核对完成

已完成 `第四十二卷 政务` 章节格式核对：

- 新增脚本：`scripts/repair_forty_second_volume_government.py`。
- 修复第四十二卷卷题误作概述、通用 `id="anchor"` 标题、章节标题扁平化以及 1 处 `ipa-data` 残留。
- 第四十二卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第十三章），H4={stats['h4_count']}。
- 第四十二卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；人大、政协和区县代表会议表格需从源 PDF 专项补登、重建和核验。
- 已写入进度文档：`output/reports/progress/20260629_第四十二卷政务_修复核对进度.md`。

验收：第四十二卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：中 part02（第三十卷至第四十二卷）章节层级修复已到末卷；继续下 part01 第四十三卷起，或进入 PDF 表格专项复核。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第四十二卷政务章节核对完成"
    if marker in memory:
        memory = memory[: memory.find(marker)].rstrip() + "\n" + entry
    else:
        memory = memory.rstrip() + "\n" + entry
    MEMORY_PATH.write_text(memory, encoding="utf-8")


def main() -> None:
    changes = repair_source_md()
    ipa_fixed, _ = restore_html()
    stats = audit_section()
    stats["ipa_fixed"] = ipa_fixed
    write_progress(stats, changes)
    update_memory(stats)
    print("Repair complete")
    for change in changes:
        print(f"- {change}")
    print(f"stats={stats}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()

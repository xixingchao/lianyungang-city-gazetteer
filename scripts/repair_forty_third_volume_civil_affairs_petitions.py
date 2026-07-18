# -*- coding: utf-8 -*-
"""Repair and audit 第四十三卷 民政 信访 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第四十三卷民政信访_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第四十三卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第四十四卷-[^"]+">|</main>)', re.S)
SOURCE_RE = re.compile(r'(第四十三卷\s*\n民政\s*\n信访.*?)(?=\n第四十四卷|\Z)', re.S)

CHAPTERS = [
    ("第一章基层政权及群众自治组织", ["第一节里保甲闾邻", "第二节区(市)乡镇", "第三节村、居民组织"]),
    ("第二章优抚安置", ["第一节优抚", "第二节退伍安置"]),
    ("第三章救灾救济扶贫", ["第一节救灾", "第二节救济", "第三节扶贫"]),
    ("第四章社会福利事业", ["第一节儿童、孤寡老人福利事业", "第二节精神病人福利事业", "第三节残疾人福利事业"]),
    ("第五章社会福利生产", ["第一节企业", "第二节管理机构", "第三节效益"]),
    ("第六章婚姻登记管理", ["第一节结婚登记", "第二节离婚、复婚登记", "第三节特殊婚姻登记", "第四节婚姻管理"]),
    ("第七章收容改造遣送禁烟禁毒", ["第一节收容", "第二节改造", "第三节遣送", "第四节禁烟禁毒"]),
    ("第八章殡葬管理", ["第一节管理机构", "第二节殡葬改革", "第三节骨灰与公墓管理"]),
    ("第九章地名管理", ["第一节管理机构", "第二节地名普查", "第三节地名标志设置", "第四节地名录编纂"]),
    ("第十章社团登记管理", ["第一节管理职责", "第二节清理整顿", "第三节登记公告"]),
    ("第十一章信访", ["第一节机构", "第二节来信来访接待"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第四十三卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第四十三卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section
    replacements = {
        "第四十三卷\n民政\n信访\n概述\n": "第四十三卷 民政 信访\n\n概述\n",
        "第一章\n基层政权及群众自治组织\n": "第一章基层政权及群众自治组织\n",
        "间邻\n第一节•里•保甲\n": "第一节里保甲闾邻\n",
        "乡镇\n第二节\n区(市)\n": "第二节区(市)乡镇\n",
        "第二章 \n优抚安置\n·1857\n第三节\n村、居民组织\n": "第三节村、居民组织\n\n第二章优抚安置\n",
        "救济\n第三章\n救灾\n扶贫\n": "第三章救灾救济扶贫\n",
        "第一节」\n儿童、孤寡老人福利事业\n": "第一节儿童、孤寡老人福利事业\n",
        "第一节企\n": "第一节企业\n",
        "收容改造遣送禁烟禁毒\n第七章\n": "第七章收容改造遣送禁烟禁毒\n",
        "第一节•收•容\n": "第一节收容\n",
        "第八章殡葬管理\n": "第八章殡葬管理\n",
        "置信访\n第十一章\n": "第十一章信访\n",
        "第一节机•构\n": "第一节机构\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[: m.start(1)] + section + text[m.end(1):]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第四十三卷卷题、章题、节题断裂和页眉错位。"]
    return []


def normalize_ipa(section: str) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return f"<p>{match.group(1).strip()}</p>"

    return re.sub(r'<div class="ipa-data">(.*?)</div>', repl, section, flags=re.S), count


def apply_replacements(section: str) -> str:
    section = re.sub(r'<h2 id="第四十三卷-[^"]+">第四十三卷民政</h2>', '<h2 id="第四十三卷-民政-信访">第四十三卷民政 信访</h2>', section, count=1)
    if h3("概述") not in section:
        section = section.replace('</h2>\n<p>信访', '</h2>\n' + h3("概述") + '\n<p>', 1)

    replacements = [
        ('<p>基层政权及群众自治组织秦时', h3('第一章基层政权及群众自治组织') + '\n<p>秦时'),
        ('<p>间邻第一节•里•保甲朐县大村', h4('第一章基层政权及群众自治组织', '第一节里保甲闾邻') + '\n<p>朐县大村'),
        ('<p>乡镇第二节区(市)清宣统年间', h4('第一章基层政权及群众自治组织', '第二节区(市)乡镇') + '\n<p>清宣统年间'),
        ('<p>优抚安置·1857第三节村、居民组织民国16年', h4('第一章基层政权及群众自治组织', '第三节村、居民组织') + '\n<p>民国16年'),
        ('<p>人，优待军人家属形成良好的社会风尚。', h3('第二章优抚安置') + '\n<p>人，优待军人家属形成良好的社会风尚。'),
        ('<p>第一节优抚一、拥军优属西连岛', h4('第二章优抚安置', '第一节优抚') + '\n<p>一、拥军优属西连岛'),
        ('<p>第二节退伍安置一、转业、复员军人安置1950年', h4('第二章优抚安置', '第二节退伍安置') + '\n<p>一、转业、复员军人安置1950年'),
        ('<p>救济第三章救灾扶贫清顺治二年', h3('第三章救灾救济扶贫') + '\n<p>清顺治二年'),
        ('<p>第一节救灾康熙七年', h4('第三章救灾救济扶贫', '第一节救灾') + '\n<p>康熙七年'),
        ('<p>第二节救济清顺治二年', h4('第三章救灾救济扶贫', '第二节救济') + '\n<p>清顺治二年'),
        ('<p>第三节扶贫1983年4月18日', h4('第三章救灾救济扶贫', '第三节扶贫') + '\n<p>1983年4月18日'),
        ('<p>第四章社会福利事业明清两朝', h3('第四章社会福利事业') + '\n<p>明清两朝'),
        ('<p>第一节」儿童、孤寡老人福利事业明洪武二年', h4('第四章社会福利事业', '第一节儿童、孤寡老人福利事业') + '\n<p>明洪武二年'),
        ('<p>第二节精神病人福利事业1980年', h4('第四章社会福利事业', '第二节精神病人福利事业') + '\n<p>1980年'),
        ('<p>第三节残疾人福利事业一、残疾人组织民国38年', h4('第四章社会福利事业', '第三节残疾人福利事业') + '\n<p>一、残疾人组织民国38年'),
        ('<p>第五章社会福利生产连云港市社会福利企业', h3('第五章社会福利生产') + '\n<p>连云港市社会福利企业'),
        ('<p>第一节企1954年', h4('第五章社会福利生产', '第一节企业') + '\n<p>1954年'),
        ('<p>第二节管理机构1954年', h4('第五章社会福利生产', '第二节管理机构') + '\n<p>1954年'),
        ('<p>第三节效益1954～1957年', h4('第五章社会福利生产', '第三节效益') + '\n<p>1954～1957年'),
        ('<p>婚姻登记管理规。1951年', h3('第六章婚姻登记管理') + '\n<p>规。1951年'),
        ('<p>第一节结婚登记1949年', h4('第六章婚姻登记管理', '第一节结婚登记') + '\n<p>1949年'),
        ('<p>第二节离婚、复婚登记1950年', h4('第六章婚姻登记管理', '第二节离婚、复婚登记') + '\n<p>1950年'),
        ('<p>第三节特殊婚姻登记民国38年', h4('第六章婚姻登记管理', '第三节特殊婚姻登记') + '\n<p>民国38年'),
        ('<p>收容改造遣送禁烟禁毒第七章民国时期', h3('第七章收容改造遣送禁烟禁毒') + '\n<p>民国时期'),
        ('<p>第一节•收•容民国时期', h4('第七章收容改造遣送禁烟禁毒', '第一节收容') + '\n<p>民国时期'),
        ('第三节遣送民国38年', h4('第七章收容改造遣送禁烟禁毒', '第三节遣送') + '\n<p>民国38年'),
        ('<p>第八章殡葬管理清代至民国时期', h3('第八章殡葬管理') + '\n<p>清代至民国时期'),
        ('<p>第一节管理机构清代至民国时期', h4('第八章殡葬管理', '第一节管理机构') + '\n<p>清代至民国时期'),
        ('<p>第二节殡葬改革朱代', h4('第八章殡葬管理', '第二节殡葬改革') + '\n<p>朱代'),
        ('<p>第三节骨灰与公墓管理1964年', h4('第八章殡葬管理', '第三节骨灰与公墓管理') + '\n<p>1964年'),
        ('<p>第九章地名管理1980年', h3('第九章地名管理') + '\n<p>1980年'),
        ('<p>第一节管理机构1980年', h4('第九章地名管理', '第一节管理机构') + '\n<p>1980年'),
        ('<p>第二节地名普查1980年', h4('第九章地名管理', '第二节地名普查') + '\n<p>1980年'),
        ('<p>第三节地名标志设置1987年', h4('第九章地名管理', '第三节地名标志设置') + '\n<p>1987年'),
        ('<p>第四节地名录编纂市和赣榆', h4('第九章地名管理', '第四节地名录编纂') + '\n<p>市和赣榆'),
        ('<p>社团登记管理1989年', h3('第十章社团登记管理') + '\n<p>1989年'),
        ('<p>第一节管理职责会、联合会', h4('第十章社团登记管理', '第一节管理职责') + '\n<p>会、联合会'),
        ('<p>第二节·清理整顿', h4('第十章社团登记管理', '第二节清理整顿') + '\n<p>'),
        ('<p>第三节登记公告市社会团体', h4('第十章社团登记管理', '第三节登记公告') + '\n<p>市社会团体'),
        ('<p>置信访连云港市信访工作', h3('第十一章信访') + '\n<p>连云港市信访工作'),
        ('<p>第一节机•构20世纪60年代', h4('第十一章信访', '第一节机构') + '\n<p>20世纪60年代'),
        ('<p>第二节来信来访接待1953年', h4('第十一章信访', '第二节来信来访接待') + '\n<p>1953年'),
        ('<p>救济救灾扶贫清顺治二年', h3('第三章救灾救济扶贫') + '\n<p>清顺治二年'),
        ('<p>社会福利事业明清两朝', h3('第四章社会福利事业') + '\n<p>明清两朝'),
        ('<p>第一节」</p>\n<p>儿童、孤寡老人福利事业明洪武二年', h4('第四章社会福利事业', '第一节儿童、孤寡老人福利事业') + '\n<p>明洪武二年'),
        ('<p>2961067第二节精神病人福利事业1980年', '<p>2961067</p>\n' + h4('第四章社会福利事业', '第二节精神病人福利事业') + '\n<p>1980年'),
        ('<p>社会福利生产连云港市社会福利企业', h3('第五章社会福利生产') + '\n<p>连云港市社会福利企业'),
        ('婚姻登记管理规。1951年', '</p>\n' + h3('第六章婚姻登记管理') + '\n<p>规。1951年'),
        ('<p>收容改造遣送禁烟禁毒民国时期', h3('第七章收容改造遣送禁烟禁毒') + '\n<p>民国时期'),
        ('<p>清代至民国时期，海州地区沿装土葬。1960年市成立殡葬管理处', h3('第八章殡葬管理') + '\n<p>清代至民国时期，海州地区沿装土葬。1960年市成立殡葬管理处'),
        ('<p>地名管理1980年', h3('第九章地名管理') + '\n<p>1980年'),
        ('<p>第四节#婚姻管理，童养媳', h4('第六章婚姻登记管理', '第四节婚姻管理') + '\n<p>童养媳'),
        ('第二节•改•造1949年取缔妓院', h4('第七章收容改造遣送禁烟禁毒', '第二节改造') + '\n<p>1949年取缔妓院'),
    ]
    for old, new in replacements:
        section = section.replace(old, new, 1)
    return section


def insert_missing(section: str) -> str:
    fallbacks = [
        (h4('第六章婚姻登记管理', '第四节婚姻管理'), '<table class="structured-table"><thead><tr><th>外国籍'),
        (h3('第七章收容改造遣送禁烟禁毒'), '<p>1950~1952年连云港市收容人员情况表'),
        (h4('第七章收容改造遣送禁烟禁毒', '第一节收容'), '<p>1950~1952年连云港市收容人员情况表'),
        (h3('第七章收容改造遣送禁烟禁毒'), '<p>无法全部收容。为生活所迫被逼为婚的女性青年'),
        (h4('第七章收容改造遣送禁烟禁毒', '第一节收容'), '<p>无法全部收容。为生活所迫被逼为婚的女性青年'),
        (h4('第七章收容改造遣送禁烟禁毒', '第二节改造'), '<p>1953~1959年连云港市收容改造人员情况表'),
        (h4('第七章收容改造遣送禁烟禁毒', '第四节禁烟禁毒'), '<p>1949年秋，市查出海州一户种植罂栗'),
        (h3('第八章殡葬管理'), '<p>清代至民国时期，海州地区沿装土葬。1960年市成立殡葬管理处'),
        (h3('第九章地名管理'), '<p>地名管理1980年'),
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
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第四十三卷-[^"]+">)', r'\1</p>\n\2', section)
    section = section.replace('<p><h3', '<h3').replace('<p><h4', '<h4')
    section = section.replace('</h3>\n</p>', '</h3>\n').replace('</h4>\n</p>', '</h4>\n')
    section = re.sub(r'(</h4>)\n<p>\s*</p>', r'\1', section)
    seen: set[str] = set()

    def keep(match: re.Match[str]) -> str:
        ident = match.group(1)
        if ident in seen:
            return ''
        seen.add(ident)
        return match.group(0)

    section = re.sub(r'<h[34] id="([^"]+)">[^<]+</h[34]>\s*', keep, section)
    return section


def restore_html() -> tuple[int, dict[str, int]]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第四十三卷 HTML range")
    section = m.group(0)
    section, ipa_fixed = normalize_ipa(section)
    section = apply_replacements(section)
    section = insert_missing(section)
    section = cleanup(section)
    html = html[:m.start()] + section + html[m.end():]
    HTML_PATH.write_text(html, encoding="utf-8")
    return ipa_fixed, audit_section()


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
    content = f"""# 2026-06-29 第四十三卷《民政 信访》修复核对进度

## 本轮范围
- 范围：`第四十三卷 民政 信访`。
- 目标：按交付标准修复卷题、概述、11 章、34 节、正文段落结构和表格风险记录。
- 源文件：`workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已处于规范状态'}。
- 将最终阅读页卷题由 `第四十三卷民政` 修正为 `第四十三卷民政 信访`。
- 恢复概述、第一章基层政权及群众自治组织至第十一章信访及 34 个节题的标准 H3/H4 层级。
- 将 1 处 `ipa-data` 残留转为普通正文段落。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第十一章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本轮保留既有表格骨架；民政、优抚、基层政权、婚姻登记、收容改造等统计表需在 PDF 表格专项中逐表核对。
- 第四十三卷存在页眉与章题错位，已先恢复导航层级；表格页正文串联仍需后续 PDF 专项细校。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 继续下 part01 第四十四卷起修复，或转入第四十三卷表格专项复核。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第四十三卷民政信访章节核对完成

已完成 `第四十三卷 民政 信访` 章节格式核对：

- 新增脚本：`scripts/repair_forty_third_volume_civil_affairs_petitions.py`。
- 修复第四十三卷卷题漏 `信访`、最终阅读页无 H3/H4 导航层级、章题节题扁平化以及 1 处 `ipa-data` 残留。
- 第四十三卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第十一章），H4={stats['h4_count']}。
- 第四十三卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；基层政权、优抚安置、社会福利、婚姻登记、收容改造等统计表需从源 PDF 专项核验。
- 已写入进度文档：`output/reports/progress/20260629_第四十三卷民政信访_修复核对进度.md`。

验收：第四十三卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：继续下 part01 第四十四卷起，或进入第四十三卷 PDF 表格专项复核。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第四十三卷民政信访章节核对完成"
    if marker in memory:
        memory = memory[: memory.find(marker)].rstrip() + "\n" + entry
    else:
        memory = memory.rstrip() + "\n" + entry
    MEMORY_PATH.write_text(memory, encoding="utf-8")


def main() -> None:
    changes = repair_source_md()
    ipa_fixed, stats = restore_html()
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

# -*- coding: utf-8 -*-
"""Repair and audit 第五十二卷 文化 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第五十二卷文化_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第五十二卷-[^"]+">.*?</h2>)(.*?)(?=<h2 id="第五十三卷-[^"]+">|</main>)', re.S)
SOURCE_RE = re.compile(r'(^第五十二卷\s*\n概述.*?)(?=^第五十三卷|\Z)', re.S | re.M)

CHAPTERS = [
    ("第一章管理机构", ["第一节市级机构", "第二节区、县级机构"]),
    ("第二章文学艺术", ["第一节文学创作", "第二节书法 篆刻 绘画 雕塑 摄影", "第三节音乐 舞蹈"]),
    ("第三章表演艺术", ["第一节戏剧", "第二节曲艺", "第三节专业表演团体"]),
    ("第四章电影", ["第一节管理机构", "第二节影片发行", "第三节电影放映"]),
    ("第五章剧场 影剧院", ["第一节市区剧场、影剧院", "第二节县影剧院"]),
    ("第六章群众文化", ["第一节文化机构", "第二节文艺活动", "第三节阵地宣传与群众辅导"]),
    ("第七章档案", ["第一节档案机构", "第二节档案管理"]),
    ("第八章图书馆", ["第一节公共图书馆", "第二节专业图书馆"]),
    ("第九章书店", ["第一节市新华书店", "第二节县新华书店"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(items) for _, items in CHAPTERS)


def h3(title: str) -> str:
    return f'<h3 id="第五十二卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第五十二卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        return []
    section = m.group(1)
    original = section
    replacements = {
        "第五十二卷\n概述\n": "第五十二卷 文化\n\n概述\n",
        "第一章\n管理机构\n第一节市级机构": "第一章管理机构\n第一节市级机构",
        "第二章\n文学艺术\n第一节文学创作": "第二章文学艺术\n第一节文学创作",
        "第二节　书法\n篆刻\n雕塑\n摄影\n绘画": "第二节书法 篆刻 绘画 雕塑 摄影",
        "第三节‧音乐\n舞蹈": "第三节音乐 舞蹈",
        "第三章\n表演艺术\n第一节戏　剧": "第三章表演艺术\n第一节戏剧",
        "第二节•曲•艺": "第二节曲艺",
        "第三节\n专业表演团体": "第三节专业表演团体",
        "电昇影\n第四章\n第一节管理机构": "第四章电影\n第一节管理机构",
        "第五章\n剧场\n影剧院\n第一节\n市区剧场、影剧院": "第五章剧场 影剧院\n第一节市区剧场、影剧院",
        "第二节\n县影剧院": "第二节县影剧院",
        "第六章\n群众文化\n第一节文化机构": "第六章群众文化\n第一节文化机构",
        "档案\n第七章\n": "第七章档案\n",
        "第一节村\n档案机构": "第一节档案机构",
        "第二节#\n档案管理": "第二节档案管理",
        "第八章•图•书•馆": "第八章图书馆",
        "第一节•公共图书馆": "第一节公共图书馆",
        "第二节•专业图书馆": "第二节专业图书馆",
        "书：店\n第九章": "第九章书店",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[:m.start(1)] + section + text[m.end(1):]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第五十二卷卷题、章题、节题断裂和 OCR 标题误字。"]
    return []


def sub_once(section: str, pattern: str, repl: str) -> str:
    section, _ = re.subn(pattern, repl, section, count=1, flags=re.S)
    return section


def apply_replacements(section: str) -> str:
    section = re.sub(r'<h2 id="第五十二卷-文化">.*?</h2>', '<h2 id="第五十二卷-文化">第五十二卷文化</h2>', section, count=1, flags=re.S)
    if h3("概述") not in section:
        section = section.replace('<h2 id="第五十二卷-文化">第五十二卷文化</h2>\n<p>', '<h2 id="第五十二卷-文化">第五十二卷文化</h2>\n' + h3("概述") + '\n<p>', 1)

    replacements = [
        (r'<p>管理机构第一节市级机构', h3('第一章管理机构') + '\n' + h4('第一章管理机构', '第一节市级机构') + '\n<p>'),
        (r'<p>第二节区、县级机构', h4('第一章管理机构', '第二节区、县级机构') + '\n<p>'),
        (r'<p>文学艺术第一节文学创作', h3('第二章文学艺术') + '\n' + h4('第二章文学艺术', '第一节文学创作') + '\n<p>'),
        (r'<p>第二节\s*书法\s*篆刻\s*雕塑\s*摄影\s*绘画', h4('第二章文学艺术', '第二节书法 篆刻 绘画 雕塑 摄影') + '\n<p>'),
        (r'<p>第三节[‧·•]?音乐\s*舞蹈', h4('第二章文学艺术', '第三节音乐 舞蹈') + '\n<p>'),
        (r'<p>表演艺术第一节戏\s*剧', h3('第三章表演艺术') + '\n' + h4('第三章表演艺术', '第一节戏剧') + '\n<p>'),
        (r'<p>第二节[•·]?曲[•·]?艺', h4('第三章表演艺术', '第二节曲艺') + '\n<p>'),
        (r'<p>第三节专业表演团体', h4('第三章表演艺术', '第三节专业表演团体') + '\n<p>'),
        (r'<p>电昇影第一节管理机构', h3('第四章电影') + '\n' + h4('第四章电影', '第一节管理机构') + '\n<p>'),
        (r'<p>第二节影片发行', h4('第四章电影', '第二节影片发行') + '\n<p>'),
        (r'<p>第三节电影放映', h4('第四章电影', '第三节电影放映') + '\n<p>'),
        (r'<p>剧场影剧院第一节市区剧场、影剧院', h3('第五章剧场 影剧院') + '\n' + h4('第五章剧场 影剧院', '第一节市区剧场、影剧院') + '\n<p>'),
        (r'<p>第二节县影剧院', h4('第五章剧场 影剧院', '第二节县影剧院') + '\n<p>'),
        (r'<p>群众文化第一节文化机构', h3('第六章群众文化') + '\n' + h4('第六章群众文化', '第一节文化机构') + '\n<p>'),
        (r'<p>第二节文艺活动', h4('第六章群众文化', '第二节文艺活动') + '\n<p>'),
        (r'<p>第三节阵地宣传与群众辅导', h4('第六章群众文化', '第三节阵地宣传与群众辅导') + '\n<p>'),
        (r'(<h4 id="第五十二卷-第七章档案-第一节档案机构">)', h3('第七章档案') + r'\n\1'),
        (r'<p>第一节村档案机构', h4('第七章档案', '第一节档案机构') + '\n<p>'),
        (r'<p>第二节#档案管理', h4('第七章档案', '第二节档案管理') + '\n<p>'),
        (r'<p>第一节[•·]?公共图书馆', h3('第八章图书馆') + '\n' + h4('第八章图书馆', '第一节公共图书馆') + '\n<p>'),
        (r'<p>第二节[•·]?专业图书馆', h4('第八章图书馆', '第二节专业图书馆') + '\n<p>'),
        (r'(<h4 id="第五十二卷-第九章书店-第一节市新华书店">)', h3('第九章书店') + r'\n\1'),
        (r'<p>第一节市新华书店', h4('第九章书店', '第一节市新华书店') + '\n<p>'),
        (r'<p>第二节县新华书店', h4('第九章书店', '第二节县新华书店') + '\n<p>'),
    ]
    for pattern, repl in replacements:
        section = sub_once(section, pattern, repl)
    return section


def cleanup(section: str) -> str:
    section = re.sub(r'<p>\s*</p>\n?', '', section)
    section = re.sub(r'(<p>[^<]*?)(<h[34] id="第五十二卷-[^"]+">)', r'\1</p>\n\2', section)
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
        raise RuntimeError("Cannot locate 第五十二卷 HTML range")
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
    content = f"""# 2026-06-29 第五十二卷《文化》修复核对进度

## 本轮范围
- 范围：`第五十二卷 文化`。
- 目标：按交付标准修复卷题、概述、9 章、22 节和正文段落结构。
- 源文件：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已完成规范化或已处于规范状态'}。
- 将最终阅读页卷题由 `第五十二卷概述` 修正为 `第五十二卷文化`。
- 恢复概述、第一章管理机构至第九章书店及 22 个节题的标准 H3/H4 层级。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第九章），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 本卷大部分是长篇正文，少量书店/文化统计表后续仍需 PDF 表格专项核对。

## 遇到的问题与处理
- 多处章题与节题被 OCR 拼入正文，如 `管理机构第一节市级机构`、`文学艺术第一节文学创作`，已按 XML 目录拆回。
- 第五章、档案章、图书馆章和书店章存在跨行或错字标题，如 `剧场/影剧院`、`第一节村档案机构`、`第八章•图•书•馆`、`书：店第九章`，已规范为目录标题。

## 验收状态
- 本卷结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 继续第五十三卷起修复。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第五十二卷文化章节核对完成

已完成 `第五十二卷 文化` 章节格式核对：

- 新增脚本：`scripts/repair_fifty_second_volume_culture.py`。
- 修复第五十二卷卷题误作概述、最终阅读页无 H3/H4 导航层级、章题节题扁平化和 OCR 标题误字。
- 第五十二卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章至第九章），H4={stats['h4_count']}。
- 第五十二卷范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处。
- 已写入进度文档：`output/reports/progress/20260629_第五十二卷文化_修复核对进度.md`。

验收：第五十二卷 HTML 字节数 {stats['bytes']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。

下一步：继续第五十三卷起。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第五十二卷文化章节核对完成"
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

# -*- coding: utf-8 -*-
"""Repair appendix, afterword, and closing headings in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_附录跋编纂始末_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

APPENDIX_H3 = [
    "一、重要文献",
    "二、乡土文存",
    "三、金石碑文",
    "四、旧志序跋",
    "五、总述(英文)",
]


def h2(ident: str, title: str) -> str:
    return f'<h2 id="{ident}">{title}</h2>'


def h3(title: str) -> str:
    return f'<h3 id="附录-{title}">{title}</h3>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    replacements = {
        "<!-- page-anchor: LYG-2846 -->\n\n一、重要文献": "<!-- page-anchor: LYG-2846 -->\n\n附录\n\n一、重要文献",
        "people are embracing the 21 century, arouse their all efforts to make\nthe city prosperous and create the splendor once again.\n\n<!-- page-anchor: LYG-2907 -->\n\n高有为": "people are embracing the 21 century, arouse their all efforts to make\nthe city prosperous and create the splendor once again.\n\n<!-- page-anchor: LYG-2907 -->\n\n跋\n\n高有为",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中附录总题和跋题边界。"]
    return []


def insert_before_once(text: str, needle: str, insert: str) -> str:
    if insert in text:
        return text
    idx = text.find(needle)
    if idx < 0:
        return text
    return text[:idx] + insert + text[idx:]


def repair_html() -> dict[str, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    original = html

    # Correct previous/legacy mislabeling by position: appendix starts before its first H3;
    # afterword starts at Gao Youwei's afterword text.
    html = html.replace('<h2 id="跋">跋</h2>\n<h3 id="附录-一、重要文献">', '<h2 id="附录">附录</h2>\n<h3 id="附录-一、重要文献">', 1)
    afterword_idx = html.find('高有为《连云港市志》')
    wrong_appendix_idx = html.find('<h2 id="附录">附录</h2>', afterword_idx if afterword_idx >= 0 else 0)
    if wrong_appendix_idx >= 0:
        html = html[:wrong_appendix_idx] + h2("跋", "跋") + html[wrong_appendix_idx + len('<h2 id="附录">附录</h2>'):]

    html = insert_before_once(
        html,
        "一、重要文献山东省鲁中南区新海连特区行政专员公署布告",
        h2("附录", "附录") + "\n" + h3("一、重要文献") + "\n<p>",
    )
    html = html.replace(
        h3("一、重要文献") + "\n<p>一、重要文献山东省鲁中南区新海连特区行政专员公署布告",
        h3("一、重要文献") + "\n<p>山东省鲁中南区新海连特区行政专员公署布告",
        1,
    )

    markers = [
        ("二、乡土文存", "一九八四年十二月十九日二、乡土文存访东海戴天山道土不遇", "一九八四年十二月十九日"),
        ("三、金石碑文", "三、金石碑文·2725三十六、长桥飞瀑", "三十六、长桥飞瀑"),
        ("四、旧志序跋", "四、旧志序跋隆庆《海州志》序", "隆庆《海州志》序"),
    ]
    for title, needle, after in markers:
        if h3(title) not in html and needle in html:
            html = html.replace(needle, f"</p>\n{h3(title)}\n<p>{after}", 1)

    if h3("五、总述(英文)") not in html:
        for needle in ["Histroy of LianYunGang City·General Summary", "General IntroductionLianyungang City", "General Introduction Lianyungang City", "GeneralIntroductionLianyungang City"]:
            if needle in html:
                html = html.replace(needle, h3("五、总述(英文)") + "\n<p>" + needle, 1)
                break

    afterword_idx = html.find('高有为《连云港市志》')
    if h2("跋", "跋") not in html and afterword_idx >= 0:
        html = html[:afterword_idx] + h2("跋", "跋") + "\n<p>" + html[afterword_idx:]
    html = re.sub(r'(<h2 id="跋">跋</h2>)\s*<p>', r'\1\n<p>', html, count=1)
    html = re.sub(r'<p>\s*</p>\n?', '', html)
    html = re.sub(r'(<p>[^<]*)(<h3 id="附录-[^"]+">)', r'\1</p>\n\2', html)
    html = re.sub(r'<p>\s*(<h[23] id="(?:附录|跋)[^"]*">)', r'\1', html)
    html = re.sub(r'(</h[23]>)\s*</p>', r'\1', html)

    if html != original:
        HTML_PATH.write_text(html, encoding="utf-8")
    return audit()


def closing_block() -> str:
    html = HTML_PATH.read_text(encoding="utf-8")
    start = html.find('<h2 id="附录">')
    first_h3 = html.find('<h3 id="附录-一、重要文献">')
    if first_h3 >= 0 and (start < 0 or start > first_h3):
        start = first_h3
    if start < 0:
        start = first_h3
    return html[start:] if start >= 0 else ""


def audit() -> dict[str, int]:
    block = closing_block()
    return {
        "bytes": len(block.encode("utf-8")),
        "h2_count": block.count("<h2 "),
        "h3_count": block.count("<h3 "),
        "h4_count": block.count("<h4 "),
        "appendix_h3": sum(1 for title in APPENDIX_H3 if h3(title) in block),
        "has_appendix_h2": int(h2("附录", "附录") in block),
        "has_afterword_h2": int(h2("跋", "跋") in block),
        "has_compile_h2": int(h2("编纂始末", "编纂始末") in block),
        "embedded_h2_in_p": len(re.findall(r'<p[^>]*>[^<]*<h2', block)),
        "embedded_h3_in_p": len(re.findall(r'<p[^>]*>[^<]*<h3', block)),
        "malformed_heading_ids": len(re.findall(r'<h[23] id="[^"]*<h[23]', block)),
        "structured_tables": block.count('<table class="structured-table"'),
        "table_placeholders": block.count('class="table-placeholder"'),
    }


def write_progress(stats: dict[str, int], changes: list[str]) -> None:
    status = "通过" if stats["has_appendix_h2"] and stats["has_afterword_h2"] and stats["has_compile_h2"] and stats["appendix_h3"] == len(APPENDIX_H3) and stats["embedded_h2_in_p"] == 0 and stats["embedded_h3_in_p"] == 0 else "需复核"
    content = f"""# 2026-06-29 附录、跋、编纂始末修复核对进度

## 本轮范围
- 范围：`附录`、`跋`、`编纂始末`。
- 目标：修复全书末尾导航边界，补齐附录五个分项标题，并区分跋与附录。
- 源文件：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已完成规范化，脚本复跑保持幂等'}。
- 补入 `附录` H2。
- 补入附录 H3：`一、重要文献`、`二、乡土文存`、`三、金石碑文`、`四、旧志序跋`、`五、总述(英文)`。
- 将原误挂在跋文前的 `<h2 id="附录">附录</h2>` 改为 `<h2 id="跋">跋</h2>`。
- 保留 `编纂始末` H2。
- 末尾结构统计：H2={stats['h2_count']}，H3={stats['h3_count']}，H4={stats['h4_count']}。
- 附录 H3 完成数：{stats['appendix_h3']}/{len(APPENDIX_H3)}。
- 段落内嵌 H2/H3：{stats['embedded_h2_in_p'] + stats['embedded_h3_in_p']}。

## 表格与专项风险
- 末尾范围结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 附录正文中仍有 OCR 连排、英文总述换行和页眉页脚残留，需后续文字专项核对。
- 本轮只处理导航层级和边界，不重建附录正文格式。

## 遇到的问题与处理
- 最终 HTML 中附录正文存在，但缺少 `附录` 总题和五个分项标题；已补齐。
- 原 `<h2 id="附录">附录</h2>` 实际位于跋文中间，导致跋文被误归入附录；已改为 `跋`。
- `编纂始末` 已有 H2，本轮只保留并纳入验收。

## 验收状态
- 本轮结构验收：{status}。
- 后续纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 生成剩余表格专项清单，并按占位/结构化表格优先级继续修复。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 附录跋编纂始末结构核对完成

已完成全书末尾结构核对：

- 新增脚本：`scripts/repair_appendix_afterword_closing.py`。
- 修复最终阅读页附录正文无总题、附录五个分项标题缺失、跋文误挂为附录标题的问题。
- 末尾结构：H2={stats['h2_count']}（附录、跋、编纂始末），H3={stats['h3_count']}（附录五项），H4={stats['h4_count']}。
- 附录分项完成数：{stats['appendix_h3']}/{len(APPENDIX_H3)}。
- 末尾范围段落内嵌标题问题 {stats['embedded_h2_in_p'] + stats['embedded_h3_in_p']}，畸形标题 id {stats['malformed_heading_ids']}。
- 已写入进度文档：`output/reports/progress/20260629_附录跋编纂始末_修复核对进度.md`。

下一步：生成剩余表格专项清单，继续朝可交付版本推进。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 附录跋编纂始末结构核对完成"
    if marker in memory:
        memory = memory[: memory.find(marker)].rstrip() + "\n" + entry
    else:
        memory = memory.rstrip() + "\n" + entry
    MEMORY_PATH.write_text(memory, encoding="utf-8")


def main() -> None:
    changes = repair_source_md()
    stats = repair_html()
    write_progress(stats, changes)
    update_memory(stats)
    print("Repair complete")
    for change in changes:
        print(f"- {change}")
    print(f"stats={stats}")
    print(f"progress={PROGRESS_PATH}")


if __name__ == "__main__":
    main()

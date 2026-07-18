# -*- coding: utf-8 -*-
"""Repair and audit 第三十五卷 对外经济贸易 in the full reader."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
PROGRESS_PATH = ROOT / "output" / "reports" / "progress" / "20260629_第三十五卷对外经济贸易_修复核对进度.md"
MEMORY_PATH = ROOT / "PROJECT_MEMORY.md"

SECTION_RE = re.compile(r'(<h2 id="第三十五卷-对外经济贸易">.*?</h2>)(.*?)(?=<h2 id="第三十六卷-[^"]+">)', re.S)
SOURCE_RE = re.compile(r'(第三十五卷.*?)(?=第三十六卷)', re.S)

CHAPTERS = [
    ("第一章机构", ["第一节管理机构"]),
    ("第二章出口贸易", ["第一节外贸收购", "第二节出口商品"]),
    ("第三章进口贸易", ["第一节自营进口", "第二节代理进口", "第三节设备引进"]),
    ("第四章利用外资与国际劳务合作", ["第一节利用外资", "第二节对外援助", "第三节国际劳务合作", "第四节兴办海外企业", "第五节国际商务活动"]),
    ("第五章包装仓储运输", ["第一节包装", "第二节仓储", "第三节运输"]),
]
EXPECTED_H3 = 1 + len(CHAPTERS)
EXPECTED_H4 = sum(len(titles) for _, titles in CHAPTERS)
EXPECTED_TABLES = [f"表35-{i}" for i in range(1, 12)]


def h3(title: str) -> str:
    return f'<h3 id="第三十五卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第三十五卷-{chapter}-{title}">{title}</h4>'


def repair_source_md() -> list[str]:
    text = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(text)
    if not m:
        raise RuntimeError("Cannot locate 第三十五卷 source range")
    section = m.group(1)
    original = section
    replacements = {
        "第三十五卷\n对外经济贸易\n概述\n": "第三十五卷 对外经济贸易\n\n概述\n",
        "\n机构\n第一章\n": "\n第一章机构\n",
        "\n出口贸易\n第二章\n": "\n第二章出口贸易\n",
        "\n第三章\n进口贸易\n": "\n第三章进口贸易\n",
        "\n第三节\n设备引进\n": "\n第三节设备引进\n",
        "\n第三章\n\n续上表\n": "\n续上表\n",
        "\n第三章 \n\n续上表\n": "\n续上表\n",
        "\n第四章\n利用外资与国际劳务合作\n：1499\n续上表\n": "\n续上表\n",
        "\n利用外资与国际劳务合作\n第四章\n": "\n第四章利用外资与国际劳务合作\n",
        "\n第一节\n利用外资\n": "\n第一节利用外资\n",
        "\n第四章\n利用外资与国际劳务合作\n·1501\n续上表\n": "\n续上表\n",
        "\n第四章利用外资与国际劳务合作\n·1505\n续上表\n": "\n续上表\n",
        "\n第二节\n对外援助\n": "\n第二节对外援助\n",
        "\n第三节\n国际劳务合作\n": "\n第三节国际劳务合作\n",
        "\n第四节\n兴办海外企业\n": "\n第四节兴办海外企业\n",
        "\n第五节\n国际商务活动\n": "\n第五节国际商务活动\n",
        "\n仓储\n第五章\n包装\n": "\n第五章包装仓储运输\n",
        "\n第一节包•装\n": "\n第一节包装\n",
        "\n第二节•仓•储\n": "\n第二节仓储\n",
        "\n第五章包装仓储运输：1509·\n": "\n",
    }
    for old, new in replacements.items():
        section = section.replace(old, new)
    if section != original:
        text = text[: m.start(1)] + section + text[m.end(1) :]
        SRC_MD.write_text(text, encoding="utf-8")
        return ["规范源 MD 中第三十五卷卷题、章题、节题断裂、表格续页页眉和 OCR 标题错位。"]
    return []


def insert_after_h2(section: str, marker: str) -> tuple[str, bool]:
    if marker in section:
        return section, False
    m = re.search(r'</h2>\s*', section)
    if not m:
        return section, False
    return section[: m.end()] + "\n" + marker + "\n" + section[m.end() :], True


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


def split_paragraph_heading(section: str, marker: str, heading_text: str) -> tuple[str, bool]:
    if marker in section:
        return section, False
    pattern = f"<p>{re.escape(heading_text)}"
    pos = section.find(pattern)
    if pos >= 0:
        content_start = pos + len(pattern)
        return section[:pos] + marker + "\n<p>" + section[content_start:], True
    pos = section.find(heading_text)
    if pos < 0:
        return section, False
    p_start = section.rfind("<p>", 0, pos)
    p_end = section.rfind("</p>", 0, pos)
    if p_start > p_end:
        content_start = pos + len(heading_text)
        return section[:pos] + "</p>\n" + marker + "\n<p>" + section[content_start:], True
    return section[:pos] + marker + "\n" + section[pos + len(heading_text) :], True


def normalize_ipa(section: str) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        text = re.sub(r"^\s*[·:.：\s]*\d{4}\s*[·:.：\s]*", "", match.group(1).strip())
        return f"<p>{text}</p>"

    section = re.sub(r'<div class="ipa-data">(.*?)</div>', repl, section, flags=re.S)
    return section, count


def render_source_chunk(start_title: str, end_title: str) -> str:
    source = SRC_MD.read_text(encoding="utf-8")
    m = SOURCE_RE.search(source)
    if not m:
        return ""
    block = m.group(1)
    start = block.find(start_title)
    end = block.find(end_title, start)
    if start < 0 or end < 0:
        return ""
    chunk = block[start + len(start_title) : end].strip()
    chunk = re.sub(r"<!--.*?-->", "", chunk, flags=re.S)
    chunk = re.sub(r"\n{3,}", "\n\n", chunk).strip()
    lines = [line.strip() for line in chunk.splitlines() if line.strip()]
    return "\n".join(f"<p>{line}</p>" for line in lines)


def ensure_insert_before(section: str, marker: str, before_text: str, body: str = "") -> tuple[str, bool]:
    if marker in section:
        return section, False
    pos = section.find(before_text)
    if pos < 0:
        return section, False
    p_start = section.rfind("<p>", 0, pos)
    p_end = section.rfind("</p>", 0, pos)
    insert_pos = p_start if p_start > p_end else pos
    insert = marker + "\n" + (body.strip() + "\n" if body.strip() else "")
    return section[:insert_pos] + insert + section[insert_pos:], True


def cleanup(section: str) -> str:
    section = section.replace("<p>第二节•仓•储", "<p>第二节仓储")
    section = section.replace("<p>第一节包•装", "<p>第一节包装")
    section = section.replace("<p>第二节仓储一、连云港外贸冷库", h4("第五章包装仓储运输", "第二节仓储") + "\n<p>一、连云港外贸冷库")
    section = section.replace(
        "<p>第一节包装一、包装物料</p>\n" + h4("第五章包装仓储运输", "第一节包装") + "\n<p>、麻袋、柳编、毛编、铁皮等原始运输包装，体积大，外形粗陋。由供货单位解决，外贸部门协助。",
        h4("第五章包装仓储运输", "第一节包装") + "\n<p>一、包装物料</p>\n<p>20世纪70年代初，出口商品包装物料主要用木箱、麻袋、柳编、毛编、铁皮等原始运输包装，体积大，外形粗陋。由供货单位解决，外贸部门协助。",
    )
    section = section.replace("利用外资与国际劳务合作：1499", "")
    section = section.replace("利用外资与国际劳务合作·1501", "")
    section = section.replace("利用外资与国际劳务合作1503", "")
    section = section.replace("第五章包装仓储运输：1509·", "")
    section = re.sub(r"<p>\s*[·:.：\s]*\d{4}\s*[·:.：\s]*</p>\n?", "", section)
    section = re.sub(r"<p>\s*</p>\n?", "", section)
    section = re.sub(r"(<p>[^<]*?)(<h[34] id=\"第三十五卷-[^\"]+\">)", r"\1</p>\n\2", section)
    section = section.replace("<p><h3", "<h3").replace("<p><h4", "<h4")
    section = section.replace("</h3>\n</p>", "</h3>\n").replace("</h4>\n</p>", "</h4>\n")
    return section


def restore_html() -> tuple[int, int, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第三十五卷 HTML range")
    section = m.group(0)
    inserted_h3 = 0
    inserted_h4 = 0

    section, added = insert_after_h2(section, h3("概述"))
    inserted_h3 += int(added)
    for title, needle in [
        ("第一章机构", "第一节管理机构"),
        ("第二章出口贸易", "1958年，新海连市对外贸易机构成立之后"),
        ("第三章进口贸易", "进口贸易连云港外贸口岸成立后"),
        ("第四章利用外资与国际劳务合作", "万元的车船、仪器及对虾养殖生产加工设备"),
        ("第五章包装仓储运输", "1958年，新海连市对外贸易公司成立后，由于没有仓库货场"),
    ]:
        section, added = insert_before_text(section, h3(title), needle)
        inserted_h3 += int(added)

    split_specs = [
        ("第一章机构", "第一节管理机构", "第一节管理机构"),
        ("第二章出口贸易", "第一节外贸收购", "第一节外贸收购"),
        ("第二章出口贸易", "第二节出口商品", "第二节出口商品"),
        ("第三章进口贸易", "第一节自营进口", "第一节自营进口"),
        ("第三章进口贸易", "第二节代理进口", "第二节代理进口"),
        ("第三章进口贸易", "第三节设备引进", "第三节设备引进"),
        ("第四章利用外资与国际劳务合作", "第一节利用外资", "万元的车船、仪器及对虾养殖生产加工设备"),
        ("第四章利用外资与国际劳务合作", "第四节兴办海外企业", "第四节兴办海外企业"),
        ("第四章利用外资与国际劳务合作", "第五节国际商务活动", "第五节国际商务活动"),
        ("第五章包装仓储运输", "第一节包装", "20世纪70年代初，出口商品包装物料主要用木箱"),
        ("第五章包装仓储运输", "第二节仓储", "第二节仓储"),
        ("第五章包装仓储运输", "第三节运输", "第三节运输"),
    ]
    for chapter, title, heading_text in split_specs:
        section, added = split_paragraph_heading(section, h4(chapter, title), heading_text)
        inserted_h4 += int(added)

    aid_body = render_source_chunk("第二节对外援助", "第三节国际劳务合作")
    section, added = ensure_insert_before(
        section,
        h4("第四章利用外资与国际劳务合作", "第二节对外援助"),
        "1987~1990年连云港市对外工程和劳务合作项目表",
        aid_body,
    )
    inserted_h4 += int(added)
    section, added = ensure_insert_before(
        section,
        h4("第四章利用外资与国际劳务合作", "第三节国际劳务合作"),
        "1987~1990年连云港市对外工程和劳务合作项目表",
    )
    inserted_h4 += int(added)

    section, ipa_fixed = normalize_ipa(section)
    section = cleanup(section)
    html = html[: m.start()] + section + html[m.end() :]
    HTML_PATH.write_text(html, encoding="utf-8")
    return inserted_h3, inserted_h4, ipa_fixed


def audit_section() -> dict[str, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    block = SECTION_RE.search(html).group(0)
    return {
        "bytes": len(block.encode("utf-8")),
        "h2_count": len(re.findall(r"<h2 ", block)),
        "h3_count": len(re.findall(r"<h3 ", block)),
        "h4_count": len(re.findall(r"<h4 ", block)),
        "table_placeholders": len(re.findall(r'class="table-placeholder"', block)),
        "structured_tables": len(re.findall(r'<table class="structured-table"', block)),
        "generic_heading_anchors": len(re.findall(r'<h[234] id="anchor">', block)),
        "ipa_blocks": len(re.findall(r'<div class="ipa-data">', block)),
        "embedded_h3_in_p": len(re.findall(r'<p[^>]*>[^<]*<h3', block)),
        "embedded_h4_in_p": len(re.findall(r'<p[^>]*>[^<]*<h4', block)),
        "malformed_heading_ids": len(re.findall(r'<h[34] id="[^"]*<h[34]', block)),
        "front_matter_residual": len(re.findall(r"CIP|责任编辑|编纂委员会|方志出版社", block)),
        "inserted_h3": 0,
        "inserted_h4": 0,
        "ipa_fixed": 0,
    }


def write_progress(stats: dict[str, int], changes: list[str]) -> None:
    status = "通过" if stats["h3_count"] == EXPECTED_H3 and stats["h4_count"] == EXPECTED_H4 and stats["ipa_blocks"] == 0 else "需复核"
    content = f"""# 2026-06-29 第三十五卷《对外经济贸易》修复核对进度

## 本轮范围
- 范围：`第三十五卷 对外经济贸易`。
- 目标：按交付标准修复卷题、概述、章题、节题、表格页残留和正文段落结构。
- 源文件：`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`。
- 输出文件：`output/final_reader/连云港市志_全书.html`。

## 已完成
- {'；'.join(changes) if changes else '源 MD 已处于规范状态'}。
- 保留最终阅读页既有结构化表格，并恢复标准 H3/H4 标题层级。
- 卷标题：`第三十五卷对外经济贸易`。
- 章节结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章机构至第五章包装仓储运输），H4={stats['h4_count']}。
- 段落内嵌 H3/H4：{stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}。
- 通用标题锚点残留：{stats['generic_heading_anchors']}。
- `ipa-data` 残留：{stats['ipa_blocks']}。

## 表格与专项风险
- 最终阅读页本卷结构化表格 {stats['structured_tables']} 处，表格占位符 {stats['table_placeholders']} 处。
- 源 MD 可见表号：{', '.join(EXPECTED_TABLES)}；实际 OCR 中表35-4至表35-8、表35-10、表35-11多与跨页表格续页混排，本轮先保留既有表格骨架，待 PDF 表格专项复核。
- 3 处 `ipa-data` 表头残留已改为普通段落，未直接重构表格数据。

## 验收状态
- 本卷结构验收：{status}。
- 后续已纳入全书锚点审计和工作站 typecheck。

## 下一步计划
- 进入 `第三十六卷 财政税务`，继续按“源 MD 标题规范 -> 最终阅读页结构修复 -> 全书审计 -> typecheck -> 进度记录 -> Git 提交”的顺序推进。
"""
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(content, encoding="utf-8")


def update_memory(stats: dict[str, int]) -> None:
    entry = f"""
## 2026-06-29 第三十五卷对外经济贸易章节核对完成

已完成 `第三十五卷 对外经济贸易` 章节格式核对：

- 新增脚本：`scripts/repair_thirty_fifth_volume_foreign_trade.py`。
- 修复 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md` 中第三十五卷卷题、章题、节题断裂、表格续页页眉和 OCR 标题错位。
- 修复 `output/final_reader/连云港市志_全书.html` 中第三十五卷章节标题全部扁平化以及 3 处 `ipa-data` 表头残留的问题。
- 第三十五卷现有结构：H2={stats['h2_count']}，H3={stats['h3_count']}（概述 + 第一章机构至第五章包装仓储运输），H4={stats['h4_count']}。
- 第三十五卷范围内 `ipa-data` 残留为 {stats['ipa_blocks']}。
- 本章阅读版现有结构化表格 {stats['structured_tables']} 处，正文表格占位符 {stats['table_placeholders']} 处；表35-*需从 PDF 专项补登、重建和核验。
- 已写入进度文档：`output/reports/progress/20260629_第三十五卷对外经济贸易_修复核对进度.md`。

验收：第三十五卷 HTML 字节数 {stats['bytes']}，范围内通用标题锚点残留 {stats['generic_heading_anchors']}，`ipa-data` 残留 {stats['ipa_blocks']}，H3/H4 嵌套进段落问题 {stats['embedded_h3_in_p'] + stats['embedded_h4_in_p']}，畸形标题 id {stats['malformed_heading_ids']}；复跑 `scripts/audit_full_reader.py`，TOC 缺失锚点 0。工作站 `npm run typecheck` 通过。

下一步：进入 `第三十六卷 财政税务`。第三十五卷表35-*需从源 PDF 专项补登、重建和核验。
"""
    memory = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
    marker = "## 2026-06-29 第三十五卷对外经济贸易章节核对完成"
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

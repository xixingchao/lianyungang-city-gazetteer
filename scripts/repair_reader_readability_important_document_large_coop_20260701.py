# -*- coding: utf-8 -*-
"""Repair flattened appendix important document text for 大社的优越性."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_important_document_large_coop_20260701.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_important_document_large_coop_20260701.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_附录重要文献大社的优越性残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

START_LINE = "从满把抓到分工分业"
END_LINE = "省人民政府并报国务院："
START_HTML = "<p>从满把抓到分工分业"
END_HTML = "省人民政府并报国务院：</p>"
NEXT_HEADING_OLD = "<p>连云港市人民政府一九八四年七月七日连云港市进一步对外开放的方案连云港市现辖"
NEXT_HEADING_NEW = "<p>连云港市人民政府</p>\n<p>一九八四年七月七日</p>\n<p><strong>连云港市进一步对外开放的方案</strong></p>\n<p>连云港市现辖"

SUBHEADS = {
    "从满把抓到分工分业",
    "从一窝蜂到有条不紊",
    "政治思想工作",
    "社越大，优越性越大",
}
NEXT_DOC_TITLE = "关于报送连云港市进一步对外开放方案的报告"
SPECIAL_SINGLE_LINES = {
    "中共新海连市委员会",
    "一九五五年九月二十一日",
    NEXT_DOC_TITLE,
    "连政发[1984]108号",
    END_LINE,
}
PARA_START_PATTERNS = [
    re.compile(r"^事实教育了"),
    re.compile(r"^1955年，"),
    re.compile(r"^其次，"),
    re.compile(r"^当计划"),
    re.compile(r"^再次，"),
    re.compile(r"^如果全队"),
    re.compile(r"^以防备"),
    re.compile(r"^[1-4]、"),
    re.compile(r"^发挥劳动力"),
    re.compile(r"^由于生产的发展"),
]


def source_lines() -> list[str]:
    lines = SRC.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == START_LINE)
    end = next(i for i, line in enumerate(lines[start:], start) if line.strip() == END_LINE)
    kept: list[str] = []
    for line in lines[start : end + 1]:
        s = line.strip()
        if not s:
            continue
        if s.startswith("<!-- page-anchor:"):
            continue
        if re.fullmatch(r"一、重要文献·\s*\d+\s*·", s):
            continue
        kept.append(s)
    return kept


def starts_new_paragraph(line: str) -> bool:
    return any(pattern.search(line) for pattern in PARA_START_PATTERNS)


def build_blocks(lines: list[str]) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    current: list[str] = []

    def flush() -> None:
        nonlocal current
        if current:
            blocks.append(("p", "".join(current)))
            current = []

    for line in lines:
        if line in SUBHEADS:
            flush()
            blocks.append(("subhead", line))
            continue
        if line in SPECIAL_SINGLE_LINES:
            flush()
            kind = "doc-title" if line == NEXT_DOC_TITLE else "p"
            blocks.append((kind, line))
            continue
        if current and starts_new_paragraph(line):
            flush()
        current.append(line)
    flush()
    return blocks


def render(blocks: list[tuple[str, str]]) -> str:
    out = ['<section class="important-document-repair" data-document="large-coop-superiority">']
    for kind, text in blocks:
        safe = html.escape(text, quote=False)
        if kind == "subhead":
            out.append(f"<p><strong>{safe}</strong></p>")
        elif kind == "doc-title":
            out.append(f"<p><strong>{safe}</strong></p>")
        else:
            out.append(f"<p>{safe}</p>")
    out.append("</section>")
    return "\n".join(out)


def patch_reader(block: str) -> int:
    text = HTML.read_text(encoding="utf-8")
    start = text.find(START_HTML)
    if start == -1:
        start = text.find('<section class="important-document-repair" data-document="large-coop-superiority">')
    if start == -1:
        raise RuntimeError("large-coop block start not found")

    end = text.find(END_HTML, start)
    if end == -1:
        section_end = text.find("</section>", start)
        if section_end == -1:
            raise RuntimeError("large-coop block end not found")
        end = section_end + len("</section>")
    else:
        end += len(END_HTML)

    if text.find(START_HTML, start + 1) != -1:
        raise RuntimeError("large-coop block start is not unique")
    text = text[:start] + block + text[end:]
    text = text.replace(NEXT_HEADING_OLD, NEXT_HEADING_NEW, 1)
    HTML.write_text(text, encoding="utf-8")
    return 1


def write_reports(line_count: int, block_count: int, replaced: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "附录 / 一、重要文献 / 大社的优越性",
        "source": "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:21642-21828",
        "reader_path": str(HTML),
        "source_lines_used": line_count,
        "rendered_blocks": block_count,
        "flattened_blocks_replaced": replaced,
        "principle": "按源文小标题和自然段重建阅读版，过滤 page-anchor 与页眉页码，不改写史料内容。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 附录重要文献《大社的优越性》残文修复

- 时间：{now}
- 范围：`附录 / 一、重要文献 / 大社的优越性`
- 源文依据：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:21642-21828`

## 修复动作

- 将阅读版中 `从满把抓到分工分业...` 至下一篇 `省人民政府并报国务院：` 的压平块，按源文恢复为小标题、正文段和下一篇题头。
- 过滤夹在词中的页眉页码：`一、重要文献· 2701 ·`、`一、重要文献· 2703 ·`。
- 修复标题粘连：`从满把抓到分工分业`、`从一窝蜂到有条不紊`、`政治思想工作`、`社越大，优越性越大` 均恢复为独立小标题。
- 修复文末署名、日期、下一篇题名、文号和收文对象的粘连。
- 同步拆分下一篇正文前的发文机关、日期和 `连云港市进一步对外开放的方案` 标题。
- 替换阅读版压平残文：{replaced} 组；源文有效行：{line_count} 行；输出块：{block_count} 个。

## 核对说明

- 本轮不展示或嵌入任何图片，只依据正常源文汇总文件核对。
- 未改写史料含义；源文中的疑似 OCR 字词保留，后续若有图文证据再单独校字。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(line_count: int, block_count: int, replaced: int) -> None:
    marker = "## 2026-07-01 附录重要文献《大社的优越性》残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的附录“一、重要文献”《大社的优越性》残文进行回源修复。
- 源文依据：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:21642-21828`，使用有效行 {line_count} 行，输出阅读块 {block_count} 个。
- 阅读版已过滤 `一、重要文献· 2701 ·`、`一、重要文献· 2703 ·` 页眉页码，并恢复 `从满把抓到分工分业`、`从一窝蜂到有条不紊`、`政治思想工作`、`社越大，优越性越大` 等小标题。
- 同步拆开文末署名、日期、下一篇题名、文号和收文对象；替换压平残文 {replaced} 组。
- 继续拆开下一篇正文前的 `连云港市人民政府一九八四年七月七日连云港市进一步对外开放的方案` 粘连题头。
- 报告：`output/reports/reader_readability_important_document_large_coop_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    lines = source_lines()
    blocks = build_blocks(lines)
    block = render(blocks)
    replaced = patch_reader(block)
    write_reports(len(lines), len(blocks), replaced)
    update_memory(len(lines), len(blocks), replaced)
    print("important document large-coop block repaired")
    print(f"source_lines_used={len(lines)}")
    print(f"rendered_blocks={len(blocks)}")
    print(f"flattened_blocks_replaced={replaced}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

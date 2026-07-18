# -*- coding: utf-8 -*-
"""Repair flattened English general summary section (VII)."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_english_summary_section7_20260701.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_english_summary_section7_20260701.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_附录英文总述第七节残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

START_LINE = "(七）"
END_LINE = "（八）"
START_HTML = "<p>Lianyungang had once been"
END_HTML = "（八）</p>"
BLOCK_START = '<section class="english-summary-section" data-section="seven">'
BLOCK_END = "<p>（八）</p>"


def source_section() -> list[str]:
    lines = SRC.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == START_LINE)
    end = next(i for i, line in enumerate(lines[start + 1 :], start + 1) if line.strip() == END_LINE)
    kept: list[str] = []
    for line in lines[start + 1 : end]:
        s = line.strip()
        if not s:
            kept.append("")
            continue
        if s.startswith("<!-- page-anchor:"):
            continue
        if re.fullmatch(r"General Summary[.:] ?\d+", s) or "Histroy of LianYunGang City" in s:
            continue
        kept.append(s)
    return kept


def join_wrapped_lines(lines: list[str]) -> list[str]:
    paragraphs: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if line == "":
            if current:
                paragraphs.append(current)
                current = []
            continue
        current.append(line)
    if current:
        paragraphs.append(current)

    rendered: list[str] = []
    for para_lines in paragraphs:
        text = ""
        for line in para_lines:
            if not text:
                text = line
                continue
            if text.endswith("-"):
                text = text[:-1] + line
            else:
                text += " " + line
        text = text.replace("ter.After", "ter. After")
        text = text.replace("circu lation", "circulation")
        text = text.replace("com modities", "commodities")
        text = text.replace("16. 7%", "16.7%")
        text = text.replace("made. great", "made great")
        text = re.sub(r"\s+", " ", text).strip()
        rendered.append(text)
    return split_long_english_paragraphs(rendered)


def split_long_english_paragraphs(paragraphs: list[str], limit: int = 380) -> list[str]:
    result: list[str] = []
    for paragraph in paragraphs:
        sentences = re.split(r"(?<=[.!?])\s+", paragraph)
        current = ""
        for sentence in sentences:
            candidate = sentence if not current else current + " " + sentence
            if current and len(candidate) > limit:
                result.append(current)
                current = sentence
            else:
                current = candidate
        if current:
            result.append(current)
    return result


def render(paragraphs: list[str]) -> str:
    body = ['<section class="english-summary-section" data-section="seven">', "<p><strong>(七）</strong></p>"]
    for para in paragraphs:
        body.append("<p>" + html.escape(para, quote=False) + "</p>")
    body.append("</section>")
    body.append("<p>（八）</p>")
    return "\n".join(body)


def patch_reader(block: str) -> int:
    text = HTML.read_text(encoding="utf-8")
    start = text.find(START_HTML)
    end = text.find(END_HTML, start)
    if start != -1 and end != -1:
        end += len(END_HTML)
        if text.find(START_HTML, start + 1) != -1:
            raise RuntimeError("English summary section VII start is not unique")
    else:
        start = text.find(BLOCK_START)
        end = text.find(BLOCK_END, start)
        if start == -1 or end == -1:
            raise RuntimeError("English summary section VII boundary not found")
        end += len(BLOCK_END)
        if text.find(BLOCK_START, start + 1) != -1:
            raise RuntimeError("English summary section VII block is not unique")
    HTML.write_text(text[:start] + block + text[end:], encoding="utf-8")
    return 1


def write_reports(source_line_count: int, paragraph_count: int, replaced: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "附录 / 五、总述(英文) / (七）",
        "source": "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:23409-23487",
        "reader_path": str(HTML),
        "source_lines_used": source_line_count,
        "paragraphs_rendered": paragraph_count,
        "flattened_blocks_replaced": replaced,
        "principle": "按源文行界和空行恢复英文小节段落，过滤页眉页码和 page-anchor，合并英文断词。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 附录英文总述第七节残文修复

- 时间：{now}
- 范围：`附录 / 五、总述(英文) / (七）`
- 源文依据：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:23409-23487`

## 修复动作

- 将阅读版中 `(七）` 英文总述从单个超长段恢复为独立英文小节和自然段。
- 过滤源文页眉页码和 `page-anchor` 标记。
- 合并跨行断词，如 `cen-ter`、`busi-nesses`、`trans-formed`、`com-modities`。
- 替换阅读版压平残文：{replaced} 组；源文有效行：{source_line_count} 行；输出段落：{paragraph_count} 段。

## 核对说明

- 本轮只处理 `(七）`，边界止于 `(八）` 前，后续英文小节留待后续按同样方式分批修复。
- 未改写英文内容含义，只修复断行、断词和小节边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(source_line_count: int, paragraph_count: int, replaced: int) -> None:
    marker = "## 2026-07-01 附录英文总述第七节残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的附录英文总述 `Lianyungang had once been...` 超长压平段回源修复。
- 源文依据：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:23409-23487`，使用有效行 {source_line_count} 行，输出英文段落 {paragraph_count} 段。
- 阅读版中 `(七）` 已恢复为 `english-summary-section` 小节；边界止于 `(八）` 前，未触碰后续英文小节。
- 报告：`output/reports/reader_readability_english_summary_section7_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    src_lines = source_section()
    paragraphs = join_wrapped_lines(src_lines)
    block = render(paragraphs)
    replaced = patch_reader(block)
    write_reports(len([line for line in src_lines if line]), len(paragraphs), replaced)
    update_memory(len([line for line in src_lines if line]), len(paragraphs), replaced)
    print("English summary section VII repaired")
    print(f"source_lines_used={len([line for line in src_lines if line])}")
    print(f"paragraphs_rendered={len(paragraphs)}")
    print(f"flattened_blocks_replaced={replaced}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

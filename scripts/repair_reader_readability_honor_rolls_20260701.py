# -*- coding: utf-8 -*-
"""Repair flattened honor-roll lists in volume 60."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_honor_rolls_20260701.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_honor_rolls_20260701.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第六十卷劳动模范等名录残文修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

START_LINE = "二、劳动模范、先进生产（工作)者名录"
END_LINE = "谭洪海"
START_HTML = "<p>二、劳动模范、先进生产（工作)者名录"
END_HTML = "唐雨谭洪海</p>"
BLOCK_START = '<div class="honor-roll-list">'
BLOCK_END = "</div>"


def is_heading(line: str) -> bool:
    return (
        bool(re.match(r"^[一二三四五六七八九十]+、", line))
        or bool(re.match(r"^[（(][一二三四五六七八九十]+[）)]", line))
        or bool(re.match(r"^\d+\.", line))
        or bool(re.match(r"^\d{4}\s*年", line))
    )


def merge_wrapped_heading_lines(lines: list[str]) -> list[str]:
    merged: list[str] = []
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if re.match(r"^\d+\.", line) and idx + 1 < len(lines) and not is_heading(lines[idx + 1]):
            nxt = lines[idx + 1]
            joined = line + nxt
            if any(token in joined for token in ["代表大会", "授奖大会", "表彰大会", "先进生产", "先进工作"]):
                merged.append(joined)
                idx += 2
                continue
        merged.append(line)
        idx += 1
    return merged


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
        if re.fullmatch(r"第三章名录·\d+", s) or re.fullmatch(r"录·\d+", s) or s == "第三章":
            continue
        kept.append(s)
    return merge_wrapped_heading_lines(kept)


def render(lines: list[str]) -> str:
    parts = [BLOCK_START]
    bucket: list[str] = []

    def flush() -> None:
        nonlocal bucket
        if bucket:
            parts.append("<p>" + html.escape(" ".join(bucket), quote=False) + "</p>")
            bucket = []

    for line in lines:
        if is_heading(line):
            flush()
            parts.append("<p><strong>" + html.escape(line, quote=False) + "</strong></p>")
        else:
            bucket.append(line)
            if len(bucket) >= 12:
                flush()
    flush()
    parts.append(BLOCK_END)
    return "\n".join(parts)


def patch_reader(new_block: str) -> int:
    text = HTML.read_text(encoding="utf-8")
    start = text.find(START_HTML)
    end = text.find(END_HTML, start)
    if start != -1 and end != -1:
        end += len(END_HTML)
        if text.find(START_HTML, start + 1) != -1:
            raise RuntimeError("honor-roll start marker is not unique")
    else:
        start = text.find(BLOCK_START)
        end = text.find(BLOCK_END, start)
        if start == -1 or end == -1:
            raise RuntimeError("honor-roll block boundary not found")
        end += len(BLOCK_END)
        if text.find(BLOCK_START, start + 1) != -1:
            raise RuntimeError("honor-roll block is not unique")
    HTML.write_text(text[:start] + new_block + text[end:], encoding="utf-8")
    return 1


def write_reports(line_count: int, replaced: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第六十卷人物 / 第三章名录 / 劳动模范、五一奖章、三八红旗手、体育冠军名录",
        "source": "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:20535-21594",
        "reader_path": str(HTML),
        "source_lines_used": line_count,
        "flattened_blocks_replaced": replaced,
        "principle": "按工作台源文行界恢复名录段落结构，过滤页眉页码和 page-anchor，不改写人名内容。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第六十卷劳动模范等名录残文修复

- 时间：{now}
- 范围：`第六十卷人物 / 第三章名录`
- 源文依据：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:20535-21594`

## 修复动作

- 将阅读版中从 `二、劳动模范、先进生产（工作)者名录` 到 `六、全国体育冠军名录` 的超长压平段恢复为名录块。
- 按源文行界恢复标题、年度和名单段落；过滤页眉、页码和 `page-anchor` 标记。
- 对源文中因 OCR 行宽拆开的长标题进行相邻行合并。
- 替换阅读版压平/已生成名录块：{replaced} 组；使用源文有效行：{line_count} 行。

## 核对说明

- 本轮不重写人名，不拆分无法从源文确认的连写姓名，只恢复阅读边界。
- 该段后接附录，替换边界止于 `谭洪海`，未触碰附录正文。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(line_count: int, replaced: int) -> None:
    marker = "## 2026-07-01 第六十卷劳动模范等名录残文修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第六十卷人物 `二、劳动模范、先进生产（工作)者名录...` 超长压平段回源修复。
- 源文依据：`workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:20535-21594`，使用有效行 {line_count} 行，过滤页眉页码和 page-anchor。
- 阅读版中该段已恢复为 `honor-roll-list` 名录块，替换压平残文 {replaced} 组；边界止于 `谭洪海`，未触碰附录。
- 报告：`output/reports/reader_readability_honor_rolls_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    lines = source_lines()
    block = render(lines)
    replaced = patch_reader(block)
    write_reports(len(lines), replaced)
    update_memory(len(lines), replaced)
    print("honor-roll block repaired")
    print(f"source_lines_used={len(lines)}")
    print(f"flattened_blocks_replaced={replaced}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Restore compressed people's representative committee list layout."""

from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SOURCE = ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_people_representative_committee_lists_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_people_representative_committee_lists_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_各界人民代表会议常委协商名录版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h4 id="第四十二卷-第九章新海连特区、新海连市各界人民代表会议-第三节常务(协商)委员会">第三节常务(协商)委员会</h4>'
SCOPE_END = '<h3 id="第四十二卷-第十章连云港(新海连)市人民代表大会">第十章连云港(新海连)市人民代表大会</h3>'
SRC_START = "一、历届常务（协商)委员名录"
SRC_END = "第十章"

COMMITTEE_TITLES = [
    "新海连特区、新海连市第一届各界人民代表会议常务委员会",
    "新海县第二届各界人民代表会议常务委员会",
    "新海连市第三届各界人民代表会议常务委员会",
    "新海连市第四届各界人民代表会议协商委员会",
    "新海连市第五届各界人民代表会议协商委员会",
]
SUBHEADS = {"二、会议纪略", "、出席山东省各界人民代表会议代表名单", "二、出席江苏省协商委员会委员名单"}
RESIDUALS = [
    "委员名录新海连市从第届",
    "魏伯衡新海连市第三届",
    "薛立人陆荫强二、会议纪略",
    "附42-2：出席省各界代表会议代表、省协商委员会代表名单、出席山东省",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def source_lines() -> list[str]:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    start = lines.index(SRC_START)
    end = lines.index(SRC_END, start)
    return [line.strip() for line in lines[start:end] if line.strip() and not line.startswith("<!--")]


def render(lines: list[str]) -> list[str]:
    out: list[str] = []
    in_list = False
    in_intro = False
    for line in lines:
        if line == SRC_START:
            out.append(f"<h5>{html.escape(line)}</h5>")
            in_intro = True
            continue
        if line in COMMITTEE_TITLES:
            if in_intro:
                out.append("</p>")
                in_intro = False
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h5>{html.escape(line)}</h5>")
            continue
        if line == "附42-2：出席省各界代表会议代表、省协商委员会代表名单":
            if in_intro:
                out.append("</p>")
                in_intro = False
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h4>{html.escape(line)}</h4>")
            continue
        if line in SUBHEADS:
            if in_intro:
                out.append("</p>")
                in_intro = False
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h5>{html.escape(line)}</h5>")
            continue
        if in_intro:
            if not out or not out[-1].startswith("<p>"):
                out.append("<p>" + html.escape(line))
            else:
                out[-1] += html.escape(line)
            continue
        if line.startswith(("主席：", "副主席：", "常务委员：", "协商委员：")):
            if in_list:
                out.append("</ul>")
            out.append(f"<p><strong>{html.escape(line)}</strong></p>")
            out.append('<ul class="reader-restored-list">')
            in_list = True
            continue
        if in_list:
            out.append(f"<li>{html.escape(line)}</li>")
        else:
            out.append(f"<p>{html.escape(line)}</p>")
    if in_intro:
        out.append("</p>")
    if in_list:
        out.append("</ul>")
    return out


def patch_html(new_lines: list[str]) -> int:
    text = HTML.read_text(encoding="utf-8")
    start = text.index(SCOPE_START) + len(SCOPE_START)
    end = text.index(SCOPE_END, start)
    replacement = "\n" + "\n".join(new_lines) + "\n"
    changed = int(text[start:end] != replacement)
    if changed:
        text = text[:start] + replacement + text[end:]
        HTML.write_text(text, encoding="utf-8")
    scope = HTML.read_text(encoding="utf-8")[start : start + len(replacement) + 200]
    for residue in RESIDUALS:
        if residue in scope:
            raise RuntimeError(f"compressed committee residue remains: {residue}")
    return changed


def main() -> None:
    lines = source_lines()
    rendered = render(lines)
    changed = patch_html(rendered)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十二卷政务：新海连特区、新海连市各界人民代表会议常务(协商)委员会",
        "html_scope_rewritten": changed,
        "source_evidence": [
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:32702-32783",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md:90926-91009",
        ],
        "notes": ["按源 Markdown 行边界恢复标题、职务行和名单列表；源文疑似 OCR 错字照录，不猜修。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 各界人民代表会议常委协商名录版式修复

- 时间：{now}
- 范围：第四十二卷政务，第九章第三节常务(协商)委员会。
- 本次重写 HTML 范围：{changed} 处。

## 修复

- 将 `一、历届常务（协商)委员名录` 从段首粘连恢复为小节标题。
- 将第一至第五届常务/协商委员会标题、主席/副主席/委员职务行恢复为分层列表。
- 将误粘在名单后的 `二、会议纪略` 恢复为独立小节标题。
- 将 `附42-2` 的附录标题和两个名单小标题从压缩段恢复出来。

## 暂缓

- 源文中的 `第届`、`周瑞（女）杨文雄走`、`徐敬甫．`、`刘玉和「` 等疑似 OCR 问题，本批照录，不猜修。

## 依据

- `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:32702-32783`
- `workbench/body_chapters/连云港市志_全书_正文汇总.md:90926-91009`
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 各界人民代表会议常委协商名录版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四十二卷政务第九章第三节常务(协商)委员会在最终阅读版中名录、会议纪略、附42-2 被压成长段的问题。
- 按 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:32702-32783` 的行边界恢复标题、职务行和 `reader-restored-list` 名单。
- 源文疑似 OCR 错字照录，不猜修。
- 报告：`output/reports/reader_readability_people_representative_committee_lists_20260705.md`。
""",
    )
    print(f"html_scope_rewritten={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Repair formatting for the Overview and Chronicle section."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SRC_MD = ROOT / "workbench" / "body_chapters" / "paddle_上" / "总述与大事记.md"

DYNASTY_YEAR_RE = re.compile(
    r"^(春秋|周|秦|汉|东汉|西汉|新|三国|晋|东晋|南朝|北朝|隋|唐|宋|元|明|清|民国)[^<]{0,30}年(?:（[^）]+）)?$"
)
AD_YEAR_RE = re.compile(r"^(?:19|20)\d{2}年(?:\d+月\d+日)?$")
SECTION_RE = re.compile(r'(<h2 id="总述">总述</h2>)(.*?)(<h2 id="第一卷-自然环境">)', re.S)


def repair_source_md() -> list[str]:
    actions: list[str] = []
    text = SRC_MD.read_text(encoding="utf-8")
    original = text
    text = text.replace("总\n述", "总述", 1)
    text = text.replace("\n大事记\n", "\n大事记\n", 1)
    if text != original:
        SRC_MD.write_text(text, encoding="utf-8")
        actions.append("规范源 MD 中 `总述` 标题断行。")
    return actions


def is_year_entry(text: str) -> bool:
    text = text.strip()
    if DYNASTY_YEAR_RE.match(text):
        return True
    if AD_YEAR_RE.match(text):
        return True
    return False


def repair_html() -> tuple[list[str], int, int]:
    html = HTML_PATH.read_text(encoding="utf-8")
    match = SECTION_RE.search(html)
    if not match:
        raise RuntimeError("Cannot locate 总述 section in full reader HTML")

    prefix, section, suffix = match.groups()
    actions: list[str] = []

    ipa_before = section.count('<div class="ipa-data">')
    # In this section these blocks are ordinary prose mistakenly styled as IPA.
    section = section.replace('<div class="ipa-data">', '<p>')
    section = section.replace('</div>', '</p>')
    ipa_after = section.count('<div class="ipa-data">')
    if ipa_before != ipa_after:
        actions.append(f"将总述区误用 `ipa-data` 的正文块转回普通段落：{ipa_before - ipa_after} 处。")

    year_changes = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal year_changes
        attrs = match.group(1)
        body = match.group(2).strip()
        if 'class="year-entry"' in attrs:
            return match.group(0)
        if is_year_entry(body):
            year_changes += 1
            return f'<p class="year-entry">{body}</p>'
        return match.group(0)

    section = re.sub(r'<p([^>]*)>([^<]+)</p>', repl, section)
    if year_changes:
        actions.append(f"统一大事记年份条目样式：新增 year-entry {year_changes} 处。")

    fixed = html[: match.start()] + prefix + section + suffix + html[match.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    return actions, ipa_before - ipa_after, year_changes


def main() -> None:
    actions = []
    actions.extend(repair_source_md())
    html_actions, ipa_fixed, year_fixed = repair_html()
    actions.extend(html_actions)
    print("Repair complete")
    for action in actions:
        print(f"- {action}")
    print(f"ipa_fixed={ipa_fixed}")
    print(f"year_fixed={year_fixed}")


if __name__ == "__main__":
    main()

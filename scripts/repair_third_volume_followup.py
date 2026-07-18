# -*- coding: utf-8 -*-
"""Follow-up fixes for 第三卷 区县概况 heading edge cases."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SECTION_RE = re.compile(
    r'(<h2 id="第三卷-区县概况">第三卷区县概况</h2>)(.*?)(?=<h2 id="第四卷-人口">)',
    re.S,
)

CHAPTERS = [
    "第一章新浦区",
    "第二章海州区",
    "第三章云台区",
    "第四章连云区",
    "第五章赣榆县",
    "第六章东海县",
    "第七章灌云县",
]


def h3(title: str) -> str:
    return f'<h3 id="第三卷-{title}">{title}</h3>'


def h4(chapter: str, title: str) -> str:
    return f'<h4 id="第三卷-{chapter}-{title}">{title}</h4>'


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第三卷 section")
    heading, section = m.groups()
    original = section

    insertions = [
        ("第六章东海县", '<p>东海县位于江苏省东北部，'),
        ("第七章灌云县", '<p>灌云县位于江苏省北部，'),
    ]
    for title, intro in insertions:
        marker = h3(title)
        if marker not in section and intro in section:
            section = section.replace(intro, marker + "\n" + intro, 1)

    for idx, chapter in enumerate(CHAPTERS):
        marker = h3(chapter)
        start = section.find(marker)
        if start < 0:
            continue
        end = len(section)
        for later in CHAPTERS[idx + 1 :]:
            pos = section.find(h3(later), start + 1)
            if pos >= 0:
                end = pos
                break
        block = section[start:end]
        for raw in ["第三节经济", "第三节 经济", "第三节 经 济", "第三节经 济", "第三节 经", "第三节经"]:
            title = "第三节经济"
            marker4 = h4(chapter, title)
            if marker4 in block:
                break
            pat = f"<p>{raw}"
            if pat in block:
                block = block.replace(pat, marker4 + "\n<p>", 1)
                break
        # Fill first/second/fourth sections if later chapter insertions created a new unprocessed block.
        for title in ["第一节建置区划", "第二节自然环境", "第四节社会事业"]:
            marker4 = h4(chapter, title)
            if marker4 not in block:
                pat = f"<p>{title}"
                if pat in block:
                    block = block.replace(pat, marker4 + "\n<p>", 1)
        section = section[:start] + block + section[end:]

    fixed = html[: m.start()] + heading + section + html[m.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")

    print("changed=", section != original)
    print("h3=", len(re.findall(r"<h3 ", section)))
    print("h4=", len(re.findall(r"<h4 ", section)))
    print("ipa=", len(re.findall(r'<div class="ipa-data">', section)))
    print("embedded_h4_in_p=", len(re.findall(r'<p[^>]*>[^<]*<h4', section)))


if __name__ == "__main__":
    main()

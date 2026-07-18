# -*- coding: utf-8 -*-
"""Follow-up fixes for 第二卷 建置区划 heading edge cases."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
SECTION_RE = re.compile(
    r'(<h2 id="第二卷-建置区划">第二卷建置区划</h2>)(.*?)(?=<h2 id="第三卷-区县概况">)',
    re.S,
)


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    m = SECTION_RE.search(html)
    if not m:
        raise RuntimeError("Cannot locate 第二卷 section")
    heading, section = m.groups()
    original = section

    section = section.replace(
        "区1986.6～：赣榆县、东海县、灌云县、新浦区、海州区、云台区、连云区划第一节民国时期一、东海县民国元年（1912年），",
        "区1986.6～：赣榆县、东海县、灌云县、新浦区、海州区、云台区、连云区</p>\n"
        "<h3 id=\"第二卷-第二章区划\">第二章区划</h3>\n"
        "<h4 id=\"第二卷-第二章-第一节民国时期\">第一节民国时期</h4>\n"
        "<p>一、东海县</p>\n<p>民国元年（1912年），",
        1,
    )
    section = section.replace(
        "</p></p>\n<h3 id=\"第二卷-第二章区划\">",
        "</p>\n<h3 id=\"第二卷-第二章区划\">",
        1,
    )
    section = section.replace(
        "海平乡、大兴乡<h4 id=\"第二卷-第二章-第二节解放以后\">第二节解放以后</h4>",
        "海平乡、大兴乡</p>\n<h4 id=\"第二卷-第二章-第二节解放以后\">第二节解放以后</h4>",
        1,
    )
    section = section.replace("</p>\n<p></p>", "</p>")

    fixed = html[: m.start()] + heading + section + html[m.end() :]
    if fixed != html:
        HTML_PATH.write_text(fixed, encoding="utf-8")
    print("changed=", section != original)
    print("h3=", len(re.findall(r"<h3 ", section)))
    print("h4=", len(re.findall(r"<h4 ", section)))
    print("embedded_h4_in_p=", len(re.findall(r"<p[^>]*>[^<]*<h4", section)))


if __name__ == "__main__":
    main()

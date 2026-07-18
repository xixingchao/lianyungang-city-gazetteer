# -*- coding: utf-8 -*-
"""Restore city government leader list layout from line-preserved source."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_city_government_leaders_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_city_government_leaders_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_市人民政府首长名录版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h4 id="第四十二卷-第六章连云港市人民政府-第二节政府首长">第二节政府首长</h4>'
SCOPE_END = '<h4 id="第四十二卷-第六章连云港市人民政府-第三节政务纪要">第三节政务纪要</h4>'

SECTIONS = [
    {
        "title": "一、第六届连云港市人民政府市长、副市长名录",
        "roles": [
            ("市长", ["耿杰民（1980.2~1983.2)"]),
            ("代理市长", ["何仁华（1983.2~1983.3）"]),
            ("副市长", ["耿志英（女）（1980.2~1983.4）", "李敬松（1980.2~1983.4)", "徐河均（1980.2~1983.4)", "林永(1980.2~1983.4)", "李(1980.2~1983.4)", "徐进德（1980.2~1983.4)", "刘余隆（1980.2~1983.4）", "常钜勋（1980.7~1983.4)"]),
        ],
    },
    {
        "title": "二、第七届连云港市人民政府市长、副市长、秘书长名录",
        "roles": [
            ("市长", ["何仁华（1983.4~1986.5)", "唐贯准(1986.5~1988.1)"]),
            ("副市长", ["李敬松（1983.4~1984.8)", "胡为德（1983.4~1988.1)", "吴学志(1983.4~1985.6)", "毛庚年（1983.4~1985.8）", "严健(1983.4~1987.8)", "郑申雄（1984.8~1985.6)", "高有为(1984.8~1988.1)", "徐沙(1984.10~1988.1)", "唐贯准(1985.6~1986.5)", "许维铭（1985.6~1988.1)", "周国林（1986.5~1988.1)"]),
            ("秘书长", ["程智培（1986.7~1987.5)"]),
        ],
    },
    {
        "title": "三、第八届连云港市人民政府市长、副市长、秘书长名录",
        "roles": [
            ("市长", ["王稳卿(1988.1~", "高有为(1988.1~"]),
            ("副市长", ["刘步生(1988.1~", "许维铭(1988.1~", "周国林(1988.1~", "吴炳裔（1988.6~", "程智培(1989.1~"]),
            ("秘书长", ["范永泉（1988.2~1990.10)", "谢兆玉(1990.10~"]),
        ],
    },
]

RESIDUALS = [
    "名录市长耿杰民",
    "常钜勋（1980.7~1983.4)二、第七届",
    "秘书长程智培（1986.7~1987.5)三、第八届",
    "谢兆玉(1990.10~第三节政务纪要",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def section_html() -> str:
    parts: list[str] = []
    for section in SECTIONS:
        parts.append(f"<h5>{section['title']}</h5>")
        for role, names in section["roles"]:
            parts.append(f"<p><strong>{role}</strong></p>")
            parts.append('<ul class="leader-list">')
            parts.extend(f"<li>{name}</li>" for name in names)
            parts.append("</ul>")
    return "\n" + "\n".join(parts) + "\n"


def patch_html() -> int:
    text = HTML.read_text(encoding="utf-8")
    start = text.index(SCOPE_START) + len(SCOPE_START)
    end = text.index(SCOPE_END, start)
    new_segment = section_html()
    changed = int(text[start:end] != new_segment)
    if changed:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")
    verify = HTML.read_text(encoding="utf-8")
    scope = verify[verify.index(SCOPE_START):verify.index(SCOPE_END, verify.index(SCOPE_START))]
    for item in RESIDUALS:
        if item in scope:
            raise RuntimeError(f"linearized government leader residue remains: {item}")
    for section in SECTIONS:
        if f"<h5>{section['title']}</h5>" not in scope:
            raise RuntimeError(f"missing section title: {section['title']}")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十二卷政务：连云港市人民政府政府首长名录",
        "html_scope_rewritten": changed,
        "source_evidence": [
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:32232-32279",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md:90456-90503",
        ],
        "deferred": ["第八届任期源文为开放式 1988.1~ / 1990.10~，本批照录不补终止年份。", "李(1980.2~1983.4) 源文姓名不完整，本批不猜修。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 市人民政府首长名录版式修复

- 时间：{now}
- 范围：第四十二卷政务，第六章第二节政府首长。
- 本次重写 HTML 范围：{changed} 处。

## 修复

- 将第六至第八届市人民政府市长、副市长、秘书长名录从压扁长段恢复为届次标题、职务标题和名单列表。
- 将被粘入名单段的 `第三节政务纪要` 恢复为独立标题。
- 复用最终阅读版已有 `leader-list` 样式。

## 依据

- `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:32232-32279`
- `workbench/body_chapters/连云港市志_全书_正文汇总.md:90456-90503`

## 暂缓

- 第八届任期源文为开放式 `1988.1~` / `1990.10~`，本批照录不补终止年份。
- `李(1980.2~1983.4)` 源文姓名不完整，本批不猜修。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 市人民政府首长名录版式修复"
    memory = f"""
{marker}
- 修复第四十二卷政务 `连云港市人民政府 / 政府首长` 在最终阅读版中被压成长段的问题，恢复为届次标题、职务标题和 `leader-list` 名单。
- `第三节政务纪要` 原被粘进第八届秘书长名单段，本次恢复为独立标题。
- 源文姓名/任期不完整处照录，不猜修。
- 报告：`output/reports/reader_readability_city_government_leaders_20260705.md`。
"""
    append_once(MEMORY, marker, memory)
    print(f"html_scope_rewritten={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

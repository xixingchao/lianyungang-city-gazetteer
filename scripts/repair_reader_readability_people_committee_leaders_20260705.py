# -*- coding: utf-8 -*-
"""Restore the People's Committee leader list layout from line-preserved source."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_people_committee_leaders_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_people_committee_leaders_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_市人民委员会领导人名录版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h4 id="第四十二卷-第四章连云港(新海连)市人民委员会-第二节市人民委员会领导人">第二节市人民委员会领导人</h4>'
SCOPE_END = '<h4 id="第四十二卷-第四章连云港(新海连)市人民委员会-第三节政务纪要">第三节政务纪要</h4>'

SECTIONS = [
    {
        "title": "一、第一届新海连市人民委员会领导人名录",
        "roles": [
            ("市长", ["周思德（1955.4~1957.1）"]),
            ("副市长", ["季士杰(1955.4~1957.1)", "张书伦(1955.4~1957.1)", "刘-麟(1955.4 ~ 1957.1)", "牛耀华（1955.4~1957.1)", "邹乃福(1955.4~1957.1)", "刘文(1955.4~ 1957.1)", "王玉焕(1955.4~1957.1)"]),
            ("委员", ["文中让李明信　吴鲁星　许耀林　陈心文", "崔文华（女）黄荔岑张多琦张金堂冯克玉", "杨玉生杨道五叶志俊刘克明严剑寒"]),
        ],
    },
    {
        "title": "二、第二届新海连市人民委员会领导人名录",
        "roles": [
            ("市长", ["周思德（1957.1~1958.5)", "张书伦(1957.1~1958.5)"]),
            ("副市长", ["刘一麟(1957.1~1958.5)", "牛耀华(1957.1~1958.5)", "邹乃福(1957.1~1958.5)", "刘文(1957.1~1958.5)", "王玉焕(1957.1~1958.5)"]),
            ("委员", ["文中让", "王友芝", "叶志俊", "冯克玉", "刘克明", "吴鲁星", "许耀林", "严剑寒", "李明信", "张金堂", "张多琦", "杨琴亭(女）", "赵浩俊梁立法崔文华(女)", "黄荔岑陶洪贯"]),
        ],
    },
    {
        "title": "三、第三届新海连市人民委员会领导人名录",
        "roles": [
            ("市长", ["周思德（1958.5~1960.4)", "祝斌(1960.5~1961.9)"]),
            ("副市长", ["季士杰(1958.5~1961.9)", "刘麟(1958.5~1961.9)", "王玉焕(1958.5~1961.9)", "张绍云（1958.5~1961.9)"]),
            ("委员", ["王友芝‧冯克玉‧许耀林‧朱景云", "孙金芝陈心文", "陈志学　邹本文李明信　张书伦张捷夫", "梁立法", "张剑秋(女）"]),
        ],
    },
    {
        "title": "四、第四届连云港市人民委员会领导人名录",
        "roles": [
            ("市长", ["祝斌(1961.9~1963.12)", "季士杰(1961.9~1963.12)"]),
            ("副市长", ["张绍云（1961.9~1963.12)", "陈心文（1961.9~1963.12)", "刘文(1961.9~1963.4)", "徐河均(1961.9~1963.12)", "王玉焕（1961.9~1963.1)", "王友芝", "陈立义", "李明信"]),
            ("委员", ["孙全芝", "孙志来", "孙景源", "梁立法", "邹本文", "车秀明", "罗大章", "徐开第", "张剑秋(女）", "张捷夫省", "张书伦", "崔文华（女）", "熊正文", "黄荔岑钱厚康程绪和"]),
            ("秘书长", ["王玉焕（1963~1963.12)"]),
        ],
    },
    {
        "title": "五、第五届连云港市人民委员会领导人名录",
        "roles": [
            ("市长", ["祝斌(1963.12 ~1967.1)"]),
            ("副市长", ["季士杰(1963.12~1967.1)", "张绍云(1963.12~1967.1)", "陈心文(1963.12 ~ 1967.1)", "梁甲昆（1963.12~1967.1)", "徐河均（1963.12~1967.1)", "刘-麟(1963.12~ 1967.1)"]),
            ("委员", ["王玉焕", "李明信", "王友芝", "孙全芝", "孙志来", "孙景源", "陈立文", "邹本文‧林永", "徐开第", "高杰生", "梁立法", "张书伦", "黄荔岑", "张剑秋(女）", "崔文华(女)", "程绪和", "钱厚康", "熊正文"]),
            ("秘书长", ["王玉焕(1963.12~1967.1)"]),
        ],
    },
]

RESIDUALS = [
    "领导人名录市长",
    "委员文中让",
    "严剑寒二、第二届",
    "黄荔岑陶洪贯三、第三届",
    "秘书长王玉焕（1963~1963.12)五、第五届",
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
    old_segment = text[start:end]
    new_segment = section_html()
    changed = int(old_segment != new_segment)
    if changed:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")
    verify = HTML.read_text(encoding="utf-8")
    new_scope = verify[verify.index(SCOPE_START):verify.index(SCOPE_END, verify.index(SCOPE_START))]
    for item in RESIDUALS:
        if item in new_scope:
            raise RuntimeError(f"linearized leader residue remains: {item}")
    for section in SECTIONS:
        if f"<h5>{section['title']}</h5>" not in new_scope:
            raise RuntimeError(f"missing section title: {section['title']}")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十二卷政务：市人民委员会领导人名录",
        "html_scope_rewritten": changed,
        "source_evidence": [
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:31989-32098",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md:90189-90310",
        ],
        "deferred": ["源文本中仍粘连的姓名串，如 黄荔岑陶洪贯、张捷夫省，本批不猜修。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 市人民委员会领导人名录版式修复

- 时间：{now}
- 范围：第四十二卷政务，第四章第二节市人民委员会领导人。
- 本次重写 HTML 范围：{changed} 处。

## 修复

- 将第一至第五届市人民委员会领导人名录从压扁长段恢复为届次标题、职务标题和名单列表。
- 复用最终阅读版已有 `leader-list` 样式，与后文“市革命委员会首长”一致。

## 依据

- `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:31989-32098`
- `workbench/body_chapters/连云港市志_全书_正文汇总.md:90189-90310`

## 暂缓

- 源文本中仍粘连或疑似错识的姓名串，如 `黄荔岑陶洪贯`、`张捷夫省`，本批不猜修。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 市人民委员会领导人名录版式修复"
    memory = f"""
{marker}
- 修复第四十二卷政务 `市人民委员会领导人` 在最终阅读版中被压成长段的问题，恢复为届次标题、职务标题和 `leader-list` 名单。
- 依据 `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md` 与全书正文汇总的行边界；未猜修源文本中仍粘连的姓名串。
- 报告：`output/reports/reader_readability_people_committee_leaders_20260705.md`。
"""
    append_once(MEMORY, marker, memory)
    print(f"html_scope_rewritten={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

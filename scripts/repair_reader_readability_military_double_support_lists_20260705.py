# -*- coding: utf-8 -*-
"""Restore military double-support award lists from line-preserved body text."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
BODY = ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md"
SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_military_double_support_lists_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_military_double_support_lists_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_双拥表彰单位名单版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

LIST_1980 = [
    "海军上海基地八二工地机械运输连",
    "83075部队炮兵营",
    "37519部队后勤部医疗所",
    "83075部队炮兵营一连",
    "海军376274部队4331艇",
    "83075部队修理所",
    "海军37519部队司令部舰船修理所",
    "83075部队船运队修理所",
    "海军37885部队云台山观通站",
    "83075部队步兵营机炮连",
    "149 医院外--科",
    "83075部队通信营通信连",
    "83076部队二营",
    "54573部队盐场七连-一班",
    "83077部队三营五连",
    "54573造纸厂三连",
    "83077部队一营一连",
    "54573造纸厂卫生所",
    "54573部队四连司机排",
    "83077部队一营二连",
    "83077部队炮兵营一连",
    "83573部队管理科",
    "83077部队二营四连",
    "83573部队二科",
    "83075部队工兵连花果山执勤点",
    "连云港边防检查站监护连",
    "83075部队守备营二连",
    "87092部队71分队",
    "海军37637部队卫生队",
    "87092部队52分队",
]

LIST_1984 = [
    "83075部队医院",
    "37519部队",
    "83076部队炮兵营三连",
    "东海县人民武装部",
    "83078部队通信连",
    "39817部队",
    "37519部队医疗所",
    "149医院院务处团支部",
    "云台山观通站",
    "54573部队造纸厂化工车间",
    "83077部队一营机炮连",
    "连云港市人民武装警察支队高公岛边防派出所",
]

OLD_HTML = """<p>附45-3：连云港市第一次“双拥大会表彰单位（1980年）</p>
<p>海军上海基地八二工地机械运输连83075部队炮兵营37519部队后勤部医疗所83075部队炮兵营一连海军376274部队4331艇83075部队修理所海军37519部队司令部舰船修理所83075部队船运队修理所海军37885部队云台山观通站83075部队步兵营机炮连149 医院外--科83075部队通信营通信连83076部队二营54573部队盐场七连-一班83077部队三营五连54573造纸厂三连83077部队一营一连54573造纸厂卫生所54573部队四连司机排83077部队一营二连83077部队炮兵营一连83573部队管理科83077部队二营四连83573部队二科83075部队工兵连花果山执勤点连云港边防检查站监护连83075部队守备营二连87092部队71分队海军37637部队卫生队87092部队52分队附45－4：连云港市第二次“双拥”代表大会表彰单位（1984年）</p>
<p>83075部队医院37519部队83076部队炮兵营三连东海县人民武装部83078部队通信连39817部队37519部队医疗所149医院院务处团支部云台山观通站54573部队造纸厂化工车间83077部队一营机炮连连云港市人民武装警察支队高公岛边防派出所</p>"""

NEW_HTML = """<h5>附45-3：连云港市第一次“双拥”大会表彰单位（1980年）</h5>
<ul class="reader-restored-list">
%s
</ul>
<h5>附45-4：连云港市第二次“双拥”代表大会表彰单位（1984年）</h5>
<ul class="reader-restored-list">
%s
</ul>""" % (
    "\n".join(f"<li>{item}</li>" for item in LIST_1980),
    "\n".join(f"<li>{item}</li>" for item in LIST_1984),
)

TEXT_FIXES = [
    ("附45-3：连云港市第一次“双拥大会表彰单位（1980年）", "附45-3：连云港市第一次“双拥”大会表彰单位（1980年）"),
    ("连云港市人民武装警察支队高\n公岛边防派出所", "连云港市人民武装警察支队高公岛边防派出所"),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> int:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(OLD_HTML)
    if count:
        text = text.replace(OLD_HTML, NEW_HTML)
        HTML.write_text(text, encoding="utf-8")
    verify = HTML.read_text(encoding="utf-8")
    if OLD_HTML in verify:
        raise RuntimeError("old double-support linearized block still remains")
    for item in [*LIST_1980, *LIST_1984]:
        if f"<li>{item}</li>" not in verify:
            raise RuntimeError(f"missing restored list item: {item}")
    return count


def patch_text_sources() -> dict[str, int]:
    out: dict[str, int] = {}
    for path in [BODY, SUMMARY]:
        text = path.read_text(encoding="utf-8")
        changed = 0
        for old, new in TEXT_FIXES:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                changed += count
        path.write_text(text, encoding="utf-8")
        out[str(path)] = changed
    return out


def main() -> None:
    html_changes = patch_html()
    source_changes = patch_text_sources()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = html_changes + sum(source_changes.values())
    payload = {
        "time": now,
        "scope": "第四十五卷拥政爱民：附45-3、附45-4双拥表彰单位名单",
        "total_changes": total,
        "html_block_replacements": html_changes,
        "source_text_changes": source_changes,
        "source_evidence": [
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md:10084-10127",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md:160498-160541",
        ],
        "deferred": ["149 医院外--科", "54573部队盐场七连-一班"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 双拥表彰单位名单版式修复

- 时间：{now}
- 范围：第四十五卷拥政爱民，附45-3、附45-4。
- 本次变更：{total} 处。

## 修复

- 将最终阅读版中两张“双拥”表彰单位名单从长段落恢复为两个标题和列表。
- 同步正文源中的 `第一次“双拥大会` 为 `第一次“双拥”大会`。
- 合并 `连云港市人民武装警察支队高/公岛边防派出所` 断行。

## 依据

- `workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md:10084-10127`
- `workbench/body_chapters/连云港市志_全书_正文汇总.md:160498-160541`

## 暂缓

- `149 医院外--科`、`54573部队盐场七连-一班` 等疑似 OCR 字形问题未找到更强页级证据，本批不猜修。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 双拥表彰单位名单版式修复"
    memory = f"""
{marker}
- 修复第四十五卷拥政爱民附45-3/附45-4在最终阅读版中被压成一段的问题，恢复为两个标题和列表。
- 同步修正正文源 `第一次“双拥大会` 漏右引号，并合并 `高/公岛边防派出所` 断行。
- 暂缓 `149 医院外--科` 等未闭合字形疑点。
- 报告：`output/reports/reader_readability_military_double_support_lists_20260705.md`。
"""
    append_once(MEMORY, marker, memory)
    print(f"html_block_replacements={html_changes}")
    print(f"source_text_changes={sum(source_changes.values())}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

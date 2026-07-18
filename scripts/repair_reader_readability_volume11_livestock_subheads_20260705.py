# -*- coding: utf-8 -*-
"""Repair source-backed livestock subheading boundaries in volume 11."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume11_livestock_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume11_livestock_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第十一卷畜牧业小标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md"

REPAIRS = [
    ("h5", "一、猪饲养规模", "1949年境内生猪饲养量", "第一章第一节猪"),
    ("h5", "二、牛饲养规模", " 1949年全境养牛42873头", "第一章第一节牛"),
    ("h5", "三、马驴骡", "马1949年，全境养马仅7匹", "第一章第一节马驴骡"),
    ("h5", "四、羊饲养规模", "1949年，全境存栏羊1806只", "第一章第一节羊"),
    ("h5", "五、兔饲养规模", " 20世纪50年代初期，境内养兔很少", "第一章第一节兔"),
    ("h5", "一、家禽饲养规模", "建国初期，鸡、鸭、鹅均为土种散养", "第一章第二节禽类饲养"),
    ("h5", "二、特种禽", "鹌鹑20世纪80年代初期", "第一章第二节禽类饲养"),
    ("h5", "一、蜂", "清朝末年，海州城郊已有零星养蜂", "第一章第三节其它动物养殖"),
    ("h5", "二、水貂", "1958年，市外贸公司在墟沟平山建饲养场", "第一章第三节其它动物养殖"),
    ("h5", "二、加工", "20世纪50年代初期，境内饲料加工", "第二章第二节饲料"),
    ("h5", "一、传染病防治", "猪瘟病 俗称“烂肠瘟”", "第三章第一节疫病防治"),
    ("h5", "二、寄生虫病防治", "肝片吸虫病为牛、羊等反刍动物", "第三章第一节疫病防治"),
    ("h5", "一、防疫", "1953年，境内主要依靠各乡镇中兽医", "第三章第二节防疫检疫"),
    ("h5", "二、检疫", "1985年以前，境内畜禽检疫工作", "第三章第二节防疫检疫"),
    ("h5", "二、兽药供应及管理", "民国时期，境内兽用药品无统一供应渠道", "第三章第三节兽医兽药"),
]

SPECIAL_REPAIRS = [
    (
        "<p>第三节兽医兽药一、兽医组织建国前，境内无畜牧兽医组织",
        '<h4 id="第十一卷-第三章疫病防治与检疫-第三节兽医兽药">第三节兽医兽药</h4>\n<h5>一、兽医组织</h5>\n<p>建国前，境内无畜牧兽医组织',
        "第三章第三节兽医兽药",
    ),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> list[dict[str, str]]:
    text = HTML.read_text(encoding="utf-8")
    fixed = []
    for old, new, group in SPECIAL_REPAIRS:
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected one match for {group}, got {count}")
        text = text.replace(old, new, 1)
        fixed.append({"heading": "第三节兽医兽药 / 一、兽医组织", "group": group, "prefix": "建国前，境内无畜牧兽医组织"})

    for tag, heading, prefix, group in REPAIRS:
        old = f"<p>{heading}{prefix}"
        new = f"<{tag}>{heading}</{tag}>\n<p>{prefix}"
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected one match for {group} {heading!r}, got {count}")
        text = text.replace(old, new, 1)
        fixed.append({"heading": heading, "group": group, "prefix": prefix})

    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第十一卷畜牧业：畜禽饲养、饲料、疫病防治与检疫小标题边界",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "evidence": [
            f"{SOURCE}:5200-5644 第十一卷畜牧业源文显示相关标题为独立行或独立层级",
            "output/final_reader/连云港市志_全书.html:5971-6054 当前最终阅读版残留小标题正文粘连",
        ],
        "notes": ["仅恢复标题边界，不改正文文字、数字、序号或动物/病名。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第十一卷畜牧业小标题边界补修

- 时间：{now}
- 范围：第十一卷畜牧业，畜禽饲养、饲料、疫病防治与检疫。
- 本次修复边界：{len(fixed)} 处。

## 依据

- `{SOURCE}:5200-5644`：源文显示相关标题为独立行或独立层级。
- `output/final_reader/连云港市志_全书.html:5971-6054`：最终阅读版残留小标题正文粘连。

## 修复

"""
    md += "".join(f"- `{item['heading']}`（{item['group']}；前缀 `{item['prefix']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 仅恢复源文结构可证明的标题边界，不改正文文字、数字、序号或动物/病名。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第十一卷畜牧业小标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第十一卷畜牧业 16 处小标题正文粘连，覆盖畜禽饲养、饲料加工、疫病防治、防疫检疫、兽医兽药。
- 依据 `{SOURCE}` 的第十一卷源文上下文，只恢复标题边界，不改正文文字、数字或序号。
- 报告：`output/reports/reader_readability_volume11_livestock_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

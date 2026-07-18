# -*- coding: utf-8 -*-
"""Repair source-backed water engineering subheading boundaries in volume 10."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume10_water_subheads_followup_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume10_water_subheads_followup_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第十卷水利小标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md"

REPAIRS = [
    ("一、河道工程", "沭新河为淮沭新河下段。1957年", "第六章第一节沭新河、沭新渠调水线"),
    ("二、引水涵闸站", "蔷北地涵又称沭新地涵。位于沭阳县", "第六章第一节沭新河、沭新渠调水线"),
    ("一、河道工程", "石安河位于东海县中部，因北起", "第六章第二节石安河调水线"),
    ("二、翻水站", "房山翻水站 位于东海县房山镇山前村", "第六章第二节石安河调水线"),
    ("二、控制涵闸", "青湖闸位于东海县青湖镇北", "第六章第二节石安河调水线"),
    ("一、河道工程", "龙梁河位于东海县西部山丘区", "第六章第三节龙梁河调水线"),
    ("二、翻水站", "磨山翻水站 位于东海县磨山北麓", "第六章第三节龙梁河调水线"),
    ("三、控制涵闸", "龙梁河水闸位于大石埠水库东岸", "第六章第三节龙梁河调水线"),
    ("一、河道工程", "古城渠位于赣榆县西部山丘区", "第六章第四节古城渠调水线"),
    ("二、翻水站", "古城翻水站位于赣榆县班庄乡古城村", "第六章第四节古城渠调水线"),
    ("三、控制涵闸", "陈洪爽漫水闸位于赣榆县夹山乡陈洪爽村南", "第六章第四节古城渠调水线"),
    ("一、河道工程", "沭北引河自沭北通航闸起", "第六章第五节沭北引河调水线"),
    ("二、翻水站", "朱堵一级翻水站 位于赣榆县朱堵乡驻地南", "第六章第五节沭北引河调水线"),
    ("三、控制涵闸", "沭南通航闸位于东海县浦南乡下滩村东", "第六章第五节沭北引河调水线"),
    ("一、水情测报", "清乾隆十年（1745年），知州卫哲治", "第七章第二节水情调度"),
    ("二、洪水调度", "1983年前，境内新沭河、蔷薇河", "第七章第二节水情调度"),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> list[dict[str, str]]:
    text = HTML.read_text(encoding="utf-8")
    fixed = []
    for heading, prefix, group in REPAIRS:
        old = f"<p>{heading}{prefix}"
        new = f"<h5>{heading}</h5>\n<p>{prefix}"
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
        "scope": "第十卷水利：调引江淮沭水、水情调度小标题边界",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "evidence": [
            f"{SOURCE}:1972-1983 目录列出沭新河、石安河、龙梁河、古城渠调水线层级",
            "output/final_reader/连云港市志_全书.html:5763-5830 当前章节内连续出现同类小标题正文粘连",
            "output/final_reader/连云港市志_全书.html:5854-5874 第七章第二节水情调度下的一、二级小标题粘连",
        ],
        "notes": ["仅恢复标题边界，不改正文文字、序号或工程名称。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第十卷水利小标题边界补修

- 时间：{now}
- 范围：第十卷水利，调引江淮沭水与水情调度。
- 本次修复边界：{len(fixed)} 处。

## 依据

- `{SOURCE}:1972-1983`：目录列出沭新河、石安河、龙梁河、古城渠调水线等层级。
- `output/final_reader/连云港市志_全书.html:5763-5830`：同章同节内连续出现同类小标题正文粘连。
- `output/final_reader/连云港市志_全书.html:5854-5874`：第七章第二节水情调度下“一、水情测报”“二、洪水调度”粘连。

## 修复

"""
    md += "".join(f"- `{item['heading']}`（{item['group']}；前缀 `{item['prefix']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 仅恢复源文结构可证明的标题边界，不改正文文字、序号或工程名称。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第十卷水利小标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第十卷水利 16 处小标题正文粘连，覆盖第六章调引江淮沭水及第七章第二节水情调度。
- 依据 `{SOURCE}` 的水利卷目录/章节结构与最终 HTML 连续上下文，只恢复标题边界，不改正文文字或序号。
- 报告：`output/reports/reader_readability_volume10_water_subheads_followup_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

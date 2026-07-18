# -*- coding: utf-8 -*-
"""Repair source-backed subheading boundaries in volumes 5-10."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volumes5_10_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volumes5_10_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第五至十卷小标题边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>四、地图编绘1978年，市测量队编制": "<h5>四、地图编绘</h5>\n<p>1978年，市测量队编制",
    "<p>四、节约用水连云港市于1981年开始城市节水工作": "<h5>四、节约用水</h5>\n<p>连云港市于1981年开始城市节水工作",
    "<p>四、轮渡1958年，经市交通部门批准": "<h5>四、轮渡</h5>\n<p>1958年，经市交通部门批准",
    "<p>四、海滨浴场海滨浴场是海滨景区重要景点": "<h5>四、海滨浴场</h5>\n<p>海滨浴场是海滨景区重要景点",
    "<p>四、海宁园该园为居住区（南小区）公园": "<h5>四、海宁园</h5>\n<p>该园为居住区（南小区）公园",
    "<p>四、专用绿地化工部化工矿山设计研究院绿地": "<h5>四、专用绿地</h5>\n<p>化工部化工矿山设计研究院绿地",
    "<p>四、噪声监测1980年，市环境监测站": "<h5>四、噪声监测</h5>\n<p>1980年，市环境监测站",
    "<p>四、海监1974年，国务院颁布": "<h5>四、海监</h5>\n<p>1974年，国务院颁布",
    "<p>四、投入产出调查1985年投入产出调查": "<h5>四、投入产出调查</h5>\n<p>1985年投入产出调查",
    "<p>四、“重合同、守信用企业”评选1986年7月": "<h5>四、“重合同、守信用企业”评选</h5>\n<p>1986年7月",
    "<p>四、市郊山港城蔬菜区位于市区周围": "<h5>四、市郊山港城蔬菜区</h5>\n<p>位于市区周围",
    "<p>四、海州水萝卜为海州近郊菜农培育": "<h5>四、海州水萝卜</h5>\n<p>为海州近郊菜农培育",
}

SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:2683-2684",
    "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:4472-4473",
    "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:4948-4949",
    "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:5272-5273",
    "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:5314-5315",
    "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:5390-5391",
    "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:7681-7682",
    "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:8175-8176",
    "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:10489-10490",
    "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:12496-12497",
    "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:13742-13743",
    "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md:15398-15399",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> int:
    text = HTML.read_text(encoding="utf-8")
    changed = 0
    for old, new in REPLACEMENTS.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected one match for {old!r}, got {count}")
        text = text.replace(old, new, 1)
        changed += 1
    HTML.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五至十卷：城乡建设、环境保护、经济管理、农林业等小标题边界",
        "html_boundaries_fixed": changed,
        "source_evidence": SOURCE_LINES,
        "notes": ["仅按 PaddleOCR 源文独立行恢复标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第五至十卷小标题边界修复

- 时间：{now}
- 范围：第五至十卷合并源文件中城乡建设、环境保护、经济管理、农林业等残留小标题。
- 本次修复边界：{changed} 处。

## 修复

- 恢复 `四、地图编绘`、`四、节约用水`、`四、轮渡`、`四、海滨浴场`、`四、海宁园`、`四、专用绿地`。
- 恢复 `四、噪声监测`、`四、海监`、`四、投入产出调查`、`四、“重合同、守信用企业”评选`。
- 恢复 `四、市郊山港城蔬菜区`、`四、海州水萝卜`。
- 仅恢复源文可证明的版式边界，不改正文文字。

## 依据

"""
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第五至十卷小标题边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第五至十卷合并段 12 处小标题粘正文问题，覆盖城乡建设、环境保护、经济管理、农林业等章节。
- 依据 `workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md` 中独立行，只恢复标题边界，不改正文文字。
- 报告：`output/reports/reader_readability_volumes5_10_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

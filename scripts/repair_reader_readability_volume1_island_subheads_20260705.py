# -*- coding: utf-8 -*-
"""Split source-backed first-volume island subheads."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume1_island_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume1_island_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷岛屿条目标题版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>一、东西连岛由东连岛和西连岛两部分组成": "<h5>一、东西连岛</h5>\n<p>由东连岛和西连岛两部分组成",
    "<p>二、秦山岛秦山岛位于北纬": "<h5>二、秦山岛</h5>\n<p>秦山岛位于北纬",
    "<p>三、前三岛前三岛是海州湾最前面的": "<h5>三、前三岛</h5>\n<p>前三岛是海州湾最前面的",
    "<p>四、开山岛开山岛位于北纬": "<h5>四、开山岛</h5>\n<p>开山岛位于北纬",
}

SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1021",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1050",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1070",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1129",
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
    for residue in REPLACEMENTS:
        if residue in text:
            raise RuntimeError(f"residue remains: {residue}")
    HTML.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第一卷自然环境：海域第二节岛前四个条目标题",
        "html_boundaries_split": changed,
        "source_evidence": SOURCE_LINES,
        "notes": ["仅拆最终 HTML 条目标题边界，不改正文文字；五至七条目已具备独立强调标题，本批不重复处理。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷岛屿条目标题版式修复

- 时间：{now}
- 范围：第一卷自然环境，第三章海域第二节岛前四个条目标题。
- 本次拆分边界：{changed} 处。

## 修复

- 将 `一、东西连岛`、`二、秦山岛`、`三、前三岛`、`四、开山岛` 从段首粘连中恢复为独立条目标题。
- `五、羊山岛`、`六、竹岛`、`七、鸽岛` 在最终阅读版中已经是独立强调标题，本批不重复处理。
- 仅恢复版式边界，不改正文文字。

## 依据

"""
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第一卷岛屿条目标题版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第一卷自然环境第三章海域第二节岛前四个条目标题粘正文问题。
- 覆盖 `一、东西连岛`、`二、秦山岛`、`三、前三岛`、`四、开山岛`；五至七已为独立强调标题，本批不重复处理。
- 仅按 PaddleOCR 源文独立行恢复版式边界，不改正文文字。
- 报告：`output/reports/reader_readability_volume1_island_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Repair a small source-backed batch of reader label boundaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_cross_volume_label_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_cross_volume_label_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_跨卷小标题边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>二、气候新浦地区位处暖温带南缘": "<h5>二、气候</h5>\n<p>新浦地区位处暖温带南缘",
    "<p>三、资源植物资源较丰富": "<h5>三、资源</h5>\n<p>植物资源较丰富",
    "<p>二、三洋港渔港位于临洪河口": "<h5>二、三洋港渔港</h5>\n<p>位于临洪河口",
    "<p>集体农业贷款1964年为支持海洋集体渔业生产": "<p><strong>集体农业贷款</strong>1964年为支持海洋集体渔业生产",
    "<p>路面管理民国36年（1947年）10月": "<p><strong>路面管理</strong>民国36年（1947年）10月",
}

SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第三卷_区县概况.md:54-65",
    "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:6217-6218",
    "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:24487-24489",
    "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md:4419",
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
        "scope": "第三卷、十二卷、四十卷、四十四卷：小标题/段首标签边界",
        "html_boundaries_fixed": changed,
        "source_evidence": SOURCE_LINES,
        "notes": ["仅恢复源文可证明的小标题或段首标签边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 跨卷小标题边界修复

- 时间：{now}
- 范围：第三卷区县概况、第十二卷水产、第四十卷金融、第四十四卷治安司法。
- 本次修复边界：{changed} 处。

## 修复

- 第三卷新浦地区：恢复 `二、气候`、`三、资源` 两个独立小标题。
- 第十二卷水产：恢复 `二、三洋港渔港` 独立小标题。
- 第四十卷金融：将 `集体农业贷款` 标为段首标签。
- 第四十四卷治安司法：将 `路面管理` 标为段首标签。
- 仅恢复版式边界，不改正文文字。

## 依据

"""
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 跨卷小标题边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第三卷、十二卷、四十卷、四十四卷共 5 处源文可证明的小标题/段首标签粘正文问题。
- 覆盖 `二、气候`、`三、资源`、`二、三洋港渔港`、`集体农业贷款`、`路面管理`。
- 仅恢复版式边界，不改正文文字。
- 报告：`output/reports/reader_readability_cross_volume_label_boundaries_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

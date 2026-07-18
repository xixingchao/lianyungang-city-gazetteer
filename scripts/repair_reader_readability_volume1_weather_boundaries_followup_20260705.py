# -*- coding: utf-8 -*-
"""Repair a few source-backed weather boundaries in the first volume reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume1_weather_boundaries_followup_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume1_weather_boundaries_followup_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷气象边界跟进修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p><p><strong>气温特征</strong></p>": "<p><strong>气温特征</strong></p>",
    "<p>越冬期温度连云港市越冬期平均日期始于": "<p><strong>越冬期温度</strong>连云港市越冬期平均日期始于",
    "<p>五、降水降水量 连云港市处于季风气候带": "<h5>五、降水</h5>\n<p><strong>降水量</strong> 连云港市处于季风气候带",
    "<p><p><strong>雪</strong></p>": "<p><strong>雪</strong></p>",
}

SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1514",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1529",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1532-1533",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:2142-2148",
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
        "scope": "第一卷自然环境：气象段落边界跟进",
        "html_boundaries_fixed": changed,
        "source_evidence": SOURCE_LINES,
        "notes": ["修复两处嵌套 p 标签和两处源文可证明的小标题/小标签边界。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷气象边界跟进修复

- 时间：{now}
- 范围：第一卷自然环境第三章气候气象要素段。
- 本次修复边界：{changed} 处。

## 修复

- 清理 `气温特征`、`雪` 两处 `<p><p>` 嵌套。
- 将 `越冬期温度` 恢复为段首小标签。
- 将 `五、降水` 从 `降水量` 段首拆出，并将 `降水量` 标为段首小标签。
- 仅恢复源文可证明的版式边界，不改正文文字。

## 依据

"""
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第一卷气象边界跟进修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 跟进修复第一卷自然环境气象段 4 处边界：`气温特征`、`越冬期温度`、`五、降水/降水量`、`雪`。
- 清理两处 `<p><p>` 嵌套；其余仅恢复源文可证明的小标题/小标签边界。
- 报告：`output/reports/reader_readability_volume1_weather_boundaries_followup_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

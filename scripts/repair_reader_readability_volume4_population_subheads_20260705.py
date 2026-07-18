# -*- coding: utf-8 -*-
"""Repair source-backed population volume subheading boundaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume4_population_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume4_population_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四卷人口小标题边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>一、自然变动建国后，新海连市始有人口自然变动的记载": "<h5>一、自然变动</h5>\n<p>建国后，新海连市始有人口自然变动的记载",
    "<p>一、人口分布市区人口 1949年末，市区人口15.8万": "<h5>一、人口分布</h5>\n<p>市区人口 1949年末，市区人口15.8万",
    "<p>二、人口密度民国35年(1946年)，赣榆县人口密度": "<h5>二、人口密度</h5>\n<p>民国35年(1946年)，赣榆县人口密度",
    "<p>四、“七五”期间人口规划1983年实行市管县体制后": "<h5>四、“七五”期间人口规划</h5>\n<p>1983年实行市管县体制后",
    "<p>二、技术服务1958年，市卫生局选派妇产科医师": "<h5>二、技术服务</h5>\n<p>1958年，市卫生局选派妇产科医师",
}

SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md:353-355",
    "workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md:703-705",
    "workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md:732-734",
    "workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md:1828-1830",
    "workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md:1914-1916",
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
        "scope": "第四卷人口：人口变动、分布密度、人口规划、技术服务小标题",
        "html_boundaries_fixed": changed,
        "source_evidence": SOURCE_LINES,
        "notes": ["仅按 PaddleOCR 源文独立行恢复标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第四卷人口小标题边界修复

- 时间：{now}
- 范围：第四卷人口，人口变动、人口分布与密度、人口规划、技术服务。
- 本次修复边界：{changed} 处。

## 修复

- 恢复 `一、自然变动`、`一、人口分布`、`二、人口密度` 三处人口规模小标题。
- 恢复 `四、“七五”期间人口规划` 和 `二、技术服务` 小标题。
- 仅恢复源文可证明的版式边界，不改正文文字。

## 依据

"""
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第四卷人口小标题边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四卷人口 5 处小标题粘正文问题：`一、自然变动`、`一、人口分布`、`二、人口密度`、`四、“七五”期间人口规划`、`二、技术服务`。
- 依据 `workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md` 中独立行，只恢复标题边界，不改正文文字。
- 报告：`output/reports/reader_readability_volume4_population_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

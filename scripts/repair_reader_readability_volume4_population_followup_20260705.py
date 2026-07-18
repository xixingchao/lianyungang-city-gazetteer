# -*- coding: utf-8 -*-
"""Repair remaining source-backed population subheading boundaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume4_population_followup_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume4_population_followup_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四卷人口规划优生优育边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPAIRS = [
    {
        "heading": "一、“四五”期间人口规划",
        "old": "<p>一、“四五”期间人口规划“四五”(1971～1975年)人口规划是连云港市人口发展史上第一个把人口增长规模纳入经济、社会发展轨道的规划。",
        "new": "<h5>一、“四五”期间人口规划</h5>\n<p>“四五”(1971～1975年)人口规划是连云港市人口发展史上第一个把人口增长规模纳入经济、社会发展轨道的规划。",
        "source": "workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md:1764-1765",
    },
    {
        "heading": "二、“五五”期间人口规划",
        "old": "<p>二、“五五”期间人口规划1974年末，市计划生育领导小组根据中共中央提出的“晚、稀、少”生育要求，修订婚育政策。",
        "new": "<h5>二、“五五”期间人口规划</h5>\n<p>1974年末，市计划生育领导小组根据中共中央提出的“晚、稀、少”生育要求，修订婚育政策。",
        "source": "workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md:1788-1789",
    },
    {
        "heading": "三、“六五”期间人口规划",
        "old": "<p>三、“六五”期间人口规划1978年10月，中央提倡一对夫妇生育子女数最好一个，最多两个。",
        "new": "<h5>三、“六五”期间人口规划</h5>\n<p>1978年10月，中央提倡一对夫妇生育子女数最好一个，最多两个。",
        "source": "workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md:1809-1810",
    },
    {
        "heading": "一、药具服务",
        "old": "<p>一、药具服务1957年，开始提供男用避孕套。",
        "new": "<h5>一、药具服务</h5>\n<p>1957年，开始提供男用避孕套。",
        "source": "workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md:1899-1900",
    },
    {
        "heading": "一、优生",
        "old": "<p>一、优生民国18年(1929年)，新浦、海州出现新法接生。",
        "new": "<h5>一、优生</h5>\n<p>民国18年(1929年)，新浦、海州出现新法接生。",
        "source": "workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md:1946-1947",
    },
    {
        "heading": "二、优育",
        "old": "<p>二、优育1949年前，婴幼儿大都散居在家。",
        "new": "<h5>二、优育</h5>\n<p>1949年前，婴幼儿大都散居在家。",
        "source": "workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md:1965-1966",
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> list[dict[str, str]]:
    text = HTML.read_text(encoding="utf-8")
    fixed = []
    for item in REPAIRS:
        count = text.count(item["old"])
        if count != 1:
            raise RuntimeError(f"expected one match for {item['heading']!r}, got {count}")
        text = text.replace(item["old"], item["new"], 1)
        fixed.append({"heading": item["heading"], "source": item["source"]})
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四卷人口：人口规划、药具服务、优生优育残留小标题边界",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": ["仅按 PaddleOCR 源文独立行恢复标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四卷人口规划优生优育边界补修

- 时间：{now}
- 范围：第四卷人口，人口规划、药具服务、优生优育。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['heading']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 仅恢复源文可证明的版式边界，不改正文文字。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四卷人口规划优生优育边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四卷人口 6 处残留小标题粘正文问题：`一、“四五”期间人口规划`、`二、“五五”期间人口规划`、`三、“六五”期间人口规划`、`一、药具服务`、`一、优生`、`二、优育`。
- 依据 `workbench/body_chapters/paddle_上/第四卷_人口（part01_部分）.md` 中独立行，只恢复标题边界，不改正文文字。
- 报告：`output/reports/reader_readability_volume4_population_followup_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

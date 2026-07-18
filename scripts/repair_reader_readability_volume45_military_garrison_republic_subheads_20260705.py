# -*- coding: utf-8 -*-
"""Repair source-backed Republic-era garrison subhead boundaries in volume 45."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume45_military_garrison_republic_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume45_military_garrison_republic_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四十五卷军事民国驻防标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"

REPAIRS = [
    {
        "old": "<p>一、驻军军阀及国民政府军队【江苏陆军第八师】民国元年（1912年），",
        "new": "<h5>一、驻军</h5>\n<p>军阀及国民政府军队【江苏陆军第八师】民国元年（1912年），",
        "heading": "一、驻军",
        "source": f"{SOURCE}:9278",
    },
    {
        "old": "<p>二、地方武装民国政府及国民党领导的地方武装【东海县警备队】民国初年",
        "new": "<h5>二、地方武装</h5>\n<p>民国政府及国民党领导的地方武装【东海县警备队】民国初年",
        "heading": "二、地方武装",
        "source": f"{SOURCE}:9374",
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> list[dict[str, str]]:
    text = HTML.read_text(encoding="utf-8")
    fixed: list[dict[str, str]] = []
    for item in REPAIRS:
        count = text.count(item["old"])
        if count != 1:
            raise RuntimeError(f"expected one match for {item['heading']}, got {count}")
        text = text.replace(item["old"], item["new"], 1)
        fixed.append({"heading": item["heading"], "source": item["source"]})
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十五卷军事：第二章驻防第二节",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": ["仅拆出源文独立编号子目标题；不改正文内容。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四十五卷军事民国驻防标题边界补修

- 时间：{now}
- 范围：第四十五卷军事，第二章驻防第二节。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['heading']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 拆出 `一、驻军`、`二、地方武装` 两个编号子目标题。\n- 不重写驻军、地方武装条目正文，不猜改 OCR 内容。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四十五卷军事民国驻防标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第四十五卷军事第二章驻防第二节 2 处编号子目标题边界：`一、驻军`、`二、地方武装`。
- 依据 `{SOURCE}:9278-9374` 源文独立标题行；仅拆出 h5，不改正文内容。
- 报告：`output/reports/reader_readability_volume45_military_garrison_republic_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Repair empty paragraphs and bare paragraph lines in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_html_empty_and_bare_paragraphs_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_html_empty_and_bare_paragraphs_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_HTML空段与裸段落结构修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> dict[str, object]:
    text = HTML.read_text(encoding="utf-8")
    empty_count = text.count("<p></p>\n")
    text = text.replace("<p></p>\n", "")

    wrapped: list[dict[str, object]] = []
    lines = text.splitlines()
    in_style = False
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if "<style>" in stripped:
            in_style = True
        if "</style>" in stripped:
            in_style = False
            continue
        if in_style or not stripped:
            continue
        if stripped.endswith("</p>") and not stripped.startswith("<"):
            lines[idx] = f"<p>{stripped}"
            wrapped.append({"line": idx + 1, "text_start": stripped[:80]})

    HTML.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"empty_paragraphs_removed": empty_count, "bare_paragraphs_wrapped": wrapped}


def main() -> None:
    result = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "最终阅读版 HTML 结构：空段与缺失起始 <p> 的裸段落行",
        "empty_paragraphs_removed": result["empty_paragraphs_removed"],
        "bare_paragraphs_wrapped_count": len(result["bare_paragraphs_wrapped"]),
        "bare_paragraphs_wrapped": result["bare_paragraphs_wrapped"],
        "notes": [
            "仅修复 HTML 包裹结构；不改正文文字、不改表格数据。",
            "裸段落行均为已有 </p> 但缺少起始 <p> 的正文行。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# HTML空段与裸段落结构修复

- 时间：{now}
- 范围：最终阅读版 HTML 结构。
- 删除空段：{result['empty_paragraphs_removed']} 处。
- 补齐裸段落起始 `<p>`：{len(result['bare_paragraphs_wrapped'])} 处。

## 说明

- 仅删除空 `<p></p>` 与补齐缺失的段落起始标签。
- 不改正文文字，不改表格数据。
- 这类问题来自前序标题/表格修复后留下的 HTML 包裹残缺。

## 补齐位置

"""
    for item in result["bare_paragraphs_wrapped"]:
        md += f"- line {item['line']}: `{item['text_start']}`\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 HTML空段与裸段落结构修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 删除最终阅读版空 `<p></p>` {result['empty_paragraphs_removed']} 处。
- 将 {len(result['bare_paragraphs_wrapped'])} 处已有 `</p>` 但缺起始 `<p>` 的裸正文行补齐为合法段落。
- 本批仅修复 HTML 包裹结构，不改正文文字和结构化表格数据。
- 报告：`output/reports/reader_html_empty_and_bare_paragraphs_20260705.md`。
""",
    )

    print(f"empty_paragraphs_removed={result['empty_paragraphs_removed']}")
    print(f"bare_paragraphs_wrapped={len(result['bare_paragraphs_wrapped'])}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

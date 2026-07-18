# -*- coding: utf-8 -*-
"""Split compressed headings in the major flood appendix without touching body text."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_major_flood_appendix_headings_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_major_flood_appendix_headings_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_重大抗灾纪实附录标题版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>附10-1：重大抗灾纪实一、1950年新沂河灌云段抗洪纪实1950年6月下旬，": "<h4>附10-1：重大抗灾纪实</h4>\n<h5>一、1950年新沂河灌云段抗洪纪实</h5>\n<p>1950年6月下旬，",
    "<p>二、1970年市区抗洪纪实1970年7月中旬，": "<h5>二、1970年市区抗洪纪实</h5>\n<p>1970年7月中旬，",
}

RESIDUALS = [
    "附10-1：重大抗灾纪实一、1950年",
    "二、1970年市区抗洪纪实1970年",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> int:
    text = HTML.read_text(encoding="utf-8")
    changed = 0
    for old, new in REPLACEMENTS.items():
        if old not in text:
            raise RuntimeError(f"expected compressed heading not found: {old}")
        text = text.replace(old, new, 1)
        changed += 1
    for residue in RESIDUALS:
        if residue in text:
            raise RuntimeError(f"compressed heading residue remains: {residue}")
    HTML.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第十卷水利：附10-1 重大抗灾纪实",
        "heading_splits": changed,
        "source_evidence": ["workbench/body_chapters/连云港市志_全书_正文汇总.md:44612-44643"],
        "notes": ["仅拆分最终阅读版中被压缩的附录标题和小节标题，不覆盖正文文字，避免源 OCR 错字回流。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 重大抗灾纪实附录标题版式修复

- 时间：{now}
- 范围：第十卷水利，附10-1 重大抗灾纪实。
- 本次拆分标题：{changed} 处。

## 修复

- 将 `附10-1：重大抗灾纪实` 从正文段首拆为独立附录标题。
- 将 `一、1950年新沂河灌云段抗洪纪实`、`二、1970年市区抗洪纪实` 拆为独立小节标题。
- 仅处理最终阅读版标题粘连，不用源 OCR 整段覆盖正文，避免源文错字回流。

## 依据

- `workbench/body_chapters/连云港市志_全书_正文汇总.md:44612-44643`
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 重大抗灾纪实附录标题版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第十卷水利 `附10-1：重大抗灾纪实` 在最终阅读版中附录标题、小节标题被压入正文段的问题。
- 仅拆最终 HTML 标题粘连，不用源 OCR 覆盖正文，避免 `连云港市志_全书_正文汇总.md:44612-44643` 中仍存在的 OCR 错字回流。
- 报告：`output/reports/reader_readability_major_flood_appendix_headings_20260705.md`。
""",
    )
    print(f"heading_splits={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

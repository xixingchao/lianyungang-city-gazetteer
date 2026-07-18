# -*- coding: utf-8 -*-
"""Split first-volume late appendix titles from first entries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume1_late_appendix_titles_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume1_late_appendix_titles_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷后续附录标题版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>附1-5：连云港市濒危果树名录红巴梨": "<h4>附1-5：连云港市濒危果树名录</h4>\n<p>红巴梨",
    "<p>附1-6：连云港市濒危药用植物名录多孔菌科": "<h4>附1-6：连云港市濒危药用植物名录</h4>\n<p>多孔菌科",
    "<p>附1-7：连云港市野生爬行类动物名录龟科": "<h4>附1-7：连云港市野生爬行类动物名录</h4>\n<p>龟科",
    "<p>附1-8：连云港市野生两栖类动物名录盘古蟾科": "<h4>附1-8：连云港市野生两栖类动物名录</h4>\n<p>盘古蟾科",
    "<p>附1-9：连云港市淡水鱼类名录鲤形目": "<h4>附1-9：连云港市淡水鱼类名录</h4>\n<p>鲤形目",
    "<p>附1-10：连云港市海水鱼类名录真鲨科": "<h4>附1-10：连云港市海水鱼类名录</h4>\n<p>真鲨科",
    "<p>附1-11：连云港市海水贝类名录多板纲": "<h4>附1-11：连云港市海水贝类名录</h4>\n<p>多板纲",
    "<p>附1-12：连云港市境西汉至民国时期主要地震汉前元元年": "<h4>附1-12：连云港市境西汉至民国时期主要地震</h4>\n<p>汉前元元年",
}
RESIDUALS = list(REPLACEMENTS)


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
    for residue in RESIDUALS:
        if residue in text:
            raise RuntimeError(f"late appendix title residue remains: {residue}")
    HTML.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第一卷自然环境：附1-5至附1-12标题粘连",
        "html_titles_split": changed,
        "source_evidence": [
            "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5639-5650",
            "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5731-5782",
            "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5868",
            "workbench/body_chapters/paddle_上/第一卷_自然环境.md:6272",
        ],
        "notes": ["仅拆最终 HTML 附录标题边界；名录内部分类层级另批处理。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷后续附录标题版式修复

- 时间：{now}
- 范围：第一卷自然环境，附1-5至附1-12。
- 本次拆分标题：{changed} 处。

## 修复

- 将 `附1-5` 至 `附1-12` 从首条正文中拆出为独立附录标题。
- 本批只恢复标题边界，不重排名录内部分类，不改正文文字。

## 暂缓

- `附1-9`、`附1-10`、`附1-11` 内部鱼类/贝类分类层级仍需另批按源行结构细修。

## 依据

- `workbench/body_chapters/paddle_上/第一卷_自然环境.md:5639-5650`
- `workbench/body_chapters/paddle_上/第一卷_自然环境.md:5731-5782`
- `workbench/body_chapters/paddle_上/第一卷_自然环境.md:5868`
- `workbench/body_chapters/paddle_上/第一卷_自然环境.md:6272`
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第一卷后续附录标题版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第一卷自然环境 `附1-5` 至 `附1-12` 在最终阅读版中附录标题粘首条正文的问题。
- 按 PaddleOCR 源文独立行证据，只恢复标题边界，不重排名录内部分类，不改正文文字。
- `附1-9`、`附1-10`、`附1-11` 内部鱼类/贝类分类层级另批处理。
- 报告：`output/reports/reader_readability_volume1_late_appendix_titles_20260705.md`。
""",
    )
    print(f"html_titles_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

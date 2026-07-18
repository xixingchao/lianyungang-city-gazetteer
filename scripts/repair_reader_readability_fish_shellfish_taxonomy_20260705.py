# -*- coding: utf-8 -*-
"""Restore taxonomy line breaks in volume 1 fish and shellfish appendices."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_fish_shellfish_taxonomy_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_fish_shellfish_taxonomy_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷鱼类贝类分类层级版式修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "<p>鲤形目【鲤科】": "<p><strong>鲤形目</strong></p>\n<p>【鲤科】",
    "<p>形目【鮠科】": "<p><strong>形目</strong></p>\n<p>【鮠科】",
    "<p>颌针鱼目【针鱼科】": "<p><strong>颌针鱼目</strong></p>\n<p>【针鱼科】",
    "<p>鲈形目【鲳科】": "<p><strong>鲈形目</strong></p>\n<p>【鲳科】",
    "<p>鲉目【杜父鱼科】": "<p><strong>鲉目</strong></p>\n<p>【杜父鱼科】",
    "<p>鲻形目【鲻科】": "<p><strong>鲻形目</strong></p>\n<p>【鲻科】",
    "<p>马鲅目【马鲅科】": "<p><strong>马鲅目</strong></p>\n<p>【马鲅科】",
    "<p>鳗鲡目【鳗鲡科】": "<p><strong>鳗鲡目</strong></p>\n<p>【鳗鲡科】",
    "<p>鲱形目【鲱科】": "<p><strong>鲱形目</strong></p>\n<p>【鲱科】",
    "<p>合鳃目【合鳃科】": "<p><strong>合鳃目</strong></p>\n<p>【合鳃科】",
    "<p>鲤行目【鲤科】": "<p><strong>鲤行目</strong></p>\n<p>【鲤科】",
    "<p>多板纲【石鳖目】": "<p><strong>多板纲</strong></p>\n<p>【石鳖目】",
    "<p>瓣腮纲【列齿目】": "<p><strong>瓣腮纲</strong></p>\n<p>【列齿目】",
    "<p>腹足纲【原始腹足目】": "<p><strong>腹足纲</strong></p>\n<p>【原始腹足目】",
    "<p>【中腹足目】汇螺科": "<p>【中腹足目】</p>\n<p>汇螺科",
    "<p>【新腹足目】骨螺科": "<p>【新腹足目】</p>\n<p>骨螺科",
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
            raise RuntimeError(f"taxonomy residue remains: {residue}")
    HTML.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第一卷自然环境：附1-9至附1-11鱼类贝类分类层级",
        "html_taxonomy_boundaries_split": changed,
        "source_evidence": [
            "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5745-5781",
            "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5869-5909",
        ],
        "notes": ["仅按源行恢复目/纲/部分目级边界；源 OCR 残缺词照录，不猜修。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷鱼类贝类分类层级版式修复

- 时间：{now}
- 范围：第一卷自然环境，附1-9至附1-11。
- 本次拆分分类边界：{changed} 处。

## 修复

- 按 PaddleOCR 源文独立行，将淡水鱼类名录中的 `鲤形目`、`颌针鱼目`、`鲈形目` 等目级标题从科名中拆出。
- 将海水贝类名录中的 `多板纲`、`瓣腮纲`、`腹足纲` 及部分目级标题从后续条目中拆出。
- 仅恢复版式边界；`形目`、`【科】鱼`、`鲤行目` 等源 OCR 残缺或疑似错字照录，不猜修。

## 依据

- `workbench/body_chapters/paddle_上/第一卷_自然环境.md:5745-5781`
- `workbench/body_chapters/paddle_上/第一卷_自然环境.md:5869-5909`
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第一卷鱼类贝类分类层级版式修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第一卷自然环境 `附1-9` 至 `附1-11` 中鱼类/贝类分类层级与条目粘连的问题。
- 按 PaddleOCR 源文独立行恢复目/纲/部分目级边界；源 OCR 残缺词照录，不猜修。
- 报告：`output/reports/reader_readability_fish_shellfish_taxonomy_20260705.md`。
""",
    )
    print(f"html_taxonomy_boundaries_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

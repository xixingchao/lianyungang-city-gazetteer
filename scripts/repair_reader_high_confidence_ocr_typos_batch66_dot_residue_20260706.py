# -*- coding: utf-8 -*-
"""Batch 66: verified dot-residue and short OCR fixes."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第六十六批_字间点残留短片段.md"

REPLACEMENTS = [
    (
        "市罐头食品广不断扩大基础设施建设",
        "市罐头食品厂不断扩大基础设施建设",
        "`workbench/ocr/paddle_ocr/中/part01/page_0076.txt` 作 `市罐头食品厂不断扩大基础设施建设`；raw 为形近 `食品广`",
    ),
    (
        "且时产时.停。到1979年",
        "且时产时停。到1979年",
        "同页 raw 断行为 `时产时/.停`，`workbench/ocr/paddle_ocr/中/part01/page_0076.txt` 连读为 `时产时停`",
    ),
    (
        "在2102袖珍型立体声放音机的基础.上使用香港所开模具",
        "在2102袖珍型立体声放音机的基础上使用香港所开模具",
        "`workbench/ocr/paddle_ocr/中/part01/page_0238.txt` 作 `基础上使用`，当前 reader 多余字间点",
    ),
    (
        "全市生产大理石、花岗石板材的企业8家.生产各种大理石、花岗石板材",
        "全市生产大理石、花岗石板材的企业8家，生产各种大理石、花岗石板材",
        "`workbench/ocr/raw/中/part01/page_0290.txt` 与 Paddle 均定位该行；字间点处为句内停顿，按正文标点补作逗号",
    ),
    (
        "只能作建筑.石材，不能做板材",
        "只能作建筑石材，不能做板材",
        "同段后文作 `用作建筑石料、石子`，且 `workbench/ocr/paddle_ocr/下/part01/page_0442.txt` 有同类术语 `建筑石材`；当前 reader 多余字间点",
    ),
    (
        "扩大了轻工协作.产品的照顾范围",
        "扩大了轻工协作产品的照顾范围",
        "`workbench/ocr/paddle_ocr/中/part02/page_0336.txt` 作 `扩大了轻工协作/产品的照顾范围`，当前 reader 多余字间点",
    ),
    (
        "1986年，市交警.大队全年检验机动车19860辆",
        "1986年，市交警大队全年检验机动车19860辆",
        "`workbench/ocr/paddle_ocr/下/part01/page_0088.txt` 作 `1986年，市交警/大队全年检验机动车19860辆`，当前 reader 多余字间点",
    ),
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changed = []
    for old, new, evidence in REPLACEMENTS:
        count = html.count(old)
        if count != 1:
            raise RuntimeError(f"expected 1 hit, found {count}: {old}")
        html = html.replace(old, new)
        changed.append((old, new, evidence))

    HTML.write_text(html, encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第六十六批：字间点残留短片段",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for old, new, evidence in changed:
        lines.append(f"- `{old}` -> `{new}`（命中 1 处）")
        lines.append(f"  - 证据：{evidence}")
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "- 只修主阅读版，不改 OCR 原文。",
            "- `票高献身精神`、`用破万人心`、`避选`、`上尽，然长逝` 仍缺稳定文本证据，本批不猜改。",
            "- 未展示、未嵌入页图。",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"changed={len(changed)}")
    print(f"progress={REPORT}")


if __name__ == "__main__":
    main()

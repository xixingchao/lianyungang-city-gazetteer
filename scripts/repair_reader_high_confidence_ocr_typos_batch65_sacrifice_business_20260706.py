# -*- coding: utf-8 -*-
"""Batch 65: verified sacrifice and business-knowledge short fixes."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第六十五批_牺牲业务短片段.md"

REPLACEMENTS = [
    (
        "烈士栖牲处建吕祥璧烈士纪念亭",
        "烈士牺牲处建吕祥璧烈士纪念亭",
        "同句碑文作 `吕祥璧烈士牺牲处`，当前前半句为 `栖牲处` 形近残留",
    ),
    (
        "最后朱环被枪杀，临刑前高呼：“打倒日本帝国主义！”“中国共产党万岁！”栖牲时年仅18岁",
        "最后朱环被枪杀，临刑前高呼：“打倒日本帝国主义！”“中国共产党万岁！”牺牲时年仅18岁",
        "人物烈士语境，前文作 `被枪杀`；`栖牲时` 为 `牺牲时` 形近残留",
    ),
    (
        "华川战斗栖牲通讯员",
        "华川战斗牺牲通讯员",
        "同段烈士表多处作 `战斗牺牲`，该处 `战斗栖牲` 为形近残留",
    ),
    (
        "不怕栖牲，谱写的一曲曲可歌可泣的动人事迹",
        "不怕牺牲，谱写的一曲曲可歌可泣的动人事迹",
        "`workbench/ocr/tesseract_check/book_end_20260706/page_0475_tess.txt` 作 `不怕牺牲`；raw 同页为 `不怕栖牲` 残留",
    ),
    (
        "认真学习修志理论与业.务知识",
        "认真学习修志理论与业务知识",
        "`workbench/ocr/raw/下/part02/page_0476.txt` 断行为 `业/.务知识`，Tesseract 连读为 `业务知识`；当前 reader 多余句点",
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
        "# 高置信 OCR 错字补修第六十五批：牺牲、业务短片段",
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
            "- `避选`、`上尽，然长逝`、`票高献身精神` 等仍缺稳定文本证据，本批不猜改。",
            "- 未展示、未嵌入页图。",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"changed={len(changed)}")
    print(f"progress={REPORT}")


if __name__ == "__main__":
    main()

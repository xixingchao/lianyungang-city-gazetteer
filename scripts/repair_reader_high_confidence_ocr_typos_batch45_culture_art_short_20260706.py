# -*- coding: utf-8 -*-
"""Batch 45: verified culture art short OCR fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch45_culture_art_short_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch45_culture_art_short_20260706.json"

CHANGES = [
    {
        "old": "王寿暖、程民义",
        "new": "王寿谖、程民义",
        "section": "文化雕塑阶级教育展览段",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0023.txt:10 作王寿谖、程民义"],
    },
    {
        "old": "《李时珍》《渔家姑娘》、《少先队员《徐福》等人物雕塑，屹立在工广、医院",
        "new": "《李时珍》、《渔家姑娘》、《少先队员》、《徐福》等人物雕塑，屹立在工厂、医院",
        "section": "文化雕塑人物作品段",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0023.txt:16-17 作《李时珍》、《渔家姑娘》、《少先队员》、《徐福》等人物雕塑，屹立在工厂、医院"],
    },
    {
        "old": "徐哗宇的《同心协力》",
        "new": "徐晔宇的《同心协力》",
        "section": "文化摄影作品入选段",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0024.txt:8 作徐晔宇的《同心协力》"],
    },
    {
        "old": "徐哗宇的《凯旋》",
        "new": "徐晔宇的《凯旋》",
        "section": "文化摄影新闻摄影比赛段",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0024.txt:10 作徐晔宇的《凯旋》"],
    },
    {
        "old": "徐哗宇、成磊个人摄影艺术展览",
        "new": "徐晔宇、成磊个人摄影艺术展览",
        "section": "文化摄影个人展览段",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0024.txt:11 作徐晔宇、成磊个人摄影艺术展览"],
    },
    {
        "old": "陇海铁路沼线13个城市",
        "new": "陇海铁路沿线13个城市",
        "section": "文化摄影横贯中国联展段",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0024.txt:19 作陇海铁路沿线13个城市"],
    },
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for change in CHANGES:
        count = html.count(change["old"])
        if count != 1:
            raise RuntimeError(f"expected one hit for {change['section']}, found {count}: {change['old'][:80]}")
        html = html.replace(change["old"], change["new"])
        applied.append({**change, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "note": "只修页级 PaddleOCR 闭合且旧串唯一命中的文化卷雕塑、摄影短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第四十五批：文化艺术短片段",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- {item['section']}：`{item['old']}` -> `{item['new']}`（命中 {item['count']} 处）")
        for evidence in item["evidence"]:
            lines.append(f"  - 证据：`{evidence}`")
    lines += [
        "",
        "## 边界",
        "",
        "- 只修主阅读版，不改 OCR 原文。",
        "- 每项旧串均要求唯一命中。",
        "- 只处理下册文化卷雕塑、摄影小节 `page_0023` 至 `page_0024` 已闭合短片段。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

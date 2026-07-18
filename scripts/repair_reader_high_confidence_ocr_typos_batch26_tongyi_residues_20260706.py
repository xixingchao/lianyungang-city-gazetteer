# -*- coding: utf-8 -*-
"""Twenty-sixth batch: PaddleOCR-backed '统一一' residue fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch26_tongyi_residues_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch26_tongyi_residues_20260706.json"

CHANGES = [
    {
        "old": "统一一安排船舶装卸计划",
        "new": "统一安排船舶装卸计划",
        "section": "口岸船舶预确报段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0464.txt:10 raw 作统一一安排",
            "workbench/ocr/paddle_ocr/中/part01/page_0464.txt:10 PaddleOCR 作统一安排",
        ],
    },
    {
        "old": "全国统一一的资费标准",
        "new": "全国统一的资费标准",
        "section": "邮电函件业务段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0070.txt:23 raw 作统一一的资费标准",
            "workbench/ocr/paddle_ocr/中/part02/page_0070.txt:25 PaddleOCR 作统一的资费标准",
        ],
    },
    {
        "old": "对轮胎实行统一一收购、统一供应、以旧换新、翻新复用",
        "new": "对轮胎实行统一收购、统一供应、以旧换新、翻新复用",
        "section": "物资流通机构体制段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0259.txt:38 raw 作统一一收购",
            "workbench/ocr/paddle_ocr/中/part02/page_0259.txt:38 PaddleOCR 作统一收购",
        ],
    },
    {
        "old": "仍由省公司统一一代订、代分",
        "new": "仍由省公司统一代订、代分",
        "section": "物资流通汽车配件段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0272.txt:17 raw 作统一一代订",
            "workbench/ocr/paddle_ocr/中/part02/page_0272.txt:18 PaddleOCR 作统一代订",
        ],
    },
    {
        "old": "按照“统一一领导，分级管理”的原则",
        "new": "按照“统一领导，分级管理”的原则",
        "section": "财政体制段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0280.txt:4 raw 作统一一领导",
            "workbench/ocr/paddle_ocr/中/part02/page_0280.txt:4 PaddleOCR 作统一领导",
        ],
    },
    {
        "old": "由市、区两级整顿市场办公室统一一领导",
        "new": "由市、区两级整顿市场办公室统一领导",
        "section": "税务稽查段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0340.txt:7 raw 作统一一领导",
            "workbench/ocr/paddle_ocr/中/part02/page_0340.txt:7 PaddleOCR 作统一领导",
        ],
    },
    {
        "old": "执行专业银行统一一的存款准备金制度",
        "new": "执行专业银行统一的存款准备金制度",
        "section": "金融存款准备金段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0355.txt:4 raw 作统一一的存款准备金制度",
            "workbench/ocr/paddle_ocr/中/part02/page_0355.txt:4 PaddleOCR 作统一的存款准备金制度",
        ],
    },
    {
        "old": "军队转业干部家属调动，统一一由劳动部门管理",
        "new": "军队转业干部家属调动，统一由劳动部门管理",
        "section": "劳动力管理军队转业干部家属段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0247.txt:6 raw 作统一一由劳动部门管理",
            "workbench/ocr/paddle_ocr/下/part01/page_0247.txt:6 PaddleOCR 作统一由劳动部门管理",
        ],
    },
    {
        "old": "农民业余教育委员会统一一使用。民校分扫盲班",
        "new": "农民业余教育委员会统一使用。民校分扫盲班",
        "section": "农民教育段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0397.txt:13 raw 作统一一使用",
            "workbench/ocr/paddle_ocr/下/part01/page_0397.txt:13 PaddleOCR 作统一使用",
        ],
    },
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for change in CHANGES:
        count = html.count(change["old"])
        if count != 1:
            raise RuntimeError(f"expected one hit for {change['section']}, found {count}: {change['old']}")
        html = html.replace(change["old"], change["new"])
        applied.append({**change, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "note": "只修 raw OCR 与页级 PaddleOCR 对照闭合的 `统一一` 残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第二十六批：统一一残留短片段",
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
        "- 只修主阅读版；不改中间 OCR 原文。",
        "- 未全局替换全部 `统一一`；药房段、政协标题等未取得本批同等强证据或需另行判断的项继续暂缓。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Twenty-fifth batch: PaddleOCR-backed material, finance, and labor fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch25_material_finance_labor_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch25_material_finance_labor_20260706.json"

CHANGES = [
    {
        "old": "同年东辛农场砖瓦广、赣榆县砖瓦厂成立",
        "new": "同年东辛农场砖瓦厂、赣榆县砖瓦厂成立",
        "section": "建材工业砖瓦段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0271.txt:28-29 raw 作砖瓦广",
            "workbench/ocr/paddle_ocr/中/part01/page_0271.txt:29-30 PaddleOCR 作砖瓦厂",
        ],
    },
    {
        "old": "东海县砖瓦厂广、东海曲阳砖瓦厂",
        "new": "东海县砖瓦厂、东海曲阳砖瓦厂",
        "section": "建材工业砖瓦段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0271.txt:29 raw 作砖瓦厂广",
            "workbench/ocr/paddle_ocr/中/part01/page_0271.txt:30 PaddleOCR 作砖瓦厂",
        ],
    },
    {
        "old": "灌云龙苴砖广、云台胜利砖瓦厂",
        "new": "灌云龙苴砖厂、云台胜利砖瓦厂",
        "section": "建材工业砖瓦段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0271.txt:29-30 raw 作砖广",
            "workbench/ocr/paddle_ocr/中/part01/page_0271.txt:30-31 PaddleOCR 作砖厂",
        ],
    },
    {
        "old": "市制砖厂新建-座36门轮窑",
        "new": "市制砖厂新建一座36门轮窑",
        "section": "建材工业砖瓦段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0272.txt:20 raw 作新建-座",
            "workbench/ocr/paddle_ocr/中/part01/page_0272.txt:20 PaddleOCR 作新建一座",
        ],
    },
    {
        "old": "有32门轮窑-座)划出单独核算",
        "new": "有32门轮窑一座)划出单独核算",
        "section": "建材工业砖瓦段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0272.txt:23 raw 作轮窑-座",
            "workbench/ocr/paddle_ocr/中/part01/page_0272.txt:23 PaddleOCR 作轮窑一座",
        ],
    },
    {
        "old": "1977年秋，新海电广为充分利用粉煤灰",
        "new": "1977年秋，新海电厂为充分利用粉煤灰",
        "section": "建材工业粉煤灰砖段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0273.txt:3 raw 作新海电广",
            "workbench/ocr/paddle_ocr/中/part01/page_0273.txt:3 PaddleOCR 作新海电厂",
        ],
    },
    {
        "old": "青岛人毛方培带21人到新浦西临洪滩办窑广",
        "new": "青岛人毛方培带21人到新浦西临洪滩办窑厂",
        "section": "建材工业瓦段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0273.txt:27 raw 作办窑广",
            "workbench/ocr/paddle_ocr/中/part01/page_0273.txt:28 PaddleOCR 作办窑厂",
        ],
    },
    {
        "old": "容量为5000片瓦坏的晾瓦房",
        "new": "容量为5000片瓦坯的晾瓦房",
        "section": "建材工业瓦段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0273.txt:34 raw 作瓦坏",
            "workbench/ocr/paddle_ocr/中/part01/page_0273.txt:35 PaddleOCR 作瓦坯",
        ],
    },
    {
        "old": "瓦的生产量提高倍。1955年产量达27.6万片",
        "new": "瓦的生产量提高一倍。1955年产量达27.6万片",
        "section": "建材工业瓦段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0273.txt:35 raw 漏一字",
            "workbench/ocr/paddle_ocr/中/part01/page_0273.txt:35 PaddleOCR 作提高一倍",
        ],
    },
    {
        "old": "顺水条上苦普通粘土红平瓦",
        "new": "顺水条上苫普通粘土红平瓦",
        "section": "建筑业工业建筑段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0303.txt:36 raw 作苦普通",
            "workbench/ocr/paddle_ocr/中/part01/page_0303.txt:37 PaddleOCR 作苫普通",
        ],
    },
    {
        "old": "隆丰面粉厂广因经理韩福全系历史反革命",
        "new": "隆丰面粉厂因经理韩福全系历史反革命",
        "section": "粮食加工面粉段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0253.txt:10 raw 作面粉厂广因",
            "workbench/ocr/paddle_ocr/中/part02/page_0253.txt:10 PaddleOCR 作面粉厂因",
        ],
    },
    {
        "old": "实行“统一一计划,综合平衡，条块结合，分级管理”的体制",
        "new": "实行“统一计划，综合平衡，条块结合，分级管理”的体制",
        "section": "物资流通管理体制段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0264.txt:32 raw 作统一一计划,综合平衡",
            "workbench/ocr/paddle_ocr/中/part02/page_0264.txt:31 PaddleOCR 作统一计划，综合平衡",
        ],
    },
    {
        "old": "贷款管理实行“统一一计划，分级管理，余额控制”",
        "new": "贷款管理实行“统一计划，分级管理，余额控制”",
        "section": "金融建筑业贷款段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0369.txt:7 raw 作统一一计划",
            "workbench/ocr/paddle_ocr/中/part02/page_0369.txt:7 PaddleOCR 作统一计划",
        ],
    },
    {
        "old": "坚持“保证重点，兼顾一一般，择优扶持”的原则",
        "new": "坚持“保证重点，兼顾一般，择优扶持”的原则",
        "section": "金融建筑业贷款段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0369.txt:8 raw 作一一般",
            "workbench/ocr/paddle_ocr/中/part02/page_0369.txt:8 PaddleOCR 作一般",
        ],
    },
    {
        "old": "培训主要开设（劳动就业指导》、《法律常识》、《职业道德》3门公共课，培训时间-一一般为1530天",
        "new": "培训主要开设《劳动就业指导》、《法律常识》、《职业道德》3门公共课，培训时间一般为15~30天",
        "section": "劳动就业指导培训段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0253.txt:36-37 raw 作括号/时间错识",
            "workbench/ocr/paddle_ocr/下/part01/page_0253.txt:36-37 PaddleOCR 作《劳动就业指导》与15~30天",
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
        "note": "只修 raw OCR 与页级 PaddleOCR 对照闭合的建材、物资、金融、劳动短片段。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第二十五批：建材、物资、金融与劳动短片段",
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
        "- 未批量替换全部 `广/厂`、`一一般/一般`、`统一一/统一`，只处理本批已回源闭合项。",
        "- `新海发电厂广泛开展安全教育` 为正常词组，本批不处理；人大视察段仍待更强页级证据。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

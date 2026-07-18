# -*- coding: utf-8 -*-
"""Twenty-third batch: PaddleOCR-backed education, port, and building-material fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch23_education_industry_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch23_education_industry_20260706.json"

CHANGES = [
    {
        "old": "在编写连云港口岸出口商品目录归类表的基础上，文编写了《填报进出口货物报关注意事项》",
        "new": "在编写连云港口岸出口商品目录归类表的基础上，又编写了《填报进出口货物报关注意事项》",
        "section": "口岸海关统计段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0504.txt:41 raw 作文编写",
            "workbench/ocr/paddle_ocr/中/part01/page_0504.txt:41 PaddleOCR 作又编写",
        ],
    },
    {
        "old": "结束了人工摔坏历史",
        "new": "结束了人工摔坯历史",
        "section": "建材工业砖瓦段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0272.txt:7 raw 作摔坏",
            "workbench/ocr/paddle_ocr/中/part01/page_0272.txt:7 PaddleOCR 作摔坯",
        ],
    },
    {
        "old": "除新浦港区外，海州区胸阳乡化肥厂一线有7个装卸作业点",
        "new": "除新浦港区外，海州区朐阳乡化肥厂一线有7个装卸作业点",
        "section": "交通运输港务段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0048.txt:22 raw 作胸阳乡",
            "workbench/ocr/paddle_ocr/中/part02/page_0048.txt:22 PaddleOCR 作朐阳乡",
        ],
    },
    {
        "old": "1959～1961年市技工学校对人学学生的文化程度仅要求高小毕业",
        "new": "1959～1961年市技工学校对入学学生的文化程度仅要求高小毕业",
        "section": "技工学校学制段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0252.txt:5 raw 作人学学生",
            "workbench/ocr/paddle_ocr/下/part01/page_0252.txt:5 PaddleOCR 作入学学生",
        ],
    },
    {
        "old": "招收5周岁半至6周岁幼儿人学，学制1年",
        "new": "招收5周岁半至6周岁幼儿入学，学制1年",
        "section": "学前班段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0354.txt:23 raw 作幼儿人学",
            "workbench/ocr/paddle_ocr/下/part01/page_0354.txt:23 PaddleOCR 作幼儿入学",
        ],
    },
    {
        "old": "将学前班工作纳学校计划",
        "new": "将学前班工作纳入学校计划",
        "section": "学前班段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0354.txt:26 raw 漏入字",
            "workbench/ocr/paddle_ocr/下/part01/page_0354.txt:26 PaddleOCR 作纳入学校计划",
        ],
    },
    {
        "old": "1975年，东海县聋业学校开办",
        "new": "1975年，东海县聋哑学校开办",
        "section": "初等教育发展段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0355.txt:12 raw 作聋业学校",
            "workbench/ocr/paddle_ocr/下/part01/page_0355.txt:12 PaddleOCR 作聋哑学校",
        ],
    },
    {
        "old": "安排残疾儿童人学",
        "new": "安排残疾儿童入学",
        "section": "初等教育发展段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0355.txt:14 raw 作残疾儿童人学",
            "workbench/ocr/paddle_ocr/下/part01/page_0355.txt:14 PaddleOCR 作残疾儿童入学",
        ],
    },
    {
        "old": "高级小学增设职业准备学科。儿童6岁人学。民国35年至37年",
        "new": "高级小学增设职业准备学科。儿童6岁入学。民国35年至37年",
        "section": "小学学制段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0365.txt:93 raw 作儿童6岁人学",
            "workbench/ocr/paddle_ocr/下/part01/page_0365.txt:93 PaddleOCR 作儿童6岁入学",
        ],
    },
    {
        "old": "小学人学年龄市区为6周岁半，三县为7周岁",
        "new": "小学入学年龄市区为6周岁半，三县为7周岁",
        "section": "小学学制段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0365.txt:98 raw 作小学人学年龄",
            "workbench/ocr/paddle_ocr/下/part01/page_0365.txt:98 PaddleOCR 作小学入学年龄",
        ],
    },
    {
        "old": "师范生人学即教育其热爱教育事业",
        "new": "师范生入学即教育其热爱教育事业",
        "section": "师范学校思想政治教育段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0388.txt:31 raw 作师范生人学",
            "workbench/ocr/paddle_ocr/下/part01/page_0388.txt:31 PaddleOCR 作师范生入学",
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
        "note": "只修 raw OCR 与页级 PaddleOCR 对照闭合的教育、口岸、交通和建材短片段。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第二十三批：教育、口岸、交通与建材短片段",
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
        "- 未批量替换全部 `人学/入学`、`胸阳/朐阳`、`文/又`，只处理本批已回源闭合项。",
        "- 小学学制首处 `儿童6岁人学` 因 raw/PaddleOCR 同作 `人学`，本批暂不凭类推改写。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Twenty-second batch: PaddleOCR-backed industry, port, and education fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch22_industry_education_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch22_industry_education_20260706.json"

CHANGES = [
    {
        "old": "编印了连云港口岸出口商品自录归类表",
        "new": "编印了连云港口岸出口商品目录归类表",
        "section": "口岸海关统计段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0504.txt:35 raw 作自录归类表",
            "workbench/ocr/paddle_ocr/中/part01/page_0504.txt:35 PaddleOCR 作目录归类表",
        ],
    },
    {
        "old": "对每届学生进行人学教育，增强其专业责任感",
        "new": "对每届学生进行入学教育，增强其专业责任感",
        "section": "中等专业学校思想教育段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0386.txt:18 raw 作人学教育",
            "workbench/ocr/paddle_ocr/下/part01/page_0386.txt:16 PaddleOCR 作入学教育",
        ],
    },
    {
        "old": "全县应人学聋儿童100人",
        "new": "全县应入学聋哑儿童100人",
        "section": "残疾人调查段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0038.txt:33 raw 作应人学聋儿童",
            "workbench/ocr/paddle_ocr/下/part01/page_0038.txt:33 PaddleOCR 作应入学聋哑儿童",
        ],
    },
    {
        "old": "东海县砖瓦广在西双湖西北角新建一座32门轮窑",
        "new": "东海县砖瓦厂在西双湖西北角新建一座32门轮窑",
        "section": "建材工业砖瓦段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0272.txt:13 raw 作砖瓦广",
            "workbench/ocr/paddle_ocr/中/part01/page_0272.txt:13 PaddleOCR 作砖瓦厂",
        ],
    },
    {
        "old": "有的乡镇还建了第二、第三砖瓦广",
        "new": "有的乡镇还建了第二、第三砖瓦厂",
        "section": "建材工业砖瓦段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0272.txt:19 raw 作砖瓦广",
            "workbench/ocr/paddle_ocr/中/part01/page_0272.txt:19 PaddleOCR 作砖瓦厂",
        ],
    },
    {
        "old": "扩建煤渣砖广。新海电厂投资90万元建一条粉煤灰砖生产线",
        "new": "扩建煤渣砖厂。新海电厂投资90万元建一条粉煤灰砖生产线",
        "section": "建材工业粉煤灰砖段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0273.txt:6 raw 作煤渣砖广",
            "workbench/ocr/paddle_ocr/中/part01/page_0273.txt:7 PaddleOCR 作煤渣砖厂",
        ],
    },
    {
        "old": "同年，炉渣砖广更名为连云港市节能建材厂",
        "new": "同年，炉渣砖厂更名为连云港市节能建材厂",
        "section": "建材工业粉煤灰砖段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0273.txt:9 raw 作炉渣砖广",
            "workbench/ocr/paddle_ocr/中/part01/page_0273.txt:10 PaddleOCR 作炉渣砖厂",
        ],
    },
    {
        "old": "该广研制生产的各种异型、弧型轻质耐火保温砖，年产量100方块",
        "new": "该厂研制生产的各种异型、弧型轻质耐火保温砖，年产量100万块",
        "section": "建材工业粉煤灰砖段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0273.txt:13 raw 作该广、100方块",
            "workbench/ocr/paddle_ocr/中/part01/page_0273.txt:14 PaddleOCR 作该厂、100万块",
        ],
    },
    {
        "old": "1975年春开工，1976年12月工的连云港纺织厂25000纱绽厂房位于",
        "new": "1975年春开工，1976年12月竣工的连云港纺织厂25000纱绽厂房位于",
        "section": "建筑业工业建筑段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0302.txt:30 raw 漏竣字作12月工",
            "workbench/ocr/paddle_ocr/中/part01/page_0302.txt:29 PaddleOCR 作12月竣工",
        ],
    },
    {
        "old": "1987年3月开工，1989年11月工的灌云棉纺织厂广房位于",
        "new": "1987年3月开工，1989年11月竣工的灌云棉纺织厂厂房位于",
        "section": "建筑业工业建筑段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0303.txt:34-35 raw 作11月工、厂广房",
            "workbench/ocr/paddle_ocr/中/part01/page_0303.txt:34-35 PaddleOCR 作11月竣工、厂房",
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
        "note": "只修 raw OCR 与页级 PaddleOCR 对照闭合的工业、口岸和教育短片段。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第二十二批：工业、口岸与教育短片段",
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
        "- 不批量替换全部 `广/厂`、`人学/入学`、`自录/目录`，只处理本批已回源闭合项。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

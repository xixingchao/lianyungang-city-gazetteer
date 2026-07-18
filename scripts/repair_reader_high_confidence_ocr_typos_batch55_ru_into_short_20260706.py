# -*- coding: utf-8 -*-
"""Batch 55: verified 人/入 OCR residue fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch55_ru_into_short_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch55_ru_into_short_20260706.json"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第五十五批_入字短片段.md"

CHANGES = [
    {
        "old": "自愿集资人股兴办",
        "new": "自愿集资入股兴办",
        "section": "供销合作社性质段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part02/page_0159.txt:17 作集资入股兴办",
            "workbench/ocr/raw/中/part02/page_0159.txt:18 为集资人股兴办残留",
        ],
    },
    {
        "old": "人股社员91人",
        "new": "入股社员91人",
        "section": "灌云县钱庄合作社段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part02/page_0159.txt:24 作入股社员91人",
            "output/final_reader/连云港市志_全书.html 原文为人股社员91人残留",
        ],
    },
    {
        "old": "人股，每股12.5公斤黄豆",
        "new": "入股，每股12.5公斤黄豆",
        "section": "四队乡试办供销合作社段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part02/page_0159.txt:35 作入股，每股12.5公斤黄豆",
            "output/final_reader/连云港市志_全书.html 原文为人股残留",
        ],
    },
    {
        "old": "社员人股金额",
        "new": "社员入股金额",
        "section": "供销社股金红利段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part02/page_0161.txt:37 作社员入股金额",
            "workbench/ocr/raw/中/part02/page_0161.txt:36 为社员人股金额残留",
        ],
    },
    {
        "old": "并人固定资产更新和技术改造资金",
        "new": "并入固定资产更新和技术改造资金",
        "section": "财政四项费用调整段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part02/page_0302.txt:6 作并入固定资产更新和技术改造资金",
            "workbench/ocr/raw/中/part02/page_0302.txt:6 为并人固定资产更新残留",
        ],
    },
    {
        "old": "新产品试制费并人科学技术三项费用中",
        "new": "新产品试制费并入科学技术三项费用中",
        "section": "财政四项费用调整段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part02/page_0302.txt:6 作新产品试制费并入科...",
            "workbench/ocr/raw/中/part02/page_0302.txt:6 为新产品试制费并人科...残留",
        ],
    },
    {
        "old": "路南东海县撤销，并人沭阳县",
        "new": "路南东海县撤销，并入沭阳县",
        "section": "华中银行东海办事处段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part02/page_0346.txt:16-17 作并入沭阳县",
            "workbench/ocr/raw/中/part02/page_0346.txt:14 为并人残留",
        ],
    },
    {
        "old": "潼阳并人东海时",
        "new": "潼阳并入东海时",
        "section": "中共东海县党组织段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part02/page_0404.txt:35 作潼阳并入东海时",
            "output/final_reader/连云港市志_全书.html 原文为潼阳并人东海时残留",
        ],
    },
    {
        "old": "潼阳县并人东海县",
        "new": "潼阳县并入东海县",
        "section": "抗日根据地民主政府段",
        "evidence": [
            "workbench/ocr/paddle_ocr/中/part02/page_0480.txt:33 作潼阳县并入东海县",
            "output/final_reader/连云港市志_全书.html 原文为潼阳县并人东海县残留",
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
        "note": "只修 PaddleOCR/raw OCR 对照闭合、旧串唯一命中的人/入短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第五十五批：入字短片段",
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
        "- 公安、法院、教育等其他 `并人` 残留若缺少同页 PaddleOCR 直接支撑，本批不处理。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS_MD.write_text(text, encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")
    print(f"progress={PROGRESS_MD}")


if __name__ == "__main__":
    main()

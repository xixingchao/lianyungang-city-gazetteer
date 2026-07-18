# -*- coding: utf-8 -*-
"""Twenty-ninth batch: PaddleOCR-backed industry, education, religion, bio fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch29_industry_education_religion_bio_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch29_industry_education_religion_bio_20260706.json"

CHANGES = [
    {
        "old": "这是一项自动控制多，自动点安装的设备。" ,
        "new": "这是一项自动控制多，自动化程度很高的全新中外合资的工程。垂直部分采用倒装法，解决了超大超高且在特殊地点安装的设备。", 
        "section": "建筑业成套设备安装段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0320.txt:37 raw 可见安装段误识来源",
            "workbench/ocr/paddle_ocr/中/part01/page_0321.txt:4-7 给出自动化程度与倒装法完整句",
        ],
    },
    {
        "old": "1953年，新海发电厂广泛开展安全教育，制定防范措施，组织广大职工开展安全无事</p>",
        "new": "1953年，新海发电厂广泛开展安全教育，制定防范措施，组织广大职工开展安全无事故红旗竞赛活动。</p>",
        "section": "电力工业安全监察措施段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0363.txt:109 raw 断于安全无事",
            "workbench/ocr/paddle_ocr/中/part01/page_0363.txt:41 与 page_0364.txt:4 作安全无事故红旗竞赛活动",
        ],
    },
    {
        "old": "中小学人学新生过多",
        "new": "中小学入学新生过多",
        "section": "教师队伍段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0402.txt:18 raw 作新生过多；主阅读版残留人学新生",
            "workbench/ocr/paddle_ocr/下/part01/page_0402.txt:16-17 作中小学入学新生过多",
        ],
    },
    {
        "old": "应召人至真观，后人天台山",
        "new": "应召入至真观，后入天台山",
        "section": "道教活动段",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0263.txt:30 raw 作后人天台山",
            "workbench/ocr/paddle_ocr/下/part02/page_0263.txt:28-29 作应召入至真观，后入天台山",
        ],
    },
    {
        "old": "道土道善于教育儿童",
        "new": "道士吴道善于教育儿童",
        "section": "道教活动段",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0263.txt:31 raw 作道土道善于教育儿童",
            "workbench/ocr/paddle_ocr/下/part02/page_0263.txt:29 作道士吴道善于教育儿童",
        ],
    },
    {
        "old": "分配至内蒙古伊克昭盟千部业余大学工作。1973年加入中国共产党。",
        "new": "分配至内蒙古伊克昭盟干部业余大学工作。1973年加入中国共产党。",
        "section": "周维先简介段",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0397.txt:19 raw 作千部业余大学、加人中国共产党",
            "workbench/ocr/paddle_ocr/下/part02/page_0397.txt:16-17 作干部业余大学、加入中国共产党",
        ],
    },
    {
        "old": "为了使千部和群众迅速取得经验",
        "new": "为了使干部和群众迅速取得经验",
        "section": "附录大社的优越性按语段",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0414.txt:13 raw 作千部和群众",
            "workbench/ocr/paddle_ocr/下/part02/page_0414.txt:13 作干部和群众",
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
        "note": "只修 raw/PaddleOCR 可闭合的工业、教育、宗教、人物和附录短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第二十九批：工业、教育、宗教与人物短片段",
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
        "- 未全局替换 `人/入`、`千部/干部`、`道土/道士` 等模式。",
        "- 公安查禁卖淫段、医学术语和人大视察段仍缺本批同等强证据，本批暂缓。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

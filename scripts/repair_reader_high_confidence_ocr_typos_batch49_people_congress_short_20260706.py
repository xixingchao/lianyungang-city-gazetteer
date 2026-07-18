# -*- coding: utf-8 -*-
"""Batch 49: verified people congress short OCR fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch49_people_congress_short_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch49_people_congress_short_20260706.json"

CHANGES = [
    {
        "old": "1985年4月15~221986年6月9~14日，市人大常委、市人大代表和政府有关部门负责人",
        "new": "1985年4月15~22日，组织市区人大代表对全市贯彻《水污染防治法》实施情况视察。1986年6月9~14日，市人大常委、市人大代表和政府有关部门负责人",
        "section": "人大视察日期断裂段",
        "evidence": ["workbench/ocr/tesseract_check/zhong_part02_page_0516.txt:18-20 作1985年4月15~22日，组织市区人大代表对全市贯彻《水污染防治法》实施情况视察。1986年6月9~14日..."],
    },
    {
        "old": "实地考究薇河、玉带河、西盐河、龙尾河、大浦河和茅口水厂水质情况",
        "new": "实地考究蔷薇河、玉带河、西盐河、龙尾河、大浦河和茅口水厂水质情况",
        "section": "人大环保视察河流名称段",
        "evidence": ["workbench/ocr/tesseract_check/zhong_part02_page_0516.txt:25-26 作实地考究蔷薇河、玉带河、西盐河、龙尾河、大浦河和茅口水厂水质情况"],
    },
    {
        "old": "新海发电广、市第一人民医院",
        "new": "新海发电厂、市第一人民医院",
        "section": "人大环保视察单位名称段",
        "evidence": ["workbench/ocr/tesseract_check/zhong_part02_page_0516.txt:27 作新海发电厂、市第一人民医院"],
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
        "note": "只修 Tesseract 本地 OCR 闭合且旧串唯一命中的人大视察短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第四十九批：人大视察短片段",
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
        "- `考究评议`、`实地考究` 两套 OCR 仍同样识别，本批不猜改。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

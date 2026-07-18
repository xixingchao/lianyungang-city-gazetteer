# -*- coding: utf-8 -*-
"""Repair source-backed modern duplicate punctuation residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "上" / "第三卷_区县概况.md",
    ROOT / "workbench" / "body_chapters" / "paddle_上" / "第三卷_区县概况.md",
    ROOT / "workbench" / "body_chapters" / "paddle_上" / "第四卷至第十卷（part02）.md",
    ROOT / "workbench" / "body_chapters" / "paddle_上" / "第十卷至第十六卷（part03）.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_PaddleOCR正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_modern_duplicate_punctuation_batch89_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_modern_duplicate_punctuation_batch89_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第八十九批_现代正文重复标点.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "东海教育幼儿园双逗号",
        "old": "1985年，，全县共办幼儿园",
        "new": "1985年，全县共办幼儿园",
        "source": "workbench/ocr/paddle_ocr/上/part01/page_0269.txt:30",
    },
    {
        "label": "商业网点从业数双逗号",
        "old": "服务业网点5889人，从业19047人，，社会商品零售额11275万元",
        "new": "服务业网点5889人，从业19047人，社会商品零售额11275万元",
        "source": "workbench/ocr/paddle_ocr/上/part02/page_0140.txt:17",
    },
    {
        "label": "商业网点从业数双逗号源稿断行",
        "old": "5889人，从业19047人，，社会商品零售额11275万元",
        "new": "5889人，从业19047人，社会商品零售额11275万元",
        "source": "workbench/ocr/paddle_ocr/上/part02/page_0140.txt:17",
    },
    {
        "label": "白塔地涵实灌双逗号",
        "old": "设计灌田20万亩，，实灌6万亩",
        "new": "设计灌田20万亩，实灌6万亩",
        "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:4002",
    },
    {
        "label": "甘露醇产量句点逗号残留",
        "old": "以提高产品质量。.1984年，，全市实产甘露醇",
        "new": "以提高产品质量。1984年，全市实产甘露醇",
        "source": "output/final_reader/连云港市志_全书.html:9223",
    },
    {
        "label": "化肥厂设备清单双逗号",
        "old": "Dg1600、H=6000毫米低温变换炉1台，，Dg1600、H=9850毫米碳化塔6座",
        "new": "Dg1600、H=6000毫米低温变换炉1台，Dg1600、H=9850毫米碳化塔6座",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0174.txt:30",
    },
    {
        "label": "化肥厂设备清单双逗号源稿断行",
        "old": "Dg1600、H=6000毫米低温变换炉1台，，Dg1600、H\n=9850毫米碳化塔6座",
        "new": "Dg1600、H=6000毫米低温变换炉1台，Dg1600、H\n=9850毫米碳化塔6座",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0174.txt:30",
    },
    {
        "label": "外轮服务远洋船双逗号",
        "old": "远洋船，，开展这些业务",
        "new": "远洋船，开展这些业务",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0486.txt:156",
    },
    {
        "label": "盐区委双逗号",
        "old": "建立中共盐区委，，6月份为中共陈港区委",
        "new": "建立中共盐区委，6月份为中共陈港区委",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0457.txt:29",
    },
    {
        "label": "农工党考察乡镇顿号重复",
        "old": "到东海县山左口、、桃林等乡镇实地考察",
        "new": "到东海县山左口、桃林等乡镇实地考察",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0473.txt:19",
    },
    {
        "label": "经济审判红枣案双逗号",
        "old": "热气呛人，，立即采取保全措施",
        "new": "热气呛人，立即采取保全措施",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0132.txt:17",
    },
    {
        "label": "化工研究所职工数双逗号",
        "old": "1990年，有职工30人，，其中科技人员26人",
        "new": "1990年，有职工30人，其中科技人员26人",
        "source": "output/final_reader/连云港市志_全书.html:21235",
    },
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {target}: {residuals[:3]}")
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "Modern narrative duplicate punctuation residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_total": sum(target["changed"] for target in applied),
        "targets": applied,
        "principle": "Only exact modern narrative contexts are changed; quoted ellipsis-like punctuation and old-text contexts are excluded.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第八十九批：现代正文重复标点",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的现代叙述重复标点残留。",
        "- 只处理精确短语；不处理盐政引文省略号、旧志序文、乡土文存等古文或异文风险段。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次实际替换：{payload['changed_total']} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}: `{item['old']}` -> `{item['new']}`；源/定位：`{item['source']}`")
    lines.extend([
        "",
        "## 未处理边界",
        "",
        "- 民国盐政引文中的 `。。。。。` 形态未处理，避免误改原引文省略。",
        "- 书末 `避选`、`用破万人心`、`上尽，然长逝`，以及乡土文存/旧志序文疑点继续等待更强证据。",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-06 高置信 OCR 错字补修第八十九批：现代正文重复标点

- 清理当前主阅读版和对应正文源稿/汇总中的现代叙述重复标点残留，范围包括 `1985年，，全县`、`从业19047人，，社会商品`、`远洋船，，开展`、`山左口、、桃林` 等精确短语。
- 本批证据短语 {len(REPLACEMENTS)} 项，实际替换 {payload['changed_total']} 处；报告：`output/reports/reader_modern_duplicate_punctuation_batch89_20260706.md`。
- 边界：不处理盐政引文 `。。。。。`、书末硬点、乡土文存和旧志序文疑点；未展示、未嵌入图片。
"""
    upsert_memory(MEMORY, "## 2026-07-06 高置信 OCR 错字补修第八十九批：现代正文重复标点", memory)
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_total": payload["changed_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

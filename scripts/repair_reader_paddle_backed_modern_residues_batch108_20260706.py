# -*- coding: utf-8 -*-
"""Repair narrowly Paddle-backed modern residues, batch 108."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch108_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch108_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_现代正文残留回源补修第一百零八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "九三学社第一届委员会",
        "old": "九三学社连云港市第一一届委员会委员",
        "new": "九三学社连云港市第一届委员会委员",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0474.txt:25；raw 同页误作第一一届",
    },
    {
        "label": "供给制向工资制第一步",
        "old": "这是供给制向工资制过渡的第一一步",
        "new": "这是供给制向工资制过渡的第一步",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0258.txt:13",
    },
    {
        "label": "生产任务大包干制度",
        "old": "如实行生产任务“小包干”、“大包于”制度",
        "new": "如实行生产任务“小包干”、“大包干”制度",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0261.txt:17",
    },
    {
        "label": "水利建设大包干配套措施",
        "old": "削减和“大包于”配套措施未及时跟上",
        "new": "削减和“大包干”配套措施未及时跟上",
        "source": "workbench/ocr/paddle_ocr/上/part03/page_0046.txt:11；raw 同页误作大包于",
    },
    {
        "label": "东亚旅社挟妓赌博",
        "old": "并在新浦东亚旅社妓赌博，还霸占新浦新新舞台女伶花艳舫",
        "new": "并在新浦东亚旅社挟妓赌博，还霸占新浦新新舞台女伶花艳舫",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0359.txt:8；raw 缺挟字",
    },
]

LEFT_UNTOUCHED = [
    "`中西合壁` 四处 raw 与 Paddle 均作壁，虽疑似应为合璧，本批不凭常识改。",
    "`并人徐州第四监狱` raw 与 Paddle 均同读为并人，本批保留。",
    "`进人/收人/投人/深人` 等未做全局替换，只处理页级证据闭合项。",
    "本批未使用或展示页图。",
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
        for item in items:
            item["verified"] = verify.count(item["new"])
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "Paddle OCR-backed modern residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact contexts with Paddle OCR evidence are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 现代正文残留补修第一百零八批：PaddleOCR 回源",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的现代正文残留。",
        "- 仅处理 raw 与当前正文残留、Paddle 页级文本给出更正的精确短语。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次运行新增替换：{payload['changed_this_run']} 处",
        f"- 当前核验覆盖：{payload['verified_total']} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}: `{item['old']}` -> `{item['new']}`；源/定位：`{item['source']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百零八批：现代正文残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做 PaddleOCR 页级回源，修复 `九三学社连云港市第一一届委员会委员`、供给制向工资制 `第一一步`、工资制度 `大包于`、水利建设 `大包于`、东亚旅社 `妓赌博` 缺字等现代正文残留。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_modern_residues_batch108_20260706.md`。
- 边界：`中西合壁` 与 `并人徐州第四监狱` 因 raw/Paddle 未给出更强证据，暂不凭常识改；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

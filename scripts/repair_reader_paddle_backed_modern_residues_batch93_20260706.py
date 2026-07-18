# -*- coding: utf-8 -*-
"""Repair narrowly source-backed modern prose residues, batch 93."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "上" / "总述与大事记.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第三卷_区县概况.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch93_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch93_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_现代正文残留Paddle回源补修第九十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "总述标准海岸线",
        "old": "连云港市海岸类型齐全，标淮海岸线长161.6公里",
        "new": "连云港市海岸类型齐全，标准海岸线长161.6公里",
        "source": "workbench/ocr/paddle_ocr/上/part01/page_0029.txt:17; raw same page also reads 标准海岸线",
    },
    {
        "label": "自然环境标准海岸线",
        "old": "连云港市海岸类型齐全，标淮海岸线长161.58公里",
        "new": "连云港市海岸类型齐全，标准海岸线长161.58公里",
        "source": "workbench/ocr/paddle_ocr/上/part01/page_0124.txt:21 and raw same page read 标准海岸线",
    },
    {
        "label": "表1-2标准海岸线表头",
        "old": "标淮海岸线(公里)",
        "new": "标准海岸线(公里)",
        "source": "workbench/ocr/paddle_ocr/上/part01/page_0145.txt:30 and raw same page read 标准海岸线",
    },
    {
        "label": "总述商贸增长倍数句号残留 HTML",
        "old": "增长4.41。倍",
        "new": "增长4.41倍",
        "source": "workbench/ocr/paddle_ocr/上/part01/page_0036.txt:13 reads 4.41.倍; numeric phrase requires no separator before 倍",
    },
    {
        "label": "总述商贸增长倍数点号残留源稿",
        "old": "增长4.41.倍",
        "new": "增长4.41倍",
        "source": "workbench/ocr/paddle_ocr/上/part01/page_0036.txt:13; same context",
    },
    {
        "label": "东海县供水干线",
        "old": "供水于线总长20.25公里",
        "new": "供水干线总长20.25公里",
        "source": "workbench/ocr/merged/连云港市志_上册_OCR汇总.md:15617 and current normalized chapter read 供水干线",
    },
]

LEFT_UNTOUCHED = [
    "`停泊3000～5000万吨货轮` 高度可疑，但 raw/Paddle 当前同读为 `万吨`，本批未猜改。",
    "书末序跋、乡土文存和古文段落中的疑似错字继续等待更强证据。",
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
        "scope": "Source-backed modern prose residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact modern prose contexts with direct source support are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 现代正文残留补修第九十三批：Paddle/原始 OCR 回源",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应上册源稿/汇总中的少量现代正文残留。",
        "- 只处理可由 PaddleOCR、raw OCR 或当前规范化正文闭合的精确短语。",
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第九十三批：现代正文残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做窄范围回源修复，处理总述/自然环境/表头 `标淮海岸线 -> 标准海岸线`、商贸段 `4.41。/4.41.倍 -> 4.41倍`、东海县概况 `供水于线 -> 供水干线`。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_modern_residues_batch93_20260706.md`。
- 边界：`停泊3000～5000万吨货轮` 虽可疑但 raw/Paddle 同读为 `万吨`，未猜改；书末序跋、乡土文存和古文段落继续等待更强证据；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

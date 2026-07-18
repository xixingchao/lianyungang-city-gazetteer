# -*- coding: utf-8 -*-
"""Repair narrowly source-backed modern prose residues, batch 99."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch99_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch99_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_现代正文残留Paddle回源补修第九十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "港口水电60年代末一直使用",
        "old": "建国后至60年代未，港口直使用该水库的水",
        "new": "建国后至60年代末，港口一直使用该水库的水",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0447.txt:25-26",
    },
    {
        "label": "大浦港一些有识之士",
        "old": "大浦遂为海州、新浦地区一一些有识之士所重视",
        "new": "大浦遂为海州、新浦地区一些有识之士所重视",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0442.txt:18-19",
    },
    {
        "label": "口岸推广电讯卫生检疫",
        "old": "原则上应推厂电讯卫生检疫",
        "new": "原则上应推广电讯卫生检疫",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0489.txt:22-23",
    },
    {
        "label": "远洋船舶一些特殊情况",
        "old": "对一一些特殊情况，连云港海关采用更为灵活的方法",
        "new": "对一些特殊情况，连云港海关采用更为灵活的方法",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0499.txt:28-29",
    },
    {
        "label": "电信推广长话简化操作法",
        "old": "市局推厂长话简化操作法",
        "new": "市局推广长话简化操作法",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0083.txt:26-27",
    },
]

LEFT_UNTOUCHED = [
    "文化、科技、工业段中剩余 `一一批`、`一一些`、`推厂` 等候选尚未定位到页级文本，不纳入本批。",
    "`日本80年代未期`、建筑施工两处 `70年代未` 等看似可疑，但本轮尚未找到足够强的页级证据，暂不改。",
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
        "scope": "Source-backed port, customs, and telecom OCR residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact contexts with Paddle OCR page evidence are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 现代正文残留补修第九十九批：Paddle 页级回源",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的港口、口岸、电信段 OCR 残留。",
        "- 只处理 PaddleOCR 页级文本能够闭合的精确短语。",
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第九十九批：港口口岸电信残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做 Paddle 页级回源，修复港口水电段 `60年代未/港口直使用`、大浦港 `一一些有识之士`、口岸 `推厂电讯卫生检疫`、海关 `一一些特殊情况`、电信 `推厂长话简化操作法`。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_modern_residues_batch99_20260706.md`。
- 边界：文化、科技、工业段若干相似候选尚未页级闭合，暂不批量改；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

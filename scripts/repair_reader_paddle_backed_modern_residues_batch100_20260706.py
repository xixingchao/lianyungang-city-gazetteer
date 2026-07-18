# -*- coding: utf-8 -*-
"""Repair narrowly source-backed modern prose residues, batch 100."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch100_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch100_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_现代正文残留Paddle回源补修第一百批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "硅微粉日本80年代末期产品水平",
        "old": "达到和超过日本80年代未期同等部分产品试销新加坡、日本等国家",
        "new": "达到和超过日本80年代末期同等产品水平。部分产品试销新加坡、日本等国家",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0261.txt:30-32",
    },
    {
        "label": "硅微粉日本80年代末期产品水平分行",
        "old": "达到和超过日本80年代未期同等\n部分产品试销新加坡、日本等国家",
        "new": "达到和超过日本80年代末期同等\n产品水平。部分产品试销新加坡、日本等国家",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0261.txt:30-32",
    },
    {
        "label": "硅微粉日本80年代末期分行前半句",
        "old": "达到和超过日本80年代未期同等",
        "new": "达到和超过日本80年代末期同等\n产品水平。",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0261.txt:30-32",
    },
    {
        "label": "建筑施工60年代初至70年代末",
        "old": "60年代初至70年代未，房屋建筑增至三四层",
        "new": "60年代初至70年代末，房屋建筑增至三四层",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0309.txt:5-6",
    },
    {
        "label": "建筑施工60年代初至70年代末分行",
        "old": "60年代初至70年代未，房\n屋建筑增至三四层",
        "new": "60年代初至70年代末，房\n屋建筑增至三四层",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0309.txt:5-6",
    },
    {
        "label": "建筑施工60年代初至70年代末分行前半句",
        "old": "60年代初至70年代未，房",
        "new": "60年代初至70年代末，房",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0309.txt:5-6",
    },
    {
        "label": "建筑施工预应力混凝土",
        "old": "先张法预应力混凝士中小型构件",
        "new": "先张法预应力混凝土中小型构件",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0309.txt:8-9",
    },
    {
        "label": "建筑施工70年代末至1990年",
        "old": "70年代未至1990年，民用住宅多为五六层",
        "new": "70年代末至1990年，民用住宅多为五六层",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0309.txt:9-10",
    },
    {
        "label": "建筑施工70年代末至1990年分行",
        "old": "70年代未至1990年，民用住宅多\n为五六层",
        "new": "70年代末至1990年，民用住宅多\n为五六层",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0309.txt:9-10",
    },
    {
        "label": "建筑施工70年代末至1990年前半句",
        "old": "70年代未至1990年，民用住宅多",
        "new": "70年代末至1990年，民用住宅多",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0309.txt:9-10",
    },
]

LEFT_UNTOUCHED = [
    "机电、文化、科技、司法等段中的相似 `一一批`、`一一些`、`推厂` 候选尚未页级闭合，暂不改。",
    "本批只修中册 part01 两个 Paddle 页能直接闭合的段落，不扩大到全局模式替换。",
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
        "scope": "Source-backed electronics and construction prose OCR residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact contexts with Paddle OCR page evidence are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 现代正文残留补修第一百批：Paddle 页级回源",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的电子材料、建筑施工段 OCR 残留。",
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百批：电子材料与建筑施工残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做 Paddle 页级回源，修复硅微粉段 `日本80年代未期同等部分产品` 为 `日本80年代末期同等产品水平。部分产品`，并修复建筑施工段 `70年代未`、`混凝士` 等残留。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_modern_residues_batch100_20260706.md`。
- 边界：剩余相似 OCR 噪声仍需逐页定位，不做全局替换；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

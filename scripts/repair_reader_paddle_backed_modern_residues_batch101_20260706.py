# -*- coding: utf-8 -*-
"""Repair narrowly source-backed modern prose residues, batch 101."""

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
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch101_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch101_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_现代正文残留Paddle回源补修第一百零一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "硅微粉复旦大学",
        "old": "该厂和复且大学、中科院化工研究所共同承担",
        "new": "该厂和复旦大学、中科院化工研究所共同承担",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0261.txt:18-19",
    },
    {
        "label": "硅微粉该厂生产",
        "old": "1987年11月，该广生产的普通硅微粉和活性硅微粉",
        "new": "1987年11月，该厂生产的普通硅微粉和活性硅微粉",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0261.txt:20",
    },
    {
        "label": "东海县硅微粉厂该厂",
        "old": "东海县硅微粉厂该广是生产硅微粉的专业工厂",
        "new": "东海县硅微粉厂该厂是生产硅微粉的专业工厂",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0263.txt:4-5",
    },
    {
        "label": "混凝土构件生产能力",
        "old": "形成年产2万立方米混凝士构件的能力",
        "new": "形成年产2万立方米混凝土构件的能力",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0284.txt:21-22",
    },
    {
        "label": "混凝土沉井支护",
        "old": "采用钢筋混凝士沉井支护的办法",
        "new": "采用钢筋混凝土沉井支护的办法",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0310.txt:21-22",
    },
    {
        "label": "混凝土沉井支护分行",
        "old": "混凝士沉井支护的办法",
        "new": "混凝土沉井支护的办法",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0310.txt:21-22",
    },
]

LEFT_UNTOUCHED = [
    "大量 `该广` 仍需逐条对应具体企业页核证，本批只处理已回源闭合的硅微粉段。",
    "下册科技文化段 `推厂`、`一一批`、`一一些` 本轮未找到足够强的页级文本，继续保留。",
    "上册桥梁 `混凝士` 已有线索但属于另一分册，暂不混入本批。",
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
        "scope": "Source-backed electronics and construction proper OCR residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact contexts with Paddle OCR page evidence are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 现代正文残留补修第一百零一批：Paddle 页级回源",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的硅微粉、建材与建筑施工段 OCR 残留。",
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百零一批：硅微粉与混凝土残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做 Paddle 页级回源，修复硅微粉段 `复且大学 -> 复旦大学`、`该广 -> 该厂`，以及建材/建筑施工段 `混凝士 -> 混凝土` 两处。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_modern_residues_batch101_20260706.md`。
- 边界：其余 `该广/推厂/一一批/一一些` 不做全局替换；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

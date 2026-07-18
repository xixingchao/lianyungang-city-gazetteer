# -*- coding: utf-8 -*-
"""Repair narrowly source-backed modern prose residues, batch 102."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch102_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch102_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_现代正文残留Paddle回源补修第一百零二批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "桥梁混凝土源稿残留",
        "old": "华北桥为3孔钢筋混凝士双曲拱桥",
        "new": "华北桥为3孔钢筋混凝土双曲拱桥",
        "source": "workbench/ocr/paddle_ocr/merged/连云港市志_上_part02_PaddleOCR汇总.md:4432",
    },
    {
        "label": "建筑工程研究所推广",
        "old": "建筑材料研究与推厂",
        "new": "建筑材料研究与推广",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0418.txt:3",
    },
    {
        "label": "双城糯推广",
        "old": "在苏皖诸地推厂",
        "new": "在苏皖诸地推广",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0437.txt:10",
    },
    {
        "label": "东海硅微粉厂",
        "old": "东海硅微粉广开发活性硅微粉系列产品",
        "new": "东海硅微粉厂开发活性硅微粉系列产品",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0446.txt:12-13",
    },
    {
        "label": "东海硅微粉厂断行",
        "old": "东海硅微粉广开发活性",
        "new": "东海硅微粉厂开发活性",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0446.txt:12-13",
    },
    {
        "label": "应用一些程序",
        "old": "应用了一一些程序",
        "new": "应用了一些程序",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0446.txt:14",
    },
    {
        "label": "电力系统推广",
        "old": "全省电力系统推厂",
        "new": "全省电力系统推广",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0446.txt:20-21",
    },
]

LEFT_UNTOUCHED = [
    "`调进一一批废旧机电产品`、`第一一批以市级`、`查处一一批贪污贿赂` 等在 raw OCR 中同样读作 `一一批`，本批没有足够强的页级反证，暂不改。",
    "用户贴出的旧转换压平段未按截图/图片复核；当前只按文字 OCR 路径与最终 HTML 做收口。",
    "大量 `该广` 仍需逐企业逐页闭合，本批不做全局替换。",
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
        "scope": "Source-backed bridge and lower-volume science prose OCR residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_this_run": sum(target["changed"] for target in applied),
        "verified_total": sum(item["verified"] for target in applied for item in target["items"]),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
        "principle": "Only exact contexts with Paddle OCR page evidence are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 现代正文残留补修第一百零二批：Paddle 页级回源",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应正文源稿/汇总中的桥梁、科技机构、农业推广、计算机应用段 OCR 残留。",
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百零二批：桥梁与科技推广残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按当前主交付 `output/final_reader/连云港市志_全书.html` 做 Paddle 页级回源，修复桥梁源稿 `混凝士 -> 混凝土`，下册科技机构/农业/计算机应用段 `推厂 -> 推广`、`硅微粉广 -> 硅微粉厂`、`一一些程序 -> 一些程序`。
- 本批证据短语 {len(REPLACEMENTS)} 项，当前核验覆盖 {payload['verified_total']} 处；报告：`output/reports/reader_paddle_backed_modern_residues_batch102_20260706.md`。
- 边界：`调进一一批废旧机电产品`、`第一一批以市级` 等只在 raw OCR 中同样可疑，未做猜改；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "verified_total": payload["verified_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

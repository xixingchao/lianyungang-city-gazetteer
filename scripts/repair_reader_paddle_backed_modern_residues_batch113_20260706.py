# -*- coding: utf-8 -*-
"""Repair narrowly source-backed OCR residues, batch 113."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "上" / "第一卷_自然环境.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch113_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_modern_residues_batch113_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_电力海关与工艺残留回源补修第一百一十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "工艺与自然景观栩栩如生",
        "old": "棚栩如生",
        "new": "栩栩如生",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0023.txt:12,19；workbench/ocr/paddle_ocr/上/part01/page_0140.txt:22",
    },
    {
        "label": "电力电压单位千伏",
        "old": "于伏",
        "new": "千伏",
        "source": "电力章同页/相邻页均为千伏单位；如 workbench/ocr/paddle_ocr/中/part01/page_0219.txt:31、page_0350.txt 等",
    },
    {
        "label": "平山变电所又一电源点",
        "old": "文一电源点",
        "new": "又一电源点",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0350.txt:17；raw 同页误作文一",
    },
    {
        "label": "海关出口商品目录归类表",
        "old": "出口商品自录归类表",
        "new": "出口商品目录归类表",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0504.txt:35；raw 同页误作自录",
    },
    {
        "label": "海关又编写报关注意事项",
        "old": "文编写了《填报进出口货物报关注意事项》",
        "new": "又编写了《填报进出口货物报关注意事项》",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0504.txt:41；raw 同页误作文编写",
    },
    {
        "label": "新海发电厂",
        "old": "新海发电广",
        "new": "新海发电厂",
        "source": "多页 Paddle 作新海发电厂，如 workbench/ocr/paddle_ocr/中/part01/page_0371.txt:9、下/part01/page_0441.txt:23",
    },
]

LEFT_UNTOUCHED = [
    "海关统计段 `对项目进行解除` 三套 OCR 均如此但语义可疑，继续等待更清晰页源或人工核验，不猜改。",
    "`准海/淮海` 系列暂不批量处理；电网上下文中部分疑似错字需另批逐页核验。",
    "本批不使用、不展示页图。",
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
        if not target.exists():
            continue
        text = target.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        for item in items:
            item["verified_new"] = verify.count(item["new"])
        applied.append({"target": str(target), "changed": sum(i["count"] for i in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "Paddle-backed repair for craft, customs statistics, and electrical unit residues",
        "patterns": len(REPLACEMENTS),
        "changed_this_run": sum(t["changed"] for t in applied),
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 电力海关与工艺残留补修第一百一十三批：Paddle 回源核对",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版、分册阅读版与正文源稿/汇总中的高置信 OCR 残留。",
        "- 仅处理 Paddle 同页或强单位上下文可闭合的 `棚栩/于伏/文一/自录/文编写/发电广` 等短语。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次替换：{payload['changed_this_run']} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        if target["changed"]:
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百一十三批：电力海关与工艺残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 继续按主阅读版和正文源稿做 Paddle 回源补修，处理工艺/自然景观 `棚栩如生 -> 栩栩如生`，电力章 `于伏 -> 千伏` 与 `文一电源点 -> 又一电源点`，海关统计页 `商品自录 -> 商品目录`、`文编写 -> 又编写`，以及 `新海发电广 -> 新海发电厂`。
- 本批证据短语 {len(REPLACEMENTS)} 项，报告：`output/reports/reader_paddle_backed_modern_residues_batch113_20260706.md`。
- 边界：海关统计段 `对项目进行解除` 三套 OCR 均如此但语义可疑，继续等待更清晰页源或人工核验；未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": payload["changed_this_run"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Repair Paddle-backed middle-reader area/money unit residues, batch 124."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_area_money_batch124_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_area_money_batch124_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_中册面积金额单位残字回源补修第一百二十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "徐福酒厂占地建筑面积",
        "old": "占地1.98方平方米，建筑面积1.9方平方米",
        "new": "占地1.98万平方米，建筑面积1.9万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0417.txt:23-24",
    },
    {
        "label": "徐福酒厂产值",
        "old": "1990年创产值500方元",
        "new": "1990年创产值500万元",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0417.txt:26",
    },
    {
        "label": "建材厂占地面积",
        "old": "占地2.5方平方米，建筑面积\n3600平方米",
        "new": "占地2.5万平方米，建筑面积\n3600平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0417.txt:37-38",
    },
    {
        "label": "建材厂占地面积 HTML",
        "old": "占地2.5方平方米，建筑面积3600平方米",
        "new": "占地2.5万平方米，建筑面积3600平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0417.txt:37-38",
    },
    {
        "label": "建材厂占地面积 HTML 跨段",
        "old": "占地2.5方平方米，建筑面积</p><p>3600平方米",
        "new": "占地2.5万平方米，建筑面积</p><p>3600平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0417.txt:37-38",
    },
]

LEFT_UNTOUCHED = [
    "其他 `方平方米/方亩/方人` 候选留待逐页定位，本批只处理 LYG-1291 页可证内容。",
    "本批未使用、未展示、未嵌入任何图片。",
]


def upsert_memory(marker: str, content: str) -> None:
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    MEMORY.write_text(new, encoding="utf-8")


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
        applied.append({"target": str(target), "changed": sum(i["count"] for i in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    changed = sum(t["changed"] for t in applied)
    payload = {
        "time": now,
        "scope": "Paddle-backed LYG-1291 area/money unit residue repair",
        "patterns": len(REPLACEMENTS),
        "changed_this_run": changed,
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册面积、金额单位残字补修第一百二十四批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书阅读稿、当前中册阅读稿、中册正文源稿、全书正文汇总。",
        "- 只处理 Paddle `中/part01/page_0417.txt` 可证的 LYG-1291 页单位残字。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次替换：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        if target["changed"]:
            lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`；证据：`{item['source']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百二十四批：中册面积、金额单位残字"
    upsert_memory(marker, f"""
{marker}

- 按 `workbench/ocr/paddle_ocr/中/part01/page_0417.txt` 回源，补修 LYG-1291 页徐福酒厂和建材厂简介中的单位残字：`1.98方平方米/1.9方平方米/500方元/2.5方平方米` 分别改为 `1.98万平方米/1.9万平方米/500万元/2.5万平方米`。
- 本批证据短语 {len(REPLACEMENTS)} 项，首跑替换 {changed} 处；报告：`output/reports/middle_reader_area_money_batch124_20260706.md`。
- 其他 `方平方米/方亩/方人` 候选继续留待逐页定位；本批未使用、未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

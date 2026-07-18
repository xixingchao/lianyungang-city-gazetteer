# -*- coding: utf-8 -*-
"""Repair Paddle-backed middle-reader 万亩 residues, batch 125."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_wanmu_batch125_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_wanmu_batch125_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册万亩单位残字回源补修第一百二十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "乡镇企业承包滩涂",
        "old": "承包方亩滩涂",
        "new": "承包万亩滩涂",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0414.txt:13-14",
    },
    {
        "label": "乡镇企业承包滩涂 OCR 断字",
        "old": "承包方亩滩涂进行开发，养殖对虾",
        "new": "承包万亩滩涂进行开发，养殖对虾",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0414.txt:13-14",
    },
    {
        "label": "农业支出良种繁殖基地",
        "old": "良种繁殖基地9方亩",
        "new": "良种繁殖基地9万亩",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0296.txt:29-31",
    },
]

LEFT_UNTOUCHED = [
    "本批只处理 Paddle 明确写作 `万亩` 的两处；其他单位残字继续逐页核对。",
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
        "scope": "Paddle-backed middle-reader 万亩 residue repair",
        "patterns": len(REPLACEMENTS),
        "changed_this_run": changed,
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册万亩单位残字补修第一百二十五批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前全书阅读稿、当前中册阅读稿、中册正文源稿和全书正文汇总。",
        "- 只处理 Paddle 页级 OCR 可证的 `方亩 -> 万亩` 两处。",
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百二十五批：中册万亩单位残字"
    upsert_memory(marker, f"""
{marker}

- 按 Paddle 页级 OCR 补修中册两处 `方亩` 残字：`承包方亩滩涂` 改为 `承包万亩滩涂`，证据 `workbench/ocr/paddle_ocr/中/part01/page_0414.txt:13-14`；`良种繁殖基地9方亩` 改为 `良种繁殖基地9万亩`，证据 `workbench/ocr/paddle_ocr/中/part02/page_0296.txt:29-31`。
- 本批证据短语 {len(REPLACEMENTS)} 项，首跑替换 {changed} 处；报告：`output/reports/middle_reader_wanmu_batch125_20260707.md`。
- 本批未使用、未展示、未嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

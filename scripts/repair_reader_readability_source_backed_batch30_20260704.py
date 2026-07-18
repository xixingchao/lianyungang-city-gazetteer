# -*- coding: utf-8 -*-
"""Thirtieth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch30_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch30_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第三十批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "建筑业概述设计能力",
        "old": "年设计能力达60方平方米",
        "new": "年设计能力达60万平方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0296.txt:24",
    },
    {
        "label": "建筑业概述施工工人",
        "old": "全市建筑施工工人约20方人",
        "new": "全市建筑施工工人约20万人",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0296.txt:25",
    },
    {
        "label": "开发区社会事业规划",
        "old": "一所幼儿园进人省级先进水平",
        "new": "一所幼儿园进入省级先进水平",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0423.txt:20",
    },
    {
        "label": "淮北盐场电影队首映地点",
        "old": "淮北盐场烈土纪念塔前",
        "new": "淮北盐场烈士纪念塔前",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0040.txt:29-30",
    },
    {
        "label": "附录娱乐习俗淮海戏",
        "old": "准海戏原来称“小戏”",
        "new": "淮海戏原来称“小戏”",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0293.txt:22-24",
    },
    {
        "label": "附录娱乐习俗淮海锣鼓",
        "old": "同准海戏一样",
        "new": "同淮海戏一样",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0293.txt:26-27",
    },
]


def append_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(target["changed"] for target in targets)
    payload = {
        "time": now,
        "scope": "第三十批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修复页级 OCR 可直接证明的建筑业、开发区、电影放映、附录娱乐习俗残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第三十批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修页级 OCR 可直接证明的建筑业、开发区、电影放映、附录娱乐习俗残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：仍未逐页核到的 `准海战役` 与人物传 `加人中国共产党` 等残留。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for target in targets:
        for item in target["items"]:
            if item["count"]:
                lines.append(
                    f"- {item['label']}：依据 `{item['source']}`；`{target['target']}` 命中 {item['count']} 处。"
                )
    lines.append("")
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-04 第三十批正文残留回源修复"
    memory = f"""
{marker}
- 修复页级 OCR 直接证明的建筑业、开发区、电影放映、附录娱乐习俗残留，共 {total} 处。
- 依据页：`workbench/ocr/paddle_ocr/中/part01/page_0296.txt`、`workbench/ocr/paddle_ocr/中/part01/page_0423.txt`、`workbench/ocr/paddle_ocr/下/part02/page_0040.txt`、`workbench/ocr/paddle_ocr/下/part02/page_0293.txt`。
- 同步目标：`output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md`。
- 暂缓仍未逐页核到的 `准海战役` 与人物传 `加人中国共产党` 等残留。
- 报告：`output/reports/reader_readability_source_backed_batch30_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()

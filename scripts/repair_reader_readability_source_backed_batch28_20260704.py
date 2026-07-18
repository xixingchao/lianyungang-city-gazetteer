# -*- coding: utf-8 -*-
"""Twenty-eighth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch28_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch28_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十八批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "王传业班改演淮海戏",
        "old": "改演准海戏而自行解散",
        "new": "改演淮海戏而自行解散",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0029.txt:24-27",
    },
    {
        "label": "撤销淮海剧团",
        "old": "撤销准海剧团，成立文工团",
        "new": "撤销淮海剧团，成立文工团",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0033.txt:34-36",
    },
    {
        "label": "撤销淮海剧团断行",
        "old": "撤销准海剧团，\n成立文工团",
        "new": "撤销淮海剧团，\n成立文工团",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0033.txt:34-36",
    },
    {
        "label": "重建淮海戏队",
        "old": "文工团重建准海戏队",
        "new": "文工团重建淮海戏队",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0033.txt:38-41",
    },
    {
        "label": "淮海戏逐步恢复",
        "old": "准海戏逐步恢复",
        "new": "淮海戏逐步恢复",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0033.txt:39-41",
    },
    {
        "label": "淮海戏队招收学员",
        "old": "准海戏队招收一批学员",
        "new": "淮海戏队招收一批学员",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0033.txt:40-41",
    },
    {
        "label": "朱爱周烈士墓碑文",
        "old": "朱爱周烈土墓",
        "new": "朱爱周烈士墓",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0088.txt:26-31",
    },
    {
        "label": "吕祥璧烈士墓碑",
        "old": "烈土墓碑为花岗岩结构",
        "new": "烈士墓碑为花岗岩结构",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0089.txt:8-12",
    },
    {
        "label": "吕祥璧烈士碑文",
        "old": "吕祥璧烈土永垂不朽",
        "new": "吕祥璧烈士永垂不朽",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0089.txt:10-12",
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
        "scope": "第二十八批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修复下册页级 OCR 可直接证明的淮海戏、烈士墓碑残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第二十八批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修下册页级 OCR 可直接证明的淮海戏、烈士墓碑残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：尚未定位页级证据的 `海烈土纪念塔`、`淮北盐场烈土纪念塔` 和其它残留。",
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

    marker = "## 2026-07-04 第二十八批正文残留回源修复"
    memory = f"""
{marker}
- 修复下册页级 OCR 直接证明的淮海戏、烈士墓碑残留，共 {total} 处。
- 依据页：`workbench/ocr/paddle_ocr/下/part02/page_0029.txt`、`page_0033.txt`、`page_0088.txt`、`page_0089.txt`。
- 同步目标：`output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md`。
- 暂缓尚未定位页级证据的 `海烈土纪念塔`、`淮北盐场烈土纪念塔` 和其它残留。
- 报告：`output/reports/reader_readability_source_backed_batch28_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()

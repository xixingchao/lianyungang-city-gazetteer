# -*- coding: utf-8 -*-
"""Twenty-ninth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch29_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch29_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十九批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "团市委祭扫淮海烈士纪念塔",
        "old": "祭扫海烈土纪念塔",
        "new": "祭扫淮海烈士纪念塔",
        "source": "workbench/ocr/paddle_ocr/下/part01/page_0323.txt:3-4",
    },
    {
        "label": "东海县淮海剧团前身",
        "old": "其前身为述阳县准海戏小组",
        "new": "其前身为沭阳县淮海戏小组",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0037.txt:3-6",
    },
    {
        "label": "东海县淮海剧团前身断行",
        "old": "其前身为述阳县准海戏小组。1954年进入东\n海",
        "new": "其前身为沭阳县淮海戏小组。1954年进入东\n海",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0037.txt:3-6",
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
        "scope": "第二十九批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修复下册页级 OCR 可直接证明的烈士纪念塔与淮海戏小组残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第二十九批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修下册页级 OCR 可直接证明的烈士纪念塔与淮海戏小组残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：附录民俗 `准海戏原来/同准海戏一样` 及未定位页级证据的其它残留。",
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

    marker = "## 2026-07-04 第二十九批正文残留回源修复"
    memory = f"""
{marker}
- 修复下册页级 OCR 直接证明的烈士纪念塔与淮海戏小组残留，共 {total} 处。
- 依据页：`workbench/ocr/paddle_ocr/下/part01/page_0323.txt`、`workbench/ocr/paddle_ocr/下/part02/page_0037.txt`。
- 同步目标：`output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md`。
- 暂缓附录民俗 `准海戏原来/同准海戏一样` 及未定位页级证据的其它残留。
- 报告：`output/reports/reader_readability_source_backed_batch29_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()

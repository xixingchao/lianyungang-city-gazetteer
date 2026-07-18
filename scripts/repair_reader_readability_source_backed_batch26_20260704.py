# -*- coding: utf-8 -*-
"""Twenty-sixth source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch26_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch26_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十六批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "竹庭县随军担架团支援淮海战役",
        "old": "8月中旬竹庭县组成民工随军担架团支援准海战役",
        "new": "8月中旬竹庭县组成民工随军担架团支援淮海战役",
        "source": "workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:3771",
    },
    {
        "label": "竹庭县万人小车纵队支援淮海战役",
        "old": "民国37年10月12日，竹庭县又组织万人小车纵队支援准海战役",
        "new": "民国37年10月12日，竹庭县又组织万人小车纵队支援淮海战役",
        "source": "workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:3777",
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
        "scope": "第二十六批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修复上册 OCR 汇总可直接证明的大事记淮海战役残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第二十六批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修上册 OCR 汇总可直接证明的大事记淮海战役残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：其它 `准海战役/准海戏` 残留未定位同页 OCR 证据，不做推断替换。",
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
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")

    marker = "## 2026-07-04 第二十六批正文残留回源修复"
    memory = f"""
{marker}
- 修复正文汇总中两处大事记 `准海战役` 残留，均改为 `淮海战役`。
- 依据：`workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:3771`、`:3777`。
- 最终阅读版对应两处此前已正确，本批主要同步正文汇总；其它未定位同页证据的 `准海战役/准海戏` 暂缓。
- 报告：`output/reports/reader_readability_source_backed_batch26_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()

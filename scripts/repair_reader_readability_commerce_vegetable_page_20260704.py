# -*- coding: utf-8 -*-
"""Repair source-backed commerce vegetable page residuals."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_commerce_vegetable_page_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_commerce_vegetable_page_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_商业蔬菜页残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "青椒购进单位",
        "old": "购进青椒10多万公厅",
        "new": "购进青椒10多万公斤",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0149.txt:10",
    },
    {
        "label": "1964至1965年年份范围",
        "old": "19641965年改为管秋冬供应",
        "new": "1964~1965年改为管秋冬供应",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0149.txt:31",
    },
    {
        "label": "1964至1965年亏损补贴",
        "old": "号损补贴1~3.万元",
        "new": "亏损补贴1~3万元",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0149.txt:31",
    },
    {
        "label": "蔬菜公司职工",
        "old": "蔬莱公司职工",
        "new": "蔬菜公司职工",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0149.txt:32",
    },
    {
        "label": "1976年亏损补贴",
        "old": "号亏损补贴59万元",
        "new": "亏损补贴59万元",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0150.txt:5",
    },
    {
        "label": "1983年亏损补贴",
        "old": "号亏损补贴122万元",
        "new": "亏损补贴122万元",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0150.txt:12",
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
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
        "scope": "第三十三卷商业蔬菜购销页残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "仅修复中册 part02 page_0149/page_0150 PaddleOCR 直接证明的蔬菜购销段残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 商业蔬菜页残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：仅修复中册 part02 `page_0149/page_0150` PaddleOCR 直接证明的蔬菜购销段残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for target in targets:
        for item in target["items"]:
            if item["count"]:
                lines.append(f"- {item['label']}：依据 `{item['source']}`；`{target['target']}` 命中 {item['count']} 处。")
    lines.append("")
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-04 商业蔬菜页残留回源修复"
    memory = f"""
{marker}
- 依据 `workbench/ocr/paddle_ocr/中/part02/page_0149.txt` 和 `page_0150.txt`，修复商业蔬菜购销段 `公厅/号损/号亏损/蔬莱公司/19641965年` 等残留，共 {total} 处。
- 同步目标：`output/final_reader/连云港市志_全书.html`、`workbench/body_chapters/连云港市志_全书_正文汇总.md`、`workbench/body_chapters/第三十卷至第四十二卷（中part02）.md`。
- 本批没有泛化处理其它章节 `号损/公厅/蔬莱`，仍需逐页核证。
- 报告：`output/reports/reader_readability_commerce_vegetable_page_20260704.md`。
"""
    append_once(MEMORY, marker, memory)
    print(json.dumps({"total_replacements": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

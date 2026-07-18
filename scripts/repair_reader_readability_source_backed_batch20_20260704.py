# -*- coding: utf-8 -*-
"""Repair a twentieth small source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch20_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch20_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "工会棉织厂断行残留",
        "在市棉织广建立职\n工代表大会制度",
        "在市棉织厂建立职\n工代表大会制度",
        "workbench/ocr/paddle_ocr/下/part01/page_0314.txt:5",
    ),
    (
        "教育概况断行入园入学率",
        "全市幼儿园1933所，人园\n幼儿134587人，加上人学前班的幼儿，人园率80.78%。全市小学1597所，小学生339968\n人，人学率98.94%",
        "全市幼儿园1933所，入园\n幼儿134587人，加上入学前班的幼儿，入园率80.78%。全市小学1597所，小学生339968\n人，入学率98.94%",
        "workbench/ocr/paddle_ocr/下/part01/page_0348.txt:14-16",
    ),
    (
        "干部中专断行残留",
        "成人中等教育有职工中专、于部中专、职\n工技术培训学校",
        "成人中等教育有职工中专、干部中专、职\n工技术培训学校",
        "workbench/ocr/paddle_ocr/下/part01/page_0348.txt:21",
    ),
    (
        "幼儿园发展入园9.5万人",
        "人园幼儿9.5方人",
        "入园幼儿9.5万人",
        "workbench/ocr/paddle_ocr/下/part01/page_0353.txt:10",
    ),
    (
        "幼儿园发展1990入园幼儿",
        "3506班，人园幼儿",
        "3506班，入园幼儿",
        "workbench/ocr/paddle_ocr/下/part01/page_0353.txt:12",
    ),
    (
        "幼儿园发展幼儿入园",
        "幼儿人园",
        "幼儿入园",
        "workbench/ocr/paddle_ocr/下/part01/page_0353.txt:13",
    ),
]

SKIPPED = [
    "正文汇总其它区县概况里的 `人园/人学` 残留未逐页定位，继续暂缓。",
    "本批只修上一批检查暴露出来的断行残留和同页已定位幼儿园发展概况。",
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    if next_start == -1:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for label, old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            items.append({"label": label, "old": old, "new": new, "source": source, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(item["changed"] for item in targets)
    payload = {
        "time": now,
        "scope": "第二十批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "只修复上一批检查暴露的断行残留和同页 OCR 已定位问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第二十批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修上一批检查暴露的断行残留和同页 OCR 已定位问题。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for item in targets[0]["items"]:
        lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`；依据 `{item['source']}`；命中 {item['count']} 处/文件。")
    lines += ["", "## 暂缓", *[f"- {item}" for item in SKIPPED], ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")

    marker = "## 2026-07-04 第二十批正文残留回源修复"
    memory = f"""
{marker}
- 追补第十九批检查暴露的正文汇总断行残留，并按 `workbench/ocr/paddle_ocr/下/part01/page_0353.txt` 修复学前教育发展概况中的 `人园幼儿9.5方人/幼儿人园`。
- 同步目标：`output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md`。
- 依据和命中数：`output/reports/reader_readability_source_backed_batch20_20260704.md`。
"""
    upsert_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()

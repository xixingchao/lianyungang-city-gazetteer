# -*- coding: utf-8 -*-
"""Follow up on the twenty-first source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch21_followup_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch21_followup_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十一批正文残留追补.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "戍守边疆断行残留",
        "与当地驻军联欢，为烈军属服务，并对成守边疆的\n连云港市籍的人民解放军战士进行慰问",
        "与当地驻军联欢，为烈军属服务，并对戍守边疆的\n连云港市籍的人民解放军战士进行慰问",
        "workbench/ocr/paddle_ocr/下/part01/page_0324.txt:37-38",
    ),
    (
        "勤巧小队断行残留",
        "各族儿童“勤巧小队友谊赛，全市52个少先队小队\n获全国勤巧小队奖”",
        "各族儿童“勤巧小队”友谊赛，全市52个少先队小队\n获“全国勤巧小队奖”",
        "workbench/ocr/paddle_ocr/下/part01/page_0328.txt:10-12",
    ),
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
        "scope": "第二十一批正文残留追补",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修复第二十一批定向检查暴露的正文汇总断行残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第二十一批正文残留追补",
        "",
        f"- 时间：{now}",
        "- 原则：只修第二十一批定向检查暴露的正文汇总断行残留。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for item in targets[1]["items"]:
        lines.append(f"- {item['label']}：依据 `{item['source']}`；命中 {item['count']} 处/正文汇总。")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")

    marker = "## 2026-07-04 第二十一批正文残留追补"
    memory = f"""
{marker}
- 追补第二十一批定向检查暴露的正文汇总断行残留：`成守边疆` -> `戍守边疆`，`勤巧小队` 引号缺失。
- 依据：`workbench/ocr/paddle_ocr/下/part01/page_0324.txt:37-38`、`page_0328.txt:10-12`。
- 报告：`output/reports/reader_readability_source_backed_batch21_followup_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()

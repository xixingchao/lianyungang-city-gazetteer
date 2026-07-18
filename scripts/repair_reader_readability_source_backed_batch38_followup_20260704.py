# -*- coding: utf-8 -*-
"""Follow-up sync for the thirty-eighth source-backed repair batch."""

from __future__ import annotations

import importlib.util
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH38 = ROOT / "scripts" / "repair_reader_readability_source_backed_batch38_20260704.py"
TARGETS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第三卷_区县概况.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch38_followup_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch38_followup_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第三十八批正文残留回源修复_followup.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

spec = importlib.util.spec_from_file_location("batch38", BATCH38)
batch38 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(batch38)
REPLACEMENTS = batch38.REPLACEMENTS


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
        "scope": "第三十八批正文残留回源修复 follow-up",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "复用第38批页级证据，补齐上册分章和上册汇总的同步。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第三十八批正文残留回源修复 follow-up",
        "",
        f"- 时间：{now}",
        "- 原则：复用第38批页级证据，补齐上册分章和上册汇总的同步。",
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
                lines.append(f"- {item['label']}：沿用 `{item['source']}`；`{target['target']}` 命中 {item['count']} 处。")
    lines.append("")
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-04 第三十八批正文残留回源修复 follow-up"
    memory = f"""
{marker}
- 复用第38批页级 OCR 证据，补齐上册分章和上册汇总中的金额单位残留同步，共 {total} 处。
- 同步目标：`workbench/body_chapters/连云港市志_上册_正文汇总.md`、`workbench/body_chapters/上/第三卷_区县概况.md`、`workbench/body_chapters/上/第四卷至第十卷（part02）.md`。
- 报告：`output/reports/reader_readability_source_backed_batch38_followup_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()

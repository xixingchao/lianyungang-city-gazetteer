# -*- coding: utf-8 -*-
"""Forty-first source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第十卷至第十六卷（part03）.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch41_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch41_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第四十一批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "连云港市造纸厂筹建投资",
        "old": "1956年由市搬运公司投资1.3\n方元在浦南农场筹建",
        "new": "1956年由市搬运公司投资1.3\n万元在浦南农场筹建",
        "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:10826-10827；同锚 LYG-S-0784",
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
        "scope": "第四十一批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修同锚 PaddleOCR 正文能补全金额的跨行残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第四十一批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修同锚 PaddleOCR 正文能补全金额的跨行残留。",
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

    marker = "## 2026-07-04 第四十一批正文残留回源修复"
    memory = f"""
{marker}
- 修复连云港市造纸厂筹建投资跨行残留 `投资1.3/方元在浦南农场筹建`，共 {total} 处。
- 依据 `workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:10826-10827`，同锚文本为 `投资1.3万元在浦南农场筹建`。
- 同步目标：`workbench/body_chapters/连云港市志_全书_正文汇总.md`、`workbench/body_chapters/连云港市志_上册_正文汇总.md`、`workbench/body_chapters/上/第十卷至第十六卷（part03）.md`；最终阅读版未命中该旧串。
- 报告：`output/reports/reader_readability_source_backed_batch41_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()

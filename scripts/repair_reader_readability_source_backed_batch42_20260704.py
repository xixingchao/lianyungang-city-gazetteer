# -*- coding: utf-8 -*-
"""Forty-second source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch42_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch42_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第四十二批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "沭新河沭新渠总投资", "old": "共投资1200.3方元", "new": "共投资1200.3万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:3980；同锚 LYG-S-0684"},
    {"label": "沿线工程投资", "old": "1044方元，沿线建成控制水闸", "new": "1044万元，沿线建成控制水闸", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:4118；同锚 LYG-S-0688"},
    {"label": "塔山灌区补水国家投资", "old": "国家投资255.36方元", "new": "国家投资255.36万元", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:4197；同锚 LYG-S-0690"},
    {"label": "灌区续建投资", "old": "投资25方元，装机4台", "new": "投资25万元，装机4台", "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:4239；同锚 LYG-S-0691"},
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
        "scope": "第四十二批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "清理全书汇总中漏同步的上册水利金额残留，依据同锚 PaddleOCR 正文。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第四十二批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：清理全书汇总中漏同步的上册水利金额残留，依据同锚 PaddleOCR 正文。",
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

    marker = "## 2026-07-04 第四十二批正文残留回源修复"
    memory = f"""
{marker}
- 修复全书汇总中漏同步的上册水利金额 `方元` 残留，共 {total} 处。
- 依据 `workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md` 的 LYG-S-0684、0688、0690、0691 同锚文本。
- 同步目标：`workbench/body_chapters/连云港市志_全书_正文汇总.md`；最终阅读版未命中这些旧串。
- 报告：`output/reports/reader_readability_source_backed_batch42_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Repair one PaddleOCR-backed finance sentence residue."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_residues_batch88_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_residues_batch88_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第八十八批_银行利率短句.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "银行存放款利率句",
        "old": "各银行存放款利率或执行其所兼属总行规定或参照中央银行新浦分行牌告执行。，新海连特区刚成立时",
        "new": "各银行存放款利率或执行其所隶属总行规定或参照中央银行新浦分行牌告执行。新海连特区刚成立时",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0395.txt:18-19",
    },
    {
        "label": "银行存放款利率句源稿断行",
        "old": "各银行存放款利率或执行其所兼属总行规定或参照中央银行新浦分行牌告执行。，\n新海连特区刚成立时",
        "new": "各银行存放款利率或执行其所隶属总行规定或参照中央银行新浦分行牌告执行。\n新海连特区刚成立时",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0395.txt:18-19",
    },
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {target}: {residuals[:3]}")
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "PaddleOCR-backed finance sentence residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_total": sum(target["changed"] for target in applied),
        "targets": applied,
        "principle": "Only exact context phrases backed by cited PaddleOCR pages are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第八十八批：银行利率短句",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及中册源稿、全书正文汇总中的 1 个金融卷短句。",
        "- 仅处理 PaddleOCR 同页明确支撑的 `所隶属总行` 与句末标点残留；源稿断行按等价精确模式同步。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次实际替换：{payload['changed_total']} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}: `{item['old']}` -> `{item['new']}`；源：`{item['source']}`")
    lines.extend([
        "",
        "## 未处理边界",
        "",
        "- `劳改队撤销，并人徐州第四监狱` 双 OCR 仍作 `并人`，本批不猜改。",
        "- 书末 `避选`、`用破万人心`、`上尽，然长逝` 与旧志序文疑点继续等待更强证据。",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-06 高置信 OCR 错字补修第八十八批：银行利率短句

- 依据 PaddleOCR 页 `中/part02/page_0395.txt:18-19`，修复第三十八卷财政金融银行利率段的 1 个精确短句。
- 修复：`所兼属总行规定或参照中央银行新浦分行牌告执行。，新海连特区` -> `所隶属总行规定或参照中央银行新浦分行牌告执行。新海连特区`；源稿断行版本同步处理。
- 本批证据短语 {len(REPLACEMENTS)} 项，实际替换 {payload['changed_total']} 处；报告：`output/reports/reader_paddle_backed_residues_batch88_20260706.md`。
- 边界：`并人徐州第四监狱`、书末硬点与旧志序文疑点均未猜改；未展示、未嵌入图片。
"""
    upsert_memory(MEMORY, "## 2026-07-06 高置信 OCR 错字补修第八十八批：银行利率短句", memory)
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_total": payload["changed_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

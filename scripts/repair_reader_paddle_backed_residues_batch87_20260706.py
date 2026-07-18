# -*- coding: utf-8 -*-
"""Repair PaddleOCR-backed relic/building short residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_paddle_backed_residues_batch87_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_paddle_backed_residues_batch87_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第八十七批_建筑文物银杏文曰.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "三元宫门额文曰",
        "old": "门额镌刻碑铭文日：“云台山”。字径24厘米，行书。",
        "new": "门额镌刻碑铭文曰：“云台山”。字径24厘米，行书。",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0305.txt",
    },
    {
        "label": "园林寺银杏2株",
        "old": "山门外原有银否2株，相传为唐人植。",
        "new": "山门外原有银杏2株，相传为唐人植。",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0090.txt",
    },
    {
        "label": "南城城隍庙大银杏树",
        "old": "后院有一大银否树，大可三围，也为清代植。",
        "new": "后院有一大银杏树，大可三围，也为清代植。",
        "source": "workbench/ocr/paddle_ocr/下/part02/page_0092.txt",
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
        "scope": "PaddleOCR-backed relic/building short residue repair",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_total": sum(target["changed"] for target in applied),
        "targets": applied,
        "principle": "Only exact context phrases backed by cited PaddleOCR pages are changed.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第八十七批：建筑文物银杏、文曰",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版及对应中册/下册源稿、全书正文汇总中的 3 个短片段。",
        "- 仅处理 PaddleOCR 同页明确支撑的 `文曰/银杏`。",
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
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-06 高置信 OCR 错字补修第八十七批：建筑文物银杏、文曰

- 依据 PaddleOCR 页 `中/part01/page_0305`、`下/part02/page_0090`、`下/part02/page_0092`，修复主阅读版及对应源稿/汇总中的 3 个精确短片段。
- 典型修复：三元宫门额 `文日：“云台山”` -> `文曰：“云台山”`，园林寺/南城城隍庙 `银否2株/大银否树` -> `银杏2株/大银杏树`。
- 本批证据短语 {len(REPLACEMENTS)} 项，实际替换 {payload['changed_total']} 处；报告：`output/reports/reader_paddle_backed_residues_batch87_20260706.md`。
- 边界：乡土文存古籍诗文、旧志序文、书末硬点继续等待更强证据，未做全局替换；未展示、未嵌入图片。
"""
    upsert_memory(MEMORY, "## 2026-07-06 高置信 OCR 错字补修第八十七批：建筑文物银杏、文曰", memory)
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_total": payload["changed_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

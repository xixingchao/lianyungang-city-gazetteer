# -*- coding: utf-8 -*-
"""Repair PaddleOCR-backed Haizhou city wall text in the military facilities section."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_military_facilities_haizhou_city_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_military_facilities_haizhou_city_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第七十九批_海州城军事设施.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("东海营桑格淮安", "康熙三十九年，漕运总督案格题设准安城守营时撤销", "康熙三十九年，漕运总督桑格题设淮安城守营时撤销", "workbench/ocr/paddle_ocr/下/part01/page_0166.txt"),
    ("冯子材光绪二十一年", "光绪二十年（1895年），两广提督冯子材来墟沟办理防务", "光绪二十一年（1895年），两广提督冯子材来墟沟办理防务", "workbench/ocr/paddle_ocr/下/part01/page_0166.txt"),
    ("海州城标题补足-源稿", "二、军事设施\n和壕沟，海州始为城。", "二、军事设施\n城池【海州城】南北朝时，梁将马仙埤于天监十一年（512年）在海州构筑土城\n和壕沟，海州始为城。", "workbench/ocr/paddle_ocr/下/part01/page_0166.txt"),
    ("海州城标题补足-阅读版", "<p>和壕沟，海州始为城。", "<p>城池【海州城】南北朝时，梁将马仙埤于天监十一年（512年）在海州构筑土城和壕沟，海州始为城。", "workbench/ocr/paddle_ocr/下/part01/page_0166.txt"),
    ("海州城修葺壬申", "俊相继修茸，但均未就绪。隆庆王申年（1572年）知州郑复享再度修筑", "俊相继修葺，但均未就绪。隆庆壬申年（1572年）知州郑复享再度修筑", "workbench/ocr/paddle_ocr/下/part01/page_0166.txt"),
    ("海州城屡次修葺", "清时曾屡次修茸，至民国时逐渐荒废。", "清时曾屡次修葺，至民国时逐渐荒废。", "workbench/ocr/paddle_ocr/下/part01/page_0166.txt"),
    ("南城恃此胜金兵", "实为重镇，南宋曾特此以胜金兵。", "实为重镇，南宋曾恃此以胜金兵。", "workbench/ocr/paddle_ocr/下/part01/page_0166.txt"),
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
        for label, old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            items.append({"label": label, "old": old, "new": new, "source": source, "count": count})
        target.write_text(text, encoding="utf-8")
        verify = target.read_text(encoding="utf-8")
        residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {target}: {residuals[:3]}")
        applied.append({"target": str(target), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "PaddleOCR-backed repair for the Haizhou city wall military facilities passage",
        "replacement_patterns": len(REPLACEMENTS),
        "changed_total": sum(target["changed"] for target in applied),
        "targets": applied,
        "principle": "Only exact context phrases backed by PaddleOCR page_0166 are changed; ambiguous names remain untouched.",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第七十九批：海州城军事设施",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 主阅读版、下册 part01 源稿、全书正文汇总中的驻防卷军事设施海州城段。",
        "- 只处理 `workbench/ocr/paddle_ocr/下/part01/page_0166.txt` 明确支撑的上下文短语。",
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
    for label, old, new, source in REPLACEMENTS:
        lines.append(f"- {label}: `{old}` -> `{new}`；源：`{source}`")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-06 高置信 OCR 错字补修第七十九批：海州城军事设施

- 依据下册 part01 驻防卷 PaddleOCR 页 `page_0166`，修复主阅读版、下册 part01 源稿、全书正文汇总中的军事设施海州城段。
- 典型修复：`案格/准安` 改为 `桑格/淮安`，`光绪二十年（1895年）` 改为 `光绪二十一年（1895年）`，补回 `城池【海州城】南北朝时，梁将马仙埤于天监十一年（512年）在海州构筑土城`，并将 `修茸/王申/特此以胜金兵` 改为 `修葺/壬申/恃此以胜金兵`。
- 本批证据短语 {len(REPLACEMENTS)} 项，实际替换 {payload['changed_total']} 处；报告：`output/reports/reader_military_facilities_haizhou_city_20260706.md`。
- 边界：`郑复享`、`黄九捻/黄九埝`、`营家山/莒家山` 等仍可能需要页图或更多版本证据，本批暂不改。
"""
    upsert_memory(MEMORY, "## 2026-07-06 高置信 OCR 错字补修第七十九批：海州城军事设施", memory)
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_total": payload["changed_total"], "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

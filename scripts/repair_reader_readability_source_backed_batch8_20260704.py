# -*- coding: utf-8 -*-
"""Repair a ninth small source-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch8_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch8_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第九批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "淡水渔业鱼种进入80年代",
        "北乡新华村是养殖鱼种的专业村，有利用本地废沟塘养殖鱼种的传统。进人80年代，该",
        "北乡新华村是养殖鱼种的专业村，有利用本地废沟塘养殖鱼种的传统。进入80年代，该",
        "workbench/ocr/paddle_ocr/上/part03/page_0122.txt:30",
    ),
    (
        "池塘养殖进入80年代后",
        "斤，1980年该场最高亩产622.5公斤。进人80年代后，群众养鱼积极性提高，水产养殖新",
        "斤，1980年该场最高亩产622.5公斤。进入80年代后，群众养鱼积极性提高，水产养殖新",
        "workbench/ocr/paddle_ocr/上/part03/page_0123.txt:69",
    ),
    (
        "水库养鱼进入80年代",
        "进人80年代，全市水库凡能养鱼的，都已基本利用。1985年，东海县英瞳水库面积400",
        "进入80年代，全市水库凡能养鱼的，都已基本利用。1985年，东海县英疃水库面积400",
        "workbench/ocr/paddle_ocr/上/part03/page_0124.txt:8",
    ),
    (
        "医药化学原料药进入20世纪80年代",
        "进人20世纪80年代，全市的化学原料药研制、开发和生产有了较大的进展。1980",
        "进入20世纪80年代，全市的化学原料药研制、开发和生产有了较大的进展。1980",
        "workbench/ocr/paddle_ocr/中/part01/page_0124.txt:12",
    ),
    (
        "电力用电进入80年代",
        "年代，化工用电增长迅速。进人80年代，市政建设、工业生产发展较快，家用电器普及率",
        "年代，化工用电增长迅速。进入80年代，市政建设、工业生产发展较快，家用电器普及率",
        "workbench/ocr/paddle_ocr/中/part01/page_0331.txt:16",
    ),
    (
        "市政生活用电进入80年代",
        "千瓦时。进人80年代，市政建设发展较快，人民生活水平提高，电冰箱、电视机、电饭煲等",
        "千瓦时。进入80年代，市政建设发展较快，人民生活水平提高，电冰箱、电视机、电饭煲等",
        "workbench/ocr/paddle_ocr/中/part01/page_0370.txt:34",
    ),
    (
        "口岸统计输入货物",
        "来自青岛的货物占输人货物的22%",
        "来自青岛的货物占输入货物的22%",
        "workbench/ocr/paddle_ocr/中/part01/page_0503.txt:34",
    ),
    (
        "卫生检疫入境船舶",
        "查验人境船舶356艘次",
        "查验入境船舶356艘次",
        "workbench/ocr/paddle_ocr/中/part01/page_0505.txt:20",
    ),
    (
        "卫生检疫1977至1990入境船舶",
        "查验人境中、外籍船舶4960艘次",
        "查验入境中、外籍船舶4960艘次",
        "workbench/ocr/paddle_ocr/中/part01/page_0505.txt:38",
    ),
    (
        "卫生检疫入境员工",
        "4960艘次、人境员工13067人次",
        "4960艘次、入境员工13067人次",
        "workbench/ocr/paddle_ocr/中/part01/page_0506.txt:4",
    ),
    (
        "公费医疗进入80年代MD",
        "进行了清理。1953～1980年，市公费医疗支出，平均每年10多万元，支出比较平稳。进人\n80年代，公费医疗支出增长较快",
        "进行了清理。1953～1980年，市公费医疗支出，平均每年10多万元，支出比较平稳。进入\n80年代，公费医疗支出增长较快",
        "workbench/ocr/paddle_ocr/中/part02/page_0304.txt:23-24",
    ),
    (
        "公费医疗进入80年代HTML",
        "市公费医疗支出，平均每年10多万元，支出比较平稳。进人80年代，公费医疗支出增长较快",
        "市公费医疗支出，平均每年10多万元，支出比较平稳。进入80年代，公费医疗支出增长较快",
        "workbench/ocr/paddle_ocr/中/part02/page_0304.txt:23-24",
    ),
    (
        "公费医疗一定成效",
        "取得了定成效",
        "取得了一定成效",
        "workbench/ocr/paddle_ocr/中/part02/page_0304.txt:25",
    ),
    (
        "干部理论学习进入80年代后",
        "教员队伍的水平也有较大提高。进人80年代后，干部在参与",
        "教员队伍的水平也有较大提高。进入80年代后，干部在参与",
        "workbench/ocr/paddle_ocr/中/part02/page_0444.txt:7",
    ),
    (
        "干部理论学习逐步改进",
        "学习、教育方法遂步改进",
        "学习、教育方法逐步改进",
        "workbench/ocr/paddle_ocr/中/part02/page_0444.txt:5",
    ),
    (
        "各级干部",
        "至1990年，各级于部写出",
        "至1990年，各级干部写出",
        "workbench/ocr/paddle_ocr/中/part02/page_0444.txt:8",
    ),
]

SKIPPED = [
    "`输人棉布/输人卷烟/输人13367吨`：raw/merged 仍同形，未取得同页 PaddleOCR 明确证据，本批暂缓。",
    "`传人境内` 宗教、医学段：raw 仍同形，未取得明确异源证据，本批暂缓。",
    "`时有长落`、`方吨啤酒灌装线`、`调整领导骨于`：仍缺强证据，本批不猜。",
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
        "scope": "第九批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "只修复页级 PaddleOCR 明确支撑的长上下文问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第九批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修页级 PaddleOCR 明确支撑的长上下文问题。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项"])
    for label, old, new, source in REPLACEMENTS:
        lines.append(f"- {label}: `{old}` -> `{new}`；源：`{source}`")
    lines.extend(["", "## 暂缓"])
    for item in SKIPPED:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = f"""
## 2026-07-04 第九批正文残留回源修复

- 对最终阅读版和正文汇总补做 {len(REPLACEMENTS)} 项页级 PaddleOCR 支撑修复，共替换 {total} 处。
- 修复范围包括淡水渔业、医药、电力、口岸统计、卫生检疫、财政公费医疗、政党干部理论教育中的 `进人/输人/人境/遂步/于部/英瞳/定成效` 残留。
- 依据：`output/reports/reader_readability_source_backed_batch8_20260704.md`。
- 暂缓：`输人棉布/输人卷烟/输人13367吨`、`传人境内`、`时有长落`、`方吨啤酒灌装线`、`调整领导骨于` 等未取得强证据项。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第九批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

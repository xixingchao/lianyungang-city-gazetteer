# -*- coding: utf-8 -*-
"""Repair another small PaddleOCR-backed reader residue batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch3_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch3_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第四批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "食品肉鸡加工进入手工业化",
        "肉鸡加工进人手工业化",
        "肉鸡加工进入手工业化",
        "workbench/ocr/paddle_ocr/中/part01/page_0069.txt:114",
    ),
    (
        "机械船舶制造进入80年代",
        "进人20世纪80年代，连云港市船舶制造业有所发展",
        "进入20世纪80年代，连云港市船舶制造业有所发展",
        "workbench/ocr/paddle_ocr/中/part01/page_0207.txt:6",
    ),
    (
        "电力用电进入80年代",
        "进人20世纪80年代，经济建设突飞猛进",
        "进入20世纪80年代，经济建设突飞猛进",
        "workbench/ocr/paddle_ocr/中/part01/page_0367.txt:38",
    ),
    (
        "粮油商人涌入新浦",
        "商人涌人新浦、欢墩埠、青口、板浦等地",
        "商人涌入新浦、欢墩埠、青口、板浦等地",
        "workbench/ocr/paddle_ocr/中/part02/page_0230.txt:34",
    ),
    (
        "粮油贸易日进油吨数",
        "日进油就达60饨",
        "日进油就达60吨",
        "workbench/ocr/paddle_ocr/中/part02/page_0231.txt:1",
    ),
    (
        "粮油贸易豆油出口",
        "年出口豆（生）油2方吨、油饼4万吨",
        "年出口豆（生）油2万吨、油饼4万吨",
        "workbench/ocr/paddle_ocr/中/part02/page_0231.txt:2",
    ),
    (
        "粮商加入粮谷组合",
        "粮商纷纷加人粮谷组合",
        "粮商纷纷加入粮谷组合",
        "workbench/ocr/paddle_ocr/中/part02/page_0231.txt:16",
    ),
    (
        "华商加入粮谷组合",
        "加人粮谷组合的华商达83家",
        "加入粮谷组合的华商达83家",
        "workbench/ocr/paddle_ocr/中/part02/page_0231.txt:17",
    ),
]

SKIPPED = [
    "`民国7散量达100万吨`：疑似断行/漏字，但本轮未取得完整改写证据，暂缓。",
    "`排涝骨于`：raw/merged 支持 `骨干`，但本轮未取得清晰 PaddleOCR 文本定位，暂缓。",
    "`变压器厂进人恢复、发展时期`：未找到 PaddleOCR 纠正证据，暂缓。",
    "口岸 `出人境/人境`：需按页逐条核对，暂缓。",
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
        "scope": "第四批正文可读性残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "skipped": SKIPPED,
        "principle": "仅修复 PaddleOCR 明确支撑的长上下文问题。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第四批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修 PaddleOCR 明确支撑的长上下文问题。",
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
## 2026-07-04 第四批正文残留回源修复

- 对最终阅读版和正文汇总补做 8 项 PaddleOCR 回源修复，本次替换 {total} 处。
- 修复项：食品肉鸡加工 `进人`、机械船舶/电力用电 `进人20世纪80年代`、粮油贸易 `涌人新浦/60饨/2方吨/加人粮谷组合`。
- 依据：`output/reports/reader_readability_source_backed_batch3_20260704.md`。
- 暂缓：`民国7散量达100万吨`、`排涝骨于`、`变压器厂进人恢复、发展时期`、口岸 `出人境/人境`，继续逐页核证。
"""
    upsert_memory(MEMORY, "## 2026-07-04 第四批正文残留回源修复", memory)
    print(json.dumps({"total_replacements": total, "verified_items": len(REPLACEMENTS), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

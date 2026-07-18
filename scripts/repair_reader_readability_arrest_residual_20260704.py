# -*- coding: utf-8 -*-
"""Repair source-verified residual `速捕` OCR slips."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_arrest_residual_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_arrest_residual_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_残留速捕错识回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    ("政党六一逮捕", "来不及转移的10名党员遭速捕", "来不及转移的10名党员遭逮捕", "workbench/ocr/paddle_ocr/中/part02/page_0400.txt:40"),
    ("民政禁毒逮捕", "36名贩毒者被速捕法办", "36名贩毒者被逮捕法办", "workbench/ocr/paddle_ocr/下/part01/page_0053.txt:13"),
    ("军事大逮捕", "日伪据此进行大速捕", "日伪据此进行大逮捕", "workbench/ocr/paddle_ocr/下/part01/page_0177.txt:20-22"),
    ("社团清党大逮捕", "进行清党”大速捕", "进行“清党”大逮捕", "workbench/ocr/paddle_ocr/下/part01/page_0303.txt:14"),
    ("人物杨光銮逮捕", "大肆速捕共产党员和进步师生", "大肆逮捕共产党员和进步师生", "workbench/ocr/paddle_ocr/下/part02/page_0359.txt:36"),
    ("人物王佐良逮捕", "在北伐军支持下速捕反动县长王佐良", "在北伐军支持下逮捕反动县长王佐良", "workbench/ocr/paddle_ocr/下/part02/page_0361.txt:12"),
    ("人物武同儒逮捕", "在沭阳闸庄召开会议时，被敌人速捕", "在沭阳闸庄召开会议时，被敌人逮捕", "workbench/ocr/paddle_ocr/下/part02/page_0362.txt:33-34"),
]

SKIPPED = [
    "`汉王命韩信将钟离味速捕` 未在页级 OCR 中定位到可靠源行，本批暂不修。",
]


def patch_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    counts: dict[str, int] = {}
    for label, old, new, _source in REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
        elif new not in text:
            raise RuntimeError(f"neither old nor new text found: {label}")
        counts[label] = count
    HTML.write_text(text, encoding="utf-8")
    verify_reader()
    return counts


def verify_reader() -> None:
    text = HTML.read_text(encoding="utf-8")
    missing = [new for _label, _old, new, _source in REPLACEMENTS if new not in text]
    residuals = [old for _label, old, new, _source in REPLACEMENTS if old in text and old not in new]
    if missing or residuals:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}")


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


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    items = [
        {"label": label, "old": old, "new": new, "source": source, "count": counts[label]}
        for label, old, new, source in REPLACEMENTS
    ]
    payload = {
        "time": now,
        "scope": "第四十一卷政党；第四十三卷民政信访；第四十五卷军事；第四十九卷社团；第六十卷人物",
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "skipped": SKIPPED,
        "principle": "仅修复页级 OCR 直接证明的 `速捕` 残留；未定位源页的不处理。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 残留速捕错识回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 重点：根据页级 OCR 将残留 `速捕` 分别修为 `逮捕` 或 `大逮捕`。",
        f"- 保留：{SKIPPED[0]}",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-04 残留速捕错识回源修复

- 对全书剩余 `速捕` 残留做回源核对，修复页级 OCR 可证明的 7 项。
- 源文依据：`workbench/ocr/paddle_ocr/中/part02/page_0400.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0053.txt`、`page_0177.txt`、`page_0303.txt`、`workbench/ocr/paddle_ocr/下/part02/page_0359.txt`、`page_0361.txt`、`page_0362.txt`。
- 修复方向：`速捕`→`逮捕`，`大速捕`→`大逮捕`。
- `汉王命韩信将钟离味速捕` 未在页级 OCR 中定位到可靠源行，本批暂不修。
- 报告：`output/reports/reader_readability_arrest_residual_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 残留速捕错识回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

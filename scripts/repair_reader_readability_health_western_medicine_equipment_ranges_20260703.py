# -*- coding: utf-8 -*-
"""Normalize source-verified range markers in Fifth十五卷西医医疗器械设备."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_western_medicine_equipment_ranges_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_western_medicine_equipment_ranges_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷西医医疗器械设备连接号回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0189.txt:7,22; workbench/ocr/paddle_ocr/下/part02/page_0190.txt:6-8"
SCOPE_START = '<p><strong>三、医疗器械设备</strong></p>'
SCOPE_END = '<h4 id="第五十五卷-第三章医疗-第三节中西医结合">第三节中西医结合</h4>'
REPLACEMENTS = [
    ("检验诊断设备连接号", "1970~1980年", "1970～1980年"),
    ("五官科治疗器械连接号", "1980~1984年", "1980～1984年"),
]
EXPECTED_TEXT = [
    "1970～1980年，市区级医院逐步装备72型分光度计",
    "1980～1984年，各医院配置耳科显微手术器械",
]
RESIDUALS = [old for _, old, _ in REPLACEMENTS]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int], int]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    original = text[start:end]
    segment = original
    counts: dict[str, int] = {}

    for label, needle, replacement in REPLACEMENTS:
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
        counts[label] = count

    changed = int(segment != original)
    if changed:
        HTML.write_text(text[:start] + segment + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"expected normalized text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"range marker residue remains: {remaining}")
    verified = sum(segment.count(item) for item in EXPECTED_TEXT)
    return changed, counts, verified


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int], verified: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第三章医疗 / 第二节西医 / 三、医疗器械设备",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "verified_normalized_items": verified,
        "principle": "依据页级 OCR 与当前阅读器核对，仅统一医疗器械设备小节内可证年份范围连接号，停止在第三节中西医结合前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷西医医疗器械设备连接号回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            f"- 已核定规范项：{verified}",
            "- 修复：统一 `1970～1980年`、`1980～1984年` 连接号。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷西医医疗器械设备连接号回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第三章医疗 / 第二节西医 / 三、医疗器械设备`，止于 `第三节中西医结合` 前。
- 修复内容：统一 `1970～1980年`、`1980～1984年` 连接号。
- 已核定规范项：{verified}；本次复跑改写：{changed}。
- 报告：`output/reports/reader_readability_health_western_medicine_equipment_ranges_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷西医医疗器械设备连接号回源修复

- 对第五十五卷卫生 `第三章医疗 / 第二节西医 / 三、医疗器械设备` 进行回源核对。
- 源文依据：`{SOURCE_NOTE}`。
- 统一 `1970～1980年`、`1980～1984年` 连接号。
- 当前核验已核定规范项 {verified} 处，本次复跑改写 {changed} 处。
- 报告：`output/reports/reader_readability_health_western_medicine_equipment_ranges_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷西医医疗器械设备连接号回源修复", memory)


def main() -> None:
    changed, counts, verified = patch_reader()
    write_reports(changed, counts, verified)
    print(json.dumps({"changed": changed, "counts": counts, "verified": verified, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()

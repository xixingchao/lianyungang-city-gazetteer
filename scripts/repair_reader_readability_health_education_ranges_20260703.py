# -*- coding: utf-8 -*-
"""Normalize source-verified range markers in Fifth十五卷教育科研教育段."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_education_ranges_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_education_ranges_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷教育科研教育连接号回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0206.txt:17-18,31,33; page_0207.txt:3-4"
SCOPE_START = '<h4 id="第五十五卷-第六章教育 科研-第一节教育">第一节教育</h4>'
SCOPE_END = '<h4 id="第五十五卷-第六章教育 科研-第二节科研">第二节科研</h4>'
REPLACEMENTS = [
    ("每周学习时间连接号", "8~10小时", "8～10小时"),
    ("学制连接号", "4~6年", "4～6年"),
    ("招生人数连接号", "5~10名学员", "5～10名学员"),
    ("中药学校毕业统计年代连接号", "1958~1989年", "1958～1989年"),
    ("医务培训班年代连接号", "1953~1990年", "1953～1990年"),
]
EXPECTED_TEXT = [
    "每周学习8～10小时",
    "学制4～6年",
    "招收5～10名学员",
    "从1958～1989年，该校共毕业护士专业583人",
    "1953～1990年，共办医务培训班54期",
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
        raise RuntimeError(f"residue remains: {remaining}")
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
        "scope": "第五十五卷卫生 / 第六章教育科研 / 第一节教育",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "verified_normalized_items": verified,
        "principle": "依据页级 OCR 与当前阅读器核对，仅统一第一节教育中可证的时间、年制与人数范围连接号，停止在第二节科研前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷教育科研教育连接号回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            f"- 已核定规范项：{verified}",
            "- 修复：统一 `8～10小时`、`4～6年`、`5～10名学员`、`1958～1989年`、`1953～1990年` 连接号。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷教育科研教育连接号回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第六章教育科研 / 第一节教育`，止于 `第二节科研` 前。
- 修复内容：统一 `8～10小时`、`4～6年`、`5～10名学员`、`1958～1989年`、`1953～1990年` 连接号。
- 已核定规范项：{verified}；本次复跑改写：{changed}。
- 报告：`output/reports/reader_readability_health_education_ranges_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷教育科研教育连接号回源修复

- 对第五十五卷卫生 `第六章教育科研 / 第一节教育` 进行回源核对。
- 源文依据：`{SOURCE_NOTE}`。
- 统一 `8～10小时`、`4～6年`、`5～10名学员`、`1958～1989年`、`1953～1990年` 连接号。
- 当前核验已核定规范项 {verified} 处，本次复跑改写 {changed} 处。
- 报告：`output/reports/reader_readability_health_education_ranges_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷教育科研教育连接号回源修复", memory)


def main() -> None:
    changed, counts, verified = patch_reader()
    write_reports(changed, counts, verified)
    print(json.dumps({"changed": changed, "counts": counts, "verified": verified, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()

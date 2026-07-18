# -*- coding: utf-8 -*-
"""Normalize source-verified range markers in Fifth十五卷药品检验."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_drug_inspection_ranges_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_drug_inspection_ranges_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷药品检验连接号回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0200.txt:23,36; page_0201.txt:3,6"
SCOPE_START = '<h4 id="第五十五卷-第四章医政 药政-第五节药品检验">第五节药品检验</h4>'
SCOPE_END = '<h3 id="第五十五卷-第五章保健疗养">第五章保健疗养</h3>'
REPLACEMENTS = [
    ("1961至1964连接号", "1961~1964年", "1961～1964年"),
    ("1981至1985连接号", "1981~1985年", "1981～1985年"),
]
EXPECTED_TEXT = [
    "1961～1964年，共检验药品895件",
    "1981～1985年，市药品检验所共抽检",
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
        "scope": "第五十五卷卫生 / 第四章医政药政 / 第五节药品检验",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "verified_normalized_items": verified,
        "principle": "依据页级 OCR 与当前阅读器核对，仅统一药品检验节抽检年代范围连接号，停止在第五章保健疗养前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷药品检验连接号回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            f"- 已核定规范项：{verified}",
            "- 修复：统一 `1961～1964年`、`1981～1985年` 连接号。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷药品检验连接号回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第四章医政药政 / 第五节药品检验`，止于 `第五章保健疗养` 前。
- 修复内容：统一 `1961～1964年`、`1981～1985年` 连接号。
- 已核定规范项：{verified}；本次复跑改写：{changed}。
- 报告：`output/reports/reader_readability_health_drug_inspection_ranges_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷药品检验连接号回源修复

- 对第五十五卷卫生 `第四章医政药政 / 第五节药品检验` 进行回源核对。
- 源文依据：`{SOURCE_NOTE}`。
- 统一 `1961～1964年`、`1981～1985年` 连接号。
- 当前核验已核定规范项 {verified} 处，本次复跑改写 {changed} 处。
- 报告：`output/reports/reader_readability_health_drug_inspection_ranges_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷药品检验连接号回源修复", memory)


def main() -> None:
    changed, counts, verified = patch_reader()
    write_reports(changed, counts, verified)
    print(json.dumps({"changed": changed, "counts": counts, "verified": verified, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()

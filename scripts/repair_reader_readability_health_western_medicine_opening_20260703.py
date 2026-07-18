# -*- coding: utf-8 -*-
"""Normalize source-verified punctuation in Fifth十五卷西医 opening segment."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_western_medicine_opening_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_western_medicine_opening_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷西医开头标点连接号回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0183.txt:21-38; page_0184.txt:1-38; page_0185.txt:3-12"
SCOPE_START = '<h4 id="第五十五卷-第三章医疗-第二节西医">第二节西医</h4>'
SCOPE_END = '<p><strong>普外科</strong></p>'

REPLACEMENTS = [
    ("民国元年括号", "民国元年（1912年)开始", "民国元年（1912年）开始"),
    ("消化内科标点", "1988年,开展内镜微波治疗", "1988年，开展内镜微波治疗"),
    ("神经内科连接号", "1984~1990年，开展格林", "1984～1990年，开展格林"),
]
EXPECTED_TEXT = [
    "民国元年（1912年）开始设简易病房和手术室",
    "1988年，开展内镜微波治疗消化道肿瘤",
    "1984～1990年，开展格林一巴利综合症",
]
RESIDUALS = ["民国元年（1912年)开始", "1988年,开展内镜微波治疗", "1984~1990年，开展格林"]
UNRESOLVED_NOTES = [
    "`尿、酶或蝮蛇栓酯`、`人绒毛膜促腺流毒抗核抗体` 等医学词现有 OCR 证据不足，暂不凭推测改写。",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    counts: dict[str, int] = {}
    for label, needle, replacement in REPLACEMENTS:
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            counts[label] = count

    changed = int(segment != text[start:end])
    if changed:
        HTML.write_text(text[:start] + segment + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"residue remains: {remaining}")
    return changed, counts


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第三章医疗 / 第二节西医 / 起源和发展至内分泌科",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "unresolved_notes": UNRESOLVED_NOTES,
        "principle": "依据页级 OCR 与当前阅读器核对，只清理本段可证标点和连接号残留，停止在普外科前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷西医开头标点连接号回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：统一 `民国元年（1912年）`、`1988年，开展`、`1984～1990年`。",
            f"- 暂不处理：{UNRESOLVED_NOTES[0]}",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷西医开头标点连接号回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第三章医疗 / 第二节西医` 中 `起源和发展` 至 `普外科` 前。
- 修复内容：统一 `民国元年（1912年）`、`1988年，开展`、`1984～1990年`。
- 暂不处理：{UNRESOLVED_NOTES[0]}
- 报告：`output/reports/reader_readability_health_western_medicine_opening_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷西医开头标点连接号回源修复

- 对第五十五卷卫生 `第三章医疗 / 第二节西医` 的 `起源和发展` 至 `普外科` 前进行回源核对。
- 源文依据：`{SOURCE_NOTE}`。
- 统一 `民国元年（1912年）`、`1988年，开展`、`1984～1990年`。
- 暂不凭推测改写 `尿、酶或蝮蛇栓酯`、`人绒毛膜促腺流毒抗核抗体` 等医学词。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_western_medicine_opening_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷西医开头标点连接号回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()

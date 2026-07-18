# -*- coding: utf-8 -*-
"""Normalize a source-verified range marker in Fifth十五卷西医妇产科."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_western_medicine_obstetrics_range_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_western_medicine_obstetrics_range_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷西医妇产科连接号回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0186.txt:39-41; workbench/ocr/paddle_ocr/下/part02/page_0187.txt:3-13"
SCOPE_START = '<p><strong>妇产科</strong></p>'
SCOPE_END = '<p><strong>儿科</strong></p>'
NEEDLE = "20世纪30~40年代"
REPLACEMENT = "20世纪30～40年代"
EXPECTED_TEXT = "20世纪30～40年代，新浦、海州等地的私立产科医院开始新法接生"
UNRESOLVED_NOTES = [
    "`阿米妥纳`、`Ronr-Y吻合`、`低湿下肾切开取石`、`凳下腺` 等医学词当前 OCR 未给出足够可靠正形，暂不改写。",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    count = segment.count(NEEDLE)
    if count:
        segment = segment.replace(NEEDLE, REPLACEMENT)
        HTML.write_text(text[:start] + segment + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    if EXPECTED_TEXT not in segment:
        raise RuntimeError("expected normalized range is missing")
    if NEEDLE in segment:
        raise RuntimeError("range marker residue remains")
    return int(count > 0), {"range_markers_normalized": count}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第三章医疗 / 第二节西医 / 妇产科",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "unresolved_notes": UNRESOLVED_NOTES,
        "principle": "依据页级 OCR 与当前阅读器核对，仅统一妇产科年代范围连接号，停止在儿科前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷西医妇产科连接号回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：统一 `20世纪30～40年代` 连接号。",
            f"- 暂不处理：{UNRESOLVED_NOTES[0]}",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷西医妇产科连接号回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第三章医疗 / 第二节西医 / 妇产科`，止于 `儿科` 前。
- 修复内容：统一 `20世纪30～40年代` 连接号。
- 暂不处理：{UNRESOLVED_NOTES[0]}
- 报告：`output/reports/reader_readability_health_western_medicine_obstetrics_range_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷西医妇产科连接号回源修复

- 对第五十五卷卫生 `第三章医疗 / 第二节西医 / 妇产科` 进行回源核对。
- 源文依据：`{SOURCE_NOTE}`。
- 统一 `20世纪30～40年代` 连接号。
- 暂不凭推测改写 `阿米妥纳`、`Ronr-Y吻合`、`低湿下肾切开取石`、`凳下腺` 等医学词。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_western_medicine_obstetrics_range_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷西医妇产科连接号回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()

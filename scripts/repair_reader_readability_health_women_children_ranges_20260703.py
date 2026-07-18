# -*- coding: utf-8 -*-
"""Normalize source-verified leftovers in Fifth十五卷保健疗养妇女儿童段."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_women_children_ranges_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_women_children_ranges_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷保健疗养妇女儿童连接号标点补漏.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0201.txt:31; page_0202.txt:10,28; page_0203.txt:7; page_0204.txt:11,24"
SCOPE_START = '<h4 id="第五十五卷-第五章保健疗养-第一节妇女保健">第一节妇女保健</h4>'
SCOPE_END = '<h4 id="第五十五卷-第五章保健疗养-第三节干部保健">第三节干部保健</h4>'
REPLACEMENTS = [
    ("接生年代连接号", "1960~1970年", "1960～1970年"),
    ("妇女病治疗逗号", "治愈448人,好转801人", "治愈448人，好转801人"),
    ("四期保护年代连接号", "1953~1954年", "1953～1954年"),
    ("儿童年龄连接号", "3~7岁儿童", "3～7岁儿童"),
    ("营养矫治重量连接号", "250~500克", "250～500克"),
]
EXPECTED_TEXT = [
    "1960～1970年，新法接生的优越性",
    "治愈448人，好转801人",
    "1953～1954年，全市通过图片展览",
    "3～7岁儿童入托7857人",
    "增加供应鸡蛋250～500克",
]
RESIDUALS = [old for _, old, _ in REPLACEMENTS]
UNRESOLVED_NOTES = [
    "`0.19%o` 在既有 20260702 妇女保健报告中被作为已核定文本保留，且页级 OCR 同形；本轮不凭推测改为千分号。",
]


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
        "scope": "第五十五卷卫生 / 第五章保健疗养 / 第一节妇女保健至第二节儿童保健",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "verified_normalized_items": verified,
        "unresolved_notes": UNRESOLVED_NOTES,
        "principle": "依据页级 OCR 与当前阅读器核对，仅补第一、二节中可证连接号与半角逗号残留，停止在第三节干部保健前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷保健疗养妇女儿童连接号标点补漏",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            f"- 已核定规范项：{verified}",
            "- 修复：统一 `1960～1970年`、`1953～1954年`、`3～7岁儿童`、`250～500克`，修正 `治愈448人，好转801人`。",
            f"- 暂不处理：{UNRESOLVED_NOTES[0]}",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷保健疗养妇女儿童连接号标点补漏

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第五章保健疗养` 第一节至第二节，止于 `第三节干部保健` 前。
- 修复内容：统一 `1960～1970年`、`1953～1954年`、`3～7岁儿童`、`250～500克`，修正 `治愈448人，好转801人`。
- 暂不处理：{UNRESOLVED_NOTES[0]}
- 已核定规范项：{verified}；本次复跑改写：{changed}。
- 报告：`output/reports/reader_readability_health_women_children_ranges_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷保健疗养妇女儿童连接号标点补漏

- 对第五十五卷卫生 `第五章保健疗养` 第一节至第二节进行回源核对。
- 源文依据：`{SOURCE_NOTE}`。
- 统一 `1960～1970年`、`1953～1954年`、`3～7岁儿童`、`250～500克`，修正 `治愈448人，好转801人`。
- 暂不处理：{UNRESOLVED_NOTES[0]}
- 当前核验已核定规范项 {verified} 处，本次复跑改写 {changed} 处。
- 报告：`output/reports/reader_readability_health_women_children_ranges_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷保健疗养妇女儿童连接号标点补漏", memory)


def main() -> None:
    changed, counts, verified = patch_reader()
    write_reports(changed, counts, verified)
    print(json.dumps({"changed": changed, "counts": counts, "verified": verified, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()

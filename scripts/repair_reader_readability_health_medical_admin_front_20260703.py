# -*- coding: utf-8 -*-
"""Normalize source-verified punctuation in Fifth十五卷医政药政前段."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_medical_admin_front_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_medical_admin_front_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷医政药政前段标点连接号回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0193.txt:26,32; page_0194.txt:31; page_0195.txt:36-38; page_0196.txt:7-8"
SCOPE_START = '<h3 id="第五十五卷-第四章医政 药政">第四章医政 药政</h3>'
SCOPE_END = '<h4 id="第五十五卷-第四章医政 药政-第四节药政管理">第四节药政管理</h4>'
REPLACEMENTS = [
    ("乡镇括号", "乡（镇)成立农村卫生协会", "乡（镇）成立农村卫生协会"),
    ("县区括号", "市内各县（区)也都逐步", "市内各县（区）也都逐步"),
    ("病区管理逗号", "床位增加,增设", "床位增加，增设"),
    ("献血员人数连接号", "每批5~6人", "每批5～6人"),
    ("献血间隔连接号", "间隔3~4个月", "间隔3～4个月"),
]
EXPECTED_TEXT = [
    "乡（镇）成立农村卫生协会",
    "市内各县（区）也都逐步建立农村卫生工作协会",
    "床位增加，增设五官科病区",
    "每批5～6人，每人每次献血300～500毫升",
    "间隔3～4个月。1986年，新浦中心血库改名",
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
        "scope": "第五十五卷卫生 / 第四章医政药政 / 第一节至第三节",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "verified_normalized_items": verified,
        "principle": "依据页级 OCR 与当前阅读器核对，仅清理第四章前段可证括号、逗号和连接号残留，停止在第四节药政管理前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷医政药政前段标点连接号回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            f"- 已核定规范项：{verified}",
            "- 修复：统一 `乡（镇）`、`县（区）` 右括号，修正 `床位增加，增设`，统一 `每批5～6人`、`间隔3～4个月`。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷医政药政前段标点连接号回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第四章医政药政` 第一节至第三节，止于 `第四节药政管理` 前。
- 修复内容：统一 `乡（镇）`、`县（区）` 右括号，修正 `床位增加，增设`，统一 `每批5～6人`、`间隔3～4个月`。
- 已核定规范项：{verified}；本次复跑改写：{changed}。
- 报告：`output/reports/reader_readability_health_medical_admin_front_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷医政药政前段标点连接号回源修复

- 对第五十五卷卫生 `第四章医政药政` 第一节至第三节进行回源核对。
- 源文依据：`{SOURCE_NOTE}`。
- 统一 `乡（镇）`、`县（区）` 右括号，修正 `床位增加，增设`，统一 `每批5～6人`、`间隔3～4个月`。
- 当前核验已核定规范项 {verified} 处，本次复跑改写 {changed} 处。
- 报告：`output/reports/reader_readability_health_medical_admin_front_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷医政药政前段标点连接号回源修复", memory)


def main() -> None:
    changed, counts, verified = patch_reader()
    write_reports(changed, counts, verified)
    print(json.dumps({"changed": changed, "counts": counts, "verified": verified, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()

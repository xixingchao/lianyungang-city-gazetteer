# -*- coding: utf-8 -*-
"""Repair OCR permille residues in Volume 4 population text."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_volume4_permille_ocr_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_volume4_permille_ocr_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四卷人口千分号错识修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第四卷-人口">第四卷人口</h2>'
SCOPE_END = '<h2 id="第五卷-城乡建设">第五卷城乡建设</h2>'
SOURCES = [
    "workbench/ocr/paddle_ocr/上/part01/page_0282.txt",
    "workbench/ocr/raw/上/part01/page_0282.txt",
    "workbench/body_chapters/上/第四卷_人口（part01_部分）.md",
]
PATTERN = re.compile(r"(?<=\d)%(?:o|e|0|c)\b")


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    start = html.index(SCOPE_START)
    end = html.index(SCOPE_END, start)
    segment = html[start:end]
    matches = PATTERN.findall(segment)
    if not matches:
        raise RuntimeError("no volume 4 permille OCR residues found")
    segment2 = PATTERN.sub("‰", segment)
    remaining = PATTERN.findall(segment2)
    if remaining:
        raise RuntimeError(f"remaining residues after replacement: {remaining[:5]}")
    HTML.write_text(html[:start] + segment2 + html[end:], encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    counts = {token: matches.count(token) for token in sorted(set(matches))}
    payload = {
        "time": now,
        "scope": "第四卷人口",
        "sources": SOURCES,
        "pattern": "数字后 %o/%e/%0/%c -> ‰",
        "changes": len(matches),
        "counts": counts,
        "principle": "限定第四卷人口范围，仅替换数字后明显表示千分号的 OCR 残留；普通百分号不动。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四卷人口千分号错识修复

- 时间：{now}
- 范围：第四卷人口。
- 依据：`{'`、`'.join(SOURCES)}`。

## 修复

- 将数字后明显表示千分号的 OCR 残留 `%o/%e/%0/%c` 统一修为 `‰`。
- 本次替换 {len(matches)} 处：{counts}。
- 普通百分号未改。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四卷人口千分号错识修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 限定第四卷人口范围，依据 `{SOURCES[0]}`、`{SOURCES[1]}` 等文本源，将数字后的 `%o/%e/%0/%c` OCR 千分号残留统一修为 `‰`，共 {len(matches)} 处。
- 普通百分号未改；不改表格数据。
- 报告：`output/reports/reader_volume4_permille_ocr_20260705.md`。
""",
    )

    print("volume4_permille_ocr_repaired")
    print(f"changes={len(matches)}")
    print(f"counts={counts}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

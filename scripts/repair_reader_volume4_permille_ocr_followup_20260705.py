# -*- coding: utf-8 -*-
"""Follow-up repair for remaining Volume 4 permille OCR residues."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_volume4_permille_ocr_followup_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_volume4_permille_ocr_followup_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四卷人口千分号错识第二批修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第四卷-人口">第四卷人口</h2>'
SCOPE_END = '<h2 id="第五卷-城乡建设">第五卷城乡建设</h2>'
SOURCES = [
    "workbench/ocr/paddle_ocr/上/part01/page_0282.txt",
    "workbench/ocr/raw/上/part01/page_0282.txt",
    "workbench/body_chapters/上/第四卷_人口（part01_部分）.md",
]
PATTERN = re.compile(r"(?<=\d)%(?:o|e|0|c)")


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
        raise RuntimeError("no remaining volume 4 permille OCR residues found")
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
        "pattern": "数字后剩余 %o/%e/%0/%c -> ‰",
        "changes": len(matches),
        "counts": counts,
        "principle": "第二批限定第四卷人口范围，补修后接中文或标点导致首批未命中的千分号残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四卷人口千分号错识第二批修复

- 时间：{now}
- 范围：第四卷人口。
- 依据：`{'`、`'.join(SOURCES)}`。

## 修复

- 补修数字后剩余 `%o/%e/%0/%c` 千分号 OCR 残留为 `‰`。
- 本次替换 {len(matches)} 处：{counts}。
- 仍限定第四卷，不处理其他卷。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四卷人口千分号错识第二批修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 限定第四卷人口范围，补修首批规则未命中的 `%o/%0/%c/%e` 千分号残留，共 {len(matches)} 处。
- 其他卷中类似残留待逐卷确认后处理；不改表格数据。
- 报告：`output/reports/reader_volume4_permille_ocr_followup_20260705.md`。
""",
    )

    print("volume4_permille_ocr_followup_repaired")
    print(f"changes={len(matches)}")
    print(f"counts={counts}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

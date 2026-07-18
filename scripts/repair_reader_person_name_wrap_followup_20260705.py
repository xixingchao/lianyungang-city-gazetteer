# -*- coding: utf-8 -*-
"""Follow-up repairs for source-backed person-name line-wrap residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_person_name_wrap_followup_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_person_name_wrap_followup_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_人物姓名换行串行补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "牛耀华条目姓名错位",
        "<p>）铜山县人。民国28年（1939年）参加革命，并加入中国共产牛耀华(1919~党。1956年任新海连市副市长。</p>",
        "<p>牛耀华(1919~）铜山县人。民国28年（1939年）参加革命，并加入中国共产党。1956年任新海连市副市长。</p>",
        1,
    ),
    (
        "程智培条目姓名错位",
        "<p>，）灌云县人。1967年8月参加工作，1979年加入中国共产党。</p>\n<p>程智培(1944～1983年任连云港市政府副秘书长。1989年起任连云港市副市长。</p>",
        "<p>程智培(1944～，）灌云县人。1967年8月参加工作，1979年加入中国共产党。1983年任连云港市政府副秘书长。1989年起任连云港市副市长。</p>",
        1,
    ),
    (
        "高有为条目姓名错位",
        "<p>）山东省沂南县人。1965年10月加入中国共产党，1969年8月高有为(1944 ~参加工作。1984年起任连云港市副市长。</p>",
        "<p>高有为(1944 ~）山东省沂南县人。1965年10月加入中国共产党，1969年8月参加工作。1984年起任连云港市副市长。</p>",
        1,
    ),
    (
        "王稳卿条目姓名错位",
        "<p>）丰县人。1969年8月参加工作，1965年11月加入中国共产王稳卿(1944 ~党。先后任东海县县长、中共东海县委书记。1986年任中共连云港市委副书记兼组织部长。1986年任中共连云港市委副书记。1988年1月任连云港市市长。</p>",
        "<p>王稳卿(1944 ~）丰县人。1969年8月参加工作，1965年11月加入中国共产党。先后任东海县县长、中共东海县委书记。1986年任中共连云港市委副书记兼组织部长。1986年任中共连云港市委副书记。1988年1月任连云港市市长。</p>",
        1,
    ),
    (
        "吴炳裔条目姓名错位",
        "<p>）靖江县人。1964年8月参加工作。1976年10月加入中国共吴炳裔（1945～产党。1988年6月任中共连云港市委常委、市政府常务副市长。</p>",
        "<p>吴炳裔（1945～）靖江县人。1964年8月参加工作。1976年10月加入中国共产党。1988年6月任中共连云港市委常委、市政府常务副市长。</p>",
        1,
    ),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for label, old, new, expected in REPLACEMENTS:
        count = html.count(old)
        if count != expected:
            raise RuntimeError(f"expected {expected} occurrence(s) for {label}, got {count}")
        html = html.replace(old, new)
        changes.append({"label": label, "old": old, "new": new, "count": count})
    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sources = [
        "workbench/ocr/raw/下/part02/page_0389.txt",
        "workbench/ocr/raw/下/part02/page_0399.txt",
    ]
    payload = {"time": now, "target": str(HTML.relative_to(ROOT)).replace("\\", "/"), "sources": sources, "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 人物姓名换行串行补修",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 原则：只修 raw OCR 页可定位的姓名换行串行和 `中国共产党` 被姓名插入的问题。",
        "",
        "## 依据",
        "",
    ]
    lines.extend(f"- `{source}`" for source in sources)
    lines.extend(["", "## 修复清单", "", "| 项 | 次数 |", "|---|---:|"])
    for item in changes:
        lines.append(f"| {item['label']} | {item['count']} |")
    md = "\n".join(lines) + "\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 人物姓名换行串行补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_person_name_wrap_followup_20260705.py`，补修人物简介中姓名换行串行残留。
- 依据 `workbench/ocr/raw/下/part02/page_0389.txt` 与 `page_0399.txt`，修复牛耀华、程智培、高有为、王稳卿、吴炳裔条目。
- 报告：`output/reports/reader_person_name_wrap_followup_20260705.md`。
""",
    )

    print("reader_person_name_wrap_followup_repaired")
    print(f"changes={len(changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

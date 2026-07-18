# -*- coding: utf-8 -*-
"""Remove a table-tail residue before the judicial land disputes paragraph."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_judicial_land_table_tail_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_judicial_land_table_tail_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_司法卷土地小节表尾残片清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = (
    "<p>96.143633491949 ~ 19591515100.001960 ~ 19661023.001967 ~ 197396.033283151974 ~ "
    "198196.259088471982 ~ 1990合计1527152993.97土地20世纪50年代，市、县法院受理的土地案件"
)
NEW = "<p>土地20世纪50年代，市、县法院受理的土地案件"

OLD_DAMAGE = (
    "<p>89697.49201949 ~ 195888.891959 ~ 196690.482101901983~ 1990损害赔偿建国后至“文化大革命”前，"
    "市、县损害赔偿案件"
)
NEW_DAMAGE = "<p>损害赔偿建国后至“文化大革命”前，市、县损害赔偿案件"


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for label, old, new in [
        ("土地小节前房屋案件表尾残片", OLD, NEW),
        ("损害赔偿小节前土地案件表尾残片", OLD_DAMAGE, NEW_DAMAGE),
    ]:
        count = html.count(old)
        if count == 1:
            html = html.replace(old, new, 1)
            changes.append({"label": label, "status": "changed", "changed": 1})
        elif count == 0 and html.count(new) >= 1:
            changes.append({"label": label, "status": "already_applied", "changed": 0})
        else:
            raise RuntimeError(f"expected {label} once, got {count}")

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sources = [
        "workbench/ocr/raw/下/part01/page_0128.txt:50",
        "workbench/ocr/raw/下/part01/page_0129.txt:4",
        "workbench/ocr/raw/下/part01/page_0129.txt:19",
    ]
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "sources": sources,
        "changes": changes,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = "\n".join([
        "# 司法卷土地小节表尾残片清理",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：删除司法卷民事案件小节前误粘入正文的表尾数字串，保留正文从 `土地...`、`损害赔偿...` 开始。",
        "",
        "## 依据",
        "",
        *[f"- `{source}`" for source in sources],
        "",
        "## 结果",
        "",
        *[f"- {item['label']}：{item['status']}，本次变更 {item['changed']}" for item in changes],
    ]) + "\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 司法卷土地小节表尾残片清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_judicial_land_table_tail_20260705.py`，清理第四十四卷治安司法中 `土地` 小节前误粘的上一张表尾数字串。
- 依据 `workbench/ocr/raw/下/part01/page_0128.txt`：第50-57行为房屋案件表尾，正文从第58行 `土地20世纪50年代...` 开始；依据 `page_0129.txt`：第4-18行为土地案件表，第19行正文从 `损害赔偿...` 开始。
- 报告：`output/reports/reader_judicial_land_table_tail_20260705.md`。
""",
    )

    print("reader_judicial_land_table_tail_repaired")
    print(f"changed={sum(item['changed'] for item in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

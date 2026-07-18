# -*- coding: utf-8 -*-
"""Clean pre-delivery review wording from verified table LYG-上-T001."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "workbench" / "table_entries" / "上" / "data" / "LYG-上-T001.json"
STRUCTURED = ROOT / "output" / "structured_tables" / "index.html"
REPORT_JSON = ROOT / "output" / "reports" / "t001_verified_note_cleanup_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "t001_verified_note_cleanup_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_地层系统表已核说明清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = "跨页表：page_130(上部) + page_131(续上表)。建议对照原图复核"
NEW = "已据页级 OCR 跨页核录：workbench/ocr/paddle_ocr/上/part01/page_0130.txt（上部）与 page_0131.txt（续上表）；线性化残文已从最终阅读版撤出。"


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if data.get("table_id") != "LYG-上-T001":
        raise RuntimeError("unexpected table file")
    if data.get("notes") != OLD:
        raise RuntimeError(f"unexpected notes: {data.get('notes')!r}")
    data["notes"] = NEW
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    structured_changed = False
    if STRUCTURED.exists():
        text = STRUCTURED.read_text(encoding="utf-8")
        if OLD in text:
            STRUCTURED.write_text(text.replace(OLD, NEW), encoding="utf-8")
            structured_changed = True

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "table_id": "LYG-上-T001",
        "changed": [str(DATA.relative_to(ROOT))],
        "structured_index_updated": structured_changed,
        "old_notes": OLD,
        "new_notes": NEW,
        "data_values_changed": False,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 地层系统表已核说明清理

- 时间：{now}
- 表ID：`LYG-上-T001`
- 数据值变更：无。
- 更新文件：`workbench/table_entries/上/data/LYG-上-T001.json`。
- 同步结构化表格站：{structured_changed}。

## 处理

- 将已核表 notes 中的交付前措辞 `建议对照原图复核` 改为证据型说明。
- 新说明指向 `workbench/ocr/paddle_ocr/上/part01/page_0130.txt` 与 `page_0131.txt`。
- 不改行列、表题、数值和最终阅读版正文。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 地层系统表已核说明清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 清理 `LYG-上-T001` notes 中的 `建议对照原图复核` 交付前措辞，改为 page_0130/page_0131 跨页核录证据说明。
- 未改表格数据；同步 `output/structured_tables/index.html` 中 TABLES 数据。
- 报告：`output/reports/t001_verified_note_cleanup_20260705.md`。
""",
    )

    print("updated=LYG-上-T001")
    print(f"structured_index_updated={structured_changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

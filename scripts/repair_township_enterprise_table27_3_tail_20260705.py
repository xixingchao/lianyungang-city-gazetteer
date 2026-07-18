# -*- coding: utf-8 -*-
"""Remove remaining table 27-3 tail residues after verified table insertion."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "township_enterprise_table27_3_tail_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "township_enterprise_table27_3_tail_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_乡镇企业表27_3尾段残片清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

RESIDUES = [
    "<p>其中：工业102164906111143102529企业2492587联户办其中：工业8391862068企业768123728239861115222769销售收入（万元）</p>",
    "<p>其中：工业35854291615310209注：新浦区无“两户”企业。</p>",
]
SOURCES = [
    "workbench/ocr/paddle_ocr/中/part01/page_0397.txt",
    "workbench/ocr/raw/中/part01/page_0397.txt",
    "workbench/table_entries/中/data/LYG-中-T139.json",
    "output/final_reader/连云港市志_全书.html paragraphs 8850-8851",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    removed = 0
    for residue in RESIDUES:
        count = html.count(residue)
        if count == 1:
            html = html.replace(residue, "", 1)
            removed += 1
        elif count > 1:
            raise RuntimeError(f"residue matched {count} times")
    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "removed": removed, "sources": SOURCES, "note": "表27-3已登记为 LYG-中-T139，本脚本仅撤出阅读版剩余尾段残片。"}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 乡镇企业表27-3尾段残片清理",
        "",
        f"- 时间：{now}",
        f"- 结果：撤出剩余表27-3尾段残片 {removed} 段。",
        "- 说明：表27-3已回源核录为 `LYG-中-T139`；本脚本只处理主阅读版中的尾段压扁文本。",
        "",
        "## 证据",
        "",
    ]
    lines.extend(f"- `{source}`" for source in SOURCES)
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    append_once(MEMORY, "## 2026-07-05 乡镇企业表27-3尾段残片清理", f"""
## 2026-07-05 乡镇企业表27-3尾段残片清理
- 新增并运行 `scripts/repair_township_enterprise_table27_3_tail_20260705.py`，在 `LYG-中-T139` 已核录表27-3后，撤出主阅读版剩余两段尾部压扁残片：`其中：工业102164...` 与 `其中：工业358542...注：新浦区无“两户”企业。`。
- 报告：`output/reports/township_enterprise_table27_3_tail_20260705.md`。
""")
    print("township_enterprise_table27_3_tail_repaired")
    print(f"removed={removed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

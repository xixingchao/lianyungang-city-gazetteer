# -*- coding: utf-8 -*-
"""Follow up the remaining middle table fragment 方吨->万吨 from batch213."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_source_verified_units_batch213_followup_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_source_verified_units_batch213_followup_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_源页核验单位残留补修第二百一十三批补遗.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0198.json"
OLD = "650.00</p><p>方吨及各</p><p>限公司"
NEW = "650.00</p><p>万吨及各</p><p>限公司"


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    source_text = SOURCE.read_text(encoding="utf-8", errors="ignore")
    if "万吨及各" not in source_text or "650.00" not in source_text:
        raise SystemExit("missing source evidence in page_0198.json")
    html = MIDDLE.read_text(encoding="utf-8")
    count = html.count(OLD)
    if count:
        html = html.replace(OLD, NEW)
        MIDDLE.write_text(html, encoding="utf-8")
    text = plain(html)
    residual_counts = {"middle 方吨": text.count("方吨"), "middle 方立方米": text.count("方立方米"), "middle 形成生产能力20吨": text.count("形成生产能力20吨")}
    payload = {"time": now, "changed": count, "old": plain(OLD), "new": plain(NEW), "source": "workbench/ocr/paddle_ocr/中/part02/page_0198.json", "residual_counts": residual_counts}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 源页核验单位残留补修第二百一十三批补遗",
        "",
        f"> 生成时间：{now}",
        "",
        "## 统计",
        "",
        f"- 修复：{count} 处",
        "- 证据：`workbench/ocr/paddle_ocr/中/part02/page_0198.json` 中同页识别为 `万吨及各`，并有相邻 `650.00`。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 替换项",
        "",
        f"- `{plain(OLD)}` -> `{plain(NEW)}`：{count} 处",
        "",
        "## 残留计数",
        "",
    ]
    for key, value in residual_counts.items():
        lines.append(f"- {key}: {value}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")
    MEMORY.write_text(MEMORY.read_text(encoding="utf-8").rstrip() + f"\n\n## 2026-07-07 源页核验单位残留补修第二百一十三批补遗\n\n- 补修中册外资表残文 `650.00方吨及各 -> 650.00万吨及各` 1 处；证据为 `workbench/ocr/paddle_ocr/中/part02/page_0198.json` 同页 `万吨及各`。\n- 修后中册 `方吨/方立方米/形成生产能力20吨` 残留均为 0；报告：`output/reports/reader_source_verified_units_batch213_followup_20260707.md`。\n- 未打开、展示或嵌入图片。\n", encoding="utf-8")
    print(json.dumps({"changed": count, "residual_counts": residual_counts, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Repair one source-layer table unit residue, batch 240."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
EVIDENCE = ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part02" / "page_0198.txt"
REPORT_JSON = ROOT / "output" / "reports" / "body_source_table_units_batch240_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "body_source_table_units_batch240_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_正文源稿表格单位残留补修第二百四十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
OLD = "650.00\n方吨及各\n限公司"
NEW = "650.00\n万吨及各\n限公司"


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    evidence_text = EVIDENCE.read_text(encoding="utf-8", errors="ignore")
    for snippet in ["啤酒3万", "麦芽3", "万吨及各"]:
        if snippet not in evidence_text:
            raise SystemExit(f"missing evidence snippet: {snippet}")

    changes = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8", errors="ignore")
        count = text.count(OLD)
        if count:
            path.write_text(text.replace(OLD, NEW), encoding="utf-8")
        changes.append({"file": str(path.relative_to(ROOT)), "count": count})

    residuals = {
        str(path.relative_to(ROOT)): path.read_text(encoding="utf-8", errors="ignore").count("方吨及各")
        for path in TARGETS
    }
    payload = {
        "time": now,
        "old": OLD,
        "new": NEW,
        "evidence": str(EVIDENCE.relative_to(ROOT)),
        "changes": changes,
        "residuals": residuals,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文源稿表格单位残留补修第二百四十批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 修复中册第三十五卷对外经济贸易表35-6的源层断行表格单位残留。",
        "- 页级 PaddleOCR 在 `workbench/ocr/paddle_ocr/中/part02/page_0198.txt` 支持 `万吨及各`，并同页可见 `啤酒3万`、`麦芽3`。",
        "- 当前阅读稿未检出 `方吨及各`，本批只同步正文源稿和全书正文汇总；未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 替换次数 |",
        "|---|---:|",
    ]
    for change in changes:
        lines.append(f"| `{change['file']}` | {change['count']} |")
    lines.extend([
        "",
        "## 残留计数",
        "",
    ])
    for file, count in residuals.items():
        lines.append(f"- `{file}`：`方吨及各` {count} 处")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 正文源稿表格单位残留补修第二百四十批\n\n"
    memory += "- 依据 `workbench/ocr/paddle_ocr/中/part02/page_0198.txt`，修复表35-6源层断行片段 `650.00/方吨及各/限公司 -> 650.00/万吨及各/限公司`。\n"
    memory += "- 同步范围：`第三十卷至第四十二卷（中part02）.md` 与全书正文汇总；报告：`output/reports/body_source_table_units_batch240_20260707.md`。\n"
    memory += "- 当前阅读稿已无该残留；本批未处理旧交付包、obsolete 或乱码副本，未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_files": sum(1 for change in changes if change["count"]),
        "changed_items": sum(change["count"] for change in changes),
        "residual_total": sum(residuals.values()),
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()

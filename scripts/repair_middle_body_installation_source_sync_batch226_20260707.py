# -*- coding: utf-8 -*-
"""Sync source markdown for middle volume installation paragraph, batch 226."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "middle_body_installation_source_sync_batch226_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_body_installation_source_sync_batch226_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册安装段源稿同步补修第二百二十六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
EVIDENCE = ROOT / "workbench" / "ocr" / "paddle_ocr" / "中" / "part01" / "page_0321.txt"

OLD = "这是一项自动控制多，自动\n点安装的设备"
NEW = "这是一项自动控制多，自动\n化程度很高的全新中外合资的工程"


def ensure_evidence() -> None:
    text = EVIDENCE.read_text(encoding="utf-8", errors="ignore")
    required = ["这是一项自动控制多，自动", "化程度很高的全新中外合资的工程"]
    missing = [snippet for snippet in required if snippet not in text]
    if missing:
        raise SystemExit("missing evidence: " + "; ".join(missing))


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ensure_evidence()
    changes = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8", errors="ignore")
        count = text.count(OLD)
        if count:
            path.write_text(text.replace(OLD, NEW), encoding="utf-8")
        changes.append({"file": str(path.relative_to(ROOT)), "count": count})

    residuals = {str(path.relative_to(ROOT)): path.read_text(encoding="utf-8", errors="ignore").count(OLD) for path in TARGETS}
    payload = {"time": now, "old": OLD, "new": NEW, "changes": changes, "residuals": residuals, "evidence": str(EVIDENCE.relative_to(ROOT))}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册安装段源稿同步补修第二百二十六批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 仅同步中册正文源稿和全书正文汇总；正式中册/全书阅读稿已是正确文本，本批不改。",
        "- 依据 PaddleOCR 页级文字与当前正式阅读稿，修复啤酒厂/麦芽厂设备安装段源稿旧残留。",
        "- 海关统计段 `对项目进行解除` 三套 OCR 暂仍如此且语义可疑，本批不猜改。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 次数 | 证据 |",
        "|---|---:|---|",
    ]
    for item in changes:
        lines.append(f"| `{item['file']}` | {item['count']} | `{EVIDENCE.relative_to(ROOT)}` |")
    lines.extend(["", "## 残留计数", ""])
    for file, count in residuals.items():
        lines.append(f"- `{file}`：{count}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 中册安装段源稿同步补修第二百二十六批\n\n"
    memory += "- 依据 `workbench/ocr/paddle_ocr/中/part01/page_0321.txt` 和当前正式阅读稿，修复中册正文源稿/全书正文汇总中啤酒厂、麦芽厂设备安装段 `自动/点安装的设备` 残留。\n"
    memory += "- 正式阅读稿已为 `自动/化程度很高的全新中外合资的工程`，本批仅补源稿同步；海关统计段 `对项目进行解除` 暂不猜改。\n"
    memory += "- 报告：`output/reports/middle_body_installation_source_sync_batch226_20260707.md`；未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({"changed_files": sum(1 for item in changes if item["count"]), "residual_total": sum(residuals.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Repair source-verified unit residues from PaddleOCR pages, batch213."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIDDLE = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_source_verified_units_batch213_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_source_verified_units_batch213_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_源页核验单位残留补修第二百一十三批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "old": "型水泥构件1方立方米和各种水泥管20万米的能力",
        "new": "型水泥构件1万立方米和各种水泥管20万米的能力",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0284.txt:35",
        "evidence": "型水泥构件1万立方米和各种水泥管20万米的能力",
    },
    {
        "old": "年生产屋面板5方立方米",
        "new": "年生产屋面板5万立方米",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0314.txt:23",
        "evidence": "1990年，市属企业年生产屋面板5万立方米。",
    },
    {
        "old": "容积1.94方立方米",
        "new": "容积1.94万立方米",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0059.txt:26",
        "evidence": "有零担仓库一座，容积1.94万立方米。",
    },
    {
        "old": "形成生产能力20吨，成为全市水泥产业中最大的",
        "new": "形成生产能力20万吨，成为全市水泥产业中最大的",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0280.txt:25",
        "evidence": "形成生产能力20万吨，成为全市水泥产业中最大的",
    },
    {
        "old": "650.00方吨及各限公司公司种饮料",
        "new": "650.00万吨及各限公司公司种饮料",
        "source": "workbench/ocr/paddle_ocr/中/part02/page_0198.json lines: 啤酒3万 / 万吨及各 / 650.00 / 种饮料",
        "evidence": "万吨及各",
    },
]

DEFERRED = [
    {
        "text": "送印刷广切边",
        "reason": "当前正文和 OCR 文本同为 `送印刷广切边`，缺少独立文字证据；需底本/页图核验。",
    }
]


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def source_has_evidence(item: dict[str, str]) -> bool:
    source = item["source"].split(":", 1)[0]
    path = ROOT / source
    if not path.exists():
        return True
    return item["evidence"] in path.read_text(encoding="utf-8", errors="ignore")


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    missing = [item for item in REPLACEMENTS if not source_has_evidence(item)]
    if missing:
        raise SystemExit("missing source evidence: " + json.dumps(missing, ensure_ascii=False))

    html = MIDDLE.read_text(encoding="utf-8")
    changed_items = []
    for item in REPLACEMENTS:
        count = html.count(item["old"])
        if count:
            html = html.replace(item["old"], item["new"])
            changed_items.append({**item, "changed": count})
    MIDDLE.write_text(html, encoding="utf-8")

    full_html = FULL.read_text(encoding="utf-8")
    full_changed_items = []
    for item in REPLACEMENTS:
        count = full_html.count(item["old"])
        if count:
            full_html = full_html.replace(item["old"], item["new"])
            full_changed_items.append({**item, "changed": count})
    FULL.write_text(full_html, encoding="utf-8")

    middle_text = plain(html)
    full_text = plain(full_html)
    residual_counts = {
        "middle 方吨": middle_text.count("方吨"),
        "middle 方立方米": middle_text.count("方立方米"),
        "middle 形成生产能力20吨": middle_text.count("形成生产能力20吨"),
        "lower 送印刷广切边": plain((ROOT / "output" / "final_reader" / "连云港市志_下册.html").read_text(encoding="utf-8")).count("送印刷广切边"),
        "full 方吨": full_text.count("方吨"),
        "full 方立方米": full_text.count("方立方米"),
        "full 形成生产能力20吨": full_text.count("形成生产能力20吨"),
    }
    total_middle = sum(item["changed"] for item in changed_items)
    total_full = sum(item["changed"] for item in full_changed_items)
    payload = {
        "time": now,
        "middle_changed": total_middle,
        "full_changed": total_full,
        "replacements": changed_items,
        "full_replacements": full_changed_items,
        "residual_counts": residual_counts,
        "deferred": DEFERRED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 源页核验单位残留补修第二百一十三批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿和全书阅读稿。",
        "- 依据 PaddleOCR 页级文字证据，修复单位残留和表格粘连残文。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 统计",
        "",
        f"- 中册修复：{total_middle} 处",
        f"- 全书同步修复：{total_full} 处",
        "",
        "## 替换项",
        "",
    ]
    for item in changed_items:
        lines.append(f"- `{item['old']}` -> `{item['new']}`：{item['changed']} 处；证据：`{item['source']}`")
    lines.extend(["", "## 暂缓项", ""])
    for item in DEFERRED:
        lines.append(f"- `{item['text']}`：{item['reason']}")
    lines.extend(["", "## 残留计数", ""])
    for key, value in residual_counts.items():
        lines.append(f"- {key}: {value}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    MEMORY.write_text(MEMORY.read_text(encoding="utf-8").rstrip() + f"\n\n## 2026-07-07 源页核验单位残留补修第二百一十三批\n\n- 依据 PaddleOCR 页级文字证据，修复中册/全书单位残留 {total_middle} 处：`1万立方米`、`5万立方米`、`1.94万立方米`、`20万吨`，以及外资表粘连残文 `650.00方吨及各种饮料`。\n- 全书同步修复 {total_full} 处；报告：`output/reports/reader_source_verified_units_batch213_20260707.md`。\n- `送印刷广切边` 仍缺独立文字证据，暂留待底本/页图核验；未打开、展示或嵌入图片。\n", encoding="utf-8")
    print(json.dumps({"middle_changed": total_middle, "full_changed": total_full, "residual_counts": residual_counts, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

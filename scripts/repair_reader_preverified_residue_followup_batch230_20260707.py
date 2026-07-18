# -*- coding: utf-8 -*-
"""Follow-up repair for source-backed residues surfaced after batch 229."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_preverified_residue_followup_batch230_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_preverified_residue_followup_batch230_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_已回源正文残留同步回填第二百三十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ITEMS = [
    ("中药加工炮制生产由原来的手</p><p>工操作遂步被机械设备所代替", "中药加工炮制生产由原来的手</p><p>工操作逐步被机械设备所代替", "workbench/ocr/paddle_ocr/中/part01/page_0122.txt"),
    ("一日西域通往内地的陆地丝绸之路逐遂步问东延伸所至", "一曰西域通往内地的陆地丝绸之路逐步向东延伸所至", "output/reports/reader_readability_source_backed_batch12_20260704.json"),
    ("日西域通往内地的陆地丝绸之路逐遂步问东延伸所至", "曰西域通往内地的陆地丝绸之路逐步向东延伸所至", "output/reports/reader_readability_source_backed_batch12_20260704.json"),
    ("学习、教育方法遂步改进", "学习、教育方法逐步改进", "output/reports/reader_readability_source_backed_batch8_20260704.json"),
    ("新浦的手工业生产遂步向机器生产发展", "新浦的手工业生产逐步向机器生产发展", "output/reports/reader_readability_source_backed_batch10_20260704.json"),
    ("经济遂步恢复。在生产发展的基础上", "经济逐步恢复。在生产发展的基础上", "output/reports/reader_readability_source_backed_batch9_20260704.json"),
    ("合同定购，遂步", "合同定购，逐步", "workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md"),
    ("座地面水广一茅口水厂计划任务书", "座地面水厂—茅口水厂计划任务书", "workbench/ocr/paddle_ocr/上/part02/page_0062.txt"),
    ("日供水2.5方吨的茅口", "日供水2.5万吨的茅口", "workbench/ocr/paddle_ocr/上/part02/page_0062.txt"),
    ("市造纸广科协财务收支情况进行审计，审计认为该广科协", "市造纸厂科协财务收支情况进行审计，审计认为该厂科协", "workbench/ocr/paddle_ocr/上/part02/page_0184.txt"),
    ("市桐木广的拼板加工机器", "市桐木厂的拼板加工机器", "workbench/ocr/paddle_ocr/中/part02/page_0190.txt"),
]
EVIDENCE_SNIPPETS = {
    "workbench/ocr/paddle_ocr/中/part01/page_0122.txt": "逐步被机械设备所代替",
    "workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md": "合同定购，逐步",
    "workbench/ocr/paddle_ocr/上/part02/page_0062.txt": "座地面水厂—茅口水厂计划任务书",
    "workbench/ocr/paddle_ocr/上/part02/page_0184.txt": "市造纸厂科协财务收支情况进行审计，审计认为该厂科协",
    "workbench/ocr/paddle_ocr/中/part02/page_0190.txt": "市桐木厂的拼板加工机器",
    "output/reports/reader_readability_source_backed_batch8_20260704.json": "学习、教育方法逐步改进",
    "output/reports/reader_readability_source_backed_batch9_20260704.json": "经济逐步恢复。在生产发展的基础上",
    "output/reports/reader_readability_source_backed_batch10_20260704.json": "新浦的手工业生产逐步向机器生产发展",
    "output/reports/reader_readability_source_backed_batch12_20260704.json": "逐步向东延伸所至",
}


def ensure_evidence() -> None:
    missing = []
    for rel, snippet in EVIDENCE_SNIPPETS.items():
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        if snippet not in text:
            missing.append(f"{rel}: {snippet}")
    if missing:
        raise SystemExit("missing evidence: " + "; ".join(missing))


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ensure_evidence()
    changes = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        file_items = []
        for old, new, evidence in ITEMS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                file_items.append({"old": old, "new": new, "count": count, "evidence": evidence})
        if text != original:
            path.write_text(text, encoding="utf-8")
        changes.append({"file": str(path.relative_to(ROOT)), "items": file_items})

    residuals = {old: {str(path.relative_to(ROOT)): path.read_text(encoding="utf-8", errors="ignore").count(old) for path in TARGETS} for old, _, _ in ITEMS}
    payload = {"time": now, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 已回源正文残留同步回填第二百三十批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 处理第二百二十九批后复查发现的 HTML 分段变体和源稿残留。",
        "- 所有替换均由页级 OCR 或既有回源报告支撑；未做全局猜改。",
        "- 未打开、展示或嵌入图片。",
        "",
        "## 修改统计",
        "",
        "| 文件 | 原文 | 新文 | 次数 | 证据 |",
        "|---|---|---|---:|---|",
    ]
    for item in changes:
        for change in item["items"]:
            lines.append(f"| `{item['file']}` | `{change['old']}` | `{change['new']}` | {change['count']} | `{change['evidence']}` |")
    lines.extend(["", "## 残留计数", ""])
    for old, files in residuals.items():
        lines.append(f"- `{old}`：{sum(files.values())}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text(REPORT_MD.read_text(encoding="utf-8"), encoding="utf-8")

    memory = MEMORY.read_text(encoding="utf-8", errors="ignore").rstrip()
    memory += "\n\n## 2026-07-07 已回源正文残留同步回填第二百三十批\n\n"
    memory += "- 依据页级 OCR 与 20260704 既有回源报告，补修第二百二十九批后发现的 HTML 分段变体和源稿残留。\n"
    memory += "- 覆盖 `遂步/逐遂步问东` 变体、茅口水厂 `水广一/方吨`、造纸厂科协 `广->厂`、市桐木厂拼板加工机器。报告：`output/reports/reader_preverified_residue_followup_batch230_20260707.md`。\n"
    memory += "- 未做全局替换；未打开、展示或嵌入图片。\n"
    MEMORY.write_text(memory + "\n", encoding="utf-8")

    print(json.dumps({
        "changed_files": sum(1 for item in changes if item["items"]),
        "changed_items": sum(change["count"] for item in changes for change in item["items"]),
        "residual_total": sum(sum(files.values()) for files in residuals.values()),
        "report": str(REPORT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()

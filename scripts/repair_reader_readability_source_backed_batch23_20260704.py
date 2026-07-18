# -*- coding: utf-8 -*-
"""Twenty-third source-backed reader readability repair batch."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_source_backed_batch23_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_source_backed_batch23_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十三批正文残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    (
        "淮海大学校名误识",
        "准海大学",
        "淮海大学",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:5486；:14870；workbench/ocr/paddle_ocr/merged/连云港市志_上_part02_PaddleOCR汇总.md:12458",
    ),
    (
        "大事记烈士字误识（李少堂等）",
        "李少堂等10人为革命烈土。",
        "李少堂等10人为革命烈士。",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:5276-5278",
    ),
    (
        "大事记烈士字误识（朱爱周）",
        "追认朱爱周为革命烈土的批复",
        "追认朱爱周为革命烈士的批复",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:5527-5529",
    ),
    (
        "抗日山烈士英名字误识",
        "铭刻着3576位烈土的英名",
        "铭刻着3576位烈士的英名",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:3588-3592",
    ),
    (
        "吴伦东民兵段烈士字误识",
        "被追认为革命烈土，被南京军区授予“民兵英雄”称号",
        "被追认为革命烈士，被南京军区授予“民兵英雄”称号",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:5279-5281；workbench/body_chapters/连云港市志_全书_正文汇总.md:114864-114865",
    ),
    (
        "纺织章毛巾企业误识",
        "市第五毛币厂",
        "市第五毛巾厂",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part03_PaddleOCR汇总.md:16688-16691",
    ),
    (
        "纺织章毛巾织机误识",
        "毛市织机329台",
        "毛巾织机329台",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part03_PaddleOCR汇总.md:16688-16691",
    ),
    (
        "纺织章产量单位误识",
        "灌云县12方条",
        "灌云县12万条",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part03_PaddleOCR汇总.md:16688-16691",
    ),
    (
        "科技章毛巾厂误识",
        "市毛币厂设计的22个毛巾花型图案",
        "市毛巾厂设计的22个毛巾花型图案",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part03_PaddleOCR汇总.md:16630-16639；:16688-16691",
    ),
    (
        "科技章割绒装置单位误识",
        "市毛币厂“割绒刀具保护装置研究”",
        "市毛巾厂“割绒刀具保护装置研究”",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part03_PaddleOCR汇总.md:16673-16676；:16688-16691",
    ),
    (
        "七五计划重点项目单位误识",
        "新海电广、淮海大学等重点项目的投人",
        "新海电厂、淮海大学等重点项目的投入",
        "workbench/ocr/paddle_ocr/merged/连云港市志_上_part02_PaddleOCR汇总.md:12456-12458",
    ),
]

CHECK_OLDS = [old for _label, old, _new, _source in REPLACEMENTS]


def append_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    targets = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        items = []
        for label, old, new, source in REPLACEMENTS:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            items.append({"label": label, "old": old, "new": new, "source": source, "count": count})
        path.write_text(text, encoding="utf-8")
        verify = path.read_text(encoding="utf-8")
        residuals = [old for old in CHECK_OLDS if old in verify]
        if residuals:
            raise RuntimeError(f"replacement verification failed for {path}: {residuals}")
        targets.append({"target": str(path), "changed": sum(item["count"] for item in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(item["changed"] for item in targets)
    payload = {
        "time": now,
        "scope": "第二十三批正文残留回源修复",
        "targets": targets,
        "total_replacements": total,
        "verified_items": len(REPLACEMENTS),
        "principle": "只修复已由 OCR 汇总或同章可靠上下文支撑的固定错字串。",
        "deferred": ["人物传大量加人中国共产党", "剩余零散烈土/方字单位", "红领币禁赌宣传队"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第二十三批正文残留回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：只修已由 OCR 汇总或同章可靠上下文支撑的固定错字串。",
        f"- 核验项：{len(REPLACEMENTS)} 项。",
        f"- 本次替换：{total} 处。",
        "- 暂缓：人物传大量 `加人中国共产党`、剩余零散 `烈土/方` 单位、`红领币禁赌宣传队`。",
        "",
        "## 文件",
    ]
    for target in targets:
        lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines += ["", "## 明细"]
    for label, _old, _new, source in REPLACEMENTS:
        count = sum(item["count"] for target in targets for item in target["items"] if item["label"] == label)
        lines.append(f"- {label}：依据 `{source}`；命中 {count} 处。")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")

    marker = "## 2026-07-04 第二十三批正文残留回源修复"
    memory = f"""
{marker}
- 修复 `准海大学`、大事记/民兵段中已核源的 `革命烈土`，以及纺织章 `毛币厂/毛市织机/12方条` 等固定残留。
- 同步目标：`output/final_reader/连云港市志_全书.html` 与 `workbench/body_chapters/连云港市志_全书_正文汇总.md`。
- 依据：`workbench/ocr/paddle_ocr/merged/连云港市志_上_part01_PaddleOCR汇总.md:3588-3592`、`:5276-5290`、`:5486`、`:5527-5529`、`:14870`，`上_part02_PaddleOCR汇总.md:12456-12458`，`上_part03_PaddleOCR汇总.md:16688-16691`。
- 暂缓：人物传大量 `加人中国共产党` 和零散 `烈土/方` 单位仍需逐页核源。
- 报告：`output/reports/reader_readability_source_backed_batch23_20260704.md`。
"""
    append_memory(MEMORY, marker, memory)


if __name__ == "__main__":
    main()

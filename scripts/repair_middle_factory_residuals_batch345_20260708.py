# -*- coding: utf-8 -*-
"""Repair source-backed middle-volume factory `该广/该厂` residuals."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "middle_factory_residuals_batch345_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "middle_factory_residuals_batch345_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_中册企业厂字残留补修第三百四十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 中册企业厂字残留补修第三百四十五批"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
]

REPLACEMENTS = [
    {
        "old": "1983年4月，季道池主持",
        "new": "1983年4月，李道池主持",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0027.txt` 明确为“1983年4月，李道池主持该厂工作后”。",
    },
    {
        "old": "该广工作后",
        "new": "该厂工作后",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0027.txt` 明确为“该厂工作后”。",
    },
    {
        "old": "该广“茶\n叶盒礼品包装”",
        "new": "该厂“茶\n叶盒礼品包装”",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0051.txt` 明确为“该厂‘茶叶盒礼品包装’”。",
    },
    {
        "old": "该广“茶 叶盒礼品包装”",
        "new": "该厂“茶 叶盒礼品包装”",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0051.txt` 明确为“该厂‘茶叶盒礼品包装’”。",
    },
    {
        "old": "该广位于赣榆县徐福镇",
        "new": "该厂位于赣榆县徐福镇",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0074.txt` 明确为“该厂位于赣榆县徐福镇”。",
    },
    {
        "old": "广内设5个职能科室",
        "new": "厂内设5个职能科室",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0074.txt` 明确为“厂内设5个职能科室”。",
    },
    {
        "old": "该广为市属全民企业",
        "new": "该厂为市属全民企业",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0225.txt` 明确为“该厂为市属全民企业”。",
    },
    {
        "old": "该广走技术引进和技术改造的道路",
        "new": "该厂走技术引进和技术改造的道路",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0257.txt` 明确为“该厂走技术引进和技术改造的道路”。",
    },
    {
        "old": "该广是生产硅微粉的专业工厂",
        "new": "该厂是生产硅微粉的专业工厂",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0263.txt` 明确为“该厂是生产硅微粉的专业工厂”。",
    },
    {
        "old": "该广贷款21万元",
        "new": "该厂贷款21万元",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0264.txt` 明确为“该厂贷款21万元”。",
    },
    {
        "old": "该广研制生产的各种异型、弧型轻质耐火保温砖",
        "new": "该厂研制生产的各种异型、弧型轻质耐火保温砖",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0273.txt` 明确为“该厂研制生产的各种异型、弧型轻质耐火保温砖”。",
    },
    {
        "old": "1975年，该广更名为连云港市",
        "new": "1975年，该厂更名为连云港市",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part01/page_0279.txt` 明确为“1975年，该厂更名为连云港市水泥厂”。",
    },
]

CHECK_TERMS = [
    "季道池主持",
    "李道池主持",
    "该广工作后",
    "该广“茶",
    "该广位于赣榆县徐福镇",
    "广内设5个职能科室",
    "该广为市属全民企业",
    "该广走技术引进",
    "该广是生产硅微粉",
    "该广贷款21万元",
    "该广研制生产",
    "该广更名为连云港市",
    "该广",
    "广内设",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_fix() -> tuple[list[dict], dict[str, int]]:
    changes: list[dict] = []
    for path in TARGETS:
        if not path.exists():
            continue
        text = read(path)
        updated = text
        for item in REPLACEMENTS:
            count = updated.count(item["old"])
            if not count:
                continue
            updated = updated.replace(item["old"], item["new"])
            changes.append({"path": rel(path), "old": item["old"], "new": item["new"], "count": count, "evidence": item["evidence"]})
        if updated != text:
            path.write_text(updated, encoding="utf-8")
    residuals = {term: sum(read(path).count(term) for path in TARGETS if path.exists()) for term in CHECK_TERMS}
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 中册企业厂字残留补修 batch345",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正式全书、正式中册、全书正文汇总、中册 part01 当前源稿。",
        "- 依据：中册 part01 page_0027、0051、0074、0225、0257、0263、0264、0273、0279 页级 PaddleOCR 成句证据。",
        "- 原则：只替换完整企业语境短语；不作 `广 -> 厂` 或姓名宽泛替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    if changes:
        for item in changes:
            lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['evidence']}")
    else:
        lines.append("- 本次未产生新增替换。")
    lines.extend(["", "## 检查结果", ""])
    for term, count in residuals.items():
        lines.append(f"- `{term}`：{count}")
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据中册 part01 多个页级 PaddleOCR 成句证据，补修企业语境 `该广/广内 -> 该厂/厂内` 及 `1983年4月，季道池主持 -> 1983年4月，李道池主持`，同步正式阅读稿与中册 part01 源稿，共 {total} 处。
- 本批后检查范围：`季道池主持` {residuals['季道池主持']}，`该广` {residuals['该广']}，`广内设` {residuals['广内设']}。
- 未作 `广 -> 厂` 或姓名宽泛替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/middle_factory_residuals_batch345_20260708.md`；进度：`output/reports/progress/20260708_中册企业厂字残留补修第三百四十五批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    if next_start < 0:
        new = old[:start].rstrip() + "\n\n" + block.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + block.strip() + old[next_start:]
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    changes, residuals = apply_fix()
    total = sum(item["count"] for item in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "changes": changes, "residuals": residuals, "replacements": REPLACEMENTS}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(changes, residuals)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total, residuals)
    print(f"total={total}")
    print(f"residuals={residuals}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()

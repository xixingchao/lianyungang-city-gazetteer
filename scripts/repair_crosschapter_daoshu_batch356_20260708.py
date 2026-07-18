# -*- coding: utf-8 -*-
"""Repair source-backed cross-chapter 导述/述南 residuals."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "crosschapter_daoshu_batch356_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "crosschapter_daoshu_batch356_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_跨章节导沭沭南残留补修第三百五十六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 跨章节导沭沭南残留补修第三百五十六批"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
]

REPLACEMENTS = [
    {
        "old": "导述水利民工粮",
        "new": "导沭水利民工粮",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0213.txt` 明确为“导沭水利民工粮”。",
    },
    {
        "old": "导述粮任务",
        "new": "导沭粮任务",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0213.txt` 明确为“导沭粮任务”。",
    },
    {
        "old": "述南西部",
        "new": "沭南西部",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0404.txt` 明确为“沭南西部”。",
    },
    {
        "old": "开展导述工程",
        "new": "开展导沭工程",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/中/part02/page_0483.txt` 明确为“开展导沭工程”。",
    },
    {
        "old": "《导述经沙入海工程计划初稿。",
        "new": "《导沭经沙入海工程计划初稿》。",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/下/part01/page_0436.txt` 明确书名为“《导沭经沙人海工程计划初稿》。”；正式阅读稿同段已规范为“入海”。",
    },
    {
        "old": "《导沭经沙入海工程计划初稿。",
        "new": "《导沭经沙入海工程计划初稿》。",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/下/part01/page_0436.txt` 显示书名号应闭合；正式阅读稿同段已规范为“入海”。",
    },
    {
        "old": "《导述经沙人海工程计划初稿。",
        "new": "《导沭经沙人海工程计划初稿》。",
        "evidence": "页级 PaddleOCR `workbench/ocr/paddle_ocr/下/part01/page_0436.txt` 明确为“《导沭经沙人海工程计划初稿》。”；本处只修 `导述` 和书名号，不据此改 `人海`。",
    },
]

CHECK_TERMS = [
    "导述水利民工粮",
    "导述粮任务",
    "开展导述工程",
    "述南西部",
    "导述经沙入海工程计划初稿",
    "导述经沙人海工程计划初稿",
    "《导沭经沙入海工程计划初稿。",
    "《导沭经沙人海工程计划初稿。",
    "导述",
    "述南",
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
        "# 跨章节导沭沭南残留补修 batch356",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正式全书/中册/下册阅读稿、全书正文汇总、中册 part02 源稿、下册 part01 源稿。",
        "- 依据：中册 part02 page_0213、page_0404、page_0483 与下册 part01 page_0436 页级 PaddleOCR 成句证据。",
        "- 原则：只替换已定位的完整短语；不作 `述 -> 沭`、`人 -> 入` 全局替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    if changes:
        for item in changes:
            old = item["old"].replace("\n", "\\n")
            new = item["new"].replace("\n", "\\n")
            lines.append(f"- `{item['path']}`：`{old}` -> `{new}`；次数 {item['count']}；依据：{item['evidence']}")
    else:
        lines.append("- 本次未产生新增替换。")
    lines.extend(["", "## 检查结果", ""])
    for term, count in residuals.items():
        lines.append(f"- `{term}`：{count}")
    lines.extend([
        "",
        "## 保留边界",
        "",
        "- 下册源稿 `导沭经沙人海工程计划初稿` 的 `人海` 暂按 OCR 原样保留；正式阅读稿同段为 `入海`。",
        "- 全书正文汇总中其它 `新述河/新沐河/述北/导述` 残留继续按页级证据另批核对。",
        "- 未处理 OCR 源文件、backup、obsolete、历史交付包。",
    ])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据中册 part02 page_0213、page_0404、page_0483 与下册 part01 page_0436 页级 PaddleOCR 成句证据，补修跨章节 `导述/述南` 残留，共 {total} 处。
- 代表修复：`导述水利民工粮 -> 导沭水利民工粮`、`导述粮任务 -> 导沭粮任务`、`述南西部 -> 沭南西部`、`开展导述工程 -> 开展导沭工程`、下册水利书名 `《导述经沙...初稿。 -> 《导沭经沙...初稿》。`。
- 本批后检查范围：`导述水利民工粮` {residuals['导述水利民工粮']}，`导述粮任务` {residuals['导述粮任务']}，`开展导述工程` {residuals['开展导述工程']}，`述南西部` {residuals['述南西部']}，未闭合 `《导沭经沙...初稿。` {residuals['《导沭经沙入海工程计划初稿。'] + residuals['《导沭经沙人海工程计划初稿。']}。
- 下册源稿 `导沭经沙人海工程计划初稿` 的 `人海` 暂按 OCR 原样保留；正式阅读稿同段为 `入海`；未作 `述 -> 沭`、`人 -> 入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/crosschapter_daoshu_batch356_20260708.md`；进度：`output/reports/progress/20260708_跨章节导沭沭南残留补修第三百五十六批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old[next_start:])
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    changes, residuals = apply_fix()
    total = sum(item["count"] for item in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "changes": changes, "residuals": residuals, "replacements": REPLACEMENTS, "targets": [rel(path) for path in TARGETS]}
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

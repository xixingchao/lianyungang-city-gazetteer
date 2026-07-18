# -*- coding: utf-8 -*-
"""Repair source-backed Wu Tongju water-title residues."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "wutongju_shu_titles_batch366_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "wutongju_shu_titles_batch366_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_武同举水利书名残留补修第三百六十六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 武同举水利书名残留补修第三百六十六批"

TARGETS = [
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
CHECK_FILES = TARGETS + [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_下册.html",
]
CHECK_TERMS = ["泗、沂、述", "沂沐偏重", "泗、沂、沭", "沂沭偏重", "人海口"]


@dataclass(frozen=True)
class Change:
    path: Path
    old: str
    new: str
    evidence: str


CHANGES = [
    Change(
        TARGETS[0],
        "《泗、沂、述分治合治之研究》",
        "《泗、沂、沭分治合治之研究》",
        "下/part02/page_0350 PaddleOCR 明确为《泗、沂、沭分治合治之研究》。",
    ),
    Change(
        TARGETS[1],
        "《泗、沂、述分治合治之研究》",
        "《泗、沂、沭分治合治之研究》",
        "下/part02/page_0350 PaddleOCR 明确为《泗、沂、沭分治合治之研究》。",
    ),
    Change(
        TARGETS[1],
        "《沂沐偏重筹泄淮泗宜蓄泄兼筹",
        "《沂沭偏重筹泄淮泗宜蓄泄兼筹",
        "下/part02/page_0350 PaddleOCR 明确为《沂沭偏重筹泄淮泗宜蓄泄兼筹论》。",
    ),
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_fix() -> tuple[list[dict], dict[str, dict[str, int]]]:
    changes: list[dict] = []
    for item in CHANGES:
        text = read(item.path)
        count = text.count(item.old)
        if count:
            item.path.write_text(text.replace(item.old, item.new), encoding="utf-8")
            changes.append({"path": rel(item.path), "old": item.old, "new": item.new, "count": count, "evidence": item.evidence})

    residuals: dict[str, dict[str, int]] = {}
    for path in CHECK_FILES:
        if not path.exists():
            continue
        text = read(path)
        hits = {term: text.count(term) for term in CHECK_TERMS if text.count(term)}
        if hits:
            residuals[rel(path)] = hits
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, dict[str, int]]) -> str:
    total = sum(c["count"] for c in changes)
    lines = [
        "# 武同举水利书名残留补修 batch366",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：下册源稿、全书正文汇总。正式 reader 已为正确文本，本批未改 reader。",
        "- 依据：`workbench/ocr/paddle_ocr/下/part02/page_0350.txt`。",
        "- 原则：只修完整书名短语；不作 `述 -> 沭`、`沐 -> 沭` 全局替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['evidence']}")
    if not changes:
        lines.append("- 本次未产生新增替换。")
    lines.extend(["", "## 残留检查", ""])
    if residuals:
        for path, hits in residuals.items():
            compact = "，".join(f"`{term}` {count}" for term, count in hits.items())
            lines.append(f"- `{path}`：{compact}")
    else:
        lines.append("- 检查范围未见目标残留词。")
    lines.extend([
        "",
        "## 保留边界",
        "",
        "- 表段 `获水村人海口` OCR 与精修源稿不一致，本批不处理，继续保留待单独视觉或权威源核验。",
        "- 未处理 OCR 源文件、backup、obsolete、历史交付包。",
    ])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, dict[str, int]]) -> None:
    full_hits = residuals.get("workbench/body_chapters/连云港市志_全书_正文汇总.md", {})
    block = f"""{MARKER}

- 依据下册 PaddleOCR `workbench/ocr/paddle_ocr/下/part02/page_0350.txt`，补修武同举传水利书名残留，共 {total} 处，范围为下册源稿、全书正文汇总；正式 reader 原已为正确文本，本批未改 reader。
- 修复：`泗、沂、述分治合治之研究 -> 泗、沂、沭分治合治之研究`，`沂沐偏重筹泄淮泗宜蓄泄兼筹 -> 沂沭偏重筹泄淮泗宜蓄泄兼筹`。
- 本批后全书汇总保留检查范围：`泗、沂、述` {full_hits.get('泗、沂、述', 0)}，`沂沐偏重` {full_hits.get('沂沐偏重', 0)}，`人海口` {full_hits.get('人海口', 0)}。
- 表段 `获水村人海口` OCR 与精修源稿不一致，本批保留待单独核验；未作 `述 -> 沭`、`沐 -> 沭`、`人 -> 入` 全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/wutongju_shu_titles_batch366_20260708.md`；进度：`output/reports/progress/20260708_武同举水利书名残留补修第三百六十六批.md`。
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
    total = sum(c["count"] for c in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "changes": changes, "residuals": residuals}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(changes, residuals)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total, residuals)
    print(f"total={total}")
    print(json.dumps(residuals, ensure_ascii=False, indent=2))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()

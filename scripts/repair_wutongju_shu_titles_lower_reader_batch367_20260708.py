# -*- coding: utf-8 -*-
"""Repair lower-reader Wu Tongju water-title residue."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "wutongju_shu_titles_lower_reader_batch367_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "wutongju_shu_titles_lower_reader_batch367_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_武同举水利书名单册读者页补修第三百六十七批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 武同举水利书名单册读者页补修第三百六十七批"
TARGET = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
OLD = "《泗、沂、述分治合治之研究》"
NEW = "《泗、沂、沭分治合治之研究》"
CHECK_TERMS = ["泗、沂、述", "沂沐偏重", "泗、沂、沭", "沂沭偏重"]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_fix() -> tuple[int, dict[str, int]]:
    text = read(TARGET)
    count = text.count(OLD)
    if count:
        TARGET.write_text(text.replace(OLD, NEW), encoding="utf-8")
        text = read(TARGET)
    hits = {term: text.count(term) for term in CHECK_TERMS if text.count(term)}
    return count, hits


def render(count: int, hits: dict[str, int]) -> str:
    compact = "，".join(f"`{term}` {value}" for term, value in hits.items()) or "无"
    return "\n".join([
        "# 武同举水利书名单册读者页补修 batch367",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{count}",
        "- 范围：下册 reader 单文件。",
        "- 依据：`workbench/ocr/paddle_ocr/下/part02/page_0350.txt` 明确为《泗、沂、沭分治合治之研究》。",
        "- 原则：只修完整书名短语；不作 `述 -> 沭` 全局替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
        f"- `{rel(TARGET)}`：`{OLD}` -> `{NEW}`；次数 {count}。" if count else "- 本次未产生新增替换。",
        "",
        "## 残留检查",
        "",
        f"- `{rel(TARGET)}`：{compact}",
    ]) + "\n"


def upsert_memory(count: int, hits: dict[str, int]) -> None:
    block = f"""{MARKER}

- 依据下册 PaddleOCR `workbench/ocr/paddle_ocr/下/part02/page_0350.txt`，补修下册 reader 中武同举传水利书名残留，共 {count} 处。
- 修复：`泗、沂、述分治合治之研究 -> 泗、沂、沭分治合治之研究`；本批只动完整书名短语，不作 `述 -> 沭` 全局替换。
- 本批后下册 reader 检查范围：`泗、沂、述` {hits.get('泗、沂、述', 0)}，`沂沐偏重` {hits.get('沂沐偏重', 0)}，`泗、沂、沭` {hits.get('泗、沂、沭', 0)}，`沂沭偏重` {hits.get('沂沭偏重', 0)}。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/wutongju_shu_titles_lower_reader_batch367_20260708.md`；进度：`output/reports/progress/20260708_武同举水利书名单册读者页补修第三百六十七批.md`。
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
    count, hits = apply_fix()
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": count, "target": rel(TARGET), "old": OLD, "new": NEW, "residuals": hits}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(count, hits)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(count, hits)
    print(f"total={count}")
    print(json.dumps(hits, ensure_ascii=False, indent=2))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()

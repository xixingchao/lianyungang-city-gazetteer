# -*- coding: utf-8 -*-
"""Full-summary-only 述阳 -> 沭阳 repairs backed by OCR fragments."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
OCR_ROOT = ROOT / "workbench" / "ocr" / "paddle_ocr"
REPORT = ROOT / "output" / "reports" / "shuyang_full_summary_ocr_batch329_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "shuyang_full_summary_ocr_batch329_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_全书汇总沭阳残留OCR补修第三百二十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def build_ocr_index() -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    for path in sorted(OCR_ROOT.rglob("*.txt")):
        text = read(path)
        if "沭阳" in text:
            items.append((str(path.relative_to(ROOT)).replace("\\", "/"), text))
    return items


def evidence_fragment(candidate: str) -> tuple[str, str] | None:
    idx = candidate.find("沭阳")
    if idx < 0:
        return None
    frag = candidate[max(0, idx - 12): idx + 24]
    for rel, text in OCR_INDEX:
        if frag in text:
            return rel, frag
    return None


OCR_INDEX = build_ocr_index()


def apply_repairs() -> tuple[list[dict], int]:
    lines = read(FULL).splitlines()
    changes: list[dict] = []
    new_lines: list[str] = []
    for line_no, line in enumerate(lines, 1):
        if "述阳" not in line:
            new_lines.append(line)
            continue
        candidate = line.replace("述阳", "沭阳")
        evidence = evidence_fragment(candidate)
        if evidence:
            rel, frag = evidence
            changes.append({
                "line": line_no,
                "old": line,
                "new": candidate,
                "count": line.count("述阳"),
                "evidence_file": rel,
                "evidence_fragment": frag,
            })
            new_lines.append(candidate)
        else:
            new_lines.append(line)
    if changes:
        FULL.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    residual = read(FULL).count("述阳")
    return changes, residual


def render(changes: list[dict], residual: int) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 全书汇总沭阳残留 OCR 补修 batch329",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：仅 `workbench/body_chapters/连云港市志_全书_正文汇总.md`。",
        "- 依据：将含 `述阳` 的全书汇总行改为 `沭阳` 后，必须在 PaddleOCR 文本中命中同句片段才替换。",
        "- 原则：不作全局 `述阳 -> 沭阳`；无 OCR 片段证据的残留继续保留。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(
            f"- 行 {item['line']}：`述阳` -> `沭阳`；次数 {item['count']}；依据：`{item['evidence_file']}` 命中片段 `{item['evidence_fragment']}`。"
        )
    lines.extend(["", "## 残留计数", "", f"- `述阳`：{residual}"])
    return "\n".join(lines) + "\n"


def append_memory(total: int, residual: int) -> None:
    marker = "## 2026-07-08 全书汇总沭阳残留OCR补修第三百二十九批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 仅处理 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 中的 `述阳` 残留：候选行替换为 `沭阳` 后，需在 PaddleOCR 文本中命中同句片段才落地，共 {total} 处。
- 本批后全书汇总 `述阳` 残留 {residual} 处，均为本批未取得 OCR 片段命中的条目，留待后续逐页核对。
- 报告：`output/reports/shuyang_full_summary_ocr_batch329_20260708.md`；进度：`output/reports/progress/20260708_全书汇总沭阳残留OCR补修第三百二十九批.md`。
- 未作全局 `述阳 -> 沭阳`；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residual = apply_repairs()
    total = sum(item["count"] for item in changes)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "residual": residual,
        "changes": changes,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    content = render(changes, residual)
    REPORT.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")
    append_memory(total, residual)
    print(f"total={total}")
    print(f"residual={residual}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()

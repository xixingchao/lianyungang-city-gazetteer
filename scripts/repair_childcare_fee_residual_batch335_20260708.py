# -*- coding: utf-8 -*-
"""Single-point childcare fee residual repair."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "childcare_fee_residual_batch335_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "childcare_fee_residual_batch335_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_超生子女入托费单点补修第三百三十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷_人口（part01_部分）.md",
]

REPLACEMENTS = [
    (
        "超生女子入托费和学费",
        "超生子女入托费和学费",
        "同句为计划外生育处罚语境，下句亦为“超生子女”；“女子”应为“子女”。",
    ),
    (
        "超生女子人托费和学费",
        "超生子女入托费和学费",
        "同句为计划外生育处罚语境，下句亦为“超生子女”；同时修正 `人托 -> 入托`。",
    ),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_replacements() -> tuple[list[dict], dict[str, int]]:
    changes: list[dict] = []
    for path in TARGETS:
        if not path.exists():
            continue
        text = read(path)
        original = text
        for old, new, evidence in REPLACEMENTS:
            count = text.count(old)
            if not count:
                continue
            text = text.replace(old, new)
            changes.append({
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "old": old,
                "new": new,
                "count": count,
                "evidence": evidence,
            })
        if text != original:
            path.write_text(text, encoding="utf-8")
    residuals: dict[str, int] = {}
    for path in TARGETS:
        if not path.exists():
            continue
        text = read(path)
        count = text.count("超生女子入托费") + text.count("超生女子人托费") + text.count("女子人托费")
        if count:
            residuals[str(path.relative_to(ROOT)).replace("\\", "/")] = count
    return changes, residuals


def render(changes: list[dict], residuals: dict[str, int]) -> str:
    total = sum(item["count"] for item in changes)
    lines = [
        "# 超生子女入托费单点补修 batch335",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：正式全书 HTML、全书正文汇总、上册正文汇总、上册人口分卷源稿。",
        "- 原则：只修计划生育处罚语境中的固定短语；不处理 OCR 源文件、paddle 派生稿、obsolete、历史交付包。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['evidence']}")
    lines.extend(["", "## 残留计数", ""])
    if residuals:
        for path, count in residuals.items():
            lines.append(f"- `{path}`：相关残留 {count} 处")
    else:
        lines.append("- 当前修复范围内 `超生女子入托费/超生女子人托费/女子人托费`：0")
    return "\n".join(lines) + "\n"


def append_memory(total: int, residuals: dict[str, int]) -> None:
    marker = "## 2026-07-08 超生子女入托费单点补修第三百三十五批"
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in old:
        return
    block = f"""
{marker}

- 单点补修计划生育处罚语境 `超生女子入托费/超生女子人托费 -> 超生子女入托费`，共 {total} 处。
- 范围限于正式全书 HTML、全书正文汇总、上册正文汇总、上册人口分卷源稿；未处理 OCR 源文件、paddle 派生稿、obsolete、历史交付包。
- 本批后当前修复范围相关残留 {sum(residuals.values())} 处；报告：`output/reports/childcare_fee_residual_batch335_20260708.md`。
- 未打开、展示或嵌入图片。
"""
    MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> None:
    changes, residuals = apply_replacements()
    total = sum(item["count"] for item in changes)
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "residuals": residuals, "changes": changes}
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    content = render(changes, residuals)
    REPORT.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")
    append_memory(total, residuals)
    print(f"total={total}")
    print(f"residual={sum(residuals.values())}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()

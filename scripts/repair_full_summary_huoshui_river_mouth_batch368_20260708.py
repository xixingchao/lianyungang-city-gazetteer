# -*- coding: utf-8 -*-
"""Repair one full-summary river-mouth table residue."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "huoshui_river_mouth_batch368_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "huoshui_river_mouth_batch368_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_获水村入海口表段残留补修第三百六十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 获水村入海口表段残留补修第三百六十八批"
TARGET = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
OLD = "省界东棘荡村一获水村人海口"
NEW = "省界东棘荡村一获水村入海口"
EVIDENCE_FILES = [
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
]
CHECK_FILES = [TARGET, *EVIDENCE_FILES, ROOT / "output" / "final_reader" / "连云港市志_全书.html"]
CHECK_TERMS = ["获水村人海口", "获水村入海口", "人海口", "泗、沂、述", "沂沐偏重"]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needle: str) -> list[int]:
    return [i for i, line in enumerate(read(path).splitlines(), 1) if needle in line]


def apply_fix() -> tuple[int, dict[str, dict[str, int]], dict[str, list[int]]]:
    evidence = {rel(path): line_hits(path, NEW) for path in EVIDENCE_FILES}
    text = read(TARGET)
    count = text.count(OLD)
    if count:
        TARGET.write_text(text.replace(OLD, NEW), encoding="utf-8")

    residuals: dict[str, dict[str, int]] = {}
    for path in CHECK_FILES:
        if not path.exists():
            continue
        current = read(path)
        hits = {term: current.count(term) for term in CHECK_TERMS if current.count(term)}
        if hits:
            residuals[rel(path)] = hits
    return count, residuals, evidence


def render(count: int, residuals: dict[str, dict[str, int]], evidence: dict[str, list[int]]) -> str:
    lines = [
        "# 获水村入海口表段残留补修 batch368",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{count}",
        "- 范围：全书正文汇总单文件。",
        "- 依据：同一精修源稿表行已为 `省界东棘荡村一获水村入海口`。",
        "- 原则：只修完整表格短语；不作 `人 -> 入` 全局替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 证据位置",
    ]
    for path, lines_no in evidence.items():
        compact = "，".join(str(i) for i in lines_no) or "未命中"
        lines.append(f"- `{path}`：行 {compact} 命中 `{NEW}`。")
    lines.extend([
        "",
        "## 替换明细",
        f"- `{rel(TARGET)}`：`{OLD}` -> `{NEW}`；次数 {count}。" if count else "- 本次未产生新增替换。",
        "",
        "## 残留检查",
        "",
    ])
    if residuals:
        for path, hits in residuals.items():
            compact = "，".join(f"`{term}` {value}" for term, value in hits.items())
            lines.append(f"- `{path}`：{compact}")
    else:
        lines.append("- 检查范围未见目标残留词。")
    return "\n".join(lines) + "\n"


def upsert_memory(count: int, residuals: dict[str, dict[str, int]]) -> None:
    full_hits = residuals.get("workbench/body_chapters/连云港市志_全书_正文汇总.md", {})
    block = f"""{MARKER}

- 依据精修源稿 `workbench/body_chapters/上/第四卷至第十卷（part02）.md` 与 `workbench/body_chapters/连云港市志_上册_正文汇总.md` 中同一表行，补修全书正文汇总 `省界东棘荡村一获水村人海口 -> 省界东棘荡村一获水村入海口`，共 {count} 处。
- 本批只修完整表格短语，不作 `人 -> 入` 全局替换；页级 OCR 仍有 `人海口` 识别痕迹，作为 OCR 源差异记录保留，不改 OCR 源文件。
- 本批后全书汇总检查范围：`获水村人海口` {full_hits.get('获水村人海口', 0)}，`获水村入海口` {full_hits.get('获水村入海口', 0)}，`人海口` {full_hits.get('人海口', 0)}，`泗、沂、述` {full_hits.get('泗、沂、述', 0)}，`沂沐偏重` {full_hits.get('沂沐偏重', 0)}。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/huoshui_river_mouth_batch368_20260708.md`；进度：`output/reports/progress/20260708_获水村入海口表段残留补修第三百六十八批.md`。
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
    count, residuals, evidence = apply_fix()
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": count,
        "target": rel(TARGET),
        "old": OLD,
        "new": NEW,
        "evidence": evidence,
        "residuals": residuals,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render(count, residuals, evidence)
    REPORT.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(count, residuals)
    print(f"total={count}")
    print(json.dumps(residuals, ensure_ascii=False, indent=2))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()

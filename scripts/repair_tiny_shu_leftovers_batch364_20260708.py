# -*- coding: utf-8 -*-
"""Repair two source-backed tiny Shu leftovers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "tiny_shu_leftovers_batch364_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "tiny_shu_leftovers_batch364_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_沭新蔷北极小残留补修第三百六十四批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 沭新蔷北极小残留补修第三百六十四批"

FULL = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
UP_SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md"
CHECK_FILES = [
    FULL,
    UP_SUMMARY,
    ROOT / "workbench" / "body_chapters" / "上" / "第四卷至第十卷（part02）.md",
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "output" / "final_reader" / "连云港市志_中册.html",
]
CHECK_TERMS = ["新述河", "新沐河", "述南", "述北", "沐南", "沐北", "临沐县", "沂述", "沂沐", "人海口", "沐阳县", "准述", "沐新", "述城", "蕃北地涵"]


@dataclass(frozen=True)
class Replacement:
    path: Path
    old: str
    new: str
    evidence: str


REPLACEMENTS = [
    Replacement(FULL, "蕃北地涵", "蔷北地涵", "上 part03 merged OCR line 5618 及同段水利工程正文均为“蔷北地涵”。"),
    Replacement(UP_SUMMARY, "开挖了石梁河水库、准述新\n河", "开挖了石梁河水库、淮沭新\n河", "上 part02 merged OCR line 16358 明确为“淮沭新河”。"),
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def apply_fix() -> tuple[list[dict], dict[str, dict[str, int]]]:
    changes: list[dict] = []
    for item in REPLACEMENTS:
        if not item.path.exists():
            continue
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
        "# 沭新蔷北极小残留补修 batch364",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：全书正文汇总与上册正文汇总中两个已回源确认的短残留。",
        "- 原则：只修完整短语；不作 `准 -> 淮`、`蕃 -> 蔷` 或其它全局替换。",
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
        "- 正式 reader 的 `沐北航道` 未找到页级 OCR 证据，本批继续保留。",
        "- 全书汇总 `沂沐偏重筹泄...` 位于题名/书名语境，本批继续保留。",
        "- 表段 `获水村人海口` 延续前批保留边界，本批不处理。",
        "- 未处理 OCR 源文件、backup、obsolete、历史交付包。",
    ])
    return "\n".join(lines) + "\n"


def upsert_memory(total: int, residuals: dict[str, dict[str, int]]) -> None:
    full_hits = residuals.get(rel(FULL), {})
    up_hits = residuals.get(rel(UP_SUMMARY), {})
    block = f"""{MARKER}

- 依据上册 part03 merged OCR line 5618 与上册 part02 merged OCR line 16358，补修全书正文汇总/上册正文汇总两个可证极小残留，共 {total} 处。
- 修复：`蕃北地涵 -> 蔷北地涵`、`准述新河 -> 淮沭新河`。
- 本批后全书汇总保留检查范围：`沐北` {full_hits.get('沐北', 0)}，`沂沐` {full_hits.get('沂沐', 0)}，`人海口` {full_hits.get('人海口', 0)}，`准述` {full_hits.get('准述', 0)}，`蕃北地涵` {full_hits.get('蕃北地涵', 0)}。
- 本批后上册正文汇总保留检查范围：`准述` {up_hits.get('准述', 0)}。
- 正式 reader 的 `沐北航道` 未找到页级 OCR 证据，本批继续保留；题名/书名和表段保留项未处理；未作全局替换；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
- 报告：`output/reports/tiny_shu_leftovers_batch364_20260708.md`；进度：`output/reports/progress/20260708_沭新蔷北极小残留补修第三百六十四批.md`。
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

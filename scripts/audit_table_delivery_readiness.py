# -*- coding: utf-8 -*-
"""Audit whether the structured table site is ready for Dongxin-style delivery."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "output" / "structured_tables" / "index.html"
REPORT_MD = ROOT / "output" / "reports" / "结构化表格交付就绪审计报告.md"
REPORT_JSON = ROOT / "output" / "reports" / "结构化表格交付就绪审计报告.json"

BAD_TOKENS = ["待对照原图录入", "待精修", "待确认", "标题待确认", "从OCR自动提取骨架", "待对照原图"]
BAD_TITLE_RE = re.compile(r"^(第\d+页表格|表\d+[-－]?$)|。|，|同年|正式|^年|^米的|^树\d|^业。")


@dataclass
class TableIssue:
    table_id: str
    title: str
    volume: str
    pages: str
    kind: str
    excerpt: str


def load_tables() -> list[dict]:
    text = SITE.read_text(encoding="utf-8")
    match = re.search(r"const TABLES = (\[.*?\]);\s*\n\s*function escape", text, re.S)
    if not match:
        raise SystemExit("TABLES payload not found in structured table site")
    return json.loads(match.group(1))


def flat_values(table: dict) -> list[str]:
    values: list[str] = []
    for key in ("table_id", "title", "table_number", "status", "notes", "volume"):
        values.append(str(table.get(key, "")))
    values.extend(str(c) for c in table.get("columns") or [])
    for row in table.get("rows") or []:
        values.extend(str(cell) for cell in row)
    return values


def excerpt(table: dict, limit: int = 120) -> str:
    text = " ".join(v for v in flat_values(table) if v).strip()
    text = re.sub(r"\s+", " ", text)
    return text if len(text) <= limit else text[: limit - 1] + "..."


def pages_label(table: dict) -> str:
    pages = table.get("pages") or ([] if table.get("page") is None else [table.get("page")])
    return ",".join(str(p) for p in pages)


def audit(tables: list[dict]) -> list[TableIssue]:
    issues: list[TableIssue] = []
    for table in tables:
        table_id = str(table.get("table_id", ""))
        title = str(table.get("title", ""))
        volume = str(table.get("volume", table.get("vol", "")))
        pages = pages_label(table)
        values = flat_values(table)
        joined = "\n".join(values)
        rows = table.get("rows") or []
        cols = table.get("columns") or []

        if any(token in joined for token in BAD_TOKENS):
            hits = [token for token in BAD_TOKENS if token in joined]
            issues.append(TableIssue(table_id, title, volume, pages, "含待核/待录入标记", "、".join(hits) + "；" + excerpt(table)))
        if title in {"(标题待确认)", "标题待确认"} or not title.strip():
            issues.append(TableIssue(table_id, title, volume, pages, "表题未确认", excerpt(table)))
        elif BAD_TITLE_RE.search(title):
            issues.append(TableIssue(table_id, title, volume, pages, "表题疑似OCR粘连", excerpt(table)))
        if rows and len(rows) == 1 and len([c for c in rows[0] if str(c).strip()]) <= 1:
            issues.append(TableIssue(table_id, title, volume, pages, "疑似空壳表", excerpt(table)))
        if len(cols) == 1 and cols[0] == "数值":
            issues.append(TableIssue(table_id, title, volume, pages, "单列骨架表", excerpt(table)))
        status = str(table.get("status", "")).lower()
        if status == "verified" and any(token in joined for token in BAD_TOKENS):
            issues.append(TableIssue(table_id, title, volume, pages, "verified状态与待核内容冲突", excerpt(table)))
        if status == "pending-source-check":
            issues.append(TableIssue(table_id, title, volume, pages, "待回源核录状态", excerpt(table)) )
    return issues


def render(tables: list[dict], issues: list[TableIssue]) -> str:
    issue_ids = {issue.table_id for issue in issues}
    by_kind = Counter(issue.kind for issue in issues)
    by_volume = defaultdict(Counter)
    for issue in issues:
        by_volume[issue.volume][issue.kind] += 1

    lines = [
        "# 结构化表格交付就绪审计报告",
        "",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"基于：`{SITE.relative_to(ROOT)}`",
        "",
        "## 结论",
        "",
    ]
    if issues:
        lines.extend([
            "- 结构化表格站未达到东辛式已核表格交付标准。",
            "- 含待核/待录入/空壳/表题待确认的表格不得作为主交付入口，只能作为回源核录清单。",
        ])
    else:
        lines.append("- 结构化表格站未发现待核/空壳/表题待确认问题，可进入交付包入口候选。")

    lines.extend([
        "",
        "## 统计",
        "",
        f"- 表格总数：{len(tables)}",
        f"- 命中问题的表格：{len(issue_ids)}",
        f"- 问题记录数：{len(issues)}",
        "",
        "| 问题类型 | 数量 |",
        "|---|---:|",
    ])
    for kind, count in by_kind.most_common():
        lines.append(f"| {kind} | {count} |")

    lines.extend(["", "## 分册分布", "", "| 分册 | 问题记录 | 主要类型 |", "|---|---:|---|"])
    for volume, counts in sorted(by_volume.items()):
        total = sum(counts.values())
        kinds = "；".join(f"{k} {v}" for k, v in counts.most_common())
        lines.append(f"| {volume or '未标注'} | {total} | {kinds} |")

    lines.extend(["", "## 问题清单", "", "| 表ID | 分册 | 页码 | 类型 | 表题/摘录 |", "|---|---|---|---|---|"])
    for issue in issues:
        text = (issue.title or issue.excerpt).replace("|", "\\|")
        lines.append(f"| {issue.table_id} | {issue.volume} | {issue.pages} | {issue.kind} | {text} |")

    lines.extend([
        "",
        "## 下一步",
        "",
        "1. 按本清单优先处理 `含待核/待录入标记`、`单列骨架表`、`表题未确认` 的表。",
        "2. 每表必须回源 PDF/页图核读后再改为可交付状态。",
        "3. 表格站问题清零前，不得放入交付包推荐入口。",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    tables = load_tables()
    issues = audit(tables)
    REPORT_JSON.write_text(json.dumps({"issues": [issue.__dict__ for issue in issues]}, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_MD.write_text(render(tables, issues), encoding="utf-8")
    print(f"tables={len(tables)}")
    print(f"problem_tables={len({issue.table_id for issue in issues})}")
    print(f"issues={len(issues)}")
    for kind, count in Counter(issue.kind for issue in issues).most_common():
        print(f"{kind}: {count}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

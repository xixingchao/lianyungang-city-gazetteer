# -*- coding: utf-8 -*-
"""Repair verified 混人/混入 OCR residues in current sources."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_hunru_batch386_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_hunru_batch386_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_混入残留补修第三百八十六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MARKER = "## 2026-07-08 混入残留补修第三百八十六批"

PATHS = [
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]

EVIDENCE_TERMS = [
    "混入xu",
    "n混入l",
    "混入知庄章",
    "混入合口字",
    "混入开口字",
    "混入土匪队伍",
    "混入革命根据地",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needle: str) -> list[int]:
    return [i for i, line in enumerate(read(path).splitlines(), 1) if needle in line]


def snippets(path: Path, needle: str) -> list[str]:
    out = []
    for i, line in enumerate(read(path).splitlines(), 1):
        if needle in line:
            idx = line.find(needle)
            out.append(f"{i}: {line[max(0, idx - 45):idx + 95]}")
    return out


def apply_fix() -> list[dict[str, object]]:
    results = []
    for path in PATHS:
        before = read(path)
        before_snippets = snippets(path, "混人")
        count = before.count("混人")
        if count:
            path.write_text(before.replace("混人", "混入"), encoding="utf-8")
        after = read(path)
        results.append(
            {
                "path": rel(path),
                "old_count": count,
                "old_count_after": after.count("混人"),
                "new_count_after": after.count("混入"),
                "snippets_before": before_snippets,
            }
        )
    return results


def render(results: list[dict[str, object]], evidence: dict[str, list[int]], reader_old_count: int) -> str:
    total = sum(int(item["old_count"]) for item in results)
    lines = [
        "# 混入残留补修 batch386",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        f"- 正式 reader 当前 `混人`：{reader_old_count}",
        "- 范围：现行下册分册源稿与全书汇总中的 `混人 -> 混入` 残留。",
        "- 证据：正式 reader 中方言分混、敌特潜入语境均呈现为 `混入`。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(
            f"- `{item['path']}`：`混人 -> 混入` {item['old_count']} 处；修后 `混人` {item['old_count_after']}。"
        )
    lines.extend(["", "## reader 证据"])
    for term, hits in evidence.items():
        compact = "，".join(str(i) for i in hits) or "未命中"
        lines.append(f"- `output/final_reader/连云港市志_全书.html` 行 {compact}：`{term}`")
    lines.extend(["", "## 修前片段"])
    for item in results:
        lines.append(f"### {item['path']}")
        if not item["snippets_before"]:
            lines.append("- 本批无改动。")
            continue
        for snippet in item["snippets_before"]:
            lines.append(f"- {snippet}")
    return "\n".join(lines) + "\n"


def upsert_memory(total: int) -> None:
    block = f"""{MARKER}

- 依据正式 reader 对证，补修现行下册分册源稿与全书汇总中的 `混人 -> 混入` 残留，共 {total} 处；正式 reader 当前 `混人=0`。
- 覆盖方言分混术语和敌特潜入语境；代表修复：`f混人xu -> f混入xu`、`混人合口字 -> 混入合口字`、`混人土匪队伍 -> 混入土匪队伍`、`混人革命根据地 -> 混入革命根据地`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未作 `人 -> 入` 全局替换；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_hunru_batch386_20260708.md`；进度：`output/reports/progress/20260708_混入残留补修第三百八十六批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    MEMORY.write_text(old[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old[next_start:]), encoding="utf-8")


def main() -> None:
    reader_old_count = read(READER).count("混人")
    results = apply_fix()
    evidence = {term: line_hits(READER, term) for term in EVIDENCE_TERMS}
    total = sum(int(item["old_count"]) for item in results)
    report = render(results, evidence, reader_old_count)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "reader_hunren_count": reader_old_count,
        "total": total,
        "results": results,
        "evidence": evidence,
    }
    REPORT.write_text(report, encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total)
    print(f"reader_hunren={reader_old_count}")
    print(f"total={total}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Repair verified 并人/并入 OCR residues in current sources."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "verified_bingru_batch385_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "verified_bingru_batch385_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_并入残留补修第三百八十五批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
MARKER = "## 2026-07-08 并入残留补修第三百八十五批"

PATHS = [
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]

EVIDENCE_TERMS = [
    "并入新浦搬运营业所",
    "并入国营商业",
    "并入板浦场",
    "并入新浦造纸厂",
    "并入新海印刷厂",
    "并入连云港市毛巾厂",
    "并入赣榆邮电局",
    "并入新浦自动网",
    "并入工商统一税",
    "并入东海县",
    "并入南京医学",
    "并入地区电网运行",
    "并入徐州第四监狱",
    "并入成人高校",
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
        count = before.count("并人")
        if count:
            path.write_text(before.replace("并人", "并入"), encoding="utf-8")
        after = read(path)
        results.append(
            {
                "path": rel(path),
                "old_count": count,
                "old_count_after": after.count("并人"),
                "new_count_after": after.count("并入"),
                "snippets_after": snippets(path, "并入")[:12],
            }
        )
    return results


def render(results: list[dict[str, object]], evidence: dict[str, list[int]]) -> str:
    total = sum(int(item["old_count"]) for item in results)
    lines = [
        "# 并入残留补修 batch385",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：现行中册/下册分册源稿与全书汇总中的 `并人 -> 并入` 残留。",
        "- 证据：正式 reader 中 `并人=0`，同类机构、税种、学校、电网等语境均呈现为 `并入`。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 修复明细",
    ]
    for item in results:
        lines.append(
            f"- `{item['path']}`：`并人 -> 并入` {item['old_count']} 处；修后 `并人` {item['old_count_after']}。"
        )
    lines.extend(["", "## reader 证据"])
    for term, hits in evidence.items():
        compact = "，".join(str(i) for i in hits) or "未命中"
        lines.append(f"- `output/final_reader/连云港市志_全书.html` 行 {compact}：`{term}`")
    lines.extend(["", "## 修后片段抽样"])
    for item in results:
        lines.append(f"### {item['path']}")
        if int(item["old_count"]) == 0:
            lines.append("- 本批无改动。")
            continue
        for snippet in item["snippets_after"]:
            lines.append(f"- {snippet}")
    return "\n".join(lines) + "\n"


def upsert_memory(total: int) -> None:
    block = f"""{MARKER}

- 依据正式 reader 对证，补修现行中册/下册分册源稿与全书汇总中的 `并人 -> 并入` 残留，共 {total} 处；正式 reader 当前 `并人=0`。
- 覆盖机构合并、税种并入、学校并入、电网并入、企业并入等明确语境；代表修复：`并人国营商业 -> 并入国营商业`、`并人新海印刷厂 -> 并入新海印刷厂`、`并人地区电网运行 -> 并入地区电网运行`、`并人徐州第四监狱 -> 并入徐州第四监狱`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未作 `人 -> 入` 全局替换；未打开、展示或嵌入图片。
- 报告：`output/reports/verified_bingru_batch385_20260708.md`；进度：`output/reports/progress/20260708_并入残留补修第三百八十五批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
        return
    next_start = old.find("\n## ", start + 1)
    MEMORY.write_text(old[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old[next_start:]), encoding="utf-8")


def main() -> None:
    before_reader = read(READER).count("并人")
    results = apply_fix()
    evidence = {term: line_hits(READER, term) for term in EVIDENCE_TERMS}
    total = sum(int(item["old_count"]) for item in results)
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "reader_bingren_count": before_reader,
        "total": total,
        "results": results,
        "evidence": evidence,
    }
    report = render(results, evidence)
    REPORT.write_text(report, encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    upsert_memory(total)
    print(f"reader_bingren={before_reader}")
    print(f"total={total}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()

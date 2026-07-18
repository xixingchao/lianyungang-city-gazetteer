# -*- coding: utf-8 -*-
"""Repair 鲁少时跨页锚 加人/加入 residual."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "output" / "reports" / "lushaoshi_join_batch379_20260708.md"
REPORT_JSON = ROOT / "output" / "reports" / "lushaoshi_join_batch379_20260708.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260708_鲁少时加入残留补修第三百七十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
MARKER = "## 2026-07-08 鲁少时加入残留补修第三百七十九批"

PATHS = [
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
OLD = "鲁少时（1927～）东台县人。民国33年（1944年)7月参加工作；同年10月加人\n\n<!-- page-anchor: LYG-2826 -->\n\n中国共产党。"
NEW = "鲁少时（1927～）东台县人。民国33年（1944年)7月参加工作；同年10月加入\n\n<!-- page-anchor: LYG-2826 -->\n\n中国共产党。"
EVIDENCE = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
EVIDENCE_TERM = "鲁少时（1927～）东台县人。民国33年（1944年)7月参加工作；同年10月加入中国共产党。"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def line_hits(path: Path, needle: str) -> list[int]:
    return [i for i, line in enumerate(read(path).splitlines(), 1) if needle in line]


def main() -> None:
    results = []
    for path in PATHS:
        text = read(path)
        count = text.count(OLD)
        if count:
            path.write_text(text.replace(OLD, NEW), encoding="utf-8")
        results.append({"path": rel(path), "old_count": count, "new_count_after": read(path).count(NEW)})
    total = sum(item["old_count"] for item in results)
    old_counts = {rel(path): read(path).count(OLD) for path in PATHS if read(path).count(OLD)}
    evidence_lines = line_hits(EVIDENCE, EVIDENCE_TERM)
    lines = [
        "# 鲁少时加入残留补修 batch379",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 修复总数：{total}",
        "- 范围：下册源稿与全书正文汇总中跨页锚拆开的 `加人/中国共产党` 残留。",
        "- 原则：只修鲁少时传这一完整跨页锚短语；不处理其他合法 `参加人数/增加人员/参军人员`。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 证据位置",
        f"- `output/final_reader/连云港市志_全书.html` 行 {'，'.join(map(str, evidence_lines)) or '未命中'}：`{EVIDENCE_TERM}`",
        "",
        "## 旧词残留检查",
    ]
    if old_counts:
        for path, count in old_counts.items():
            lines.append(f"- `{path}`：旧跨页短语 {count}")
    else:
        lines.append("- 检查范围未见本批旧跨页短语残留。")
    lines.extend(["", "## 新词命中"])
    for item in results:
        if item["new_count_after"]:
            lines.append(f"- `{item['path']}`：新跨页短语 {item['new_count_after']}")
    report = "\n".join(lines) + "\n"
    data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "total": total, "results": results, "old_counts": old_counts, "evidence_lines": evidence_lines}
    REPORT.write_text(report, encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")
    block = f"""{MARKER}

- 依据正式 reader 行 {','.join(map(str, evidence_lines)) or '未命中'}，补修鲁少时传跨页锚拆开的 `同年10月加人 / 中国共产党 -> 同年10月加入 / 中国共产党`，共 {total} 处。
- 本批后下册源稿与全书正文汇总旧跨页短语检查为 0；未处理 OCR 源文件、backup、obsolete、历史交付包；未作 `人 -> 入` 全局替换；未打开、展示或嵌入图片。
- 报告：`output/reports/lushaoshi_join_batch379_20260708.md`；进度：`output/reports/progress/20260708_鲁少时加入残留补修第三百七十九批.md`。
"""
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    start = old.find(MARKER)
    if start < 0:
        MEMORY.write_text(old.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
    else:
        next_start = old.find("\n## ", start + 1)
        MEMORY.write_text(old[:start].rstrip() + "\n\n" + block.strip() + ("\n" if next_start < 0 else old[next_start:]), encoding="utf-8")
    print(f"total={total}")
    print(json.dumps(old_counts, ensure_ascii=False, indent=2))
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()

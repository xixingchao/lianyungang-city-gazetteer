# -*- coding: utf-8 -*-
"""Repair lower-reader area unit residues, batch 131."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "output" / "final_reader" / "连云港市志_下册.html"]
REPORT_JSON = ROOT / "output" / "reports" / "lower_reader_area_batch131_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "lower_reader_area_batch131_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_下册面积单位残字回源补修第一百三十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "消防审核工业建筑面积", "old": "建筑面积482.61方平方米", "new": "建筑面积482.61万平方米"},
    {"label": "连云港中药学校建筑面积", "old": "建筑面积1.03方平方米", "new": "建筑面积1.03万平方米"},
    {"label": "抗震加固建筑物面积", "old": "加固建筑物122.1方平方米", "new": "加固建筑物122.1万平方米"},
    {"label": "大村遗址面积", "old": "面积约2方平方米", "new": "面积约2万平方米"},
]

LEFT_UNTOUCHED = [
    "下册 `方人` 本批核对为正常身份词或表尾噪声，不处理。",
    "本批没有打开、展示或嵌入图片。",
]


def upsert_memory(marker: str, content: str) -> None:
    old = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in old:
        MEMORY.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    MEMORY.write_text(new, encoding="utf-8")


def main() -> None:
    applied = []
    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        target.write_text(text, encoding="utf-8")
        applied.append({"target": str(target), "changed": sum(i["count"] for i in items), "items": items})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    changed = sum(t["changed"] for t in applied)
    payload = {
        "time": now,
        "scope": "lower reader area unit residue repair",
        "patterns": len(REPLACEMENTS),
        "changed_this_run": changed,
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 下册面积单位残字补修第一百三十一批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前下册阅读稿。",
        "- 只处理面积上下文中固定 `方平方米` 残字。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本次替换：{changed} 处",
        "",
        "## 文件",
        "",
    ]
    for target in applied:
        if target["changed"]:
            lines.append(f"- `{target['target']}`：{target['changed']} 处")
    lines.extend(["", "## 修复项", ""])
    for item in REPLACEMENTS:
        lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百三十一批：下册面积单位残字"
    upsert_memory(marker, f"""
{marker}

- 补修当前下册阅读稿中面积上下文的 `方平方米` 固定短语，改为 `万平方米`。
- 本批证据短语 {len(REPLACEMENTS)} 项，替换 {changed} 处；报告：`output/reports/lower_reader_area_batch131_20260707.md`。
- 下册 `方人` 本批核对为正常身份词或表尾噪声，不处理；未打开、展示或嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

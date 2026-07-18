# -*- coding: utf-8 -*-
"""Repair middle-reader area/person unit residues, batch 130."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "output" / "final_reader" / "连云港市志_中册.html"]
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_area_people_batch130_20260707.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_area_people_batch130_20260707.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260707_中册面积人数单位残字回源补修第一百三十批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {"label": "贝雕厂购地", "old": "购地1方平方米", "new": "购地1万平方米"},
    {"label": "襄河乳品厂占地", "old": "占地面积2方平方米", "new": "占地面积2万平方米"},
    {"label": "屠宰冷藏企业建筑面积", "old": "建筑面积10.7方平方米", "new": "建筑面积10.7万平方米"},
    {"label": "肉联公司建筑面积", "old": "建筑面积3.46方平方米", "new": "建筑面积3.46万平方米"},
    {"label": "罐头加工企业建筑面积", "old": "建筑面积5.05方平方米", "new": "建筑面积5.05万平方米"},
    {"label": "抗日烈士陵园总面积", "old": "陵园总面积21.06方平方米", "new": "陵园总面积21.06万平方米"},
    {"label": "食品工业全民企业职工", "old": "全民企业职工1.25方人", "new": "全民企业职工1.25万人"},
    {"label": "供销合作社职工", "old": "职工1.6方人", "new": "职工1.6万人"},
    {"label": "屠宰冷藏企业建筑面积分行", "old": "积10.7方平方米", "new": "积10.7万平方米"},
    {"label": "抗日烈士陵园总面积分行", "old": "陵园总面积21.06方平</p><p>方米", "new": "陵园总面积21.06万平</p><p>方米"},
]

LEFT_UNTOUCHED = [
    "`沪方人员/外方人员/私方人员` 等合法身份词不处理。",
    "本批没有打开、展示或嵌入图片。",
]
CUMULATIVE_FIXED = 8


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
        "scope": "middle reader area/person unit residue repair",
        "patterns": len(REPLACEMENTS),
        "changed_this_run": changed,
        "cumulative_fixed": CUMULATIVE_FIXED,
        "targets": applied,
        "left_untouched": LEFT_UNTOUCHED,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册面积、人数单位残字补修第一百三十批",
        "",
        f"> 生成时间：{now}",
        "",
        "## 范围",
        "",
        "- 当前中册阅读稿。",
        "- 只处理面积、人数上下文中固定 `方平方米/方人` 残字。",
        "",
        "## 统计",
        "",
        f"- 证据短语：{len(REPLACEMENTS)} 项",
        f"- 本批累计命中：{CUMULATIVE_FIXED} 处",
        f"- 本次复跑替换：{changed} 处",
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

    marker = "## 2026-07-07 高置信 OCR 错字补修第一百三十批：中册面积、人数单位残字"
    upsert_memory(marker, f"""
{marker}

- 补修当前中册阅读稿中面积、人数上下文的 `方平方米/方人` 固定短语，改为 `万平方米/万人`。
- 本批证据短语 {len(REPLACEMENTS)} 项，累计命中 {CUMULATIVE_FIXED} 处；报告：`output/reports/middle_reader_area_people_batch130_20260707.md`。
- 保留合法身份词 `沪方人员/外方人员/私方人员` 等；未打开、展示或嵌入图片。
""")
    print(json.dumps({"patterns": len(REPLACEMENTS), "changed_this_run": changed, "cumulative_fixed": CUMULATIVE_FIXED, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

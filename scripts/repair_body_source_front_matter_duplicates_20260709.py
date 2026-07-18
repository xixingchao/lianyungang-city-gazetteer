# -*- coding: utf-8 -*-
"""Remove merge-only part headings and duplicated front matter from the full body summary."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
REPORT_MD = ROOT / "output" / "reports" / "body_source_front_matter_duplicates_20260709.md"
REPORT_JSON = ROOT / "output" / "reports" / "body_source_front_matter_duplicates_20260709.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260709_正文汇总分段标题与重复前置页清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

PART_HEADING_RE = re.compile(r"(?m)^# 第.*(?:part\d+|部分|中part|下part).*$\n*")
FRONT_START = "连云港市志\n连云港市地方志编纂委员会编\n方志出版社"
FRONT_END_MARKERS = [
    "<!-- page-anchor: LYG-S-0307 -->",
    "<!-- page-anchor: LYG-S-0612 -->",
]
FRONT_TAIL_BLOCKS = [
    ("主体照片提供人员", "<!-- page-anchor: LYG-S-0312 -->"),
    ("主体照片提供人员", "<!-- page-anchor: LYG-S-0617 -->"),
]
FRONT_MARKERS = [
    "《连云港市志》编纂机构、人员及审定单位",
    "《连云港市志》编纂人员",
    "《连云港市志》评审人员",
    "《连云港市志》审定单位",
]


def remove_front_blocks(text: str) -> tuple[str, list[dict[str, object]]]:
    changes = []
    for end_marker in FRONT_END_MARKERS:
        start = text.find(FRONT_START)
        if start < 0:
            continue
        end = text.find(end_marker, start)
        if end < 0:
            continue
        block = text[start:end]
        changes.append({
            "action": "delete_front_matter_block",
            "start_line": text.count("\n", 0, start) + 1,
            "end_line": text.count("\n", 0, end) + 1,
            "chars": len(block),
            "end_marker": end_marker,
            "front_marker_counts": {marker: block.count(marker) for marker in FRONT_MARKERS},
        })
        text = text[:start] + text[end:]
    for start_marker, end_marker in FRONT_TAIL_BLOCKS:
        start = text.find(start_marker)
        if start < 0:
            continue
        end = text.find(end_marker, start)
        if end < 0:
            continue
        block = text[start:end]
        changes.append({
            "action": "delete_front_matter_tail_block",
            "start_line": text.count("\n", 0, start) + 1,
            "end_line": text.count("\n", 0, end) + 1,
            "chars": len(block),
            "end_marker": end_marker,
            "front_marker_counts": {marker: block.count(marker) for marker in FRONT_MARKERS},
        })
        text = text[:start] + text[end:]
    return text, changes


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    changes = []

    def part_repl(match: re.Match[str]) -> str:
        changes.append({
            "action": "delete_part_heading",
            "line": text.count("\n", 0, match.start()) + 1,
            "text": match.group(0).strip(),
        })
        return ""

    new_text = PART_HEADING_RE.sub(part_repl, text)
    new_text, front_changes = remove_front_blocks(new_text)
    changes.extend(front_changes)
    changed = new_text != text
    if changed:
        SOURCE.write_text(new_text, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "changed": changed, "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = []
    for item in changes:
        if item["action"] == "delete_part_heading":
            rows.append(f"| {item['action']} | {item['line']} | `{item['text']}` |")
        else:
            rows.append(f"| {item['action']} | {item['start_line']}-{item['end_line']} | chars={item['chars']} |")
    md = f"""# 正文汇总分段标题与重复前置页清理

- 时间：{now}
- 文件：`{SOURCE.relative_to(ROOT)}`

## 动作

- 删除合并过程残留的分段源文件标题。
- 删除上册 part02 / part03 重复夹入的版权页、编纂机构人员页等前置材料。
- 不改各卷正文内容。

## 明细

| 动作 | 位置 | 内容 |
|---|---|---|
{chr(10).join(rows)}

## 结果

- 发生改写：{changed}
- 处理项：{len(changes)}
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-09 正文汇总分段标题与重复前置页清理"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in memory:
        entry = f"""
{marker}

- 清理 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 中合并过程残留的分段源文件标题和重复夹入的前置材料。
- 删除对象限于 `# ...part...` 标题，以及上册 part02/part03 开头重复版权页、编纂机构人员页等；不改各卷正文内容。
- 报告：`output/reports/body_source_front_matter_duplicates_20260709.md`；进度：`output/reports/progress/20260709_正文汇总分段标题与重复前置页清理.md`。
"""
        MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")

    print("body source front matter duplicates repaired")
    print(f"changed={int(changed)}")
    print(f"changes={len(changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

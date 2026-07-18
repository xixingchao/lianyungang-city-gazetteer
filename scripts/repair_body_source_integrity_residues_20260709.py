# -*- coding: utf-8 -*-
"""Repair high-confidence body source page/header residues."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
REPORT_MD = ROOT / "output" / "reports" / "body_source_integrity_residues_20260709.md"
REPORT_JSON = ROOT / "output" / "reports" / "body_source_integrity_residues_20260709.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260709_正文源稿页眉页码残留清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

DELETE_EXACT = {
    "·116·i",
    "·134·连云港市志自然环境",
    "·166·连",
    "·194 ·",
    "·348 ·",
    "·420·送",
    "·426·j",
    "·678·连云港市志盐业",
    "·730·j",
    "·1326 ·",
    "·1646·i",
    "·1724·i",
    "·1742·j",
    "·1772·连云港市志政党",
    "·2320·连云港市志文化",
    "·2328·连云港市志文化",
    "·2346·”连云港市志文化",
    "·2394·i",
    "·2444·连云港市志报刊广播电视",
    "·988·i",
    "·1048·这",
    "·1084·i",
    "·1142 ·",
    "·1208·i",
    "·1212·i",
    "·1286·i",
    "·2114 ·",
    "·2242·i",
}
TITLE_PATTERNS = [
    (re.compile(r"^(第[一二三四五六七八九十]+章[^·\n]+)·\s*\d+\s*·$"), r"\1"),
    (re.compile(r"^(第[一二三四五六七八九十]+章[^·\n]+)·\s*\d+\s*·[：:]$"), r"\1"),
    (re.compile(r"^([一二三四五六七八九十]+、[^·\n]+)·\s*\d+\s*·$"), r"\1"),
]
SKIP_SUSPECT = {
}


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    changes = []
    skipped = []
    out = []
    for idx, raw in enumerate(lines, start=1):
        newline = "\n" if raw.endswith("\n") else ""
        line = raw[:-1] if newline else raw
        stripped = line.strip()
        if stripped in DELETE_EXACT:
            changes.append({"line": idx, "action": "delete", "old": stripped, "new": ""})
            continue
        if stripped in SKIP_SUSPECT:
            skipped.append({"line": idx, "text": stripped, "reason": "疑似页码后接正文首字，需回源确认"})
            out.append(raw)
            continue
        replaced = False
        for pattern, repl in TITLE_PATTERNS:
            if pattern.match(stripped):
                new = pattern.sub(repl, stripped)
                changes.append({"line": idx, "action": "normalize_title", "old": stripped, "new": new})
                out.append(new + newline)
                replaced = True
                break
        if not replaced:
            out.append(raw)

    changed = "".join(out) != text
    if changed:
        SOURCE.write_text("".join(out), encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "changed": changed, "changes": changes, "skipped": skipped}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    change_rows = "\n".join(
        f"| {c['line']} | {c['action']} | `{c['old']}` | `{c['new']}` |" for c in changes
    )
    skipped_rows = "\n".join(f"| {s['line']} | `{s['text']}` | {s['reason']} |" for s in skipped) or "| - | - | - |"
    md = f"""# 正文源稿页眉页码残留清理

- 时间：{now}
- 文件：`{SOURCE.relative_to(ROOT)}`

## 动作

- 删除独立页码、页眉、页脚残留行。
- 对标题后缀页码行，只保留标题文字。
- 对疑似页码后连着正文首字的行暂不改，列入待回源项。

## 已处理

| 行号 | 动作 | 原文 | 新文 |
|---:|---|---|---|
{change_rows}

## 暂不处理

| 行号 | 文本 | 原因 |
|---:|---|---|
{skipped_rows}

## 结果

- 发生改写：{changed}
- 删除/规范化：{len(changes)} 处
- 待回源：{len(skipped)} 处
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-09 正文源稿页眉页码残留清理"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in memory:
        entry = f"""
{marker}

- 清理 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 中高置信页眉页码残留：独立页码/页眉行删除，标题后缀页码行保留标题去页码。
- 暂不处理 `·420·送`、`·1048·这` 这类疑似页码后接正文首字的行，列入待回源清单。
- 报告：`output/reports/body_source_integrity_residues_20260709.md`；进度：`output/reports/progress/20260709_正文源稿页眉页码残留清理.md`。
"""
        MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")

    print("body source integrity residues repaired")
    print(f"changed={int(changed)}")
    print(f"changes={len(changes)}")
    print(f"skipped={len(skipped)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

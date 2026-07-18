# -*- coding: utf-8 -*-
"""Repair a source-confirmed port loading dispatch paragraph."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_port_loading_dispatch_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_port_loading_dispatch_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第二十九卷港口装卸调度回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/中/part01/page_0463.txt:27-28"
OLD = "<p>1958年11月18日，连云港下放地方管理。此后，港务调度、商务的代表起参加在北京举行的由国家交通部、铁道部、外贸部召开的每月一一次的月度计划平衡会。会上由交通部根据连云港的货源情况下达月度计划。局调度代表根据月度计划制定调度月计划及装卸作业计划。局调度室调度计划员每日根据作业计划下达作业调度的命令，各装卸单位接命令后到指定现场按指定作业方式进行作业。</p>"
NEW = "<p>1958年11月18日，连云港下放地方管理。此后，港务调度、商务的代表一起参加在北京举行的由国家交通部、铁道部、外贸部召开的每月一次的月度计划平衡会。会上由交通部根据连云港的货源情况下达月度计划。局调度代表根据月度计划制定调度月计划及装卸作业计划。局调度室调度计划员每日根据作业计划下达作业调度的命令，各装卸单位接命令后到指定现场按指定作业方式进行作业。</p>"

EXPECTED_TEXT = ["代表一起参加", "每月一次的月度计划平衡会"]
RESIDUALS = ["代表起参加", "每月一一次的月度计划平衡会"]


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    changed = 0
    if OLD in text:
        text = text.replace(OLD, NEW, 1)
        HTML.write_text(text, encoding="utf-8")
        changed = 1

    text = HTML.read_text(encoding="utf-8")
    if NEW not in text:
        raise RuntimeError("expected repaired paragraph missing")
    missing = [item for item in EXPECTED_TEXT if item not in text]
    if missing:
        raise RuntimeError(f"expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in text]
    if remaining:
        raise RuntimeError(f"residue remains: {remaining}")
    return changed, {"paragraph_replacements": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第二十九卷交通 / 第二章港口运输 / 第四节装卸 / 调度作业计划",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本修正单段，不触碰后续船舶预、确报段。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第二十九卷港口装卸调度回源修复

- 时间：{now}
- 范围：`第二十九卷交通 / 第二章港口运输 / 第四节装卸 / 调度作业计划`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 按页级 OCR 将 `港务调度、商务的代表起参加` 修为 `港务调度、商务的代表一起参加`。
- 按页级 OCR 将 `每月一一次的月度计划平衡会` 修为 `每月一次的月度计划平衡会`。
- 当前核验复跑段落替换：{changed} 处。

## 核对说明

- 本次仅替换 1958 年调度月度计划平衡会这一段，未触碰后续 `船舶预、确报` 与 `会议制度` 段。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第二十九卷港口装卸调度回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第二十九卷交通 `第二章港口运输 / 第四节装卸 / 调度作业计划` 进行单段回源修复。
- 源文依据：`{SOURCE_NOTE}`；修正 `港务调度、商务的代表一起参加` 与 `每月一次的月度计划平衡会`。
- 当前核验复跑段落替换 {changed} 处。
- 报告：`output/reports/reader_readability_port_loading_dispatch_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print(json.dumps({"changed": changed, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()

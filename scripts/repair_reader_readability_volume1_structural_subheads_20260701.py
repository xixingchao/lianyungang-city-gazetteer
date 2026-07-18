# -*- coding: utf-8 -*-
"""Split additional flattened structural subheadings in volume 1 reader text."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume1_structural_subheads_20260701.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume1_structural_subheads_20260701.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第一卷自然环境结构小标题粘连修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/body_chapters/paddle_上/第一卷_自然环境.md:611-1164,1429-2153,2728-2745"

HEADINGS: list[tuple[str, str]] = [
    ("一、西山", "由园林山"),
    ("二、中山", "由香炉顶"),
    ("三、东山", "由白鸽顶"),
    ("四、刘志洲山", "由岗嘴峰"),
    ("五、青龙山", "由淮河顶"),
    ("六、其馀独立山体", "孔望山"),
    ("五、羊山岛", "羊山岛"),
    ("六、竹岛", "竹岛"),
    ("七、鸽岛", "鸽岛"),
    ("四、气温", "气温特征"),
    ("九、霜雪", "霜 连云港市"),
    ("十、蒸发", "连云港市"),
    ("第二节水文", "清乾隆十年"),
]

INLINE_SUBHEADS: list[tuple[str, str]] = [
    ("霜", "连云港市有霜期"),
    ("雪", "连云港市降雪"),
    ("气温特征", "连云港市年平均气温"),
]


def split_one_heading(text: str, heading: str, body_start: str) -> tuple[str, int]:
    strong = f"<p><strong>{heading}</strong></p>"
    needle = heading + body_start
    if needle not in text:
        return text, 0
    pos = text.find(needle)
    replacement = f"</p>\n{strong}\n<p>{body_start}"
    if text.rfind("<p>", 0, pos) > text.rfind("</p>", 0, pos):
        text = text[:pos] + replacement + text[pos + len(needle):]
    else:
        text = text[:pos] + strong + "\n<p>" + body_start + text[pos + len(needle):]
    return text, 1


def split_inline_subhead(text: str, label: str, body_start: str) -> tuple[str, int]:
    strong = f"<p><strong>{label}</strong></p>"
    needle = label + body_start
    if needle not in text:
        return text, 0
    pos = text.find(needle)
    if text.rfind("<p>", 0, pos) <= text.rfind("</p>", 0, pos):
        return text, 0
    text = text[:pos] + f"{strong}\n<p>{body_start}" + text[pos + len(needle):]
    return text, 1


def patch_reader() -> int:
    text = HTML.read_text(encoding="utf-8")
    changed = 0
    for heading, body_start in HEADINGS:
        text, count = split_one_heading(text, heading, body_start)
        changed += count
    for label, body_start in INLINE_SUBHEADS:
        text, count = split_inline_subhead(text, label, body_start)
        changed += count

    remaining = [heading + body_start for heading, body_start in HEADINGS if heading + body_start in text]
    remaining += [label + body_start for label, body_start in INLINE_SUBHEADS if label + body_start in text]
    if remaining:
        raise RuntimeError(f"volume 1 structural heading residue remains: {remaining}")
    HTML.write_text(text, encoding="utf-8")
    return changed


def write_reports(changed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = len(HEADINGS) + len(INLINE_SUBHEADS)
    payload = {
        "time": now,
        "scope": "第一卷自然环境 / 锦屏山、岛屿、气候、水文若干结构标题",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "headings_split_this_run": changed,
        "note": "幂等复跑时 headings_split_this_run 可为 0；headings_in_scope 表示本脚本覆盖的标题/小题边界。",
        "headings_in_scope": total,
        "principle": "依据 PaddleOCR 正文汇总中的独立标题行，仅拆分阅读版标题粘连，不改写正文内容。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷自然环境结构小标题粘连修复

- 时间：{now}
- 范围：`第一卷自然环境 / 锦屏山、岛屿、气候、水文若干结构标题`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `一、西山由园林山...` 至 `六、其馀独立山体孔望山...` 等锦屏山小标题粘连。
- 拆分 `五、羊山岛羊山岛...`、`六、竹岛竹岛...`、`七、鸽岛鸽岛...` 岛屿小标题粘连。
- 拆分 `四、气温气温特征...`、`九、霜雪霜...`、`雪连云港市...`、`十、蒸发连云港市...`。
- 拆分 `第二节水文清乾隆十年...` 节标题粘连。
- 本轮只调整段落结构，不重录正文文字，不进行图片核字。
- 本脚本覆盖标题/小题边界：{total} 处；本次复跑新增拆分：{changed} 处。

## 核对说明

- 依据 `paddle_上/第一卷_自然环境.md` 中对应独立标题行确认边界。
- 脚本复跑会检查上述残串是否仍存在；若存在则报错。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-01 第一卷自然环境结构小标题粘连修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    total = len(HEADINGS) + len(INLINE_SUBHEADS)
    entry = f"""
{marker}

- 对正文可读性审计命中的第一卷自然环境多处结构标题压平进行修复。
- 源文依据：`{SOURCE_NOTE}`，确认锦屏山小山体、岛屿、气温/霜雪/蒸发、水文等标题在源文中为独立标题或小题。
- 阅读版仅拆分标题边界，不重录正文文字；本轮拆分 {changed} 处，范围覆盖 {total} 处标题/小题粘连。
- 报告：`output/reports/reader_readability_volume1_structural_subheads_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed = patch_reader()
    write_reports(changed)
    update_memory(changed)
    print("volume 1 structural subheadings repaired")
    print(f"headings_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

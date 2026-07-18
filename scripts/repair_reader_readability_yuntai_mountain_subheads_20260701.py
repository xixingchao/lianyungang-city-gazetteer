# -*- coding: utf-8 -*-
"""Split flattened Yuntai Mountain subheadings in volume 1 reader text."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_yuntai_mountain_subheads_20260701.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_yuntai_mountain_subheads_20260701.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260701_第一卷云台山小标题粘连修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/body_chapters/paddle_上/第一卷_自然环境.md:705-790"

HEADINGS: list[tuple[str, str]] = [
    ("四、九岭山", "九岭山"),
    ("五、虎窝山", "虎窝山"),
    ("六、推磨山", "推磨山"),
    ("七、万年山", "万年山"),
    ("八、抬崖山", "抬崖山"),
    ("九、双石人山", "位于"),
    ("十、朱麻山", "朱麻山"),
    ("十一、鬲峰山", "位于"),
    ("十二、新县大东山", "又名"),
    ("十三、其馀独立山体", "鸡鸣山"),
    ("第三节中云台山", "中云台山"),
    ("一、板桥西山", "因山"),
    ("二、推磨山", "由推磨顶"),
    ("三、溪云山", "古称"),
    ("四、黄泥岭", "由黄梅岭"),
    ("五、华盖山", "山形"),
    ("六、其馀独立山体", "有弁雾山"),
    ("第四节北云台山", "北云台山"),
]


def split_one_heading(text: str, heading: str, body_start: str) -> tuple[str, int]:
    strong = f"<p><strong>{heading}</strong></p>"
    if strong in text:
        return text, 0
    needle = heading + body_start
    pos = text.find(needle)
    if pos == -1:
        return text, 0
    replacement = f"</p>\n{strong}\n<p>{body_start}"
    if text.rfind("<p>", 0, pos) > text.rfind("</p>", 0, pos):
        text = text[:pos] + replacement + text[pos + len(needle):]
    else:
        text = text[:pos] + strong + "\n<p>" + body_start + text[pos + len(needle):]
    return text, 1


def patch_reader() -> int:
    text = HTML.read_text(encoding="utf-8")
    changed = 0
    for heading, body_start in HEADINGS:
        text, count = split_one_heading(text, heading, body_start)
        changed += count
    remaining = [heading + body_start for heading, body_start in HEADINGS if heading + body_start in text]
    if remaining:
        raise RuntimeError(f"Yuntai heading residue remains: {remaining}")
    HTML.write_text(text, encoding="utf-8")
    return changed


def write_reports(changed: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_headings = len(HEADINGS)
    payload = {
        "time": now,
        "scope": "第一卷自然环境 / 云台山系 / 南云台山至北云台山局部",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "headings_split_this_run": changed,
        "headings_in_scope": total_headings,
        "principle": "依据 PaddleOCR 正文汇总中的独立标题行，仅拆分阅读版标题粘连，不改写正文内容。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷云台山小标题粘连修复

- 时间：{now}
- 范围：`第一卷自然环境 / 云台山系 / 南云台山至北云台山局部`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 将阅读版中 `四、九岭山九岭山...五、虎窝山虎窝山...` 等小标题粘连拆为独立标题段。
- 同步处理 `第三节中云台山`、`一、板桥西山` 至 `第四节北云台山` 的相邻标题粘连。
- 本轮只调整段落结构，不重录地理描述文字，不进行图片核字。
- 本次复跑新拆分标题边界：{changed} 处；本范围累计覆盖标题：{total_headings} 处。

## 核对说明

- 依据 `paddle_上/第一卷_自然环境.md` 中 705-790 行的独立标题行确认边界。
- 阅读版原有正文文字保留，避免将不同 OCR 汇总版本的字形差异带入最终阅读版。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-01 第一卷云台山小标题粘连修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    total_headings = len(HEADINGS)
    entry = f"""
{marker}

- 对正文可读性审计命中的第一卷自然环境云台山段落小标题压平进行修复。
- 源文依据：`{SOURCE_NOTE}`，确认 `四、九岭山` 至 `第四节北云台山` 相关标题在源文中为独立行。
- 阅读版仅拆分标题边界，不重录正文文字；本范围覆盖 {total_headings} 处标题粘连。
- 报告：`output/reports/reader_readability_yuntai_mountain_subheads_20260701.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed = patch_reader()
    write_reports(changed)
    update_memory(changed)
    print("Yuntai Mountain subheadings repaired")
    print(f"headings_split={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

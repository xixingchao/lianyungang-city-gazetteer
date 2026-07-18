# -*- coding: utf-8 -*-
"""Remove duplicate linearized residue before the first-volume earthquake table."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_earthquake_table_residue_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_earthquake_table_residue_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第一卷地震统计表重复残文清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/body_chapters/paddle_上/第一卷_自然环境.md:6320-6358；workbench/ocr/paddle_ocr/上/part01/page_0211.txt"
CAPTION = "表1-25 1973～1990年连云港市1级以上地震统计表"
RESIDUE = "<p>震级（Ms）</p>\n<p>备注1973.6.27灌云小伊北3.21973.10.1东海平明房山之间3.6有震感1974.12.28灌云杨集南2.51975.6.13东海桃林西南2.4有震感1979.10.12东海山左口北2.5有震感1984.8.18灌云燕尾港2.31987.9.29赣榆塔山1.11989.2.23灌云伊山1.11989.4.22赣榆塔山1.01989.5.5赣榆县1.11989.5.30东海县1.61989.8.16赣榆塔山1.01989.8.24灌云东辛农场1.21989.12.9灌西盐场1.01990.1.24赣榆塔山1.51990.4.7赣榆塔山1.01990.7.2赣榆塔山1.31990.7.25赣榆塔山1.11990.10.26赣榆塔山1.0</p>\n"
RESIDUAL_MARKERS = [
    "备注1973.6.27灌云小伊北3.2",
    "东海平明房山之间3.6有震感1974.12.28",
]


def patch_reader() -> dict[str, object]:
    html = HTML.read_text(encoding="utf-8")
    before_count = html.count(RESIDUE)
    caption_count_before = html.count(CAPTION)
    if caption_count_before < 1:
        raise RuntimeError(f"earthquake table caption not found: {CAPTION}")
    if before_count:
        html = html.replace(RESIDUE, "", 1)
        HTML.write_text(html, encoding="utf-8")
    after = HTML.read_text(encoding="utf-8")
    remaining = {marker: after.count(marker) for marker in RESIDUAL_MARKERS}
    if any(remaining.values()):
        raise RuntimeError(f"earthquake residue remains: {remaining}")
    return {
        "residue_blocks_before": before_count,
        "residue_blocks_removed": 1 if before_count else 0,
        "caption_count_before": caption_count_before,
        "caption_count_after": after.count(CAPTION),
        "residual_markers": remaining,
    }


def write_reports(result: dict[str, object]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第一卷自然环境 / 表1-25 地震统计表前重复线性化残文",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "principle": "阅读版中已存在结构化地震统计表，本轮只删除表前重复的线性化 OCR 残文，不改表数据。",
        "result": result,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷地震统计表重复残文清理

- 时间：{now}
- 范围：`第一卷自然环境 / 表1-25 地震统计表前重复线性化残文`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 阅读版中 `表1-25 1973～1990年连云港市1级以上地震统计表` 前残留了表头 `震级（Ms）` 和整张表的压平 OCR 段。
- 该表已紧随其后以结构化表呈现；本轮仅移除重复残文，不改写表格数据、注记或后续正文。

## 结果

- 删除重复残文块：{result['residue_blocks_removed']}
- 表题保留数量：{result['caption_count_after']}
- 残文标记：{json.dumps(result['residual_markers'], ensure_ascii=False)}
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(result: dict[str, object]) -> None:
    marker = "## 2026-07-02 第一卷地震统计表重复残文清理"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对正文可读性审计命中的第一卷自然环境 `备注1973.6.27灌云小伊北...` 表格压平段进行清理。
- 源文依据：`{SOURCE_NOTE}`；阅读版中已紧随残文保留结构化 `表1-25 1973～1990年连云港市1级以上地震统计表`。
- 本轮只删除重复线性化残文 {result['residue_blocks_removed']} 块，不改表格数据、注记或后续正文。
- 报告：`output/reports/reader_readability_earthquake_table_residue_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    result = patch_reader()
    write_reports(result)
    update_memory(result)
    print("earthquake table residue removed")
    print(f"residue_blocks_removed={result['residue_blocks_removed']}")
    print(f"caption_count_after={result['caption_count_after']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

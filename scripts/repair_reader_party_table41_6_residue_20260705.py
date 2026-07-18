# -*- coding: utf-8 -*-
"""Remove duplicated T136 block and unverified table 41-6 OCR residue from reader flow."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_party_table41_6_residue_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_party_table41_6_residue_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第四十一卷表41-6残文撤出.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

START = '<section class="verified-table-block" id="table-LYG-中-T136">'
END = '<h4 id="第四十一卷-第二章解放后中共连云港市地方组织-第二节市代表会议、代表大会">'
SOURCE_NOTE = "workbench/ocr/paddle_ocr/中/part02/page_0421.txt；workbench/ocr/raw/中/part02/page_0421.txt"


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    start = html.find(START)
    if start < 0:
        raise RuntimeError("first T136 block not found")
    end = html.find(END, start)
    if end < 0:
        raise RuntimeError("following section heading not found")
    removed = html[start:end]
    if "市（县）委下辖区委、直属人民公社党委沿革表（一）" not in removed:
        raise RuntimeError("expected table 41-6 residue not found in removal span")
    if "市委下辖县委、区委、直属人民公社（乡镇）党委沿革表（二）" not in removed:
        raise RuntimeError("expected table residue tail not found in removal span")

    html = html[:start].rstrip() + "\n" + html[end:]
    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第四十一卷第二章表格残文",
        "removed_chars": len(removed),
        "removed_lines": removed.count("\n") + 1,
        "source_note": SOURCE_NOTE,
        "actions": [
            "删除第一次重复出现的 table-LYG-中-T136 结构化表块；该表已保留在本章已核结构化表格区。",
            "撤出表41-6及后续未核组织沿革图式的压平 OCR 残文，不伪装为已核结构化表。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第四十一卷表41-6残文撤出

- 时间：{now}
- 范围：第四十一卷第二章解放后中共连云港市地方组织。
- 删除跨度：{payload['removed_lines']} 行，{payload['removed_chars']} 字符。
- 源页核对：`{SOURCE_NOTE}`。

## 处理

- 删除正文流中第一次重复出现的 `table-LYG-中-T136` 表块；同表已在本章“已核结构化表格”区保留。
- 撤出 `表41-6 市（县）委下辖区委、直属人民公社党委沿革表（一）` 及后续未核表题残文的压平 OCR 段落。
- 本批不新增 `表41-6` 结构化表，不推断复杂组织沿革图式关系。

## 原则

只处理读者可见的重复块和未核表残文；不改正文叙述，不改已核表 JSON。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第四十一卷表41-6残文撤出"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 删除最终阅读版中正文流第一次重复出现的 `table-LYG-中-T136`；保留本章“已核结构化表格”区的同表。
- 据 `{SOURCE_NOTE}` 确认后续为 `表41-6` 及下一张组织沿革图式的未核压平 OCR 残文，已从主阅读流撤出。
- 未新增 `表41-6` 结构化数据；复杂图式留待后续回源核录。
- 报告：`output/reports/reader_party_table41_6_residue_20260705.md`。
""",
    )

    print(f"removed_lines={payload['removed_lines']}")
    print(f"removed_chars={payload['removed_chars']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

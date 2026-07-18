# -*- coding: utf-8 -*-
"""Repair source-backed text boundaries in the first volume final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume1_text_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume1_text_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第一卷正文断段与小标签边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = {
    "人均耕地3.4亩1966年，耕地面积减少到442.2万亩": "人均耕地3.4亩</p>\n<p>1966年，耕地面积减少到442.2万亩",
    "李汝珍在《镜花缘》中称葛藤粉“唯有海州云台山所产最佳。”紫草：生长于": "李汝珍在《镜花缘》中称葛藤粉“唯有海州云台山所产最佳。”</p>\n<p>紫草：生长于",
    "<p>积温 连云港市日平均气温稳定通过0℃": "<p><strong>积温</strong> 连云港市日平均气温稳定通过0℃",
    "<p>降水日数全市年平均大于（等于）0.1毫米": "<p><strong>降水日数</strong>全市年平均大于（等于）0.1毫米",
    "<p>降水强度根据20世纪80年代降雨自动记录统计": "<p><strong>降水强度</strong>根据20世纪80年代降雨自动记录统计",
    "<p>霜 连云港市有霜期常年平均为150天": "<p><strong>霜</strong> 连云港市有霜期常年平均为150天",
    "<p>专业气象台（站）连云港市辖区内专业气象台站始建于": "<p><strong>专业气象台（站）</strong>连云港市辖区内专业气象台站始建于",
}

SOURCE_LINES = [
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1523",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1545",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:1549",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:2143",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:2493",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5470-5471",
    "workbench/body_chapters/paddle_上/第一卷_自然环境.md:5557-5559",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> int:
    text = HTML.read_text(encoding="utf-8")
    changed = 0
    for old, new in REPLACEMENTS.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected one match for {old!r}, got {count}")
        text = text.replace(old, new, 1)
        changed += 1
    for residue in REPLACEMENTS:
        if residue in text:
            raise RuntimeError(f"residue remains: {residue}")
    HTML.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    changed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第一卷自然环境：正文断段与段首小标签边界",
        "html_boundaries_fixed": changed,
        "source_evidence": SOURCE_LINES,
        "notes": [
            "仅按源文行边界拆开两处正文粘连。",
            "段首小标签只加语义强调，不改正文文字。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""# 第一卷正文断段与小标签边界修复

- 时间：{now}
- 范围：第一卷自然环境，气象小标签、土地资源保护段、野生植物条目。
- 本次修复边界：{changed} 处。

## 修复

- 按源文行边界拆开 `人均耕地3.4亩` 与 `1966年，耕地面积...`。
- 按源文行边界拆开 `葛藤：...最佳。` 与 `紫草：...`。
- 将 `积温`、`降水日数`、`降水强度`、`霜`、`专业气象台（站）` 标为段首小标签。
- 不猜修 OCR 字词，不主动补标点。

## 依据

"""
    md += "".join(f"- `{line}`\n" for line in SOURCE_LINES)
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    marker = "## 2026-07-05 第一卷正文断段与小标签边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第一卷自然环境 2 处源文可证明的正文断段粘连：`3.4亩1966年`、`最佳。”紫草：`。
- 将 5 个气象段首小标签恢复为语义强调：`积温`、`降水日数`、`降水强度`、`霜`、`专业气象台（站）`。
- 只恢复边界和标签语义，不猜修 OCR 字词，不主动补标点。
- 报告：`output/reports/reader_readability_volume1_text_boundaries_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

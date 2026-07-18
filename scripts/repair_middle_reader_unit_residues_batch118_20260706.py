# -*- coding: utf-8 -*-
"""Repair mechanical unit/fixed-phrase OCR residues in the current middle reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "output" / "final_reader" / "连云港市志_中册.html"
REPORT_JSON = ROOT / "output" / "reports" / "middle_reader_unit_residues_batch118_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "middle_reader_unit_residues_batch118_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_中册单位与固定短语残留回源补修第一百一十八批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "电力单位千伏",
        "old": "干伏",
        "new": "千伏",
        "source": "Paddle 电力页多处为 `千伏/千伏安`，如 workbench/ocr/paddle_ocr/中/part01/page_0163.txt:23、page_0345.txt:32、page_0354.txt:11；中册分册残留均为电压/容量单位上下文",
    },
    {
        "label": "投入运行固定短语",
        "old": "投人运行",
        "new": "投入运行",
        "source": "Paddle 电力/建材页为 `投入运行`，如 workbench/ocr/paddle_ocr/中/part01/page_0259.txt 同类 `投入批量生产` 可证 `入/人` 混淆；本批只限固定短语 `投人运行`",
    },
    {
        "label": "万千瓦时单位",
        "old": "方千瓦时",
        "new": "万千瓦时",
        "source": "电力章统计单位上下文均为 `万千瓦时`；全书版同段已为万千瓦时",
    },
    {
        "label": "万千瓦单位",
        "old": "方千瓦",
        "new": "万千瓦",
        "source": "电力章装机/负荷单位上下文均为 `万千瓦`；先替换 `方千瓦时` 后再处理本项",
    },
    {
        "label": "万美元单位",
        "old": "方美元",
        "new": "万美元",
        "source": "外贸/开发区/商检金额上下文均为 `万美元`；全书版同类金额已同步为万美元",
    },
    {
        "label": "推广固定词",
        "old": "推厂",
        "new": "推广",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0500 附近口岸页已证 `推广电讯卫生检疫`；中册分册其余两处均为 `推广...法/方式` 固定动词",
    },
    {
        "label": "进入发展时期",
        "old": "进人发展时期",
        "new": "进入发展时期",
        "source": "workbench/ocr/paddle_ocr/中/part01/page_0259.txt:29；raw 同页误作 `进人发展时期`",
    },
]

LEFT_UNTOUCHED = [
    "`并人/输人/准海/准阴/项自` 等需要逐条上下文核验，本批不全局处理。",
    "乱码副本 HTML 不属于当前中文主交付，本批不处理。",
    "未展示、未嵌入图片。",
]


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    if next_start != -1:
        new += "\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    items = []
    for item in REPLACEMENTS:
        count = text.count(item["old"])
        if count:
            text = text.replace(item["old"], item["new"])
        items.append({**item, "count": count})
    TARGET.write_text(text, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    changed = sum(i["count"] for i in items)
    payload = {"time": now, "target": str(TARGET), "changed_this_run": changed, "items": items, "left_untouched": LEFT_UNTOUCHED}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 中册单位与固定短语残留补修第一百一十八批：Paddle/全书版回源核对",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 当前中册阅读版 `output/final_reader/连云港市志_中册.html`。",
        "- 仅处理电力/外贸金额单位和固定动词短语的机械 OCR 残留。",
        "",
        "## 统计",
        "",
        f"- 本次替换：{changed} 处",
        "",
        "## 修复项",
        "",
    ]
    for item in items:
        lines.append(f"- {item['label']}：`{item['old']}` -> `{item['new']}`，{item['count']} 处；源/定位：`{item['source']}`")
    lines.extend(["", "## 未处理边界", ""])
    for item in LEFT_UNTOUCHED:
        lines.append(f"- {item}")
    report = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report, encoding="utf-8")
    PROGRESS.write_text(report, encoding="utf-8")

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百一十八批：中册单位与固定短语残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 按 Paddle 页级 OCR 与全书版同段文字，补修当前中册分册读者中机械单位/固定短语残留：`干伏 -> 千伏`、`投人运行 -> 投入运行`、`方千瓦时 -> 万千瓦时`、`方千瓦 -> 万千瓦`、`方美元 -> 万美元`、`推厂 -> 推广`、`进人发展时期 -> 进入发展时期`。
- 本批只改 `output/final_reader/连云港市志_中册.html`，共 {changed} 处；报告：`output/reports/middle_reader_unit_residues_batch118_20260706.md`。
- 边界：`并人/输人/准海/准阴/项自` 等仍需逐条回源，不做全局替换；未展示、未嵌入图片。
""")
    print(json.dumps({"changed_this_run": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

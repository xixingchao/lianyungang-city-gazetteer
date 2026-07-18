# -*- coding: utf-8 -*-
"""Repair Paddle/full-reader-backed lower-volume OCR residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
REPORT_JSON = ROOT / "output" / "reports" / "lower_reader_project_units_batch119_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "lower_reader_project_units_batch119_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_下册项目推广与万元残留回源补修第一百一十九批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "安全技术措施项目范围",
        "old": "安全技术措施项自范围",
        "new": "安全技术措施项目范围",
        "source": "全书版同段为 `安全技术措施项目范围`；raw 下 part01/page_0275.txt:18 为项自残留",
    },
    {
        "label": "安全技术措施主要项目统计表",
        "old": "主要项自统计表",
        "new": "主要项目统计表",
        "source": "全书版同段表题已按项目理解；raw 下 part01/page_0275.txt:20 为项自残留",
    },
    {
        "label": "东辛奶牛项目协调会",
        "old": "东辛奶牛项自协调会",
        "new": "东辛奶牛项目协调会",
        "source": "全书版同段为 `东辛奶牛项目协调会`；raw 下 part01/page_0285.txt:32 断行为项自残留",
    },
    {
        "label": "星火计划项目",
        "old": "“星火计划”项自",
        "new": "“星火计划”项目",
        "source": "全书版同段为 `“星火计划”项目`；raw 下 part01/page_0428.txt:17 为项自残留",
    },
    {
        "label": "环境监测两个项目",
        "old": "监测大气、饮用水两个项自",
        "new": "监测大气、饮用水两个项目",
        "source": "全书版同段为 `监测大气、饮用水两个项目`；raw 下 part01/page_0455.txt:38 为项自残留",
    },
    {
        "label": "退休职工比赛项目",
        "old": "比赛项自有象棋",
        "new": "比赛项目有象棋",
        "source": "全书版同段为 `比赛项目有象棋`；raw 下 part02/page_0223.txt:14 为项自残留",
    },
    {
        "label": "幼儿运动会项目",
        "old": "幼儿运动会。项自有小皮球",
        "new": "幼儿运动会。项目有小皮球",
        "source": "固定体育竞赛用语；同卷多处 Paddle/raw 为 `比赛项目`",
    },
    {
        "label": "中学竞赛项目",
        "old": "竞赛项自有田径",
        "new": "竞赛项目有田径",
        "source": "固定体育竞赛用语；同卷多处 raw 为 `比赛项目有`",
    },
    {
        "label": "体育传统项目活动",
        "old": "体育传统项自活动",
        "new": "体育传统项目活动",
        "source": "raw 下 part02/page_0229.txt:14 与同页周边均为体育传统项目",
    },
    {
        "label": "体育传统项目学校",
        "old": "体育传统项自学校",
        "new": "体育传统项目学校",
        "source": "raw 下 part02/page_0229.txt:18/29 与全书版同段为 `体育传统项目学校`",
    },
    {
        "label": "职工运动会比赛项目",
        "old": "比赛项自有田径",
        "new": "比赛项目有田径",
        "source": "raw 下 part02/page_0242.txt:32 为项自残留；同页多处为比赛项目",
    },
    {
        "label": "省运会参赛项目",
        "old": "8个项自比赛",
        "new": "8个项目比赛",
        "source": "体育比赛固定用语；全书版项目类用词已规范为项目",
    },
    {
        "label": "开放报告项目投产",
        "old": "这批项自投产后",
        "new": "这批项目投产后",
        "source": "开放报告同段上下文为技术改造项目；全书版同类为项目",
    },
    {
        "label": "开放报告技术改造项目",
        "old": "技术改造项自需五亿元",
        "new": "技术改造项目需五亿元",
        "source": "全书版同段为 `技术改造项目需五亿元`",
    },
    {
        "label": "市里集资七千万元",
        "old": "市里集资七千方元",
        "new": "市里集资七千万元",
        "source": "全书版同段为 `市里集资七千万元`；raw 下 part02/page_0424.txt:11 为方元残留",
    },
    {
        "label": "建筑材料研究与推广",
        "old": "建筑材料研究与推厂",
        "new": "建筑材料研究与推广",
        "source": "全书版同段为 `建筑材料研究与推广`；raw 下 part01/page_0418.txt:4 为推厂残留",
    },
    {
        "label": "双城糯品种推广",
        "old": "在苏皖诸地推厂",
        "new": "在苏皖诸地推广",
        "source": "全书版同段为 `在苏皖诸地推广`；raw 下 part01/page_0437.txt:9 为推厂残留",
    },
    {
        "label": "电力系统推广",
        "old": "在全省电力系统推厂",
        "new": "在全省电力系统推广",
        "source": "全书版同段为 `在全省电力系统推广`",
    },
]

LEFT_UNTOUCHED = [
    "`方元` 中的旧币、可能人名/作品名、表格单位等未逐条核定者不处理。",
    "`并人/输人/准海/准阴` 等需要单独上下文核验，本批不全局替换。",
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
        "# 下册项目推广与万元残留补修第一百一十九批：全书版/Paddle 回源核对",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 当前下册阅读版 `output/final_reader/连云港市志_下册.html`。",
        "- 仅处理全书版同段或 OCR 上下文明确支持的项目、推广、万元残留。",
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百一十九批：下册项目推广与万元残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 按全书版同段和下册 raw/Paddle OCR 回源，补修当前下册分册读者中的 `项自 -> 项目`、`推厂 -> 推广`、`七千方元 -> 七千万元` 等确定残留。
- 本批只改 `output/final_reader/连云港市志_下册.html`，共 {changed} 处；报告：`output/reports/lower_reader_project_units_batch119_20260706.md`。
- 边界：`方元` 中的旧币、可能人名/作品名、表格单位等未逐条核定者不处理；`并人/输人/准海/准阴` 继续单独核验；未展示、未嵌入图片。
""")
    print(json.dumps({"changed_this_run": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

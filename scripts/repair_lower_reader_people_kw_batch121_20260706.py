# -*- coding: utf-8 -*-
"""Repair lower-reader people-count and kilowatt OCR residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
REPORT_JSON = ROOT / "output" / "reports" / "lower_reader_people_kw_batch121_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "lower_reader_people_kw_batch121_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_下册万人与千瓦残留回源补修第一百二十一批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "人防电动警报器功率",
        "old": "7.5干瓦电动警报器",
        "new": "7.5千瓦电动警报器",
        "source": "全书版同段为 `7.5千瓦电动警报器`；raw 下 part01/page_0189.txt:26 为干瓦残留",
    },
    {
        "label": "水灾灾民人数",
        "old": "灾民50方人，断炊者20方人",
        "new": "灾民50万人，断炊者20万人",
        "source": "全书版同段为 `灾民50万人，断炊者20万人`；raw 下 part01/page_0028.txt:22 为方人残留",
    },
    {
        "label": "民兵水库工程人次",
        "old": "出动民兵62方人次",
        "new": "出动民兵62万人次",
        "source": "全书版同段为 `出动民兵62万人次`；raw 下 part01/page_0184.txt:27 为方人残留",
    },
    {
        "label": "贫协会员人数",
        "old": "贫协会员发展到10.8方人",
        "new": "贫协会员发展到10.8万人",
        "source": "raw 下 part01/page_0343.txt:12；人数上下文为农村成人数比例",
    },
    {
        "label": "幼儿园入园人数",
        "old": "人园幼儿9.5方人",
        "new": "入园幼儿9.5万人",
        "source": "全书版同段为 `入园幼儿9.5万人`；raw 下 part01/page_0353.txt:11 为 `人园/方人` 残留",
    },
    {
        "label": "山区水库饮用水人数",
        "old": "饮用山区水库水3.78方人",
        "new": "饮用山区水库水3.78万人",
        "source": "全书版同段为 `饮用山区水库水3.78万人`；raw 下 part02/page_0172.txt:18 为方人残留",
    },
    {
        "label": "高氟区改水受益人数",
        "old": "受益65.13方人",
        "new": "受益65.13万人",
        "source": "全书版同段为 `受益65.13万人`；raw 下 part02/page_0181.txt:23 为方人残留",
    },
]

LEFT_UNTOUCHED = [
    "剩余 `方人` 需逐条区分人数、原文断句和正常词，不全局处理。",
    "本批只改当前下册分册读者；未展示、未嵌入图片。",
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
        "# 下册万人与千瓦残留补修第一百二十一批：全书版/raw 回源核对",
        "",
        f"> 生成时间：{now}",
        "",
        "## 修复范围",
        "",
        "- 当前下册阅读版 `output/final_reader/连云港市志_下册.html`。",
        "- 仅处理全书版同段或 raw/Paddle 上下文明确支持的万人/千瓦单位残留。",
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

    marker = "## 2026-07-06 高置信 OCR 错字补修第一百二十一批：下册万人与千瓦残留"
    upsert_memory(MEMORY, marker, f"""
{marker}

- 按全书版同段和 raw OCR 回源，补修当前下册分册读者中 `7.5干瓦 -> 7.5千瓦`、`方人 -> 万人` 的明确单位残留，覆盖水灾灾民、民兵水库工程人次、贫协会员、幼儿园入园、饮用水源和高氟区改水受益人数。
- 本批只改 `output/final_reader/连云港市志_下册.html`，共 {changed} 处；报告：`output/reports/lower_reader_people_kw_batch121_20260706.md`。
- 边界：剩余 `方人` 不做全局替换；未展示、未嵌入图片。
""")
    print(json.dumps({"changed_this_run": changed, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

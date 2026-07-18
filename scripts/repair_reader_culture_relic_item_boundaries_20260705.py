# -*- coding: utf-8 -*-
"""Restore source-backed culture and cultural-relic item boundaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_culture_relic_item_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_culture_relic_item_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_文化文物条目边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ITEMS = [
    ("十二、青口柳琴剧团", "青口柳琴剧团为1960年在青口镇业余文工团基础上组建的专业性演出团体。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:94104-94105"),
    ("二、更新舞台", "建于民国17年（1928年）10月，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:94260-94261"),
    ("三、新浦电影院", "为民国27年（1938年）新浦恒信杂货店", "workbench/body_chapters/连云港市志_全书_正文汇总.md:94267-94268"),
    ("四、人民舞台", "建于民国34年（1945年），", "workbench/body_chapters/连云港市志_全书_正文汇总.md:94272-94273"),
    ("九、东方影视中心", "位于新浦解放西路18号，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:94311-94312"),
    ("一、东海县民众教育馆", "原名东海县通俗教育馆。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:94369-94370"),
    ("二、大贤庄旧石器地点", "位于东海县马陵山中段山左口乡。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:96166-96167"),
    ("二、二涧遗址", "位于海州区锦屏山东麓南端的二涧口。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:96236-96237"),
    ("三、龙苴城", "位于灌云县龙乡驻地东北1.5公里，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:96337-96338"),
    ("二、陡沟汉墓群", "墓群分布在灌云县龙苴、陡沟二乡境内，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:96517-96518"),
    ("七、桃花涧画像石墓", "位于锦屏山南麓的棕红色粘土堆积台地上。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:96566-96567"),
    ("八、白鸽涧画像石墓", "位于锦屏山北麓。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:96582-96583"),
    ("十三、黄谭庙", "位于连云区墟沟镇东南龙头岭上。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:96837-96838"),
    ("十五、龙洞庵", "位于海州区孔望山东南侧的山麓台地上。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:96853-96854"),
    ("十六、海州福音堂", "位于海州南中街东首。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:96865-96866"),
    ("八、海州碧霞宫", "位于海州白虎山东麓，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:105231-105232"),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for title, lead, source in ITEMS:
        old = f"<p>{title}{lead}"
        new = f"<h5>{title}</h5>\n<p>{lead}"
        old_count = html.count(old)
        if old_count == 1:
            html = html.replace(old, new, 1)
            status = "changed"
            changed = 1
        elif old_count == 0 and html.count(new) >= 1:
            status = "already_applied"
            changed = 0
        else:
            raise RuntimeError(f"expected {title} once, got {old_count}")
        changes.append({"label": title, "status": status, "changed": changed, "source": source})

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "target": str(HTML.relative_to(ROOT)).replace("\\", "/"), "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 文化文物条目边界修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：按正文汇总独立分行恢复文化、文物 16 处条目标题边界，仅拆标题，不改正文文字。",
        "",
        "## 结果",
        "",
    ]
    for change in changes:
        lines.append(f"- {change['label']}：{change['status']}，本次变更 {change['changed']}")
        lines.append(f"  - `{change['source']}`")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 文化文物条目边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_culture_relic_item_boundaries_20260705.py`，按 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 独立分行恢复文化、文物 16 处条目标题边界。
- 覆盖：`十二、青口柳琴剧团`、`二、更新舞台`、`三、新浦电影院`、`四、人民舞台`、`九、东方影视中心`、`一、东海县民众教育馆`、`二、大贤庄旧石器地点`、`二、二涧遗址`、`三、龙苴城`、`二、陡沟汉墓群`、`七、桃花涧画像石墓`、`八、白鸽涧画像石墓`、`十三、黄谭庙`、`十五、龙洞庵`、`十六、海州福音堂`、`八、海州碧霞宫`。
- 报告：`output/reports/reader_culture_relic_item_boundaries_20260705.md`。
""",
    )

    print("reader_culture_relic_item_boundaries_repaired")
    print(f"changed={sum(change['changed'] for change in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

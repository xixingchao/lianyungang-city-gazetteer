# -*- coding: utf-8 -*-
"""Restore source-backed machinery, building-material, construction and power item boundaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_mech_building_power_item_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_mech_building_power_item_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_机械建材建筑电力条目边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ITEMS = [
    ("三、连云港市第二橡胶厂", "其前身为建于1971年3月的连云橡胶厂。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:131993-131994"),
    ("四、连云港市碳化硅厂", "该厂原名东海县浦南乡碳化硅厂，筹建于1978年9月。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:132005-132006"),
    ("二、赣榆县农业机械修理制造厂", "该厂是生产农机具的专业工厂，为县属全民企业。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:132759-132760"),
    ("四、连云港旋耕机集团", "该集团为县属全民企业，其前身系始建于1958年10月的灌云县农机修造厂。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:132784-132785"),
    ("五、手拉葫芦", "连云港市刀剪厂于1975年8月试产SH型0.5~1吨小吨位手拉葫芦，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:132862-132863"),
    ("五、滚齿机床", "东海县农机修造广1971年7月试制成功1台Y-38型滚齿机床，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:133778-133779"),
    ("一、圆孔板", "连云港市圆孔板生产始于1964年，市建筑公司木材加工厂预制车间开始生产简易的", "workbench/body_chapters/连云港市志_全书_正文汇总.md:138295-138296"),
    ("三、屋面板", "连云港市屋面板生产始于20世纪70年代中期，之后，屋面板生产规模逐渐扩大，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:138315-138316"),
    ("二、连云港市第二建筑工程公司", "该公司成立于1976年，当时名为连云港市第二建筑工程处，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:138769-138770"),
    ("四、海平线", "110千伏海平线是市区电网的110千伏主要线路。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:140387-140388"),
    ("二、牛山变电所", "牛山变电所位于东海县牛山镇和平东路59号，占地1.01万平方米。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:140460-140461"),
    ("六、茅口变电所", "茅口变电所位于连云港市新浦东北约4公里的开阔地带，占地2.4万平方米，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:140521-140522"),
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
        "# 机械建材建筑电力条目边界修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：按正文汇总独立分行恢复机械、建材、建筑、电力 12 处产品/企业/设施条目标题边界，仅拆标题，不改正文文字。",
        "- 跳过：`一、连云港市第一建筑工程公司` 未在正文汇总中找到对应独立标题，源段只出现表格施工单位名，本轮不处理。",
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

    marker = "## 2026-07-05 机械建材建筑电力条目边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_mech_building_power_item_boundaries_20260705.py`，按 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 独立分行恢复机械、建材、建筑、电力 12 处条目标题边界。
- 覆盖：`三、连云港市第二橡胶厂`、`四、连云港市碳化硅厂`、`二、赣榆县农业机械修理制造厂`、`四、连云港旋耕机集团`、`五、手拉葫芦`、`五、滚齿机床`、`一、圆孔板`、`三、屋面板`、`二、连云港市第二建筑工程公司`、`四、海平线`、`二、牛山变电所`、`六、茅口变电所`。
- `一、连云港市第一建筑工程公司` 在正文汇总检索到的是表格施工单位名，非独立条目标题，本轮保守跳过。
- 报告：`output/reports/reader_mech_building_power_item_boundaries_20260705.md`。
""",
    )

    print("reader_mech_building_power_item_boundaries_repaired")
    print(f"changed={sum(change['changed'] for change in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

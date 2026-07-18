# -*- coding: utf-8 -*-
"""Restore source-backed development-zone, port, customs and trade item boundaries."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_development_port_trade_item_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_development_port_trade_item_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_开发区口岸外贸条目边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ITEMS = [
    ("九、中国煤炭进出口连云港公司", "该公司成立于1983年，地址连云区墟沟镇。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:68464-68465"),
    ("十、连云港市纺织品进出口公司", "连云港市支公司，1989年改现名。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:68469-68470"),
    ("十四、江苏省连云港云湾贸易公司", "该公司成立于1987年，地址连云区墟沟北城路陕办大厦。", "workbench/body_chapters/连云港市志_全书_正文汇总.md:68494-68495"),
    ("八、化工进出口公司西山仓库", "由市化工医药保健品进出口公司与朝阳乡西山村合资兴建，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:71117-71118"),
    ("九、五矿进出口公司尹宋仓库", "是市五金矿产进出口公司与朝阳乡尹宋村合营的五矿进出口公司尹宋仓库，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:71121-71122"),
    ("三、土地使用权有偿转让和出让", "1990年3月15日，市人民政府颁发", "workbench/body_chapters/连云港市志_全书_正文汇总.md:144554-144555"),
    ("一、连云港市肉联厂", "该厂成立于1984年，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:144810-144811"),
    ("一、龙云石材加工厂", "该厂成立于1989年12月11日，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:144826-144827"),
    ("四、赣榆诸港", "赣榆县位于连云港市市政府驻地新浦西北方向，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:145059-145060"),
    ("一、航道航标", "航道民国22年（1933年）开港", "workbench/body_chapters/连云港市志_全书_正文汇总.md:145100-145101"),
    ("五、查缉走私", "查私民国20年（1931年）海州分关设立前后，", "workbench/body_chapters/连云港市志_全书_正文汇总.md:149745-149746"),
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
        "# 开发区口岸外贸条目边界修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：按正文汇总独立分行恢复开发区、港口、海关、外贸 11 处条目标题边界，仅拆标题，不改正文文字。",
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

    marker = "## 2026-07-05 开发区口岸外贸条目边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_development_port_trade_item_boundaries_20260705.py`，按 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 独立分行恢复开发区、港口、海关、外贸 11 处条目标题边界。
- 覆盖：`九、中国煤炭进出口连云港公司`、`十、连云港市纺织品进出口公司`、`十四、江苏省连云港云湾贸易公司`、`八、化工进出口公司西山仓库`、`九、五矿进出口公司尹宋仓库`、`三、土地使用权有偿转让和出让`、`一、连云港市肉联厂`、`一、龙云石材加工厂`、`四、赣榆诸港`、`一、航道航标`、`五、查缉走私`。
- 报告：`output/reports/reader_development_port_trade_item_boundaries_20260705.md`。
""",
    )

    print("reader_development_port_trade_item_boundaries_repaired")
    print(f"changed={sum(change['changed'] for change in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

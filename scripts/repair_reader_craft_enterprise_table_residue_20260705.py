# -*- coding: utf-8 -*-
"""Remove the flattened craft-enterprise table residue from the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_craft_enterprise_table_residue_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_craft_enterprise_table_residue_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_工艺企业表格残片清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD = (
    "<p>主要产品企业设备占地面积建筑面积企业名称产原值企业地址性质(人)年份名称(台)（万平方米）</p>\n"
    "<p>(万平方米）</p>\n"
    "<p>（万元）</p>\n"
    "<p>连云港市竹藤工集体1954竹、藤制品新浦解放桥西艺厂赣榆县城南烟花集体1958烟花、爆竹17.001.360.21赣榆县城南乡爆竹厂手工羊毛集体19583800.61连云港市地毯广1.98103108.00幸福路21号地毯连云港市羽毛工新浦新农路10集体羽毛画196419.20310.670.19艺厂-2号赣榆县工艺陶瓷日用瓷、艺赣榆县青口镇集体475197316.0010.56258.4760总厂术瓷镇海路7号</p>"
)

SOURCES = [
    "output/final_reader/连云港市志_全书.html:8211-8214",
    "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:2749-2775",
    "output/final_reader/连云港市志_全书.html:8227-8246",
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    count = html.count(OLD)
    if count == 1:
        html = html.replace(OLD, "", 1)
        status = "changed"
        changed = 1
    elif count == 0 and "连云港市竹藤工集体1954竹、藤制品" not in html:
        status = "already_applied"
        changed = 0
    else:
        raise RuntimeError(f"expected craft enterprise residue once, got {count}")
    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "status": status,
        "changed": changed,
        "sources": SOURCES,
        "notes": "仅撤出第十七卷末尾压扁企业表残片；未重建结构化表。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 工艺企业表格残片清理",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}` 第十七卷末尾。",
        f"- 结果：{status}，本次变更 {changed}。",
        "- 处理：撤出第十七卷末尾压扁的工艺企业基本情况表残片；后续正文边界为已核结构化表格区与第十八卷卷题。",
        "- 说明：本批不重建结构化表，只解决阅读版正文中残片可见问题。",
        "",
        "## 证据",
        "",
    ]
    for source in SOURCES:
        lines.append(f"- `{source}`")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 工艺企业表格残片清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_craft_enterprise_table_residue_20260705.py`，撤出第十七卷末尾 1 组压扁企业表残片（以 `连云港市竹藤工集体1954...` 开头）。
- 该残片位于第十七卷正文末尾，后续为已核结构化表格区和第十八卷卷题；本批只清理阅读版可见残片，不重建结构化表。
- 报告：`output/reports/reader_craft_enterprise_table_residue_20260705.md`。
""",
    )

    print("reader_craft_enterprise_table_residue_repaired")
    print(f"changed={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

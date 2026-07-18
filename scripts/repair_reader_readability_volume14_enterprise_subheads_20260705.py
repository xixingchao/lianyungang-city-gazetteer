# -*- coding: utf-8 -*-
"""Repair source-backed enterprise subheading boundaries in volume 14."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume14_enterprise_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume14_enterprise_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第十四卷企业简介标题边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

HEADINGS = [
    ("一、连云港市造纸厂", 10825),
    ("二、中国人民解放军第九七三四工厂", 10854),
    ("三、工贸合营连云港市京宁造纸厂", 10871),
    ("四、赣榆县造纸厂", 10883),
    ("五、赣榆县第二造纸厂", 10894),
    ("六、赣榆县第三造纸厂", 10904),
    ("一、连云港市新海印刷厂", 11204),
    ("二、赣榆县印刷厂", 11225),
    ("三、东海县印刷厂", 11244),
    ("四、灌云县印刷厂", 11254),
    ("一、连云港市包装一厂", 11435),
    ("二、连云港市包装二厂", 11455),
    ("三、连云港市金属包装厂", 11467),
    ("四、连云港市药用包装材料厂", 11481),
    ("五、连云港市南云台林场纸箱厂", 11494),
    ("六、赣榆县班庄包装厂", 11503),
    ("七、灌云县包装厂", 11511),
    ("八、连云港市新海玻璃厂", 11521),
    ("九、赣榆县玻璃厂", 11539),
]

SOURCE = "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md"


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> list[dict[str, object]]:
    text = HTML.read_text(encoding="utf-8")
    fixed: list[dict[str, object]] = []
    for heading, line in HEADINGS:
        old = f"<p>{heading}该厂"
        new = f"<h5>{heading}</h5>\n<p>该厂"
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected one match for {old!r}, got {count}")
        text = text.replace(old, new, 1)
        fixed.append({"heading": heading, "source": f"{SOURCE}:{line}"})
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第十四卷轻（手）工业：造纸、印刷、包装及玻璃主要企业简介",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": ["仅按 PaddleOCR 源文独立行恢复标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第十四卷企业简介标题边界修复

- 时间：{now}
- 范围：第十四卷轻（手）工业，造纸、印刷、包装及玻璃主要企业简介。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['heading']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 仅恢复源文可证明的版式边界，不改正文文字。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第十四卷企业简介标题边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第十四卷轻（手）工业 19 处企业简介标题粘正文问题，覆盖造纸、印刷、包装及玻璃主要企业简介。
- 依据 `workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md` 中独立行，只恢复标题边界，不改正文文字。
- 报告：`output/reports/reader_readability_volume14_enterprise_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

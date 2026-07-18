# -*- coding: utf-8 -*-
"""Repair source-backed service and environment subheading boundaries in volume 5."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume5_services_environment_followup_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume5_services_environment_followup_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第五卷服务环卫环保小标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md"

REPAIRS = [
    ("一、供气", "液化石油气1984年底", 4964, "供气供热"),
    ("二、供热", "市内集中供热始于1981年", 4986, "供气供热"),
    ("一、专业清扫", "民国34年（1935年）", 5017, "环境卫生-清扫"),
    ("二、民办保洁", "民国时期，城内小街巷", 5043, "环境卫生-清扫"),
    ("二、集运", "民国时期，城内生活垃圾", 5072, "环境卫生-垃圾集运"),
    ("一、公厕", "20世纪40年代初期", 5109, "环境卫生-粪便管理"),
    ("二、集运", "民国34年（1935年），东海县组成45人的服务队", 5129, "环境卫生-粪便集运"),
    ("一、新浦公园", "原名新海连市人民公园", 5294, "园林"),
    ("一、园林植物", "1985年，市区园林植物计有", 5326, "城市绿化"),
    ("一、水污染", "河流、水库污染 连云港市的水环境", 6089, "环境保护"),
    ("一、大气污染", "20世纪70年代以后", 7092, "环境保护"),
    ("一、环境噪声污染", "连云港市噪声污染主要是交通噪声污染", 7498, "环境保护"),
    ("一、土壤污染", "连云港市从20世纪60年代开始使用化学农药", 7565, "环境保护"),
    ("一、河流、水库监测", "1955～1979年", 7641, "环境监测"),
    ("一、新污染源控制", "1980年，市环保部门与市计划经济委员会", 8057, "污染源管理"),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> list[dict[str, str]]:
    text = HTML.read_text(encoding="utf-8")
    fixed = []
    for heading, prefix, line, group in REPAIRS:
        old = f"<p>{heading}{prefix}"
        new = f"<h5>{heading}</h5>\n<p>{prefix}"
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected one match for {group} {heading!r}, got {count}")
        text = text.replace(old, new, 1)
        fixed.append({"heading": heading, "group": group, "source": f"{SOURCE}:{line}"})
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五卷城乡建设/环境保护：供气供热、环卫、园林、污染与监测小标题边界",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": ["仅按 PaddleOCR 源文独立行恢复标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五卷服务环卫环保小标题边界补修

- 时间：{now}
- 范围：第五卷城乡建设/环境保护，供气供热、环境卫生、园林绿化、污染与监测。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['heading']}`（{item['group']}；依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 仅恢复源文可证明的版式边界，不改正文文字。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第五卷服务环卫环保小标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第五卷 15 处残留小标题粘正文问题，覆盖供气供热、环境卫生、园林绿化、污染与监测。
- 依据 `workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md` 中独立行，只恢复标题边界，不改正文文字。
- 报告：`output/reports/reader_readability_volume5_services_environment_followup_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Repair source-backed urban construction subheading boundaries in volume 5."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume5_urban_subheads_followup_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume5_urban_subheads_followup_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第五卷城乡建设小标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md"

REPAIRS = [
    ("一、中心城规划", "民国24年（1935年）1月", 2338),
    ("一、赣榆县县城规划", "1982年10月，《赣榆县县城总体规划》完成。", 2432),
    ("二、东海县县城规划", "20世纪50年代末，县政府制定了一个粗略的规划", 2443),
    ("三、灌云县县城规划", "《灌云县县城总体规划》完成于1985年。", 2464),
    ("一、建制镇规划", "1982年1月7日，国务院批转了《第二次全国农村房屋建设工作会议纪要》", 2480),
    ("二、一般集镇规划", "1978年，市基本建设委员会规划组编制出新县属集镇规划。", 2625),
    ("一、控制测量", "1957年，国家城建部第一大地测量队", 2643),
    ("二、地形测量", "民国11年（1922年）6月", 2667),
    ("三、航空测量", "1978年6月，为适应港口的发展和规划要求", 2679),
    ("一、干道", "明代，海州城内道路已有一定规模", 2707),
    ("二、一般道路", "民国时期，新浦陆续建成前街", 3103),
    ("三、市区小街巷", "今海州城内小街巷", 3123),
    ("一、水源", "地下水源民国26年（1937年）7月31日", 4275),
    ("二、水厂", "汉代，水井在朐县极为多见。", 4322),
    ("三、管网", "民国24年（1935年），中兴煤炭公司", 4410),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> list[dict[str, str]]:
    text = HTML.read_text(encoding="utf-8")
    fixed = []
    for heading, prefix, line in REPAIRS:
        old = f"<p>{heading}{prefix}"
        new = f"<h5>{heading}</h5>\n<p>{prefix}"
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected one match for {heading!r}, got {count}")
        text = text.replace(old, new, 1)
        fixed.append({"heading": heading, "source": f"{SOURCE}:{line}"})
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五卷城乡建设：规划、测绘、道路、供水小标题边界",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": ["仅按 PaddleOCR 源文独立行恢复标题边界，不改正文文字。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五卷城乡建设小标题边界补修

- 时间：{now}
- 范围：第五卷城乡建设，规划、测绘、道路、供水。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['heading']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 仅恢复源文可证明的版式边界，不改正文文字。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第五卷城乡建设小标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第五卷城乡建设 15 处残留小标题粘正文问题，覆盖规划、测绘、道路、供水。
- 依据 `workbench/body_chapters/paddle_上/第四卷至第十卷（part02）.md` 中独立行，只恢复标题边界，不改正文文字。
- 报告：`output/reports/reader_readability_volume5_urban_subheads_followup_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

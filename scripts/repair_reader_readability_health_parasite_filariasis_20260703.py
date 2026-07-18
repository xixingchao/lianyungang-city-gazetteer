# -*- coding: utf-8 -*-
"""Restore Fifth十五卷寄生虫病防治丝虫病小项 from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_parasite_filariasis_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_parasite_filariasis_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷寄生虫病防治丝虫病回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0180.txt:21-32"
SCOPE_START = '<p><strong>三、丝虫病</strong></p>'
SCOPE_END = '<p><strong>四、蛔虫病</strong></p>'

NEW_HTML = """<p><strong>三、丝虫病</strong></p>
<p>建国前，新浦、海州等地常见有下肢象皮肿病人，未见疫情记载。1955年，开始丝虫病调查，血检2402人，其中有385人查出微丝蚴，感染率为16.03%。采用海群生、卡巴砷治疗，结合爱国卫生运动消灭蚊子，控制传染媒介。1956年继续调查，血检8.99万人，微丝蚴阳性者6089人，感染率6.77%。工人感染率2.62%，农民感染率17.07%；10岁以下儿童感染率为5.1%，46岁以上成人感染率16.8%。多见一家数人被感染。在此次调查中发现下肢象皮肿32人。1956年全市普查中，共查17.65万人，占市区人口83.9%，查出微丝蚴阳性者9272人，总感染率5.25%。1960年血检14.83万人，感染率5.28%。1974年后，采用海群生拌食盐等方法普治。1971～1981年共查63.04万人次，感染率1.76%。</p>
<p>1983年，抽查市区5个乡的7个村，发现微丝蚴阳性率普遍下降。1983年后，省、市卫生防疫部门经5次考核确认连云港市三县四区已达国家卫生部制订消灭丝虫病的标准1%以下。1988年开始查漏补治和各项监测工作。</p>
"""

EXPECTED_TEXT = [
    "1971～1981年共查63.04万人次，感染率1.76%",
    "1983年后，省、市卫生防疫部门经5次考核确认",
]
RESIDUALS = ["1971~1981年"]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    changed = int(text[start:end] != NEW_HTML)
    if changed:
        HTML.write_text(text[:start] + NEW_HTML + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"residue remains: {remaining}")
    return changed, {"rewrote_scope": changed, "items_restored": 1, "paragraphs_restored": 2}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第二节寄生虫病防治 / 丝虫病",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本重建丝虫病小项，停止在四、蛔虫病前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷寄生虫病防治丝虫病回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：统一 `1971～1981年` 连接号。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷寄生虫病防治丝虫病回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第二章常见病防治 / 第二节寄生虫病防治` 中 `三、丝虫病` 至 `四、蛔虫病` 前。
- 修复内容：统一 `1971～1981年` 连接号。
- 报告：`output/reports/reader_readability_health_parasite_filariasis_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷寄生虫病防治丝虫病回源修复

- 对第五十五卷卫生 `第二章常见病防治 / 第二节寄生虫病防治` 的 `三、丝虫病` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `四、蛔虫病` 前。
- 统一 `1971～1981年` 连接号残留。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_parasite_filariasis_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷寄生虫病防治丝虫病回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()

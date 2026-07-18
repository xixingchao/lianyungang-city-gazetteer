# -*- coding: utf-8 -*-
"""Normalize source-verified range markers in Fifth十五卷地方病防治."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_endemic_ranges_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_endemic_ranges_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷地方病防治连接号回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = "workbench/ocr/paddle_ocr/下/part02/page_0181.txt:19-28"
SCOPE_START = '<h4 id="第五十五卷-第二章常见病防治-第三节地方病防治">第三节地方病防治</h4>'
SCOPE_END = '<h4 id="第五十五卷-第二章常见病防治-第四节计划免疫">第四节计划免疫</h4>'

NEW_HTML = """<h4 id="第五十五卷-第二章常见病防治-第三节地方病防治">第三节地方病防治</h4>
<p><strong>一、地方性氟中毒</strong></p>
<p>1983年开始进行地方性氟中毒情况调查，在高氟地区进行降氟改水工作。1986年，查清连云港市地方性氟中毒病区共321个村，总人口达43.49万，占全市农村总人口的16.91%。按患病程度排列，以东海县为首，依次为赣榆县、灌云县、市郊区。至1989年底，全市累计建立村级水厂131个、乡级水厂34个，受益65.13万人，使高氟区群众饮用低氟水。</p>
<p><strong>二、地方性甲状腺肿</strong></p>
<p>1983年，对地方性甲状腺肿情况调查，全市共抽样调查5个乡25个村的6.41万人，确诊患有甲状腺Ⅰ～Ⅱ度肿大的917人，患病率为1.4%。1985年，对该病发生地的7～14岁儿童普遍口服碘油丸，服药半年后观察效果，甲状腺肿大率下降4.3%，一年后再观察下降17.6%。</p>
"""

EXPECTED_TEXT = [
    "确诊患有甲状腺Ⅰ～Ⅱ度肿大的917人",
    "该病发生地的7～14岁儿童普遍口服碘油丸",
    "受益65.13万人，使高氟区群众饮用低氟水",
]
RESIDUALS = ["甲状腺Ⅰ~Ⅱ度", "7~14岁"]


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
    return changed, {"rewrote_scope": changed, "items_restored": 2, "paragraphs_restored": 2}


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第二章常见病防治 / 第三节地方病防治",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本核对本节，统一医学度数和年龄范围连接号，停止在第四节计划免疫前。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join([
            "# 第五十五卷地方病防治连接号回源修复",
            "",
            f"- 时间：{now}",
            f"- 范围：{payload['scope']}",
            f"- 源文：`{SOURCE_NOTE}`",
            f"- 阅读器：`{HTML}`",
            f"- 本次是否改写：{changed}",
            "- 修复：统一 `甲状腺Ⅰ～Ⅱ度`、`7～14岁` 连接号。",
            "",
        ]),
        encoding="utf-8",
    )
    PROGRESS.write_text(
        f"""# 第五十五卷地方病防治连接号回源修复

- 时间：{now}
- 源文依据：`{SOURCE_NOTE}`。
- 修复范围：`第五十五卷卫生 / 第二章常见病防治 / 第三节地方病防治`，止于 `第四节计划免疫` 前。
- 修复内容：统一 `甲状腺Ⅰ～Ⅱ度`、`7～14岁` 连接号。
- 报告：`output/reports/reader_readability_health_endemic_ranges_20260703.md`。
""".strip() + "\n",
        encoding="utf-8",
    )
    memory = f"""
## 2026-07-03 第五十五卷地方病防治连接号回源修复

- 对第五十五卷卫生 `第二章常见病防治 / 第三节地方病防治` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；重建至 `第四节计划免疫` 前。
- 统一 `甲状腺Ⅰ～Ⅱ度`、`7～14岁` 连接号。
- 当前核验复跑整段替换 {changed} 处。
- 报告：`output/reports/reader_readability_health_endemic_ranges_20260703.md`。
"""
    append_once(MEMORY, "## 2026-07-03 第五十五卷地方病防治连接号回源修复", memory)


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    print(json.dumps({"changed": changed, "counts": counts, "source": SOURCE_NOTE}, ensure_ascii=False))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Restore medical unit subheads from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_institution_medical_units_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_institution_medical_units_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷卫生机构医疗单位选介回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0210.txt:4-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0211.txt:3-38; "
    "workbench/ocr/paddle_ocr/下/part02/page_0212.txt:3-23"
)
SCOPE_START = '<h4 id="第五十五卷-第七章卫生机构-第三节医疗单位选介">第三节医疗单位选介</h4>'
SCOPE_END = '<!-- VERIFIED-STRUCTURED-TABLES-START -->'

REPLACEMENTS = [
    ("<p>一、连云港市第一人民医院建于", "<p><strong>一、连云港市第一人民医院</strong></p>\n<p>建于"),
    ("<p>二、连云港市第二人民医院前身为", "<p><strong>二、连云港市第二人民医院</strong></p>\n<p>前身为"),
    ("<p>三、连云港市第三人民医院建于", "<p><strong>三、连云港市第三人民医院</strong></p>\n<p>建于"),
    ("<p>四、连云港市第四人民医院建于", "<p><strong>四、连云港市第四人民医院</strong></p>\n<p>建于"),
    ("<p>五、连云港市妇女儿童医院建于", "<p><strong>五、连云港市妇女儿童医院</strong></p>\n<p>建于"),
    ("<p>六、连云港市中医院建于", "<p><strong>六、连云港市中医院</strong></p>\n<p>建于"),
    ("<p>七、连云港市蜂疗医院建于", "<p><strong>七、连云港市蜂疗医院</strong></p>\n<p>建于"),
    ("<p>八、连云港市康复医院建于", "<p><strong>八、连云港市康复医院</strong></p>\n<p>建于"),
    ("<p>九、江苏省盐业公司总医院建于", "<p><strong>九、江苏省盐业公司总医院</strong></p>\n<p>建于"),
    ("<p>十、连云港港务管理局职工医院建于", "<p><strong>十、连云港港务管理局职工医院</strong></p>\n<p>建于"),
    ("<p>十一、连云港市锦屏磷矿职工医院建于", "<p><strong>十一、连云港市锦屏磷矿职工医院</strong></p>\n<p>建于"),
    ("<p>十二、江苏连云港碱厂职工医院建于", "<p><strong>十二、江苏连云港碱厂职工医院</strong></p>\n<p>建于"),
    ("<p>十三、赣榆县人民医院赣榆县人民医院创建于", "<p><strong>十三、赣榆县人民医院</strong></p>\n<p>赣榆县人民医院创建于"),
    ("<p>十四、东海县人民医院东海县人民医院坐落", "<p><strong>十四、东海县人民医院</strong></p>\n<p>东海县人民医院坐落"),
    ("<p>十五、灌云县人民医院灌云县人民医院坐落", "<p><strong>十五、灌云县人民医院</strong></p>\n<p>灌云县人民医院坐落"),
    ("“文化大革命\"期间", "“文化大革命”期间"),
    ("1989年迁人墟沟镇院前村", "1989年迁入墟沟镇院前村"),
    ("灌云县县城一—一伊山镇", "灌云县县城——伊山镇"),
]

EXPECTED_TEXT = [
    "<strong>一、连云港市第一人民医院</strong>",
    "<strong>十五、灌云县人民医院</strong>",
    "“文化大革命”期间",
    "1989年迁入墟沟镇院前村",
    "灌云县县城——伊山镇",
]
RESIDUALS = [before for before, _ in REPLACEMENTS]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START) + len(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    changes = 0
    for before, after in REPLACEMENTS:
        if before in segment:
            segment = segment.replace(before, after)
            changes += 1
    if changes:
        HTML.write_text(text[:start] + segment + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"medical unit expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"medical unit residue remains: {remaining}")
    return changes, {"subheads_restored": 15, "ocr_typos_fixed": 3}


def write_reports(changes: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第七章卫生机构 / 第三节医疗单位选介",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changes,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本拆分十五个医疗单位小标题，并修正三处明确错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷卫生机构医疗单位选介回源修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第七章卫生机构 / 第三节医疗单位选介`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 将 `一、连云港市第一人民医院` 至 `十五、灌云县人民医院` 从正文粘连段中拆出为独立加粗小标题。
- 按页级 OCR 修正 `文化大革命` 引号、`迁人墟沟镇院前村`、`县城一—一伊山镇` 三处明确错识。
- 本次复跑新增替换：{changes} 处。
- 本轮未处理第五十六卷体育。

## 核对说明

- PaddleOCR `page_0210.txt` 确认第三节起始和第一至第四人民医院前段。
- PaddleOCR `page_0211.txt` 确认第四人民医院尾段至锦屏磷矿职工医院前段。
- PaddleOCR `page_0212.txt` 确认锦屏磷矿职工医院尾段至灌云县人民医院尾段。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changes: int) -> None:
    marker = "## 2026-07-03 第五十五卷卫生机构医疗单位选介回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第七章 `卫生机构` 的 `第三节医疗单位选介` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分十五个医疗单位小标题，并修正 `文化大革命` 引号、`迁入`、`——伊山镇` 三处错识。
- 本轮新增替换 {changes} 处；第五十六卷体育未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_institution_medical_units_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changes, counts = patch_reader()
    write_reports(changes, counts)
    update_memory(changes)
    print("health institution medical units section repaired")
    print(f"changes={changes}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

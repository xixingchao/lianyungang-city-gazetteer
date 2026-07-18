# -*- coding: utf-8 -*-
"""Restore health education section from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_education_section_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_education_section_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷教育科研教育节回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0206.txt:14-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0207.txt:3-5; "
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101512-101538; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:8205-8231"
)
SCOPE_START = '<h4 id="第五十五卷-第六章教育 科研-第一节教育">第一节教育</h4>'
SCOPE_END = '<h4 id="第五十五卷-第六章教育 科研-第二节科研">第二节科研</h4>'

NEW_HTML = """<p>市境内中医传统教育方式为祖传、自学和带徒弟。西医是从海州义德医院开始。民国7年（1918年），海州义德医院由美籍医士慕庚扬负责筹备护士学校，教学方式是边学边干，不定期授课，每周学习8~10小时。教学内容为人体解剖学、生理学、药物学、护理学、内科等。学制4~6年。民国15年，第一批学员毕业。此后每隔二三年招收5~10名学员，至民国36年，有10批学员共100人左右从该校毕业或肄业，除留院少数毕业生外，大部分学员在海属各县开业行医。</p>
<p>民国38年（1949年）2月，新海连特区卫生学校建立。设医务班、护士班、助产班，招收学员120人。7月，驻山东济宁市的鲁中南建国学校医务专修科80余名学员并入新海连特区卫生学校，校名改为鲁中南卫生学校。8月，毕业学员80余人。1950年，两批共毕业学员120余人，此后学校停办。毕业学员除少数输送中国人民解放军担任医务工作外，其余由山东省卫生厅分配各地工作。</p>
<p>1958年，新海连医学专科学校成立，招收学生52人。至1959年4月，并入南京医学院徐州分院。1958年，新海连市护士学校在新海连市海州人民医院成立。1959年更名为新海连市卫生学校，校址迁至海州城内新建街，设医士、护士两个专业，招生150人。1962年毕业生分配在市内及赣榆、东海、邳县工作，学校停办，改为卫生人员培训基地。1971年，连云港市卫生学校开办，设护士、医士专业，1975年增设中药剂士专业，面向全省招生。1988年，更名为连云港市中药学校。从1958~1989年，该校共毕业护士专业583人、中药剂士专业810人、医士专业160人。</p>
<p>1953~1990年，共办医务培训班54期，结业2390人。其中市卫生科于1951年举办的新海连市业余医务进修班，参加58人，为期2年；1990年2月，市卫生局举办的厂矿医师学习班，20人参加，为期2年。市卫生局于1963年举办的药剂人员培训班、医务人员短训班等10个培训班为期1年，其余培训班均为半年左右。</p>"""

EXPECTED_TEXT = [
    "药物学、护理学、内科等",
    "毕业或肄业，除留院少数毕业生外",
    "民国38年（1949年）2月",
    "80余名学员并入新海连特区卫生学校",
    "并入南京医学院徐州分院",
    "市卫生局举办的厂矿医师学习班，20人参加",
]
RESIDUALS = [
    "药物学，护理学",
    "毕业或肆业",
    "民国38年（1949年)2月",
    "学员并人新海连特区卫生学校",
    "并人南京医学院徐州分院",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START) + len(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    new_segment = "\n" + NEW_HTML + "\n"
    changed = int(text[start:end] != new_segment)
    if changed:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"health education expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"health education residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第六章教育 科研 / 第一节教育",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本复原教育节跨页文字和明确错识；未处理第二节科研。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷教育科研教育节回源修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第六章教育 科研 / 第一节教育`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 修正 `药物学，护理学` 为 `药物学、护理学`。
- 修正 `肆业` 为 `肄业`。
- 修正 `并人新海连特区卫生学校`、`并人南京医学院徐州分院` 为 `并入...`。
- 统一 `民国38年（1949年）2月` 括号，并按页级 OCR 接续 `厂矿医师学习班` 跨页句。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `第二节科研`。

## 核对说明

- PaddleOCR `page_0206.txt` 确认第一节教育首页文字。
- PaddleOCR `page_0207.txt` 确认跨页续句和 `第二节科研` 边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十五卷教育科研教育节回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第六章 `教育 科研` 的 `第一节教育` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；修正 `肄业`、`并入`、`药物学、护理学`，并接续 `厂矿医师学习班` 跨页句。
- 本轮新增整段替换 {changed} 处；`第二节科研` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_education_section_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("health education section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Restore county/district health bureau subheads from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_institution_county_bureaus_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_institution_county_bureaus_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷卫生机构区县卫生局回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0208.txt:31-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0209.txt:3-38; "
    "workbench/ocr/paddle_ocr/下/part02/page_0210.txt:3-4"
)
SCOPE_START = '<h4 id="第五十五卷-第七章卫生机构-第二节区、县卫生局">第二节区、县卫生局</h4>'
SCOPE_END = '<h4 id="第五十五卷-第七章卫生机构-第三节医疗单位选介">第三节医疗单位选介</h4>'

NEW_HTML = """<p><strong>一、新浦区卫生局</strong></p>
<p>1957年1月，新浦区人民委员会设卫生助理1人。1958年1月改设文教卫生科，设副科长2人。1969年10月，新浦区革命委员会成立，下设文卫组。1978年3月，文卫组撤销，改建卫生科，工作人员2人。1983年，新浦区与海州合并，称新海区，两区卫生科合并改称新海区卫生局。1984年5月，区卫生局设医政、人秘、卫生三股，编制9人。1986年6月，新浦、海州二区分设后重建新浦区卫生局。1990年，共有工作人员8人，其中4人为行政编制，4人为事业编制。</p>
<p><strong>二、海州区卫生局</strong></p>
<p>1956年2月，海州区人民政府设卫生助理，受区政府和市卫生科双重领导。1959年改称海州区人民委员会文教卫生科。1969年10月，海州区革命委员会成立，设文教卫生组。1978年5月，撤销文卫组改称卫生科。1982年增设副科长1人。1983年6月，新浦海州两区合并，称新海区，卫生科合并组建新海区卫生局。1986年7月，海州区恢复建制，设海州区卫生局。1990年，有工作人员5人，设医政、药政、人秘、财会四股。</p>
<p><strong>三、云台区卫生局</strong></p>
<p>1957年1月，盐区人民委员会设文教卫生科，有科长1名。1957年11月，云台区人民委员会设卫生助理。以后因区名多次变更。1982年4月，盐区人民政府建立卫生科。</p>
<p>1983年3月，南城区人民政府建立卫生科。1983年7月，又更名为云台区，成立云台区卫生局，设人秘、医政、计财三股，有工作人员5人。1990年仍有工作人员5人。</p>
<p><strong>四、连云区卫生局</strong></p>
<p>1957年11月，连云港区人民委员会设卫生助理1人。1958年改设文教卫生科。1974年12月成立连云区革命委员会文教卫生组。1978年12月改设卫生科。1984年3月改称连云区卫生局，设医政、药政、人秘三股。1990年有工作人员7人。</p>
<p><strong>五、赣榆县卫生局</strong></p>
<p>1946年2月，竹庭县政府（1950年10月复名赣榆县）设卫生科。1951年称赣榆县政府卫生科。1956年，赣榆县人民委员会设卫生科。1967年设文教卫生组。1970年8月设赣榆县卫生局。1990年，赣榆县卫生局有编制11人，实有20人，设人秘股、财务股、医政股、药政股四股。</p>
<p><strong>六、东海县卫生局</strong></p>
<p>1945年9月，海林县人民政府卫生科成立。年底，更名为东海县卫生科。工作人员3人，既是行政机构又是卫生机构。1981年2月成立东海县卫生局。1990年，东海县卫生局设人秘股、医政股、药政股、财务股四股、设局长1人，书记1人，副局长2人。</p>
<p><strong>七、灌云县卫生局</strong></p>
<p>1951年12月，灌云县人民政府设卫生科，有工作人员6人。1958年8月改为灌云县卫生局。1965年7月和灌云县文教局合并，成立灌云县文卫办公室。1966年，文卫办解体，恢复灌云县卫生局。1972年9月改为灌云县革命委员会卫生科。1975年2月成立灌云县卫生局。1990年灌云县卫生局有编制11人。</p>"""

EXPECTED_TEXT = [
    "<strong>一、新浦区卫生局</strong>",
    "1983年7月，又更名为云台区，成立云台区卫生局",
    "<strong>七、灌云县卫生局</strong>",
    "1990年灌云县卫生局有编制11人。",
]
RESIDUALS = [
    "一、新浦区卫生局1957年",
    "二、海州区卫生局1956年",
    "三、云台区卫生局1957年",
    "四、连云区卫生局1957年",
    "五、赣榆县卫生局1946年",
    "六、东海县卫生局1945年",
    "七、灌云县卫生局1951年",
    "1983年7月，文更名为云台区",
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
        raise RuntimeError(f"county bureau expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"county bureau residue remains: {remaining}")
    return changed, {"rewrote_scope": changed, "subheads_restored": 7}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第七章卫生机构 / 第二节区、县卫生局",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本拆分七个区县卫生局小标题，并修正云台区一处明确错识。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷卫生机构区县卫生局回源修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第七章卫生机构 / 第二节区、县卫生局`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 将 `一、新浦区卫生局` 至 `七、灌云县卫生局` 从正文粘连段中拆出为独立加粗小标题。
- 按页级 OCR 修正 `1983年7月，文更名为云台区` 为 `1983年7月，又更名为云台区`。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `第三节医疗单位选介`。

## 核对说明

- PaddleOCR `page_0208.txt` 确认第二节标题和新浦区卫生局起始。
- PaddleOCR `page_0209.txt` 确认新浦区尾段至灌云县卫生局前段。
- PaddleOCR `page_0210.txt` 确认灌云县卫生局尾句和第三节边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十五卷卫生机构区县卫生局回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第七章 `卫生机构` 的 `第二节区、县卫生局` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分七个区县卫生局小标题，并修正云台区段落中 `文更名` 为 `又更名`。
- 本轮新增整段替换 {changed} 处；`第三节医疗单位选介` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_institution_county_bureaus_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("health institution county bureaus section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

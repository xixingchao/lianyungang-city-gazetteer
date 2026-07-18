# -*- coding: utf-8 -*-
"""Split drug inspection headings from OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_drug_inspection_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_drug_inspection_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷药品检验标题修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101299-101324; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7995-8020; "
    "workbench/ocr/paddle_ocr/下/part02/page_0200.txt:23-37; "
    "workbench/ocr/paddle_ocr/下/part02/page_0201.txt:3-10"
)
SCOPE_START = '<h4 id="第五十五卷-第四章医政 药政-第五节药品检验">第五节药品检验</h4>'
SCOPE_END = '<h3 id="第五十五卷-第五章保健疗养">第五章保健疗养</h3>'

NEW_HTML = """<p><strong>一、自检</strong></p>
<p>1950年，市公立医院药房开始药品单项试验。1951年，市内各医院、诊所、药店在市卫生科督促下建立药品质量自检制度。1959年，新海连市海州人民医院、新海连市新浦人民医院、新海连市连云港人民医院、淮北盐务局工人医院及锦屏磷矿职工医院培训药品快速质量检验人员，各自进行药品化学定量、定性分析，年底各医、药单位建起药品质量监督检查网络。1963年，人民医院建立药品快速检验室，对自产制剂自检。为提高制剂质量，人民医院开展制剂中间品含量测定和热源试验，连云港市新浦人民医院建立药品检验室。1979年后，市内药品的生产、经营、使用各个环节建立质量自检体系并健全自检制度。1985年，药品经营部门开始在门市部设质量检查员；各医院实行自产制剂须由药检室签发合格证后方可用于临床的规章制度。</p>
<p><strong>二、抽检</strong></p>
<p>1959年，市卫生局药品检验所建立后，对各医、药单位的药品进行抽检，当年抽检药品样品84件，合格率为77.4%。1961~1964年，共检验药品895件，其中抽检样品505件。1964年11月，对部分医、药单位抽查，共检药品117件，合格率为70%。1978年8月，对市东风制药厂抽检，发现5%、10%葡萄糖注射液及氯化钠葡萄糖注射液有霉变现象，经跟踪检验，查出原因并进行改进。</p>
<p>1981~1985年，市药品检验所共抽检各医、药单位药品样品1203件，合格的有1054件，合格率为87.64%。其中药品生产厂家样品为832件，合格758件，合格率为91.11%。</p>
<p>1986年，对省盐务局职工医院、东海县人民医院等7家医院的制剂质量抽检，共抽检样品65个，合格56个，合格率为86.15%。1988年4月，对市内部分医、药单位的中药材、中药饮片抽检，共抽样133件，合格120件，合格率90.23%。1988～1990年，共抽检各类药品1505个批次，其中合格的1395个批次，合格率为92.69%。</p>"""

EXPECTED_TEXT = [
    "<p><strong>一、自检</strong></p>",
    "<p><strong>二、抽检</strong></p>",
    "对市东风制药厂抽检，发现5%、10%葡萄糖注射液及氯化钠葡萄糖注射液有霉变现象",
    "1988～1990年，共抽检各类药品1505个批次",
]
RESIDUALS = [
    "<p>一、自检：1950年",
    "<p>二、抽检1959年",
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
        raise RuntimeError(f"drug inspection expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"drug inspection residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第四章医政 药政 / 第五节药品检验",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本拆分药品检验两个小节标题；未处理第五章保健疗养。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷药品检验标题修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第四章医政 药政 / 第五节药品检验`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `一、自检` 小节标题，并移除正文前误粘的冒号。
- 拆分 `二、抽检` 小节标题。
- 按 OCR 复原抽检段跨页续文到 `第五章保健疗养` 前。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `第五章保健疗养`。

## 核对说明

- PaddleOCR `page_0200.txt` 确认 `第五节药品检验`、`一、自检`、`二、抽检` 及抽检首页文字。
- PaddleOCR `page_0201.txt` 确认抽检跨页尾段和 `第五章保健疗养` 边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷药品检验标题修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第四章第五节 `药品检验` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分 `一、自检`、`二、抽检` 标题，并按 OCR 核对抽检跨页尾段。
- 本轮新增整段替换 {changed} 处；`第五章保健疗养` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_drug_inspection_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("drug inspection section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

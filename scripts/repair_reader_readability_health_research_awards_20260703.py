# -*- coding: utf-8 -*-
"""Restore health research awards list from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_research_awards_20260703.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_research_awards_20260703.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260703_第五十五卷教育科研科研节奖励列表回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0207.txt:6-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0208.txt:3-12; "
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101538-101576; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:8231-8276"
)
SCOPE_START = '<h4 id="第五十五卷-第六章教育 科研-第二节科研">第二节科研</h4>'
SCOPE_END = '<h3 id="第五十五卷-第七章卫生机构">第七章卫生机构</h3>'

NEW_HTML = """<p>建国前，由于战争频仍，疾病研究工作一直未提到议事日程。建国后，人民政府非常重视医学科技研究，从60年代开始逐渐建立了一些科研实验室，70年代，开始进行地方性流行疾病的情况调查及研究，80年代后，对海域及海产品的放射性作调查研究。至1990年取得了许多科研成果，主要是在流行性疾病、海域放射调查、中医治疗等方面，其中，有些项目获得省部级以上的奖励。</p>
<p><strong>附55-1：获省部级以上政府奖励的主要项目</strong></p>
<p>《医疗体育对感冒、慢性气管炎、肺气肿疗效观察》：1978年获全国医药卫生科学大会奖。科研单位：连云港市肺气肿科研协作组。</p>
<p>《蜜蜂疗法的研究》：1978年获江苏省科技大会奖。科研单位：江苏省盐务局职工医院。</p>
<p>《疟疾防治的研究》：1978年获江苏省科技大会奖。科研单位：东海县卫生防疫站。</p>
<p>《眼球内异物立体定位器》《白内障冷冻摘除器和人工晶体》：1978年获江苏省科技大会奖。科研单位：东海县人民医院宋玉斋。</p>
<p><strong>附55-2：获省部级以上政府奖励科研协作项目</strong></p>
<p>《我国核试验产生的放射性落下灰的沉降特点及对环境的污染》：1978年获全国科学大会奖。科研单位：全国45个单位，连云港市卫生防疫站为其中协作单位。</p>
<p>《骨锶90分析方法及水平的调查》：1978年获全国医药卫生科学大会奖。科研单位：全国10个单位，连云港市卫生防疫站为其中协作单位。</p>
<p>《海产食品放射性调查》：1980年获国家卫生部二级成果奖。科研单位：青岛市卫生防疫站、连云港市卫生防疫站。</p>
<p>《江苏省沿海港河口海区环境质量评价方法》：1980年获国家卫生部二级成果奖。科研单位：江苏省卫生防疫站、连云港市卫生防疫站。</p>
<p>《渤、黄海海域放射性水平调查研究》：1983年获国家卫生部二级科技成果奖。科研单位：全国6个单位，连云港市卫生防疫站为其中协作单位。</p>
<p>《一九八二年全国营养调查》：1988年获国家科学技术进步二等奖。科研单位：全国29个省、市、自治区营养调查队，连云港市卫生防疫站为其中协作单位。</p>
<p>《中医药治疗流行性出血热临床和实验研究》：1988年获国家中医药管理局科技进步一等奖。科研单位：南京医学院、东海县人民医院。</p>"""

EXPECTED_TEXT = [
    "<strong>附55-1：获省部级以上政府奖励的主要项目</strong>",
    "《疟疾防治的研究》：1978年获江苏省科技大会奖。科研单位：东海县卫生防疫站。",
    "<strong>附55-2：获省部级以上政府奖励科研协作项目</strong>",
    "《骨锶90分析方法及水平的调查》：1978年获全国医药卫生科学大会奖。",
    "科研单位：南京医学院、东海县人民医院。",
]
RESIDUALS = [
    "附55-1：获省部级以上政府奖励的主要项目《医疗体育",
    "《症疾防治的研究》",
    "附552：获省部级以上政府奖励科研协作项目",
    "《骨锶90>分析方法及水平的调查》",
    "科研单位：南京医学院、东海县人民医院</p>",
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
        raise RuntimeError(f"health research expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"health research residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第六章教育 科研 / 第二节科研",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本拆分科研奖励列表并修正明确错识；未处理第七章卫生机构。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷教育科研科研节奖励列表回源修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第六章教育 科研 / 第二节科研`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 将 `附55-1`、`附55-2` 奖励项目从一个长段拆为标题和逐项段落。
- 修正 `症疾防治` 为 `疟疾防治`。
- 修正 `附552` 为 `附55-2`。
- 修正 `骨锶90>` 为 `骨锶90`。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `第七章卫生机构`。

## 核对说明

- PaddleOCR `page_0207.txt` 确认科研节导语、附55-1和附55-2前段。
- PaddleOCR `page_0208.txt` 确认附55-2尾段和 `第七章卫生机构` 边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-03 第五十五卷教育科研科研节奖励列表回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第六章 `教育 科研` 的 `第二节科研` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分 `附55-1`、`附55-2` 奖励项目列表，并修正 `疟疾防治`、`附55-2`、`骨锶90` 等错识。
- 本轮新增整段替换 {changed} 处；`第七章卫生机构` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_research_awards_20260703.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("health research awards section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

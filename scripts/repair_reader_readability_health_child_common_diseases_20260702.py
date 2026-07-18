# -*- coding: utf-8 -*-
"""Restore child common-disease correction subsection from page OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_child_common_diseases_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_child_common_diseases_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷儿童多发病矫治回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/ocr/paddle_ocr/下/part02/page_0204.txt:20-40; "
    "workbench/ocr/paddle_ocr/下/part02/page_0205.txt:4-5; "
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101443-101463; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:8138-8158"
)
SCOPE_START_OPTIONS = (
    '<p>二、儿童多发病矫治',
    '<p><strong>二、儿童多发病矫治</strong></p>',
)
SCOPE_END_OPTIONS = (
    '<p>三、儿童体格发育调查',
    '<p><strong>三、儿童体格发育调查</strong></p>',
)

NEW_HTML = """<p><strong>二、儿童多发病矫治</strong></p>
<p><strong>营养不良矫治</strong></p>
<p>市内小儿营养不良调查和矫治始于1961年9月，市卫生保健部门共查儿童30217人，查出1441人营养不良，占4.77%。调查结束后，市政府规定每名儿童每月增加供应代乳粉375克，食糖250克，对中度和重度营养不良儿童每人每月增加供应鸡蛋250~500克。1982年，市妇幼保健所在市机关幼儿园和麻纺厂幼儿园进行一次膳食情况调查，发现儿童食物中蛋白质和热量的供应均符合营养要求，但维生素A、B、C等供应不足，建议改进。1983年，在各幼托机构配备营养技术人员。1987年7月，举办幼托儿童膳食评价学习班，有34人参加。</p>
<p><strong>佝偻病防治</strong></p>
<p>1980年6月，对儿童体检中发现儿童中患有佝偻病。1982年在儿童缺铁性贫血调查中，在1340名儿童中检查出佝偻病患儿61人，佝偻病后遗症儿童46人，督促其抓紧时间治疗，并加强该病防治知识的宣传。1986年在市妇幼保健所就诊的183名儿童中，发现有6名活动性佝偻病患者。1987年，发现14名患者。1990年，在为全市儿童进行健康体检中发现活动性佝偻病儿童466人，占被检儿童总数389381人的0.12%。</p>
<p><strong>营养性缺铁性贫血防治</strong></p>
<p>1982年4月，对儿童贫血情况调查，共检查9个单位的1340名儿童，发现血红蛋白正常者269人，占20.9%；其余1020人均低于正常值，占79.1%，其中轻度贫血988人，中度贫血32人。市妇幼保健所在《妇幼卫生》小报上加强了有关知识的宣传。1985年，在新浦区中心幼儿园、市麻纺厂幼儿园进行一次贫血情况调查，确定轻度贫血151人，中度贫血97人，患病率为70.5%。调查结束后，市妇幼保健所在上述两幼儿园召开家长座谈会，讲授该病防治知识。1989年，检查2周岁以下儿童1908人，确诊轻度贫血415人，患病率21.8%。1990年，该病患病率已降至3.5%。</p>"""

EXPECTED_TEXT = [
    '<p><strong>二、儿童多发病矫治</strong></p>',
    '<p><strong>营养不良矫治</strong></p>',
    "每人每月增加供应鸡蛋250~500克",
    '<p><strong>佝偻病防治</strong></p>',
    "检查出佝偻病患儿61人，佝偻病后遗症儿童46人",
    "活动性佝偻病儿童466人，占被检儿童总数389381人的0.12%",
    '<p><strong>营养性缺铁性贫血防治</strong></p>',
    "1990年，该病患病率已降至3.5%",
]
RESIDUALS = [
    "二、儿童多发病矫治营养不良矫治",
    "营养不良矫治市内小儿",
    "向楼病防治",
    "伺倭病",
    "楼病后遗症",
    "活动性楼病",
    "营养性缺铁性贫血防治1982年",
    "1990年,该病患病率",
]


def find_scope(text: str) -> tuple[int, int]:
    starts = [text.find(marker) for marker in SCOPE_START_OPTIONS]
    valid_starts = [start for start in starts if start != -1]
    if not valid_starts:
        raise RuntimeError("child common diseases scope start not found")
    start = min(valid_starts)
    ends = [text.find(marker, start) for marker in SCOPE_END_OPTIONS]
    valid_ends = [end for end in ends if end != -1]
    if not valid_ends:
        raise RuntimeError("child common diseases scope end not found")
    return start, min(valid_ends)


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    new_segment = NEW_HTML + "\n"
    changed = int(text[start:end] != new_segment)
    if changed:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")

    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"child common diseases expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"child common diseases residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第五章保健疗养 / 第二节儿童保健 / 二、儿童多发病矫治",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本拆分本小节和三个分项标题；医学名词以页级 OCR 为准。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷儿童多发病矫治回源修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第五章保健疗养 / 第二节儿童保健 / 二、儿童多发病矫治`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `二、儿童多发病矫治` 小节标题。
- 拆分 `营养不良矫治`、`佝偻病防治`、`营养性缺铁性贫血防治` 三个分项标题。
- 修正 `向楼病`、`伺倭病`、`楼病` 等为 `佝偻病`。
- 修正 `1990年,该病患病率` 标点残损。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `三、儿童体格发育调查`。

## 核对说明

- PaddleOCR `page_0204.txt` 确认本小节标题、三个分项标题和全部主体文字。
- PaddleOCR `page_0205.txt` 确认下一小节 `三、儿童体格发育调查` 边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷儿童多发病矫治回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第五章第二节 `儿童保健` 的 `二、儿童多发病矫治` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分小节与三个分项标题，并按页级 OCR 修正 `佝偻病` 系列错识。
- 本轮新增整段替换 {changed} 处；`三、儿童体格发育调查` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_child_common_diseases_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("child common diseases section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

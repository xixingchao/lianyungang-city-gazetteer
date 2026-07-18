# -*- coding: utf-8 -*-
"""Split and source-correct western medicine surgery through pediatrics."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_western_medicine_surgery_pediatrics_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_western_medicine_surgery_pediatrics_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷西医外科儿科标题与OCR修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:100709-100773; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7408-7489; "
    "workbench/ocr/paddle_ocr/下/part02/page_0185.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0186.txt; "
    "workbench/ocr/paddle_ocr/下/part02/page_0187.txt"
)
SCOPE_START = '<p><strong>内分泌科</strong></p>'
SCOPE_END_OPTIONS = ('<p>耳鼻咽喉科', '<p><strong>耳鼻咽喉科</strong></p>')

REPLACEMENTS: list[tuple[str, str, str]] = [
    ("普外科标题", "<p>普外科清光绪三十四年（1908年）,海州", "<p><strong>普外科</strong></p>\n<p>清光绪三十四年（1908年），海州"),
    ("泌尿外科标题", "<p>泌尿外科民国3年", "<p><strong>泌尿外科</strong></p>\n<p>民国3年"),
    ("泌尿外科字形", "肾孟", "肾盂"),
    ("神经外科标题", "<p>神经外科1961年", "<p><strong>神经外科</strong></p>\n<p>1961年"),
    ("神经外科字形", "带浅动脉肌皮瓣", "带颞浅动脉肌皮瓣"),
    ("胸外科标题", "<p>胸外科1956年", "<p><strong>胸外科</strong></p>\n<p>1956年"),
    ("胸外科字形", "纵肿瘤", "纵膈肿瘤"),
    ("骨科标题", "<p>骨科民国19年", "<p><strong>骨科</strong></p>\n<p>民国19年"),
    ("骨科标点", "1967~1969年,市", "1967～1969年，市"),
    ("骨科缺字", "右动脉（外伤性缺损）", "右肱动脉（外伤性缺损）"),
    ("骨科字形", "腔前带血管蒂肌皮瓣", "胫前带血管蒂肌皮瓣"),
    ("骨科缺字", "带血管蒂肌骨移植", "带血管蒂肌腓骨移植"),
    ("烧伤科标题", "<p>烧伤科1960年", "<p><strong>烧伤科</strong></p>\n<p>1960年"),
    ("小儿外科标题", "<p>小儿外科市第二人民医院", "<p><strong>小儿外科</strong></p>\n<p>市第二人民医院"),
    ("小儿外科字形", "先天性隔疝", "先天性膈疝"),
    ("小儿外科字形", "横隔膜膨升", "横膈膜膨升"),
    ("小儿外科缺字", "尿道期成形", "尿道一期成形"),
    ("妇产科标题", "<p>妇产科民国3年", "<p><strong>妇产科</strong></p>\n<p>民国3年"),
    ("妇产科字形", "切开部剖腹手术", "切开剖腹手术"),
    ("妇产科缺字", "废除切开宫体的腹产手术", "废除切开宫体的剖腹产手术"),
    ("妇产科标点字形", "宫外孕，子富切除手术1957年", "宫外孕、子宫切除手术；1957年"),
    ("妇产科字形", "巨天粘液性", "巨大粘液性"),
    ("妇产科字形标点", "部宫取出活男婴：", "剖宫取出活男婴；"),
    ("妇产科缺字", "尿修补手术", "尿瘘修补手术"),
    ("妇产科缺字", "腹膜外腹产手术", "腹膜外剖腹产手术"),
    ("妇产科缺字", "进行腹产。", "进行剖腹产。"),
    ("妇产科字形", "腹膜外层次分离部宫产手术", "腹膜外层次分离剖宫产手术"),
    ("妇产科标点", "方法：为先天性", "方法；为先天性"),
    ("儿科标题", "<p>儿科建国前", "<p><strong>儿科</strong></p>\n<p>建国前"),
    ("儿科字形", "部分惠儿避免", "部分患儿避免"),
    ("儿科标点", "1962年,采用", "1962年，采用"),
    ("儿科标点", "免疫兴奋剂-——左旋咪唑", "免疫兴奋剂—左旋咪唑"),
]

EXPECTED_HEADINGS = [
    "普外科",
    "泌尿外科",
    "神经外科",
    "胸外科",
    "骨科",
    "烧伤科",
    "小儿外科",
    "妇产科",
    "儿科",
]
RESIDUALS = [
    "<p>普外科清光绪",
    "<p>泌尿外科民国3年",
    "<p>神经外科1961年",
    "<p>胸外科1956年",
    "<p>骨科民国19年",
    "<p>烧伤科1960年",
    "<p>小儿外科市第二人民医院",
    "<p>妇产科民国3年",
    "<p>儿科建国前",
    "肾孟",
    "带浅动脉肌皮瓣",
    "纵肿瘤",
    "右动脉（外伤性缺损）",
    "腔前带血管蒂肌皮瓣",
    "带血管蒂肌骨移植",
    "先天性隔疝",
    "横隔膜膨升",
    "尿道期成形",
    "切开部剖腹手术",
    "宫体的腹产手术",
    "外腹产手术",
    "子富切除",
    "巨天粘液性",
    "部宫取出活男婴",
    "尿修补手术",
    "进行腹产。",
    "部宫产手术",
    "部分惠儿避免",
    "1962年,采用",
    "免疫兴奋剂-——左旋咪唑",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    ends = [text.find(marker, start) for marker in SCOPE_END_OPTIONS]
    valid_ends = [end for end in ends if end != -1]
    if not valid_ends:
        raise RuntimeError("western medicine surgery scope end not found")
    return start, min(valid_ends)


def patch_segment(segment: str) -> tuple[str, int, dict[str, int]]:
    changed = 0
    counts: dict[str, int] = {}
    for label, needle, replacement in REPLACEMENTS:
        count = segment.count(needle)
        if count:
            segment = segment.replace(needle, replacement)
            counts[label] = count
            changed += count

    missing = [h for h in EXPECTED_HEADINGS if f"<p><strong>{h}</strong></p>" not in segment]
    if missing:
        raise RuntimeError(f"western medicine surgery heading markers missing: {missing}")
    remaining = [marker for marker in RESIDUALS if marker in segment]
    if remaining:
        raise RuntimeError(f"western medicine surgery OCR residue remains: {remaining}")
    return segment, changed, counts


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    new_segment, changed, counts = patch_segment(segment)
    if new_segment != segment:
        HTML.write_text(text[:start] + new_segment + text[end:], encoding="utf-8")
    return changed, counts


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第三章医疗 / 第二节西医 / 普外科至儿科",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "target_headings": EXPECTED_HEADINGS,
        "principle": "依据 PaddleOCR 页级文本，拆分西医外科系统至儿科分项标题，并修复源页可证 OCR 错字；未处理耳鼻咽喉科及后续。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷西医外科儿科标题与 OCR 修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第三章医疗 / 第二节西医` 的 `普外科` 至 `儿科`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `普外科`、`泌尿外科`、`神经外科`、`胸外科`、`骨科`、`烧伤科`、`小儿外科`、`妇产科`、`儿科` 9 个分项标题。
- 依据 PaddleOCR `page_0185.txt` 修复 `肾盂`、`带颞浅动脉肌皮瓣` 等可证字词。
- 依据 PaddleOCR `page_0186.txt` 修复 `纵膈肿瘤`、`右肱动脉`、`胫前带血管蒂肌皮瓣`、`带血管蒂肌腓骨移植`、`膈疝`、`横膈膜`、`尿道一期成形` 等可证字词。
- 依据 PaddleOCR `page_0187.txt` 修复妇产科、儿科段落内 `剖腹产`、`子宫切除`、`巨大粘液性卵巢囊肿`、`剖宫取出活男婴`、`尿瘘修补`、`剖宫产`、`患儿`、`免疫兴奋剂—左旋咪唑` 等可证字词。
- 本次复跑新增替换：{changed} 处。
- 本轮未处理 `耳鼻咽喉科` 及后续专科。

## 核对说明

- PaddleOCR `page_0185.txt` 确认普外科、泌尿外科、神经外科前段。
- PaddleOCR `page_0186.txt` 确认神经外科续段、胸外科、骨科、烧伤科、小儿外科、妇产科起始。
- PaddleOCR `page_0187.txt` 确认妇产科续段、儿科及下一专科边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷西医外科儿科标题与OCR修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第三章第二节 `西医` 的 `普外科` 至 `儿科` 段进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；确认 9 个专科分项标题，并据页级 OCR 修复 `肾盂`、`带颞浅动脉肌皮瓣`、`纵膈肿瘤`、`右肱动脉`、`胫前带血管蒂肌皮瓣`、`先天性膈疝`、`尿道一期成形`、`剖宫产`、`患儿` 等可证字词。
- 本轮新增替换 {changed} 处；`耳鼻咽喉科` 及后续专科未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_western_medicine_surgery_pediatrics_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("western medicine surgery/pediatrics section repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

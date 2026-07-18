# -*- coding: utf-8 -*-
"""Second source-verified readability repair batch for Volume 20."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_chemical_batch2_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_chemical_batch2_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_第二十卷化学工业高置信错识第二批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SCOPE_START = '<h2 id="第二十卷-化学工业">第二十卷化学工业</h2>'
SCOPE_END = '<h2 id="第二十一卷-机械工业">第二十一卷机械工业</h2>'
SOURCE = "workbench/ocr/paddle_ocr/中/part01/page_0143.txt:1-5; page_0146.txt:21-24; page_0156.txt:28-33; page_0158.txt:12-26; page_0164.txt:9-15; page_0171.txt:17-40; page_0179.txt:31-40; page_0181.txt:29-40; page_0182.txt:1-19; page_0184.txt:37-39; page_0185.txt:1-3; page_0188.txt:1-20"
REPLACEMENTS = [
    ("原料生产厂", "化工原料专、兼营生产广31家", "化工原料专、兼营生产厂31家"),
    ("七五引号", "国家“七五计划重点项目", "国家“七五”计划重点项目"),
    ("墟沟", "在连云区沟开工", "在连云区墟沟开工"),
    ("并入南化", "并人南京化学工业", "并入南京化学工业"),
    ("第一设计院", "国家轻工业部第设计院", "国家轻工业部第一设计院"),
    ("并入海滨", "并人市海滨化工厂", "并入市海滨化工厂"),
    ("氯气", "市化工厂生产的氟气", "市化工厂生产的氯气"),
    ("甲酸创汇", "创汇32.5万美元", "创汇325万美元"),
    ("七二化工厂", "赣榆县七二二化工厂", "赣榆县七二化工厂"),
    ("海藻酸钠吨", "海藻酸钠160饨", "海藻酸钠160吨"),
    ("五十年代末", "20世纪50年代未", "20世纪50年代末"),
    ("黄磷厂", "市黄磷广", "市黄磷厂"),
    ("海滨完整产量", "1990年，该厂拥有4吨锅炉2台、整流设备1套、蒸发器3台、机床5台、电解槽60只、离心机11台，当年生产磷酸二氢钾44吨、氢氧化钾955吨、漂液11213饨、焦磷酸钾焦磷酸钾出口美国、日本等欧亚各地。</p>\n<p>万元；职工605人，其中专业技术人员65人；设有16个科室、6个生产车间、2个辅助车间和1个活性炭分厂；当年完成产值1524万元，实现利税97万元。", "1990年，该厂拥有4吨锅炉2台、整流设备1套、蒸发器3台、机床5台、电解槽60只、离心机11台，当年生产磷酸二氢钾44吨、氢氧化钾955吨、漂液11213吨、焦磷酸钾265吨、碳酸锌300吨。其中磷酸二氢钾产量为全国之冠，销往全国28个省、市、自治区，焦磷酸钾出口美国、日本等欧亚各地。</p>\n<p>1990年，该厂占地面积7.07万平方米，建筑面积1.73万平方米，固定资产原值382万元；职工605人，其中专业技术人员65人；设有16个科室、6个生产车间、2个辅助车间和1个活性炭分厂；当年完成产值1524万元，实现利税97万元."),
    ("Y25", "Y25－4压片机", "Y25-4压片机"),
    ("磷化铝出口吨", "累计出口磷化铝粉（片）剂273，", "累计出口磷化铝粉（片）剂273吨，"),
    ("溴甲烷缺段", "术。次年10月正式投产。1979年实产溴甲烷83吨，1980年实产139吨。1984年7月，该1986年12月和1987年2月，该厂的溴甲烷产品先后获省、部优质产品称号。", "溴甲烷1978年，市海水化工一厂无偿接受南京钟山化工厂的溴甲烷生产设备和技术。次年10月正式投产。1979年实产溴甲烷83吨，1980年实产139吨。1984年7月，该厂将溴甲烷车间迁往新厂并进行扩建，使年生产能力增至350吨。1985年，实产233吨。1986年12月和1987年2月，该厂的溴甲烷产品先后获省、部优质产品称号。"),
    ("搪瓷", "糖瓷反应釜", "搪瓷反应釜"),
    ("杀虫脒标题", "速灭菊酯、杀虫胖", "速灭菊酯、杀虫脒"),
    ("杀虫脒产品", "新产品杀虫胖", "新产品杀虫脒"),
    ("杀虫脒生产线", "杀虫胖生产线", "杀虫脒生产线"),
    ("305吨", "实产248饨", "实产248吨"),
    ("田菁吨", "达到2000饨", "达到2000吨"),
    ("并入硫酸厂", "并人市硫酸厂", "并入市硫酸厂"),
    ("十溴联苯醚", "十漠联苯醚", "十溴联苯醚"),
    ("游离溴", "游离漠含量", "游离溴含量"),
    ("二溴丙基", "二漠丙基", "二溴丙基"),
    ("光稃总述", "光荐香草浸膏", "光稃香草浸膏"),
    ("光稃正文", "光荐香草送经", "光稃香草送经"),
    ("光稃浸膏", "光荐香草浸膏", "光稃香草浸膏"),
    ("香豆素酊", "香豆素、玫瑰油", "香豆素酊、玫瑰油"),
    ("炭砖吨", "炭砖年生能力达到5000饨", "炭砖年生产能力达到5000吨"),
    ("炭素电极生产能力", "炭素电极类年生能力", "炭素电极类年生产能力"),
    ("光明产值", "实现产值250元，利税33.7万元", "实现产值250万元，利税33.7万元"),
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START)
    end = text.index(SCOPE_END, start)
    return start, end


def patch_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    original = text[start:end]
    segment = original
    counts: dict[str, int] = {}
    for label, old, new in REPLACEMENTS:
        count = segment.count(old)
        if count:
            segment = segment.replace(old, new)
        elif new not in segment:
            raise RuntimeError(f"neither old nor new text found: {label}")
        counts[label] = count
    if segment != original:
        HTML.write_text(text[:start] + segment + text[end:], encoding="utf-8")
    verify_reader()
    return counts


def verify_reader() -> None:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    segment = text[start:end]
    missing = [new for _label, _old, new in REPLACEMENTS if new not in segment]
    residuals = [old for _label, old, new in REPLACEMENTS if old in segment and old not in new]
    if missing or residuals:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}")


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    current_changes = sum(counts.values())
    verified_items = len(REPLACEMENTS)
    payload = {
        "time": now,
        "scope": "第二十卷化学工业第二批",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": verified_items,
        "current_run_replacements": current_changes,
        "counts": counts,
        "principle": "仅修复页级 OCR 直接证明的第二十卷残留错识和短段缺漏；未核定表格残文继续保留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第二十卷化学工业高置信错识第二批回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{verified_items} 项",
        f"- 本次脚本复跑实际改写：{current_changes} 处",
        "- 重点：继续修正生产厂、并入、氯气、杀虫脒、搪瓷、溴/光稃/吨/万元等残留错识。",
        "- 补句：按源页补回溴甲烷段和海滨化工厂 1990 年产量、厂区资产短段。",
        "- 保留：本卷剩余未由源页清楚证明的断裂与表格串行不在本批处理。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")
    memory = f"""
## 2026-07-04 第二十卷化学工业高置信错识第二批回源修复

- 继续对第二十卷化学工业做小批回源修复，范围限定在 `第二十卷-化学工业` 到 `第二十一卷-机械工业` 前。
- 源文依据：`{SOURCE}`。
- 修复示例：`生产广31家`→`生产厂31家`，`氟气`→`氯气`，`杀虫胖`→`杀虫脒`，`糖瓷反应釜`→`搪瓷反应釜`，`光荐香草浸膏`→`光稃香草浸膏`，并补回溴甲烷段和海滨化工厂产量资产短段。
- 本批核验修复 {verified_items} 项；未核定的表格残文和长段断裂继续保留。
- 报告：`output/reports/reader_readability_chemical_batch2_20260704.md`。
"""
    append_once(MEMORY, "## 2026-07-04 第二十卷化学工业高置信错识第二批回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

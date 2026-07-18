# -*- coding: utf-8 -*-
"""Restore front subsections of pharmacy administration from OCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_health_pharmacy_management_front_20260702.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_health_pharmacy_management_front_20260702.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260702_第五十五卷药政管理前两小节回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE_NOTE = (
    "workbench/body_chapters/连云港市志_全书_正文汇总.md:101175-101199; "
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:7871-7895; "
    "workbench/ocr/paddle_ocr/下/part02/page_0197.txt:11-37; "
    "workbench/ocr/paddle_ocr/下/part02/page_0198.txt:3-11"
)
SCOPE_START = '<h4 id="第五十五卷-第四章医政 药政-第四节药政管理">第四节药政管理</h4>'
SCOPE_END_OPTIONS = ("<p>三、药品经营质量管理", "<p><strong>三、药品经营质量管理</strong></p>")

NEW_HTML = """<p><strong>一、药政管理机构</strong></p>
<p>1951年1月，市政府卫生科责成市新药业公会贯彻执行由华东军政委员会卫生部颁发的药品管理条例。1958年7月，市卫生局所属的市医药公司内设药政管理处，由医药公司经理兼任处长。1961年，市药政管理处在市卫生局内办公，设专职管理人员1人。</p>
<p>1966年，市药政管理处停止办公。1969年9月，市卫生局恢复药政管理工作，在卫生组内设两名药政管理专职干部。1980年，市卫生局设药政科。1983年，改称连云港市卫生局药政管理处。</p>
<p><strong>二、药品生产质量管理</strong></p>
<p>1959年8月，市卫生局组织中西药品检查组，对新海连市海州人民医院红旗制药厂、新海连市新浦人民医院制药厂、新浦制药厂等药品生产厂家及药品使用单位建立药品质量监督网，聘请专业技术人员和老药工共38人为药品质量监督员。1961～1965年，按江苏省重工业厅和卫生厅颁发的《关于药品和医疗器械生产质量管理暂行办法》监督管理药品质量。</p>
<p>1966～1969年，药政管理工作停顿，1970年恢复。市内各医院及郊区医疗站均自制各种静脉注射液和肌肉注射液，如生理盐水、5%葡萄糖液、大蒜注射液、板兰根注射液、鱼腥草注射液等，常发生质量事故。1973年6月，贯彻国务院批转国家卫生部、商业部、燃料化学工业部《关于加强药品质量管理工作》精神，对向阳制药厂、中成药厂、生物化学制药厂及东方红化工厂、红旗化工厂、酿化厂、果酒厂、电线厂、海光化工厂等综合利用制药厂进行生产性整顿，规定凡未经江苏省卫生局审批的药品，生产单位不准生产，经营单位不准销售，医疗单位不准使用。整顿后药品质量开始提高。</p>
<p>1981年，各药厂皆设质量检验科（股），在各生产车间配备专兼职质量检查员，健全药品生产质量档案，建立药品留样观察制度。当年206个药品生产品种办理重新报省药政部门审批手续。</p>
<p>1985年，开始贯彻《中华人民共和国药品管理法》（下称《药品管理法》），举办各药厂厂长、质检科长、生产科长学习班。1985年7月1日，《药品管理法》实施后，于10月组织药政、药检专业人员对药品生产单位调查和整顿，有10家药品生产单位通过市、省药政部门检查验收，取得《药品生产企业许可证》。1987年8月，市卫生局根据省卫生厅《关于对药品生产企业监督检查的通知》，组织检查组，对4个专业药厂和3个综合利用药点进行检查，共查30个品种，176个批次。当年，还组织8位中医、药技人员对23个中成药品种的处方、疗效、工艺、质量等方面进行审评。</p>
<p>1988年5月，开始贯彻国家卫生部颁发的《药品生产质量管理规范》。9月，市卫生局组织执法检查组，对10家药品生产企业的27个品种54个批次中西药品从原料投入到产品出厂全过程和生产记录进行检查。1989年10月，对10家药品生产企业进行整顿回访，根据《药品生产质量管理规范》提出改进意见，此后举办两期药品生产质量管理学习班；对12个药品生产企业的厂长、质检科长、生产科长、车间主任、仓库主任及药品质量监督员共60人进行培训。1990年，市内12家药品生产企业领取《药品生产许可证》。</p>"""

EXPECTED_TEXT = [
    "<p><strong>一、药政管理机构</strong></p>",
    "<p><strong>二、药品生产质量管理</strong></p>",
    "设两名药政管理专职干部",
    "生物化学制药厂及东方红化工厂",
    "各药厂皆设质量检验科（股）",
    "《关于对药品生产企业监督检查的通知》",
    "从原料投入到产品出厂全过程",
]
RESIDUALS = [
    "一、药政管理机构1951年1月",
    "二、药品生产质量管理1959年8月",
    "专职于部",
    "生物化制药厂进行生产性整顿",
    "各药厂皆设质留样观察制度",
    "根据省卫生厅《关于对检查",
    "原料投人到产品出厂全过程",
]


def find_scope(text: str) -> tuple[int, int]:
    start = text.index(SCOPE_START) + len(SCOPE_START)
    ends = [text.find(marker, start) for marker in SCOPE_END_OPTIONS]
    valid_ends = [end for end in ends if end != -1]
    if not valid_ends:
        raise RuntimeError("pharmacy management front scope end not found")
    return start, min(valid_ends)


def patch_reader() -> tuple[int, dict[str, int]]:
    text = HTML.read_text(encoding="utf-8")
    start, end = find_scope(text)
    new_segment = "\n" + NEW_HTML + "\n"
    changed = int(text[start:end] != new_segment)
    if changed:
        text = text[:start] + new_segment + text[end:]
        HTML.write_text(text, encoding="utf-8")

    start, end = find_scope(HTML.read_text(encoding="utf-8"))
    segment = HTML.read_text(encoding="utf-8")[start:end]
    missing = [item for item in EXPECTED_TEXT if item not in segment]
    if missing:
        raise RuntimeError(f"pharmacy management front expected text missing: {missing}")
    remaining = [item for item in RESIDUALS if item in segment]
    if remaining:
        raise RuntimeError(f"pharmacy management front residue remains: {remaining}")
    return changed, {"rewrote_scope": changed}


def write_reports(changed: int, counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五十五卷卫生 / 第四章医政 药政 / 第四节药政管理 / 一、药政管理机构；二、药品生产质量管理",
        "source": SOURCE_NOTE,
        "reader_path": str(HTML),
        "changes_this_run": changed,
        "counts": counts,
        "principle": "依据 PaddleOCR 页级文本整体复原药政管理前两小节；未处理三、药品经营质量管理。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十五卷药政管理前两小节回源修复

- 时间：{now}
- 范围：`第五十五卷卫生 / 第四章医政 药政 / 第四节药政管理 / 一、药政管理机构；二、药品生产质量管理`
- 源文依据：`{SOURCE_NOTE}`

## 修复动作

- 拆分 `一、药政管理机构`、`二、药品生产质量管理` 两个小节标题。
- 复原 `药政管理专职干部`、`生物化学制药厂及东方红化工厂...海光化工厂`、`质量检验科（股）` 等漏损文本。
- 复原 `《关于对药品生产企业监督检查的通知》` 后续检查组语句。
- 修正 `原料投人` 为 `原料投入`。
- 本次复跑新增整段替换：{changed} 处。
- 本轮未处理 `三、药品经营质量管理`。

## 核对说明

- PaddleOCR `page_0197.txt` 确认前两小节标题与主体文字。
- PaddleOCR `page_0198.txt` 确认 `药品生产质量管理` 跨页尾段及 `三、药品经营质量管理` 边界。
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")


def update_memory(changed: int) -> None:
    marker = "## 2026-07-02 第五十五卷药政管理前两小节回源修复"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker in memory:
        return
    entry = f"""
{marker}

- 对第五十五卷卫生第四章第四节 `药政管理` 的 `一、药政管理机构`、`二、药品生产质量管理` 进行回源修复。
- 源文依据：`{SOURCE_NOTE}`；拆分两个小节标题，并按 OCR 复原跨页漏损文字。
- 本轮新增整段替换 {changed} 处；`三、药品经营质量管理` 未在本脚本中处理。
- 报告：`output/reports/reader_readability_health_pharmacy_management_front_20260702.md`。
"""
    MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")


def main() -> None:
    changed, counts = patch_reader()
    write_reports(changed, counts)
    update_memory(changed)
    print("pharmacy management front repaired")
    print(f"changes={changed}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

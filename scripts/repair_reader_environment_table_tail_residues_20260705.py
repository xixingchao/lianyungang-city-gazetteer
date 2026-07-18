# -*- coding: utf-8 -*-
"""Remove source-backed environment chapter table-tail residues from the full reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_environment_table_tail_residues_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_environment_table_tail_residues_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_环保章表尾残片清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "环保水污染海水污染小节前废水污染物表尾残片",
        "old": (
            "<p>生活污水排放量（万吨）</p>\n"
            "<p>化学耗氧量（吨）</p>\n\n"
            "<p>0.2780.1360.1360.0240.024总镉（吨）</p>\n"
            "<p>0.0050.3650.2520.3850.212六价铬（吨）</p>\n\n\n\n\n\n\n"
            "<p>23737五日生化需氧量（吨）</p>\n\n\n\n\n"
            "<p>海水污染1978～1980年，连云港市有关部门组织编写了《江苏省沿海水域污染对人体健康影响科研调查总结报告》，"
            "从中可以看出，由于海水污染，使连云港海区海生物也受到严重污染。</p>"
        ),
        "new": (
            "<h5>海水污染</h5>\n"
            "<p>1978～1980年，连云港市有关部门组织编写了《江苏省沿海水域污染对人体健康影响科研调查总结报告》，"
            "从中可以看出，由于海水污染，使连云港海区海生物也受到严重污染。</p>"
        ),
        "sources": [
            "workbench/ocr/merged/连云港市志_上册_OCR汇总.md:25819",
            "workbench/ocr/merged/连云港市志_上册_OCR汇总.md:25843",
            "workbench/ocr/merged/连云港市志_上册_OCR汇总.md:25914",
            "workbench/ocr/merged/连云港市志_上册_OCR汇总.md:26309",
        ],
    },
    {
        "label": "环保治理章前酸雨监测表尾残片",
        "old": (
            "<p>4.46～5.5515.154.27～5.5911.764.85～5.5915.094.76～5.524.834.75～5.5922.354.27～5.5835.593.95～5.5936.614.72～5.5414.42"
            "二、治理工艺废气治理1979年，市锦屏化工厂利用黄磷尾气生产草酸、甲酸，获得国家科技奖。平均年产草酸1200吨、甲酸2400吨，"
            "废气去除率达60%，每年盈利40多万元。同年，曙光化工厂采用制冷设备，回收甲醇等低沸点废气，把废气消灭在生产过程中，"
            "每吨产品原料消耗从3.06吨下降到2.77吨，既降低原料消耗，又防止环境污染，每年仅节约原料即获益16.6万元。</p>"
        ),
        "new": (
            "<h5>二、治理</h5>\n"
            "<h5>工艺废气治理</h5>\n"
            "<p>1979年，市锦屏化工厂利用黄磷尾气生产草酸、甲酸，获得国家科技奖。平均年产草酸1200吨、甲酸2400吨，"
            "废气去除率达60%，每年盈利40多万元。同年，曙光化工厂采用制冷设备，回收甲醇等低沸点废气，把废气消灭在生产过程中，"
            "每吨产品原料消耗从3.06吨下降到2.77吨，既降低原料消耗，又防止环境污染，每年仅节约原料即获益16.6万元。</p>"
        ),
        "sources": [
            "workbench/ocr/raw/上/part02/page_0110.txt:17-60",
            "workbench/ocr/raw/上/part02/page_0110.txt:61-66",
        ],
    },
    {
        "label": "环保建设烟尘控制区前工艺废气治理表尾残片",
        "old": (
            "<p>（万元）</p>\n"
            "<p>（万标立方米/时）</p>\n"
            "<p>建设烟尘控制区连云港市从1974年开始抓消烟除尘工作。1980年，市环保局在市劳动局、市能源办公室等单位配合下，"
            "对全市有污染的锅炉进行更新改造和除尘器配套工作，同时，对新装锅炉加强“三同时”管理。1986年，市政府颁发《连云港市消烟除尘管理暂行规定》，"
            "市计划经济委员会、市劳动局、市环保局联合发出《关于加强锅炉管理的通知》等文件，以促进对烟尘污染的管理和治理。"
            "至1990年，市区642台锅炉的烟尘排放达标率为90%，128座工业窑炉的改造率在26%以上。赣榆、东海、灌云三县对锅炉的消烟除尘、更新改造率达75%～85%。"
            "锅炉烟尘治理的任务基本完成后，及时进行茶水炉的更新改造。采用双层炉排反烧式茶水炉，取代了煤耗高、冒黑烟的火烧蕊式茶水炉。"
            "至1990年，共更新茶水炉269台，占应更新炉的92.1%，基本上解决了低矮小烟筒的黑烟污染问题。同时选择并引进了北京和天津使用的二次风消烟节能灶，"
            "对生活、营业大灶进行改造。市环保局还下发了《关于在市区进行生活大灶改造的通知》，共投入环保补助资金40万元，至1990年，已改造大灶376眼，"
            "占应改造的52%。为了加快烟尘控制区的建设，还加强了对型煤推广，市物资局和市燃料公司狠抓型煤质量，增加型煤品种，并帮助用户改造型煤炉具，"
            "1990年，市区型煤普及率达81%。为了减少烟尘污染，市区采用集中联电供热方法。至1990年底，市区已建成5个集中供热区，少建56台小锅炉，"
            "每年减少5000馀吨的烟尘污染。“七五”计划期间，投资1340万元，建成煤气工程，改变燃料结构，使市区气化率由1985年的5%上升到1990年的25%，"
            "从而减轻大气污染。</p>"
        ),
        "new": (
            "<h5>建设烟尘控制区</h5>\n"
            "<p>连云港市从1974年开始抓消烟除尘工作。1980年，市环保局在市劳动局、市能源办公室等单位配合下，"
            "对全市有污染的锅炉进行更新改造和除尘器配套工作，同时，对新装锅炉加强“三同时”管理。1986年，市政府颁发《连云港市消烟除尘管理暂行规定》，"
            "市计划经济委员会、市劳动局、市环保局联合发出《关于加强锅炉管理的通知》等文件，以促进对烟尘污染的管理和治理。"
            "至1990年，市区642台锅炉的烟尘排放达标率为90%，128座工业窑炉的改造率在26%以上。赣榆、东海、灌云三县对锅炉的消烟除尘、更新改造率达75%～85%。"
            "锅炉烟尘治理的任务基本完成后，及时进行茶水炉的更新改造。采用双层炉排反烧式茶水炉，取代了煤耗高、冒黑烟的火烧蕊式茶水炉。"
            "至1990年，共更新茶水炉269台，占应更新炉的92.1%，基本上解决了低矮小烟筒的黑烟污染问题。同时选择并引进了北京和天津使用的二次风消烟节能灶，"
            "对生活、营业大灶进行改造。市环保局还下发了《关于在市区进行生活大灶改造的通知》，共投入环保补助资金40万元，至1990年，已改造大灶376眼，"
            "占应改造的52%。为了加快烟尘控制区的建设，还加强了对型煤推广，市物资局和市燃料公司狠抓型煤质量，增加型煤品种，并帮助用户改造型煤炉具，"
            "1990年，市区型煤普及率达81%。为了减少烟尘污染，市区采用集中联电供热方法。至1990年底，市区已建成5个集中供热区，少建56台小锅炉，"
            "每年减少5000馀吨的烟尘污染。“七五”计划期间，投资1340万元，建成煤气工程，改变燃料结构，使市区气化率由1985年的5%上升到1990年的25%，"
            "从而减轻大气污染。</p>"
        ),
        "sources": [
            "workbench/ocr/raw/上/part02/page_0111.txt:5-37",
            "workbench/ocr/raw/上/part02/page_0111.txt:38-54",
        ],
    },
    {
        "label": "环保宣传教育节前城市环境综合整治考核表尾残片",
        "old": (
            "<p>0.480.354.505.00环境二氧化硫年日均值（毫克/立方米）</p>\n"
            "<p>0.060.0581.001.00质量饮用水源水质达标率（%）</p>\n"
            "<p>100.0099.007.006.00指标城市地面水化学耗氧量平均值（毫克/升）</p>\n"
            "<p>0.0111.400.000.00（37 分）</p>\n"
            "<p>区域环境噪声平均值（分贝A）</p>\n"
            "<p>57.6055.907.409.00城市交通干线噪声平均值（分贝A）</p>\n"
            "<p>76.2072.201.903.50烟尘控制区覆盖率（分贝A）</p>\n"
            "<p>8.4024.900.200.30污染民用型煤普及率（%）</p>\n"
            "<p>79.0080.503.504.00控制万元产值工业废水排放量（吨/万元）</p>\n"
            "<p>293.00231.004.004.50指标工业废水处理率（%）</p>\n"
            "<p>22.3040.800.501.50（28 分）</p>\n"
            "<p>工业废水处理达标率（%）</p>\n"
            "<p>28.9029.100.500.50工业固体废弃物综合利用率（%）</p>\n"
            "<p>41.6042.903.503.50城市环城市气化率（%）</p>\n"
            "<p>14.008.500.200.10境建设城市污水处理率（%）</p>\n"
            "<p>0.000.000.000.00指标（13分）</p>\n"
            "<p>城市人均绿地面积（平方米/人）</p>\n"
            "<p>2.002.260.501.00满分合计34.7039.90（78 分）</p>"
        ),
        "new": "",
        "sources": [
            "workbench/ocr/raw/上/part02/page_0128.txt:4-104",
            "workbench/ocr/raw/上/part02/page_0128.txt:105-109",
        ],
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for item in REPLACEMENTS:
        old_count = html.count(item["old"])
        new_count = html.count(item["new"]) if item["new"] else 0
        if old_count == 1:
            html = html.replace(item["old"], item["new"], 1)
            status = "changed"
            changed = 1
        elif old_count == 0 and (new_count >= 1 or item["label"].endswith("考核表尾残片")):
            status = "already_applied"
            changed = 0
        else:
            raise RuntimeError(f"expected {item['label']} once, got {old_count}")
        changes.append({
            "label": item["label"],
            "status": status,
            "changed": changed,
            "sources": item["sources"],
        })

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": changes,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 环保章表尾残片清理",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：删除已回源确认的环保章表尾数字串，恢复正文小节标题和段落边界。",
        "- 说明：已结构化表格保留在文末 verified table block，本批只清理正文流残片。",
        "",
        "## 结果",
        "",
    ]
    for change in changes:
        lines.append(f"- {change['label']}：{change['status']}，本次变更 {change['changed']}")
        for source in change["sources"]:
            lines.append(f"  - `{source}`")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 环保章表尾残片清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_environment_table_tail_residues_20260705.py`，清理主阅读版环保章 4 处已回源确认的表尾残片：废水污染物表尾粘 `海水污染`、酸雨监测表尾粘 `二、治理/工艺废气治理`、工艺废气治理表尾粘 `建设烟尘控制区`、城市环境综合整治考核表尾粘 `第四节宣传教育`。
- 本批只处理文字源页可闭合的残片；结构化表格仍保留在 `已核结构化表格` 区块。
- 报告：`output/reports/reader_environment_table_tail_residues_20260705.md`。
""",
    )

    print("reader_environment_table_tail_residues_repaired")
    print(f"changed={sum(item['changed'] for item in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Remove source-backed table-tail residues from the full reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_table_tail_residues_batch2_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_table_tail_residues_batch2_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_正文表尾残片第二批清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "城乡建设土地交易小节前房地产交易表尾残片",
        "old": (
            "<p>买卖4.101100.00继承0.2011.50分析0.606.00赠与0.108.00交换0.066.90抵押9.912.50换契0.30"
            "土地交易 土地交易在建国前普遍存在。民国5年（1916年），农村地价每亩100元（银元），街市地价每亩300元。"
            "之后，地价逐步升高，至民国14年，农村地价每亩600元，墟沟的街市地价每亩1400元，"
            "民国23年港口所在的连云、墟沟，每亩土地交易价达1800元。</p>"
        ),
        "new": (
            "<h5>土地交易</h5>\n"
            "<p>土地交易在建国前普遍存在。民国5年（1916年），农村地价每亩100元（银元），街市地价每亩300元。"
            "之后，地价逐步升高，至民国14年，农村地价每亩600元，墟沟的街市地价每亩1400元，"
            "民国23年港口所在的连云、墟沟，每亩土地交易价达1800元。</p>"
        ),
        "sources": [
            "workbench/ocr/merged/连云港市志_上册_OCR汇总.md:25672",
            "workbench/ocr/merged/连云港市志_上册_OCR汇总.md:25700",
        ],
    },
    {
        "label": "民政优抚安置章前基层组织表尾残片",
        "old": (
            "<p>6511483新浦区194海州区4322414450云台区171603722424连云区760490640赣榆县1910479362460"
            "东海县18427253082灌云县182010305合计192114317856630优抚安置连云港市人民具有褒扬革命先烈，"
            "抚恤优待烈士、伤残军人和军人家属的优良传统。</p>\n"
            "<p>建国前，在长期艰苦卓绝的革命斗争中，人民群众冒着生命危险，拥军支前，优待烈军属和伤残军人。"
            "建国后，拥军优属工作列入各级政府的重要工作。1950～1953年，以抗美援朝保家卫国为主要内容，"
            "开展轰轰烈烈的拥优活动，一人参军全家光荣成为时尚。社会主义建设时期，随着经济和社会发展，"
            "拥优活动不断赋予新的内容。妥善安置军队复员转业军</p>\n\n"
            "<h3 id=\"第四十三卷-第二章优抚安置\">第二章优抚安置</h3>\n"
            "<p>人，优待军人家属形成良好的社会风尚。1980年开始，将拥军优属和拥政爱民（简称“双拥”)结合起来，"
            "普遍开展军民共建活动，市、县（区）、乡都建立双拥工作领导小组，共建活动列为精神文明建设主要内容之一。</p>"
        ),
        "new": (
            "<h3 id=\"第四十三卷-第二章优抚安置\">第二章优抚安置</h3>\n"
            "<p>连云港市人民具有褒扬革命先烈，抚恤优待烈士、伤残军人和军人家属的优良传统。</p>\n"
            "<p>建国前，在长期艰苦卓绝的革命斗争中，人民群众冒着生命危险，拥军支前，优待烈军属和伤残军人。"
            "建国后，拥军优属工作列入各级政府的重要工作。1950～1953年，以抗美援朝保家卫国为主要内容，"
            "开展轰轰烈烈的拥优活动，一人参军全家光荣成为时尚。社会主义建设时期，随着经济和社会发展，"
            "拥优活动不断赋予新的内容。妥善安置军队复员转业军人，优待军人家属形成良好的社会风尚。"
            "1980年开始，将拥军优属和拥政爱民（简称“双拥”)结合起来，普遍开展军民共建活动，市、县（区）、乡都建立双拥工作领导小组，"
            "共建活动列为精神文明建设主要内容之一。</p>"
        ),
        "sources": [
            "workbench/ocr/raw/下/part01/page_0020.txt:17",
            "output/final_reader/连云港市志_全书.html:18418",
        ],
    },
    {
        "label": "教育教学方法小节前教学计划表尾残片",
        "old": (
            "<p>眼保健操1.51.51.51.51.51.5每天两次共10分钟1.51.51.51.51.51.5每天10分钟晨会或夕会3535394040"
            "每周在校活动总量三、教学方法民国元年（1912年），小学采用班级授课制。20世纪20年代，美国教育家杜威的实用主义教育思想与教学方法流入境内。"
            "民国19年，东海中学实验小学在低年级采用大单元混合设计教学法，中年级试行分科设计法，高年级采用自学辅导法。"
            "但大多数小学仍采用注入式教学方法。</p>"
        ),
        "new": (
            "<h5>三、教学方法</h5>\n"
            "<p>民国元年（1912年），小学采用班级授课制。20世纪20年代，美国教育家杜威的实用主义教育思想与教学方法流入境内。"
            "民国19年，东海中学实验小学在低年级采用大单元混合设计教学法，中年级试行分科设计法，高年级采用自学辅导法。"
            "但大多数小学仍采用注入式教学方法。</p>"
        ),
        "sources": [
            "workbench/ocr/raw/下/part01/page_0368.txt:22",
            "workbench/ocr/raw/下/part01/page_0368.txt:44",
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
        count = html.count(item["old"])
        if count == 1:
            html = html.replace(item["old"], item["new"], 1)
            status = "changed"
            changed = 1
        elif count == 0 and html.count(item["new"]) >= 1:
            status = "already_applied"
            changed = 0
        else:
            raise RuntimeError(f"expected {item['label']} once, got {count}")
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
        "# 正文表尾残片第二批清理",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：删除已回源确认的表尾数字串，恢复正文小节标题和段落边界。",
        "",
        "## 结果",
        "",
    ]
    for change in changes:
        lines.append(f"- {change['label']}：{change['status']}，本次变更 {change['changed']}")
        for source in change["sources"]:
            lines.append(f"  - `{source}`")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text("\n".join(lines) + "\n", encoding="utf-8")

    marker = "## 2026-07-05 正文表尾残片第二批清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_table_tail_residues_batch2_20260705.py`，清理主阅读版中 3 处已回源确认的表尾残片：城乡建设 `土地交易`、民政 `优抚安置`、教育 `三、教学方法`。
- 本批只处理证据闭合项；环保污染物表残片仍需进一步收束源页边界后再处理。
- 报告：`output/reports/reader_table_tail_residues_batch2_20260705.md`。
""",
    )

    print("reader_table_tail_residues_batch2_repaired")
    print(f"changed={sum(item['changed'] for item in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

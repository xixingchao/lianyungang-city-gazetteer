# -*- coding: utf-8 -*-
"""Restore source-backed section boundaries in the full reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_section_boundaries_batch2_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_section_boundaries_batch2_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_小节边界第二批修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "大气监测小节边界",
        "old": "<p>三、大气监测市区从1975年由市卫生防疫部门开始大气监测工作。1981年开始，由市环境监测站进行例行监测。监测方法采用人工间断性监测。每年监测4次，各代表冬、春、夏、秋4个季节。在每季的第1个月中旬监测，连续5天，每天4次，分别为7：30～8：30、10：30～11：</p>",
        "new": "<h5>三、大气监测</h5>\n<p>市区从1975年由市卫生防疫部门开始大气监测工作。1981年开始，由市环境监测站进行例行监测。监测方法采用人工间断性监测。每年监测4次，各代表冬、春、夏、秋4个季节。在每季的第1个月中旬监测，连续5天，每天4次，分别为7：30～8：30、10：30～11：</p>",
        "source": "workbench/ocr/raw/上/part02/page_0116.txt:24",
    },
    {
        "label": "残疾人抽样调查小节边界",
        "old": "<p>八、残疾人抽样调查国务院决定1987年进行残疾人抽样调查，连云港市东海县9个村被抽中。调查内容：各类残疾人的人数、致残原因及其治疗、康复、教育、就业、婚姻、家庭和参加社会活动等情况。调查时点：1987年4月1日零时。调查采用分层、等概率、整群抽样方法，共调查4479人。4月1～27日完成调查登记和复查工作。调查结果：残疾人总数246人，占调查总人数的5.49%。</p>",
        "new": "<h5>八、残疾人抽样调查</h5>\n<p>国务院决定1987年进行残疾人抽样调查，连云港市东海县9个村被抽中。调查内容：各类残疾人的人数、致残原因及其治疗、康复、教育、就业、婚姻、家庭和参加社会活动等情况。调查时点：1987年4月1日零时。调查采用分层、等概率、整群抽样方法，共调查4479人。4月1～27日完成调查登记和复查工作。调查结果：残疾人总数246人，占调查总人数的5.49%。</p>",
        "source": "workbench/ocr/raw/上/part02/page_0166.txt:41",
    },
    {
        "label": "小型灌区小节边界",
        "old": "<p>三、小型灌区境内小型自流灌区始建于1956年。至1990年，共建成小型水库自流灌区128个，设计灌溉总面积25.77万亩，实际灌溉总面积19.65万亩。</p>",
        "new": "<h5>三、小型灌区</h5>\n<p>境内小型自流灌区始建于1956年。至1990年，共建成小型水库自流灌区128个，设计灌溉总面积25.77万亩，实际灌溉总面积19.65万亩。</p>",
        "source": "workbench/ocr/raw/上/part03/page_0033.txt:28",
    },
    {
        "label": "连云港海洋渔业公司冷冻厂条目边界",
        "old": "<p>一、连云港海洋渔业公司冷冻厂始建于1958年。1960年开始冷冻加工，1963年开始加工外销出口产品。主要有各种规格的马鲛鱼、银鲳鱼、东方豚、大小黄鱼、黄姑鱼、带鱼、带鱼段、海鳗、章鱼、墨鱼、墨鱼卷、赤贝肉、青鱼籽、海蟹等。1980年以后又增添了有头对虾、无头对虾、凤尾虾仁等。产品主要出口到美国、日本、法国、韩国等国家及香港地区，国内市场覆盖16个省区。1990年，库容量为6000吨，速冻能力为100吨/日。当年出口条冻马鲛鱼400多吨。</p>",
        "new": "<h5>一、连云港海洋渔业公司冷冻厂</h5>\n<p>始建于1958年。1960年开始冷冻加工，1963年开始加工外销出口产品。主要有各种规格的马鲛鱼、银鲳鱼、东方豚、大小黄鱼、黄姑鱼、带鱼、带鱼段、海鳗、章鱼、墨鱼、墨鱼卷、赤贝肉、青鱼籽、海蟹等。1980年以后又增添了有头对虾、无头对虾、凤尾虾仁等。产品主要出口到美国、日本、法国、韩国等国家及香港地区，国内市场覆盖16个省区。1990年，库容量为6000吨，速冻能力为100吨/日。当年出口条冻马鲛鱼400多吨。</p>",
        "source": "workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:7288",
    },
    {
        "label": "东海县太平渔业公司冷冻厂条目边界",
        "old": "<p>三、东海县太平渔业公司冷冻厂1982年建厂。该厂拥有600吨冷库，速冻能力25吨/日，主要产品为海洋鱼、虾、贝的加工制品，1990年产量580吨，产值480万元，利润30万元。</p>",
        "new": "<h5>三、东海县太平渔业公司冷冻厂</h5>\n<p>1982年建厂。该厂拥有600吨冷库，速冻能力25吨/日，主要产品为海洋鱼、虾、贝的加工制品，1990年产量580吨，产值480万元，利润30万元。</p>",
        "source": "workbench/ocr/raw/上/part03/page_0120.txt:23",
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
        if old_count == 1:
            html = html.replace(item["old"], item["new"], 1)
            status = "changed"
            changed = 1
        elif old_count == 0 and html.count(item["new"]) >= 1:
            status = "already_applied"
            changed = 0
        else:
            raise RuntimeError(f"expected {item['label']} once, got {old_count}")
        changes.append({"label": item["label"], "status": status, "changed": changed, "source": item["source"]})

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "target": str(HTML.relative_to(ROOT)).replace("\\", "/"), "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 小节边界第二批修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：按源 OCR/正文分行恢复环保、统计、水利、水产 5 处小节或条目标题边界。",
        "",
        "## 结果",
        "",
    ]
    for change in changes:
        lines.append(f"- {change['label']}：{change['status']}，本次变更 {change['changed']}")
        lines.append(f"  - `{change['source']}`")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 小节边界第二批修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_section_boundaries_batch2_20260705.py`，按源 OCR/正文分行恢复 5 处标题边界：`三、大气监测`、`八、残疾人抽样调查`、`三、小型灌区`、`一、连云港海洋渔业公司冷冻厂`、`三、东海县太平渔业公司冷冻厂`。
- 源页证据：`workbench/ocr/raw/上/part02/page_0116.txt:24`、`workbench/ocr/raw/上/part02/page_0166.txt:41`、`workbench/ocr/raw/上/part03/page_0033.txt:28`、`workbench/ocr/raw/上/part03/page_0120.txt:23`，以及 `workbench/body_chapters/paddle_上/第十卷至第十六卷（part03）.md:7288`。
- 报告：`output/reports/reader_section_boundaries_batch2_20260705.md`。
""",
    )

    print("reader_section_boundaries_batch2_repaired")
    print(f"changed={sum(change['changed'] for change in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

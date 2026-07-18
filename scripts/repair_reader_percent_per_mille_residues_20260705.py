# -*- coding: utf-8 -*-
"""Repair reader-facing %o/%0/%c OCR residues that denote per mille."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_percent_per_mille_residues_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_percent_per_mille_residues_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_正文千分号残留批量修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCES = [
    "workbench/ocr/paddle_ocr/上/part01/page_0038.txt",
    "workbench/ocr/paddle_ocr/上/part01/page_0122.txt",
    "workbench/ocr/paddle_ocr/上/part01/page_0134.txt",
    "workbench/ocr/paddle_ocr/上/part01/page_0145.txt",
    "workbench/ocr/paddle_ocr/上/part01/page_0249.txt",
    "workbench/ocr/paddle_ocr/上/part02/page_0277.txt",
    "workbench/ocr/paddle_ocr/上/part03/page_0113.txt",
    "workbench/ocr/paddle_ocr/中/part01/page_0326.txt",
    "workbench/ocr/paddle_ocr/中/part01/page_0500.txt",
    "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md",
    "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
]

REPLACEMENTS = [
    ("总述人口自然增长", "24.81%o下降至80年代的12.63%", "24.81‰下降至80年代的12.63‰"),
    ("三区概况人口率", "20.67%o和6.04%o", "20.67‰和6.04‰"),
    ("自然环境平均比降", "平均比降1%o～9%o", "平均比降1‰～9‰"),
    ("海州湾盐度", "介于30%o～32%o之间，最高值小于33%o，最低值大于26%o", "介于30‰～32‰之间，最高值小于33‰，最低值大于26‰"),
    ("云台区人口率", "人口出生率为18.45%o，死亡率5.14%o", "人口出生率为18.45‰，死亡率5.14‰"),
    ("房山水库坡度", "流域坡度一般在1%o以上", "流域坡度一般在1‰以上"),
    ("对虾低盐度上册", "低盐度（2%o～5%o）驯化养殖", "低盐度（2‰～5‰）驯化养殖"),
    ("建筑事故率", "事故率全市平均在3%c以下", "事故率全市平均在3‰以下"),
    ("开发区自然增长率", "自然增长率控制在8%o以内", "自然增长率控制在8‰以内"),
    ("海关港务费率", "税率为货物从价的5%o，该项收入民国38年310月", "税率为货物从价的5‰，该项收入民国38年3～10月"),
    ("陇海铁路坡度", "最大坡度9%o", "最大坡度9‰"),
    ("储备粮损耗", "一年以内的收1.5%o", "一年以内的收1.5‰"),
    ("小贷月息3", "贷款按月息3%o计息", "贷款按月息3‰计息"),
    ("小贷月息2.1首段", "贷款利率月息调减为2.1%o", "贷款利率月息调减为2.1‰"),
    ("小贷月息2.1续段", "小贷仍为月息2.1%o，其他的小贷一律恢复月息4.2%o", "小贷仍为月息2.1‰，其他的小贷一律恢复月息4.2‰"),
    ("小贷月息6断句", "提高小贷利息至月息6%001965~1990年", "提高小贷利息至月息6‰。1965～1990年"),
    ("资金占用费", "按月利率2.1%o计征流动资金占用费", "按月利率2.1‰计征流动资金占用费"),
    ("营业税税率", "税率为1%o~10%，以资本额为课征标准的税率为2%o~20%0", "税率为1‰～10‰，以资本额为课征标准的税率为2‰～20‰"),
    ("营业税三档", "税率改为5%o、8%o、10%o三档", "税率改为5‰、8‰、10‰三档"),
    ("房捐产价", "住房按产价分别征收1.5%和0.8%o", "住房按产价分别征收1.5%和0.8‰"),
    ("房捐现值", "住房按房屋现值的5%和2.5%o分季", "住房按房屋现值的5%和2.5‰分季"),
    ("牌照税", "为5%o，50万元以上的为4%o，10万元以上的为3%o，不满10万元的为2%o", "为5‰，50万元以上的为4‰，10万元以上的为3‰，不满10万元的为2‰"),
    ("印花税首段", "税率为1%、3%o和3%o三种", "税率为1‰、3‰和3‰三种"),
    ("印花税修订", "税率分为3%o、1%o、及3%o三种", "税率分为3‰、1‰、及3‰三种"),
    ("印花税恢复", "税率分为1%o、5%o、3%oo、0.5%和0.3%o五种", "税率分为1‰、5‰、3‰、0.5‰和0.3‰五种"),
    ("运输险费率", "运输险费率由9%o降至2.5%o", "运输险费率由9‰降至2.5‰"),
    ("金融利率首段", "民营工业放款利率272%o，民营商业放款利率290%o，民营甲种存款利率120%o，民营乙种存款利率150%o，公营放款利率136%~140%o1950年", "民营工业放款利率272‰，民营商业放款利率290‰，民营甲种存款利率120‰，民营乙种存款利率150‰，公营放款利率136‰～140‰。1950年"),
    ("市级编制", "城市人口13万的0.95%o", "城市人口13万的0.95‰"),
    ("行政编制", "人口的3.5%o的比例核算", "人口的3.5‰的比例核算"),
    ("对虾低盐度下册", "低盐度（2%o~5%o）驯化养殖", "低盐度（2‰～5‰）驯化养殖"),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for label, old, new in REPLACEMENTS:
        count = html.count(old)
        if count != 1:
            raise RuntimeError(f"expected one occurrence for {label}, got {count}: {old}")
        html = html.replace(old, new, 1)
        changes.append({"label": label, "old": old, "new": new})
    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "sources": SOURCES,
        "changes": changes,
        "principle": "仅修复上下文明确为千分号的 %o/%0/%c/%00/%oo 残留及同句漏断；保留普通百分号和证据不足项。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 正文千分号残留批量修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 原则：仅修复上下文明确为千分号的 `%o/%0/%c/%00/%oo` 残留及同句漏断；保留普通百分号和证据不足项。",
        "- 源文参考：`" + "`、`".join(SOURCES) + "`。",
        "",
        "## 修复清单",
        "",
        "| 项 | 原文 | 修复后 |",
        "|---|---|---|",
    ]
    for item in changes:
        lines.append(f"| {item['label']} | `{item['old']}` | `{item['new']}` |")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS.write_text("\n".join(lines) + "\n", encoding="utf-8")

    marker = "## 2026-07-05 正文千分号残留批量修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_percent_per_mille_residues_20260705.py`，限定主阅读版修复上下文明确为千分号的 `%o/%0/%c/%00/%oo` 残留及同句漏断。
- 覆盖人口自然增长率、海水盐度、地貌坡度、港务费率、税率、月息/费率、编制比例等 {len(changes)} 项；保留普通百分号和证据不足项。
- 报告：`output/reports/reader_percent_per_mille_residues_20260705.md`。
""",
    )

    print("percent_per_mille_residues_repaired")
    print(f"changes={len(changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

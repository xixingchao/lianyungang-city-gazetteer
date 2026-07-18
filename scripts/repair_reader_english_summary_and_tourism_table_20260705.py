# -*- coding: utf-8 -*-
"""Repair two English line-break paragraphs and one flattened tourism table."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_english_summary_and_tourism_table_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_english_summary_and_tourism_table_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_英文摘要断段和旅游统计表线性残留修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

ENGLISH_JOINS = [
    (
        "<p>The local authorities also made great effort in initiating individual and private businesses, speeded up the construction of business basic installations and markets, and took good care of the construction of resource markets, essential markets and those</p>\n"
        "<p>large and middle specialized and wholesale markets when strengthening the development of the free market of agriculture products and small commodity market, so the number and the scale of all markets grew unprecedented.</p>",
        "<p>The local authorities also made great effort in initiating individual and private businesses, speeded up the construction of business basic installations and markets, and took good care of the construction of resource markets, essential markets and those large and middle specialized and wholesale markets when strengthening the development of the free market of agriculture products and small commodity market, so the number and the scale of all markets grew unprecedented.</p>",
        "workbench/body_chapters/连云港市志_全书_正文汇总.md:119951-119957",
    ),
    (
        "<p>Foreign capital has been introduced as early as 1980, and to 1985 it had introduced 6 foreign investments accounting to 1.11 million Yuan in practical utilization. During</p>\n"
        "<p>the 7th Five Year Plan （ 1986--1990 ), it had introduced 66 foreign capitals, and 63.3 million Yuan in practical use, with an annual increasing rate of 16.7% .</p>",
        "<p>Foreign capital has been introduced as early as 1980, and to 1985 it had introduced 6 foreign investments accounting to 1.11 million Yuan in practical utilization. During the 7th Five Year Plan （ 1986--1990 ), it had introduced 66 foreign capitals, and 63.3 million Yuan in practical use, with an annual increasing rate of 16.7% .</p>",
        "workbench/body_chapters/连云港市志_全书_正文汇总.md:119988-119994",
    ),
]

OLD_TOURISM = "<p>1985年、1990年连云港市接待海外旅游者统计表平均停留天数旅游者旅游人数人次(人次)(天)(人次)国别1990年1985年1985年1990年1985年1990年日本321820菲律宾2125新加坡2263美国3780英国151130323.996.119178法国19德国4218意大利4631苏联23澳大利亚23562.55华，12223.752.878769032512241港澳台同胞</p>"

TOURISM_TABLE = """<table class="structured-table"><caption>1985年、1990年连云港市接待海外旅游者统计表</caption><thead><tr><th>类别/国别</th><th>旅游人数1985年(人次)</th><th>旅游人数1990年(人次)</th><th>旅游者人次1985年(人次)</th><th>旅游者人次1990年(人次)</th><th>平均停留天数1985年(天)</th><th>平均停留天数1990年(天)</th></tr></thead><tbody><tr><td>日本</td><td>321</td><td>820</td><td></td><td></td><td></td><td></td></tr><tr><td>菲律宾</td><td>21</td><td>25</td><td></td><td></td><td></td><td></td></tr><tr><td>新加坡</td><td>22</td><td>63</td><td></td><td></td><td></td><td></td></tr><tr><td>美国</td><td>37</td><td>80</td><td></td><td></td><td></td><td></td></tr><tr><td>英国</td><td>11</td><td>15</td><td></td><td></td><td></td><td></td></tr><tr><td>外国人</td><td></td><td></td><td>3032</td><td>9178</td><td>3.99</td><td>6.11</td></tr><tr><td>法国</td><td>9</td><td>19</td><td></td><td></td><td></td><td></td></tr><tr><td>德国</td><td>42</td><td>18</td><td></td><td></td><td></td><td></td></tr><tr><td>意大利</td><td>31</td><td>46</td><td></td><td></td><td></td><td></td></tr><tr><td>苏联</td><td>3</td><td>23</td><td></td><td></td><td></td><td></td></tr><tr><td>澳大利亚</td><td>2</td><td>23</td><td></td><td></td><td></td><td></td></tr><tr><td>华侨</td><td>4</td><td>22</td><td>12</td><td>56</td><td>3</td><td>2.55</td></tr><tr><td>港澳台同胞</td><td>241</td><td>876</td><td>903</td><td>2512</td><td>3.75</td><td>2.87</td></tr></tbody></table>"""


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def replace_once_or_applied(text: str, old: str, new: str, label: str) -> tuple[str, str, int]:
    count = text.count(old)
    if count == 1:
        return text.replace(old, new, 1), "changed", 1
    if count == 0 and text.count(new) >= 1:
        return text, "already_applied", 0
    raise RuntimeError(f"expected unique match for {label}, got {count}")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []

    for idx, (old, new, source) in enumerate(ENGLISH_JOINS, 1):
        html, status, changed = replace_once_or_applied(html, old, new, f"english_join_{idx}")
        changes.append({"target": f"english_join_{idx}", "status": status, "changed": changed, "source": source})

    html, status, changed = replace_once_or_applied(html, OLD_TOURISM, TOURISM_TABLE, "tourism_table")
    changes.append(
        {
            "target": "tourism_table",
            "status": status,
            "changed": changed,
            "source": "workbench/ocr/raw/中/part02/page_0119.json:262; workbench/ocr/raw/中/part02/page_0119.txt:14",
            "note": "按 raw OCR 坐标复原表头和可判列数据；国家行无可判人次/停留天数时留空。",
        }
    )

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "target": str(HTML.relative_to(ROOT)).replace("\\", "/"), "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    changed_total = sum(item["changed"] for item in changes)
    lines = [
        "# 英文摘要断段和旅游统计表线性残留修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：合并 2 处英文摘要跨页断段；将 1 处压扁成正文的旅游统计表恢复为 HTML 表格。",
        f"- 状态：本次变更 {changed_total} 处；脚本可重复运行。",
        "",
        "## 源证据",
        "",
        "- 英文摘要断段：`workbench/body_chapters/连云港市志_全书_正文汇总.md:119951-119957`、`:119988-119994`。",
        "- 旅游统计表：`workbench/ocr/raw/中/part02/page_0119.json` 与 `workbench/ocr/raw/中/part02/page_0119.txt:14`。",
        "- 表格修复说明：按 OCR 坐标复原表头和可判列数据；国家行无可判人次/停留天数时留空，不补猜。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    PROGRESS.write_text("\n".join(lines), encoding="utf-8")

    marker = "## 2026-07-05 英文摘要断段和旅游统计表线性残留修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_english_summary_and_tourism_table_20260705.py`，修复最终阅读版 2 处英文摘要跨页断段和 1 处旅游统计表线性残留。
- 英文摘要仅合并原本连续的跨页句，不改英文内容；旅游统计表按 `workbench/ocr/raw/中/part02/page_0119.json` 坐标复原，未能判列的国家行人次/停留天数留空。
- 报告：`output/reports/reader_english_summary_and_tourism_table_20260705.md`。
""",
    )

    print("english_summary_and_tourism_table_repaired")
    print(f"changed={changed_total}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Thirty-seventh batch: PaddleOCR-backed foreign-affairs short fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch37_foreign_affairs_short_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch37_foreign_affairs_short_20260706.json"

CHANGES = [
    {
        "old": "藤尾昭受日本日南市市长委托，菜莲云港市探讨结为友好城市问题",
        "new": "藤尾昭受日本日南市市长委托，来连云港市探讨结为友好城市问题",
        "section": "日本日南市友好城市探讨段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0287.txt:25 raw 作菜莲云港市",
            "workbench/ocr/paddle_ocr/下/part01/page_0287.txt:26 PaddleOCR 作来连云港市",
        ],
    },
    {
        "old": "美国基督教福音派领袖葛培理行20人，由北京取道连云港市去淮阴访问",
        "new": "美国基督教福音派领袖葛培理一行20人，由北京取道连云港市去淮阴访问",
        "section": "葛培理一行访问段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0288.txt:7 raw 漏一字",
            "workbench/ocr/paddle_ocr/下/part01/page_0288.txt:7 PaddleOCR 作葛培理一行20人",
        ],
    },
    {
        "old": "日本《读卖新闻》记者组一行9人来华，分路采访26个城市。记者组成员原义明、小泽明于8月1922日来连云港市参观采访",
        "new": "日本《读卖新闻》记者组一行9人来华，分路采访26个城市。记者组成员原义明、小泽明于8月19~22日来连云港市参观采访",
        "section": "读卖新闻记者组日期段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0288.txt:9 raw 作8月1922日",
            "workbench/ocr/paddle_ocr/下/part01/page_0288.txt:9-10 PaddleOCR 作8月19~22日",
        ],
    },
    {
        "old": "1987年12月15~25日，市长唐贯准一行5人赴香港参加振云有限公司贸易洽谈会和开业典礼",
        "new": "1987年12月15~25日，市长唐贯淮一行5人赴香港参加振云有限公司贸易洽谈会和开业典礼",
        "section": "唐贯淮赴香港段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0288.txt:29 raw 作唐贯准",
            "workbench/ocr/paddle_ocr/下/part01/page_0288.txt:29 PaddleOCR 作唐贯淮",
        ],
    },
    {
        "old": "乌迪内省商会和维那多工业企业协会先后签订了协议书，同一一些企业签订了合作意向书",
        "new": "乌迪内省商会和维那多工业企业协会先后签订了协议书，同一些企业签订了合作意向书",
        "section": "意大利经济综合考察合作意向书段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0288.txt:34 raw 作同一一些企业",
            "workbench/ocr/paddle_ocr/下/part01/page_0288.txt:35 PaddleOCR 作同一些企业",
        ],
    },
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for change in CHANGES:
        count = html.count(change["old"])
        if count != 1:
            raise RuntimeError(f"expected one hit for {change['section']}, found {count}: {change['old'][:80]}")
        html = html.replace(change["old"], change["new"])
        applied.append({**change, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "note": "只修下册外事侨务 page_0287/page_0288 raw/PaddleOCR 可闭合的短片段；未处理侨务术语和缺证总述句。未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第三十七批：外事短片段",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        old = item["old"] if len(item["old"]) <= 90 else item["old"][:90] + "..."
        new = item["new"] if len(item["new"]) <= 90 else item["new"][:90] + "..."
        lines.append(f"- {item['section']}：`{old}` -> `{new}`（命中 {item['count']} 处）")
        for evidence in item["evidence"]:
            lines.append(f"  - 证据：`{evidence}`")
    lines += [
        "",
        "## 边界",
        "",
        "- 只修主阅读版，不改 OCR 原文。",
        "- 未处理未定位到原文页的外事概述总述句。",
        "- 未处理侨务章 `侨着/侨券/侨卷` 等术语残留，后续需按侨务页单独核证。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

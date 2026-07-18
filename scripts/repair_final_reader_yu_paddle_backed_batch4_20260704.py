# -*- coding: utf-8 -*-
"""Repair a fourth source-backed 馀->余 batch in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "final_reader_yu_paddle_backed_batch4_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "final_reader_yu_paddle_backed_batch4_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_最终阅读版余字第四批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "渔政船员编制",
        "old": "渔政机构办公室4人，其馀为船员编制，渔业指导船兼作渔政船。",
        "new": "渔政机构办公室4人，其余为船员编制，渔业指导船兼作渔政船。",
        "source": "workbench/ocr/raw/上/part03/page_0127.txt:29; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:51094; workbench/body_chapters/连云港市志_全书_正文汇总.md:47964",
    },
    {
        "label": "盐场潮灾5000余吨",
        "old": "1949年一次潮灾，就损失盐斤5000馀吨。",
        "new": "1949年一次潮灾，就损失盐斤5000余吨。",
        "source": "workbench/ocr/raw/上/part03/page_0137.txt:31; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:51758; workbench/body_chapters/连云港市志_全书_正文汇总.md:48592",
    },
    {
        "label": "元代产盐320余万担",
        "old": "两淮盐区产盐达320馀万担（每担50公斤）。",
        "new": "两淮盐区产盐达320余万担（每担50公斤）。",
        "source": "workbench/ocr/raw/上/part03/page_0143.txt:20; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:52226; workbench/body_chapters/连云港市志_全书_正文汇总.md:48983",
    },
    {
        "label": "灶丁有余丁",
        "old": "如有馀丁，注册存查。",
        "new": "如有余丁，注册存查。",
        "source": "workbench/ocr/raw/上/part03/page_0149.txt:74; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:52879; workbench/body_chapters/连云港市志_全书_正文汇总.md:49631",
    },
    {
        "label": "出口盐114.6万余吨",
        "old": "114.6万馀吨，创外汇1187万美元。",
        "new": "114.6万余吨，创外汇1187万美元。",
        "source": "workbench/ocr/raw/上/part03/page_0151.txt:85; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:53012; workbench/body_chapters/连云港市志_全书_正文汇总.md:49760",
    },
    {
        "label": "印刷厂经营一年有余",
        "old": "该厂经营一年有馀，月月亏损。",
        "new": "该厂经营一年有余，月月亏损。",
        "source": "workbench/ocr/raw/上/part03/page_0182.txt:35; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:54853; workbench/body_chapters/连云港市志_全书_正文汇总.md:51513",
    },
    {
        "label": "大中报日印量2000余份",
        "old": "日印量2000馀份。随后开张的报纸印刷业有7家",
        "new": "日印量2000余份。随后开张的报纸印刷业有7家",
        "source": "workbench/ocr/raw/上/part03/page_0185.txt:27; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:55008; workbench/body_chapters/连云港市志_全书_正文汇总.md:51664",
    },
    {
        "label": "和平日报日印量2000余份",
        "old": "在新浦开印，日印量2000馀份。",
        "new": "在新浦开印，日印量2000余份。",
        "source": "workbench/ocr/raw/上/part03/page_0185.txt:32; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:55013; workbench/body_chapters/连云港市志_全书_正文汇总.md:51669",
    },
    {
        "label": "包装企业150余家",
        "old": "1990年，全市有150馀家企业，职工1.5万人",
        "new": "1990年，全市有150余家企业，职工1.5万人",
        "source": "workbench/ocr/raw/上/part03/page_0190.txt:23; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:55203; workbench/body_chapters/连云港市志_全书_正文汇总.md:51839",
    },
    {
        "label": "火柴亏损5万余元",
        "old": "企业亏损5万馀元。",
        "new": "企业亏损5万余元。",
        "source": "workbench/ocr/raw/上/part03/page_0199.txt:9; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:55537; workbench/body_chapters/连云港市志_全书_正文汇总.md:52154",
    },
    {
        "label": "家具企业与产量",
        "old": "全市木制家具生产企业40馀家，从业人员2000馀人，其中，个体人员300馀人，年产木制家具15万馀件。",
        "new": "全市木制家具生产企业40余家，从业人员2000余人，其中，个体人员300余人，年产木制家具15万余件。",
        "source": "workbench/ocr/raw/上/part03/page_0212.txt:39; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:56293; workbench/body_chapters/连云港市志_全书_正文汇总.md:52900",
    },
    {
        "label": "沙发1000余件",
        "old": "生产各类沙发1000馀件。",
        "new": "生产各类沙发1000余件。",
        "source": "workbench/ocr/raw/上/part03/page_0213.txt:28; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:56325; workbench/body_chapters/连云港市志_全书_正文汇总.md:52930",
    },
    {
        "label": "灯管内销20余个省市",
        "old": "内销省内及山东、广东等20馀个省、市。",
        "new": "内销省内及山东、广东等20余个省、市。",
        "source": "workbench/ocr/raw/上/part03/page_0220.txt:7; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:56755; workbench/body_chapters/连云港市志_全书_正文汇总.md:53347",
    },
    {
        "label": "服装鞋帽从业800余人",
        "old": "从业人员减少到800馀人。",
        "new": "从业人员减少到800余人。",
        "source": "workbench/ocr/raw/上/part03/page_0264.txt:6; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:59208; workbench/body_chapters/连云港市志_全书_正文汇总.md:55674",
    },
    {
        "label": "皮革制品厂万余张",
        "old": "职工500馀人，利用机电设备，年均制作皮革万馀张。",
        "new": "职工500余人，利用机电设备，年均制作皮革万余张。",
        "source": "workbench/ocr/raw/上/part03/page_0275.txt:36; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:60420; workbench/body_chapters/连云港市志_全书_正文汇总.md:56824",
    },
    {
        "label": "皮坊牛皮千余张",
        "old": "王顺记皮坊年收牛皮千馀张。",
        "new": "王顺记皮坊年收牛皮千余张。",
        "source": "workbench/ocr/raw/上/part03/page_0276.txt:27; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:60451; workbench/body_chapters/连云港市志_全书_正文汇总.md:56851",
    },
    {
        "label": "年均购进牛皮千余张",
        "old": "全市年均购进牛皮仅千馀张，以驴皮及其它杂皮维持生产。",
        "new": "全市年均购进牛皮仅千余张，以驴皮及其它杂皮维持生产。",
        "source": "workbench/ocr/raw/上/part03/page_0276.txt:31; workbench/ocr/paddle_ocr/merged/连云港市志_上册_PaddleOCR汇总.md:60456; workbench/body_chapters/连云港市志_全书_正文汇总.md:56855",
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    items = []
    for item in REPLACEMENTS:
        count = text.count(item["old"])
        if count:
            text = text.replace(item["old"], item["new"])
        items.append({**item, "count": count})
    TARGET.write_text(text, encoding="utf-8")

    verify = TARGET.read_text(encoding="utf-8")
    residuals = [item["old"] for item in REPLACEMENTS if item["old"] in verify]
    if residuals:
        raise RuntimeError(f"replacement verification failed: {residuals}")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = sum(item["count"] for item in items)
    payload = {
        "time": now,
        "scope": "最终阅读版余字第四批回源修复",
        "target": str(TARGET),
        "total_replacements": total,
        "items": items,
        "principle": "仅修复最终阅读版与正文汇总不一致，且 raw OCR 与 PaddleOCR 同句闭合为 `余` 的盐业/印刷/轻工残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 最终阅读版余字第四批回源修复",
        "",
        f"- 时间：{now}",
        "- 原则：最终阅读版旧字、正文汇总已为 `余`，且 raw OCR/PaddleOCR 同句闭合后才修。",
        f"- 目标：`{TARGET}`",
        f"- 本次替换：{total} 处。",
        "- 暂缓：污染、广告、其它同形数量词及专名等未纳入本批证据链的残留。",
        "",
        "## 明细",
    ]
    for item in items:
        if item["count"]:
            lines.append(f"- {item['label']}：{item['count']} 处；依据 `{item['source']}`。")
    lines.append("")
    content = "\n".join(lines)
    REPORT_MD.write_text(content, encoding="utf-8")
    PROGRESS.write_text(content, encoding="utf-8")

    marker = "## 2026-07-04 最终阅读版余字第四批回源修复"
    memory = f"""
{marker}
- 依据正文汇总、raw OCR 与 PaddleOCR 同句闭合，修复最终阅读版 `馀 -> 余` 第四批残留，共 {total} 个短语命中。
- 本批覆盖上册 part03 的渔政、盐业、印刷、包装、火柴、家具、灯管、服装鞋帽、皮革段。
- 暂缓污染、广告、其它同形数量词及专名等未纳入本批证据链的残留。
- 报告：`output/reports/final_reader_yu_paddle_backed_batch4_20260704.md`。
"""
    append_once(MEMORY, marker, memory)
    print(json.dumps({"total_replacements": total, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Thirty-fifth batch: PaddleOCR-backed Sakai-Senboku port fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch35_sakai_senboku_port_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch35_sakai_senboku_port_20260706.json"

CHANGES = [
    {
        "old": "1985年2月2～17日，连云港港务局友好考察团一行6人，由朱林森副局长率领，对大阪府港湾局进行友好访问。同年11月2～4日，以大阪府土木部部长松山岩为团长的大阪府友好港交易团一行7人、以泉北港国际交流促进会会长川博信为团长的第二次大阪府港湾经济考察团一行13人来访，连云港港务局局长王功卿和松山岩签定了开辟连云港至泉北港友好航线协议书。</p>",
        "new": "1985年2月2～17日，连云港港务局友好考察团一行6人，由朱林森副局长率领，对大阪府港湾局进行友好访问。同年11月2～4日，以大阪府土木部部长松山岩为团长的大阪府友好港交易团一行7人、以堺泉北港国际交流促进会会长川博信为团长的第二次大阪府港湾经济考察团一行13人来访，连云港港务局局长王功卿和松山岩签定了开辟连云港至堺泉北港友好航线协议书。</p>",
        "section": "1985年堺泉北港友好航线协议段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0290.txt:4-8 raw 作泉北港",
            "workbench/ocr/paddle_ocr/下/part01/page_0290.txt:4-8 PaddleOCR 作堺泉北港",
        ],
    },
    {
        "old": "1986年1月21日，上海远洋运输公司5000吨级的“华安”轮，作为连云港港与泉北港友好航线的首次航行，于1月29日抵泉北港。同年9月2~9日，张明智副局长率领连云港港友好航线代表团一行5人访问泉北港。10月，为满足日益增长的货运量的需要，“华安”轮改由8000吨级的“方城”轮为友好航线定期班轮。11月16～17日，大阪府土木部次长福本善英率泉北港港湾代表团一行7人来访。</p>",
        "new": "1986年1月21日，上海远洋运输公司5000吨级的“华安”轮，作为连云港港与堺泉北港友好航线的首次航行，于1月29日抵堺泉北港。同年9月2~9日，张明智副局长率领连云港港友好航线代表团一行5人访问堺泉北港。10月，为满足日益增长的货运量的需要，“华安”轮改由8000吨级的“方城”轮为友好航线定期班轮。11月16～17日，大阪府土木部次长福本善英率堺泉北港港湾代表团一行7人来访。</p>",
        "section": "1986年堺泉北港友好航线首航段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0290.txt:9-14 raw 作泉北港",
            "workbench/ocr/paddle_ocr/下/part01/page_0290.txt:9-14 PaddleOCR 作堺泉北港",
        ],
    },
    {
        "old": "1987年7月28日至8月5日，副局长彭维友率领连云港友好港口经济技术考察团一行5人出访泉北港。9月21～23日，以日本大阪府顾问冈本洗司为团长的大阪府港湾局访华团一一行3人来连参观访问，与连云港港务局就开展港口现代化管理技术交流举行了会谈。11月12～14日，以大阪府港湾局局长喜多树为团长的大阪府港湾局经济协议团一行6人抵连云港港考察，并与港务局就运输、经济等问题进行会谈，达成了1988年经济技术交流协议。</p>",
        "new": "1987年7月28日至8月5日，副局长彭维友率领连云港友好港口经济技术考察团一行5人出访堺泉北港。9月21～23日，以日本大阪府顾问冈本洗司为团长的大阪府港湾局访华团一行3人来连参观访问，与连云港港务局就开展港口现代化管理技术交流举行了会谈。11月12～14日，以大阪府港湾局局长喜多树为团长的大阪府港湾局经济协议团一行6人抵连云港港考察，并与港务局就运输、经济等问题进行会谈，达成了1988年经济技术交流协议。</p>",
        "section": "1987年堺泉北港考察与大阪府访华团段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0290.txt:15-20 raw 作泉北港、一一行",
            "workbench/ocr/paddle_ocr/下/part01/page_0290.txt:15-20 PaddleOCR 作堺泉北港、一行",
        ],
    },
    {
        "old": "1988年5月21日，连云港港务局局长王功卿等3人赴泉北港参加友好港缔结五周年庆祝活动，为期9天。11月9~11日，以喜多树为团长、大阪府港湾协会会长牧野文雄为副团长的大阪府港湾经济代表团一行17人抵连云港港，参加庆祝泉北港和连云港港缔结友好港五周年活动。</p>",
        "new": "1988年5月21日，连云港港务局局长王功卿等3人赴堺泉北港参加友好港缔结五周年庆祝活动，为期9天。11月9~11日，以喜多树为团长、大阪府港湾协会会长牧野文雄为副团长的大阪府港湾经济代表团一行17人抵连云港港，参加庆祝堺泉北港和连云港港缔结友好港五周年活动。</p>",
        "section": "1988年堺泉北港友好港五周年段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0290.txt:21-24 raw 作泉北港",
            "workbench/ocr/paddle_ocr/下/part01/page_0290.txt:21-24 PaddleOCR 作堺泉北港",
        ],
    },
    {
        "old": "1989年5月24日，连云港港务局友好代表团一行6人赴泉北港等地考察港口建设工程，了解港口管理技术发展趋势。1989年11月12～14日，以大阪府土木部部长吉田喜七郎为团长的大阪府友好港代表团一行6人访问连云港港。</p>\n<p>1990年11月2224日，以大阪府港湾管理监兼港湾局局长村田正也为团长的大阪府友好港代表团一行7人来连云港港进行友好访问。</p>",
        "new": "1989年5月24日，连云港港务局友好代表团一行6人赴堺泉北港等地考察港口建设工程，了解港口管理技术发展趋势。1989年11月12～14日，以大阪府土木部部长吉田喜七郎为团长的大阪府友好港代表团一行6人访问连云港港。</p>\n<p>1990年11月22～24日，以大阪府港湾管理监兼港湾局局长村田正也为团长的大阪府友好港代表团一行7人来连云港港进行友好访问。</p>",
        "section": "1989至1990年堺泉北港考察与日期段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0290.txt:25-29 raw 作泉北港、11月2224日",
            "workbench/ocr/paddle_ocr/下/part01/page_0290.txt:25-29 PaddleOCR 作堺泉北港、11月22~24日",
        ],
    },
    {
        "old": "1983年10月至1990年12月，连云港港和泉北港友好互访团组共17批，117人次。</p>\n<p>其中连云港港出访泉北港的团组计6批，31人次，泉北港来访连云港港的团组计11批，86人次。1985～1990年，连云港港根据年度友好交流协议，先后派遣6批31人次的研修人员，每批2.75人·天，到泉北港学习日本港口生产、经营、管理和建设方面的理论、技术知识。1986年1月至1990年12月，每月往返一次的定期班轮在连云港港至泉北港航线上航行了60航次，货物运载量达31万吨。</p>",
        "new": "1983年10月至1990年12月，连云港港和堺泉北港友好互访团组共17批，117人次。</p>\n<p>其中连云港港出访堺泉北港的团组计6批，31人次，堺泉北港来访连云港港的团组计11批，86人次。1985～1990年，连云港港根据年度友好交流协议，先后派遣6批31人次的研修人员，每批2.75人·天，到堺泉北港学习日本港口生产、经营、管理和建设方面的理论、技术知识。1986年1月至1990年12月，每月往返一次的定期班轮在连云港港至堺泉北港航线上航行了60航次，货物运载量达31万吨。</p>",
        "section": "1983至1990年堺泉北港互访汇总段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0290.txt:30-35 raw 作泉北港",
            "workbench/ocr/paddle_ocr/下/part01/page_0290.txt:30-35 PaddleOCR 作堺泉北港",
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
        "note": "只修下册外事侨务友好港小节中 page_0290 raw/PaddleOCR 可闭合的堺泉北港漏字和日期/重字。未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第三十五批：外事堺泉北港友好港段",
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
        "- 只处理下册外事侨务友好港小节 page_0290 已核实段，不全局替换 `泉北港/堺泉北港`。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

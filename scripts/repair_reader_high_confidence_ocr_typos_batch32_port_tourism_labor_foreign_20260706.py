# -*- coding: utf-8 -*-
"""Thirty-second batch: PaddleOCR-backed port, tourism, labor, foreign affairs fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch32_port_tourism_labor_foreign_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch32_port_tourism_labor_foreign_20260706.json"

CHANGES = [
    {
        "old": "1987年6月开工，1988年工的天然居宾馆",
        "new": "1987年6月开工，1988年竣工的天然居宾馆",
        "section": "建筑业天然居宾馆段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0307.txt:5 raw 作1988年工",
            "workbench/ocr/paddle_ocr/中/part01/page_0307.txt:5 PaddleOCR 作1988年竣工",
        ],
    },
    {
        "old": "计360舰船次，重量达884万多吨",
        "new": "计360艘船次，重量达884万多吨",
        "section": "进口食品卫生监督段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0509.txt:10 raw 作360舰船次",
            "workbench/ocr/paddle_ocr/中/part01/page_0509.txt:10 PaddleOCR 作360艘船次",
        ],
    },
    {
        "old": "食品达14488，不合格率占0.17%",
        "new": "食品达14488吨，不合格率占0.17%",
        "section": "进口食品不合格数量段",
        "evidence": [
            "workbench/ocr/raw/中/part01/page_0509.txt:14 raw 漏吨字",
            "workbench/ocr/paddle_ocr/中/part01/page_0509.txt:14-15 PaddleOCR 作食品达14488吨",
        ],
    },
    {
        "old": "卡拉0K酒廊",
        "new": "卡拉OK酒廊",
        "section": "天然居宾馆设施段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0118.txt:13 raw 作卡拉0K酒廊",
            "workbench/ocr/paddle_ocr/中/part02/page_0118.txt:13 PaddleOCR 作卡拉OK酒廊",
        ],
    },
    {
        "old": "设：置港机维修、港电维修、外语和护土等专业。至1990年未",
        "new": "设置港机维修、港电维修、外语和护士等专业。至1990年末",
        "section": "技工学校专业设置段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0252.txt:10 raw 作设：置、护土、未",
            "workbench/ocr/paddle_ocr/下/part01/page_0252.txt:10 PaddleOCR 作设置、护士、末",
        ],
    },
    {
        "old": "海州美国教会办的义德医院一一批护士，不堪院方欺凌虐待，发动要求改善护土待遇的斗争",
        "new": "海州美国教会办的义德医院一批护士，不堪院方欺凌虐待，发动要求改善护士待遇的斗争",
        "section": "解放前工人运动护士待遇段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0304.txt:33 raw 作一一批、护土待遇",
            "workbench/ocr/paddle_ocr/下/part01/page_0304.txt:32 PaddleOCR 作一批护士、护士待遇",
        ],
    },
    {
        "old": "工会组织论为国民党东海县当局和工头把持的压迫工人的工具",
        "new": "工会组织沦为国民党东海县当局和工头把持的压迫工人的工具",
        "section": "解放前工人运动工会组织段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0305.txt:4 raw 作组织论为",
            "workbench/ocr/paddle_ocr/下/part01/page_0305.txt:4 PaddleOCR 作组织沦为",
        ],
    },
    {
        "old": "新龙区童养熄刘明英退婚案",
        "new": "新龙区童养媳刘明英退婚案",
        "section": "妇联婚姻法宣传段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0334.txt:12 raw 作童养熄",
            "workbench/ocr/paddle_ocr/下/part01/page_0334.txt:12 PaddleOCR 作童养媳",
        ],
    },
    {
        "old": "1989年2月，连云港市友好访日团一行5人出访市。3月，连云港市副市长许维铭等39人在市举办连云港市物产展览会，为期6天。物产展期间，卖品、展品销售额达256.7万美元，签订贸易协议8项，协议金额521.5万美元。5月12~13日，由市部分工会干部和劳使关系人员组成的地区同盟劳使来连云港市观光、访问。7月，连云港市市长王稳卿率领经济考察团一行7人访问市。11月23~25日，市日中友协会长林昭嘉、日本养鸡联合会副会长、印南养鸡组合组合长松田保一等一行4人，自费来连云港市进行友好访问和经济考察，客人参观了新浦农场，与场方签订了经济合作意向书。12月12～21日，连云港市教育交流访团访问日本市等城市，考察日本教育状况，与市教育委员会官员进行两次会谈，交流两市教育情况，代表团参观市的中，小学校、幼儿园和医院，签订1990年友城交流协议书。1989年5月29～31日，由市老人会组织的名铁观光团一行8人来连云港市访问，与新浦区老人代表进行座谈，并参加港务局退休职工联欢会。8月18～21日，由市中学生代表组成的市体育协会友好访华团-一行15人，在市乒乓协会会长吉川均率领下，与连云港市少年乒乓球队进行友谊比赛。9月，连云港市医疗卫生代表团访问市。10月2～3日，市日中友协访华团一行12人来访，团长为林昭嘉。10月29日至11月3日，市教育友好访华团一行10人来访，参观新海中学、解放路小学，与连云港市达成1991年度友好交流协议。11月，连云港市人民对外友好协会会长秦兆祯率对外友协访日团一行5人访问市。1990年，连云港市选派1名进修生赴市进修图书管理业务。</p>",
        "new": "1989年2月，连云港市友好访日团一行5人出访堺市。3月，连云港市副市长许维铭等39人在堺市举办连云港市物产展览会，为期6天。物产展期间，卖品、展品销售额达256.7万美元，签订贸易协议8项，协议金额521.5万美元。5月12~13日，由堺市部分工会干部和劳使关系人员组成的堺地区同盟劳使来连云港市观光、访问。7月，连云港市市长王稳卿率领经济考察团一行7人访问堺市。11月23~25日，堺市日中友协会长林昭嘉、日本养鸡联合会副会长、堺印南养鸡组合组合长松田保一等一行4人，自费来连云港市进行友好访问和经济考察，客人参观了新浦农场，与场方签订了经济合作意向书。12月12～21日，连云港市教育交流访日团访问日本堺市等城市，考察日本教育状况，与堺市教育委员会官员进行两次会谈，交流两市教育情况，代表团参观堺市的中、小学校、幼儿园和医院，签订1990年友城交流协议书。1989年5月29～31日，由堺市老人会组织的名铁观光团一行8人来连云港市访问，与新浦区老人代表进行座谈，并参加港务局退休职工联欢会。8月18～21日，由堺市中学生代表组成的堺市体育协会友好访华团一行15人，在堺市乒乓协会会长吉川均率领下，与连云港市少年乒乓球队进行友谊比赛。9月，连云港市医疗卫生代表团访问堺市。10月2～3日，堺市日中友协访华团一行12人来访，团长为林昭嘉。10月29日至11月3日，堺市教育友好访华团一行10人来访，参观新海中学、解放路小学，与连云港市达成1991年度友好交流协议。11月，连云港市人民对外友好协会会长秦兆祯率对外友协访日团一行5人访问堺市。1990年，连云港市选派1名进修生赴堺市进修图书管理业务。</p>",
        "section": "堺市友好交流段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0294.txt:11-27 raw 多处漏堺字",
            "workbench/ocr/paddle_ocr/下/part01/page_0294.txt:11-29 PaddleOCR 给出堺市完整段落",
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
        "note": "只修 raw/PaddleOCR 可闭合的港口、旅游、劳动、妇联、外事短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第三十二批：港口、旅游、劳动与外事短片段",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        old = item["old"] if len(item["old"]) <= 80 else item["old"][:80] + "..."
        new = item["new"] if len(item["new"]) <= 80 else item["new"][:80] + "..."
        lines.append(f"- {item['section']}：`{old}` -> `{new}`（命中 {item['count']} 处）")
        for evidence in item["evidence"]:
            lines.append(f"  - 证据：`{evidence}`")
    lines += [
        "",
        "## 边界",
        "",
        "- 只修主阅读版，不改 OCR 原文。",
        "- 未全局替换 `市/堺市`、`护土/护士`、`0K/OK`、`工/竣工` 等模式。",
        "- 医学术语、人大视察段、公安查禁卖淫段仍缺本批同等强证据，本批暂缓。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Thirty-sixth batch: PaddleOCR-backed Sakai-Senboku port opening fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch36_sakai_senboku_port_opening_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch36_sakai_senboku_port_opening_20260706.json"

CHANGES = [
    {
        "old": "一、连云港港一日本泉北港日本泉北港是由历史悠久的港和新兴的泉北港于1969年合并而成，地处大阪湾，是大阪府所属7个港口中最大的一个，也是日本政府指定的18个“特写重要港湾”之一，泉北港与连云港港有较相似的发展史、地理环境及在本国港口中所占的地位。</p>",
        "new": "一、连云港港一日本堺泉北港</p>\n<p>日本堺泉北港是由历史悠久的堺港和新兴的泉北港于1969年合并而成，地处大阪湾，是大阪府所属7个港口中最大的一个，也是日本政府指定的18个“特写重要港湾”之一，堺泉北港与连云港港有较相似的发展史、地理环境及在本国港口中所占的地位。</p>",
        "section": "友好港小节标题与简介",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0289.txt:6-10 raw 多处漏堺字",
            "workbench/ocr/paddle_ocr/下/part01/page_0289.txt:6-10 PaddleOCR 给出堺泉北港与堺港",
        ],
    },
    {
        "old": "1982年3月，日本大阪府知事岸昌致函中国交通部，提出该府所属的泉北港希望与江苏境内的一个港口建立友好港关系。5月，经中国交通部批准，应江苏省政府的邀请，以大阪府副知事牧野文雄为首的大阪府港湾考察团一行5人、以大阪府港湾协会会长山崎政男为团长的大阪府日中港湾友好团一行16人来江苏了解港口情况，实地考察了南通港、南京港和连云港港，经比较论证，最后选定连云港港和泉北港发展友好关系。在连期间，宾主双方就泉北港和连云港港的现状、发展规划以及港口机械设备技术、管理等方面进行了会谈，并表示积极开展两港之间的业务技术交流，为早日缔结友好港口而努力。同年11月22日至12月2日，应大阪府邀请，以连云港市人大常委会主任叶志俊为团长的江苏省友好港口代表团一行8人赴日进行友好访问，拜会了日本运输省港湾局和大阪府、泉大津市、高石市和市政府，参观考察了奈良、神户、京都、横滨、东京等城市和泉北港、神户港、横滨港，在日期间，代表团与大阪府就连云港港与泉北港缔结友好港口协议书内容、签约时间及与大阪府进行经济技术交流等事宜举行会谈并取得一致意见。</p>",
        "new": "1982年3月，日本大阪府知事岸昌致函中国交通部，提出该府所属的堺泉北港希望与江苏境内的一个港口建立友好港关系。5月，经中国交通部批准，应江苏省政府的邀请，以大阪府副知事牧野文雄为首的大阪府港湾考察团一行5人、以大阪府港湾协会会长山崎政男为团长的大阪府日中港湾友好团一行16人来江苏了解港口情况，实地考察了南通港、南京港和连云港港，经比较论证，最后选定连云港港和堺泉北港发展友好关系。在连期间，宾主双方就堺泉北港和连云港港的现状、发展规划以及港口机械设备技术、管理等方面进行了会谈，并表示积极开展两港之间的业务技术交流，为早日缔结友好港口而努力。同年11月22日至12月2日，应大阪府邀请，以连云港市人大常委会主任叶志俊为团长的江苏省友好港口代表团一行8人赴日进行友好访问，拜会了日本运输省港湾局和大阪府、泉大津市、高石市和堺市政府，参观考察了奈良、神户、京都、横滨、东京等城市和堺泉北港、神户港、横滨港，在日期间，代表团与大阪府就连云港港与堺泉北港缔结友好港口协议书内容、签约时间及与大阪府进行经济技术交流等事宜举行会谈并取得一致意见。</p>",
        "section": "1982年堺泉北港建立友好港关系段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0289.txt:11-22 raw 多处漏堺字",
            "workbench/ocr/paddle_ocr/下/part01/page_0289.txt:11-22 PaddleOCR 给出堺泉北港、堺市政府",
        ],
    },
    {
        "old": "连云港港与泉北港通过多次人员、函电来往，并经双方港上级机关的批准，1983年6月25日上午，在连云港市黄海影剧院举行了连云港港与泉北港缔结友好港签字仪式。连云港港务局局长徐德济、大阪府土木部部长松村明代表两港在友好港协议书上签字。同日下午，连云港港务局局长徐德济等与大阪府土木部参事兼港湾课长吉村源逸等举行会谈，双方正式签订了《中国连云港一日本大阪府泉北港关于友好技术交流协议的备忘录》。会谈结束后，双方代表在墟沟海滨公园共同栽下两棵象征友谊的银杏树。</p>",
        "new": "连云港港与堺泉北港通过多次人员、函电来往，并经双方港上级机关的批准，1983年6月25日上午，在连云港市黄海影剧院举行了连云港港与堺泉北港缔结友好港签字仪式。连云港港务局局长徐德济、大阪府土木部部长松村明代表两港在友好港协议书上签字。同日下午，连云港港务局局长徐德济等与大阪府土木部参事兼港湾课长吉村源逸等举行会谈，双方正式签订了《中国连云港一日本大阪府堺泉北港关于友好技术交流协议的备忘录》。会谈结束后，双方代表在墟沟海滨公园共同栽下两棵象征友谊的银杏树。</p>",
        "section": "1983年堺泉北港签字仪式段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0289.txt:23-29 raw 作泉北港",
            "workbench/ocr/paddle_ocr/下/part01/page_0289.txt:23-29 PaddleOCR 作堺泉北港",
        ],
    },
    {
        "old": "连云港港与泉北港缔结为友好港关系以后，双方根据结好协议书和友好港年度交流计划，开展人员互访和港口生产技术交流活动，开辟友好航线，推动了两港友好关系的发展。</p>\n<p>1983年10月21日，应大阪府邀请，以连云港港务局局长徐德济为团长的连云港港友好代表团一行6人赴日本访问，参加大阪府10月26日举行的友好港纪念庆祝大会，并对泉北港进行了生产技术和港口业务考察。</p>",
        "new": "连云港港与堺泉北港缔结为友好港关系以后，双方根据结好协议书和友好港年度交流计划，开展人员互访和港口生产技术交流活动，开辟友好航线，推动了两港友好关系的发展。</p>\n<p>1983年10月21日，应大阪府邀请，以连云港港务局局长徐德济为团长的连云港港友好代表团一行6人赴日本访问，参加大阪府10月26日举行的友好港纪念庆祝大会，并对堺泉北港进行了生产技术和港口业务考察。</p>",
        "section": "友好港关系总述与1983年考察段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0289.txt:30-35 raw 作泉北港",
            "workbench/ocr/paddle_ocr/下/part01/page_0289.txt:30-35 PaddleOCR 作堺泉北港",
        ],
    },
    {
        "old": "1984年7月8~13日，以大阪府港湾局企画振兴室室长武田英治为团长、市副市长大久保博之为副团长的大阪府友好港调查团一行6人来连，就港口、外贸、外运及连云港市的经济发展情况进行考察。代表团还就进一步加强两港间的友好合作与连云港港务局进行了会谈。7月12～13日，以奥村心宏为团长的大阪府经济考察团来连进行友好访问，双方就如何通过友好城市和友好港口的途径扩大经济技术交流进行了商。</p>",
        "new": "1984年7月8~13日，以大阪府港湾局企画振兴室室长武田英治为团长、堺市副市长大久保博之为副团长的大阪府友好港调查团一行6人来连，就港口、外贸、外运及连云港市的经济发展情况进行考察。代表团还就进一步加强两港间的友好合作与连云港港务局进行了会谈。7月12～13日，以奥村心宏为团长的大阪府经济考察团来连进行友好访问，双方就如何通过友好城市和友好港口的途径扩大经济技术交流进行了磋商。</p>",
        "section": "1984年大阪府友好港调查团段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0289.txt:36-40 raw 作市副市长、进行了商",
            "workbench/ocr/paddle_ocr/下/part01/page_0289.txt:36-40 PaddleOCR 作堺市副市长、进行了磋商",
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
        "note": "只修下册外事侨务友好港小节 page_0289 raw/PaddleOCR 可闭合的堺泉北港漏字、标题简介和磋商残缺。未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第三十六批：外事堺泉北港友好港开头",
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
        "- 只处理下册外事侨务友好港小节 page_0289 已核实段，不全局替换 `泉北港/堺泉北港`。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

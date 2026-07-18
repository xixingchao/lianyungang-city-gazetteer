# -*- coding: utf-8 -*-
"""Twentieth batch: PaddleOCR-backed culture and biography repairs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch20_culture_bio_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch20_culture_bio_20260706.json"

CHANGES = [
    {
        "section": "工鼓锣传统书目段",
        "old": "<p>工鼓锣有完整的表演形式。据不完全统计，清末民初时，仅灌云县有影响的艺人就达30余人。如板浦的徐礼、嵇福田，同兴乡的张士仪，伊山镇的徐五先生，杨集的段大贤、周大肚，另有东海县白塔埠的陈六，房山镇山后村的孙兆凯，安峰乡的陆文方夫妇，都在艺术上独树一帜，享有盛誉。这一时期具有代表性的书目有《大宋）、《三国》《云台中汉》《说唐》、《异奇图》、《三七美》、《下河东》等数十部。一些有文化的艺人，不满足已有传统书目，则自编自唱一些新书自，艺人们在传唱中加以完善，如《七义梅》《五剑十三保）、五花图》、《水阜山》等各类书目共150余部。</p>",
        "new": "<p>工鼓锣有完整的表演形式。据不完全统计，清末民初时，仅灌云县有影响的艺人就达30余人。如板浦的徐礼、嵇福田，同兴乡的张士仪，伊山镇的徐五先生，杨集的段大贤、周大肚，另有东海县白塔埠的陈六，房山镇山后村的孙兆凯，安峰乡的陆文方夫妇，都在艺术上独树一帜，享有盛誉。这一时期具有代表性的书目有《大宋》、《三国》《云台中汉》、《说唐》、《异奇图》、《三七美》、《下河东》等数十部。一些有文化的艺人，不满足已有传统书目，则自编自唱一些新书目，艺人们在传唱中加以完善，如《七义梅》、《五剑十三保》、《五花图》、《水旱山》等各类书目共150余部。</p>",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0031.txt:9-12 raw 可见书自、水阜山及书名标点错识",
            "workbench/ocr/paddle_ocr/下/part02/page_0031.txt:9-12 PaddleOCR 给出书目、水旱山及书名标点",
        ],
    },
    {
        "section": "工鼓锣会演段",
        "old": "<p>建国后，一向靠摆地摊，拿签子谋生的艺人，也参加国家、省、市、县级的专业曲艺、文艺会演，得到政府的嘉奖。1958年8月，灌云县工鼓锣艺人张同举作为江苏省曲艺团的代表，赴北京参加全国首届曲艺会演，表演了书自《单力赴会），受到党和国家领导人周恩来、董必武的接见。次年，该书目被上海唱片公司灌制成唱片，在全国发行。一代年轻的工鼓锣艺人也不断涌现。灌云县年方21岁的女艺人季炳红，在1985年的连云港市曲艺会演中，一篇《李三万》的书目荣登榜首，并被推为市民间艺人联合会主席。</p>",
        "new": "<p>建国后，一向靠摆地摊，拿签子谋生的艺人，也参加国家、省、市、县级的专业曲艺、文艺会演，得到政府的嘉奖。1958年8月，灌云县工鼓锣艺人张同举作为江苏省曲艺团的代表，赴北京参加全国首届曲艺会演，表演了书目《单刀赴会》，受到党和国家领导人周恩来、董必武的接见。次年，该书目被上海唱片公司灌制成唱片，在全国发行。一代年轻的工鼓锣艺人也不断涌现。灌云县年方21岁的女艺人李炳红，在1985年的连云港市曲艺会演中，一篇《李三万》的书目荣登榜首，并被推为市民间艺人联合会主席。</p>",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0031.txt:20-23 raw 可见书自、单力赴会、季炳红错识",
            "workbench/ocr/paddle_ocr/下/part02/page_0031.txt:21-24 PaddleOCR 给出书目、单刀赴会、李炳红",
        ],
    },
    {
        "section": "图书馆参考咨询段",
        "old": "建立健全馆藏工具书自录，编制各种专题书目，如《关于地震的馆藏图书报刊目录》、《连云港市图书馆经济改革专题文献馆藏目录》、《1986年全市外文期刊联合自录》、（1987年全市外文期刊目录》、《开放港口城市资料专题自录》等。",
        "new": "建立健全馆藏工具书目录，编制各种专题书目，如《关于地震的馆藏图书报刊目录》、《连云港市图书馆经济改革专题文献馆藏目录》、《1986年全市外文期刊联合目录》、《1987年全市外文期刊目录》、《开放港口城市资料专题目录》等。",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0068.txt:18-20 raw 可见工具书自录、联合自录、专题自录及左括号错识",
            "workbench/ocr/paddle_ocr/下/part02/page_0068.txt:18-20 PaddleOCR 给出目录与正确书名括号",
        ],
    },
    {
        "section": "甘瑞兰传",
        "old": "民国14年人山东滕县华北神学院学习，民国18年毕业，受聘为新浦基督教会牧师。民国36年7月被推选为中国基督教差会江准大会执行委员会副会长。",
        "new": "民国14年入山东滕县华北神学院学习，民国18年毕业，受聘为新浦基督教会牧师。民国36年7月被推选为中国基督教差会江淮大会执行委员会副会长。",
        "evidence": [
            "workbench/ocr/raw/下/part02/page_0354.txt:13-14 raw 作人山东、江准大会",
            "workbench/ocr/paddle_ocr/下/part02/page_0354.txt:13-14 PaddleOCR 作入山东、江淮大会",
        ],
    },
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for change in CHANGES:
        count = html.count(change["old"])
        if count != 1:
            raise RuntimeError(f"expected one hit for {change['section']}, found {count}")
        html = html.replace(change["old"], change["new"])
        applied.append({**change, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "note": "只修页级 PaddleOCR 与 raw OCR 对照闭合的文化、图书馆、人物短段。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第二十批：文化与人物短段",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- {item['section']}：精确替换 {item['count']} 处。")
        for evidence in item["evidence"]:
            lines.append(f"  - 证据：`{evidence}`")
    lines += [
        "",
        "## 边界",
        "",
        "- 只修主阅读版；不改中间 OCR 原文。",
        "- 不批量替换全部书自/自录/人某校，只处理本批已回源闭合的段落。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

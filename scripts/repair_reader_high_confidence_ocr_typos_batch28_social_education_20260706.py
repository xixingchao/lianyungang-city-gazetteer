# -*- coding: utf-8 -*-
"""Twenty-eighth batch: PaddleOCR-backed social and education text fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch28_social_education_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch28_social_education_20260706.json"

CHANGES = [
    {
        "old": "各县区公安机关会同文化、工商、厂广播等部门对全市262个舞厅、咖啡对3家舞厅责令停业整顿，63家自行停业",
        "new": "各县区公安机关会同文化、工商、广播等部门对全市262个舞厅、咖啡馆、录像放映点等公共娱乐场所进行安全检查，查封3户个体录像带制作、复录、经销点，对3家舞厅责令停业整顿，63家自行停业",
        "section": "公安公共场所管理段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0082.txt:23 raw 漏失咖啡馆、录像放映点等后续内容",
            "workbench/ocr/paddle_ocr/下/part01/page_0082.txt:24-26 PaddleOCR 给出完整句",
        ],
    },
    {
        "old": "收缴淫录像带81盘",
        "new": "收缴淫秽录像带81盘",
        "section": "公安公共场所管理段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0082.txt:27 作淫秽录像带81盘",
        ],
    },
    {
        "old": "查处卖淫缥、复制贩卖传播淫秽物品案件61起",
        "new": "查处卖淫嫖娼、复制贩卖传播淫秽物品案件61起",
        "section": "公安公共场所管理段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0082.txt:30 作卖淫嫖娼、复制贩卖传播淫秽物品案件61起",
        ],
    },
    {
        "old": "普及法律常识的对象是工人、农（渔）民、千部、学生、军人、其他劳动者和城镇居民中一切有接受教育能力的公民。其中，各级千部、尤其是各级领导于部、青壮年职工、农户的“当家人”或主要劳动力、街道待业青年以及大中专学校、中学师生等作为普及教育重点进行。普及内容含“九法一例”，即《宪法》、《刑法》、《刑事诉讼法》、《民法通则》、《民事诉讼法》、《婚姻法》、《继承法》、《兵役法》、《经济合同法）、《治安管理处罚条例》等。领导干部、机关一般干部、乡（镇）村干部以自学为主，定期举办法制讨论或脱产轮训。企事业职工以上大课为主。农村、街道以创办法制业余学校、农民学校等形式上法制课。组织普法宣讲团、队、文艺演出队到乡村宣传。边远乡村组织“十户一体”学法小组。1986~1990年，全市举办法制宣传骨干培训班1290期，培训法制宣传员7.95万人，举办法律知识竞赛500多场，抓普法试点109个。有225.45万人参加普法学习，占普法对象的92%，其中约有201.6万人学完规定的普法内容；5.5万名干部（含教师2.8万）中5.4万名学习了“九法一例”，经过考试，取得合格证书。职工37万人中35万人学完规定内容。146万农民中128万人学习了“九法一例”的主要内容。8万名城镇居民中7.36万人参加了普法学习。56.2万名大中小学生参加了法制课学习。市、县、区政问题，1989年，对全市个体税收专项检查，查补交税款1000余万元，依法惩处严重偷税个体户21人。",
        "new": "普及法律常识的对象是工人、农（渔）民、干部、学生、军人、其他劳动者和城镇居民中一切有接受教育能力的公民。其中，各级干部、尤其是各级领导干部、青壮年职工、农户的“当家人”或主要劳动力、街道待业青年以及大中专学校、中学师生等作为普及教育重点进行。普及内容含“九法一例”，即《宪法》、《刑法》、《刑事诉讼法》、《民法通则》、《民事诉讼法》、《婚姻法》、《继承法》、《兵役法》、《经济合同法》、《治安管理处罚条例》等。领导干部、机关一般干部、乡（镇）村干部以自学为主，定期举办法制讨论或脱产轮训。企事业职工以上大课为主。农村、街道以创办法制业余学校、农民学校等形式上法制课。组织普法宣讲团、队、文艺演出队到乡村宣传。边远乡村组织“十户一体”学法小组。1986~1990年，全市举办法制宣传骨干培训班1290期，培训法制宣传员7.95万人，举办法律知识竞赛500多场，抓普法试点109个。有225.45万人参加普法学习，占普法对象的92%，其中约有201.6万人学完规定的普法内容；5.5万名干部（含教师2.8万）中5.4万名学习了“九法一例”，经过考试，取得合格证书。职工37万人中35万人学完规定内容。146万农民中128万人学习了“九法一例”的主要内容。8万名城镇居民中7.36万人参加了普法学习。56.2万名大中小学生参加了法制课学习。市、县、区政府和有关政府部门聘请律师担任常年法律顾问134家。行政执法部门依法处理各种违法问题，1989年，对全市个体税收专项检查，查补交税款1000余万元，依法惩处严重偷税个体户21人。",
        "section": "司法行政普法段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0150.txt:正文存在千部、于部、经济合同法）、市县区政问题等误识和漏句",
            "workbench/ocr/paddle_ocr/下/part01/page_0150.txt:3-23 PaddleOCR 给出干部、领导干部、经济合同法》及政府法律顾问句",
        ],
    },
    {
        "old": "邀请郑州参加“二七大罢工和上海参加革命斗争的老工人作报告",
        "new": "邀请郑州参加“二七”大罢工和上海参加革命斗争的老工人作报告",
        "section": "工会职工教育培训段",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0316.txt:35-36 作郑州参加“二七”大罢工",
        ],
    },
    {
        "old": "有职工业余学校79所，人学职工8649人",
        "new": "有职工业余学校79所，入学职工8649人",
        "section": "工会职工教育培训段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0316.txt:38 raw 作人学职工8649人",
            "workbench/ocr/paddle_ocr/下/part01/page_0316.txt:39 PaddleOCR 作入学职工8649人",
        ],
    },
    {
        "old": "民国31年（1942年）初，中共苏北区委员会发出《关于加强妇女工作的指示》，要求各吃穿问题。",
        "new": "民国31年（1942年）初，中共苏北区委员会发出《关于加强妇女工作的指示》，要求各县“以生产纺织为中心，发动妇女垦荒种地”，“家家纺纱，户户织布”，解决抗日根据地军民吃穿问题。",
        "section": "妇联促进生产劳动段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0333.txt:6 raw 仅余要求各...吃穿问题",
            "workbench/ocr/paddle_ocr/下/part01/page_0333.txt:4-6 PaddleOCR 给出完整引文",
        ],
    },
    {
        "old": "境内小学实施《王子癸丑学制》。初等教育为两级：初小4年，为义务教育，男女同校；高小3年，男女分校。儿童6岁人学。民国13年，小学改为四二制”：前4年为初级小学，是义务教育；后2年为高级小学。初小可以单设，初小修业期满者得予以补习教育。高级小学增设职业准备学科。儿童6岁入学。民国35年至37年，市境内国民党统治区实行小学“四二制”。解放区小学采用早学、午学、夜学、全日制、半日制等上课形式。建国后，小学沿用“四二制”。1952年，部分小学试行“五年一贯制”。“文化大革命”期间，市内小学实行“五年制”。1982年，市区小学实行六年制”。赣榆、东海、灌云三县小学实行“五年制”。",
        "new": "境内小学实施《壬子癸丑学制》。初等教育为两级：初小4年，为义务教育，男女同校；高小3年，男女分校。儿童6岁入学。民国13年，小学改为“四二制”：前4年为初级小学，是义务教育；后2年为高级小学。初小可以单设，初小修业期满者得予以补习教育。高级小学增设职业准备学科。儿童6岁入学。民国35年至37年，市境内国民党统治区实行小学“四二制”。解放区小学采用早学、午学、夜学、全日制、半日制等上课形式。建国后，小学沿用“四二制”。1952年，部分小学试行“五年一贯制”。“文化大革命”期间，市内小学实行“五年制”。1982年，市区小学实行“六年制”。赣榆、东海、灌云三县小学实行“五年制”。",
        "section": "小学学制段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0365.txt:90-95 raw 作王子癸丑、儿童6岁人学、四二制”、六年制”",
            "workbench/ocr/paddle_ocr/下/part01/page_0365.txt:26-35 PaddleOCR 作壬子癸丑、入学、“四二制”、“六年制”",
        ],
    },
    {
        "old": "担任人天代表和政协委员的民进会员",
        "new": "担任人大代表和政协委员的民进会员",
        "section": "民建参政议政段",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0471.txt:6 raw 作人天代表",
            "workbench/ocr/paddle_ocr/中/part02/page_0471.txt:6 作人大代表",
        ],
    },
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for change in CHANGES:
        count = html.count(change["old"])
        if count != 1:
            raise RuntimeError(f"expected one hit for {change['section']}, found {count}: {change['old']}")
        html = html.replace(change["old"], change["new"])
        applied.append({**change, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "note": "只修 raw/PaddleOCR 可闭合的社团、公安、司法、工会、教育短片段；未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第二十八批：社团、公安、司法与教育短片段",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- {item['section']}：`{item['old']}` -> `{item['new']}`（命中 {item['count']} 处）")
        for evidence in item["evidence"]:
            lines.append(f"  - 证据：`{evidence}`")
    lines += [
        "",
        "## 边界",
        "",
        "- 只修主阅读版，不改 OCR 原文。",
        "- 未全局替换 `人学/人天/厂广/缥/娟/千部` 等模式。",
        "- 医学术语与人大视察段仍缺同等强证据，本批暂缓。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

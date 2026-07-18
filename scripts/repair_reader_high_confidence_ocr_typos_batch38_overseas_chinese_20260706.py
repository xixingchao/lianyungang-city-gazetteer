# -*- coding: utf-8 -*-
"""Thirty-eighth batch: PaddleOCR-backed overseas Chinese affairs fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch38_overseas_chinese_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch38_overseas_chinese_20260706.json"

CHANGES = [
    {
        "old": "灌云县的注德昭、杨天全等人",
        "new": "灌云县的汪德昭、杨天全等人",
        "section": "华侨外籍华人段人名",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0297.txt:20 raw 作注德昭",
            "workbench/ocr/paddle_ocr/下/part01/page_0297.txt:20 PaddleOCR 作汪德昭",
        ],
    },
    {
        "old": "国家对归侨、侨着出国、出境探亲、定居等采取了一系列优惠政策",
        "new": "国家对归侨、侨眷出国、出境探亲、定居等采取了一系列优惠政策",
        "section": "归侨侨眷出境政策段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0297.txt:27 raw 作侨着",
            "workbench/ocr/paddle_ocr/下/part01/page_0297.txt:26 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "而加入所在国的国籍，成为中国血统外籍人。他们从事的职业多为文教、科技、卫生方面的专业人员或从事经济的工商业者。据1987年的统计资料，全市华侨、外籍华人和港澳同胞中教授27人，博（硕）土35人",
        "new": "而加入所在国的国籍，成为中国血统外籍人。他们从事的职业多为文教、科技、卫生方面的专业人员或从事经济的工商业者。据1987年的统计资料，全市华侨、外籍华人和港澳同胞中教授27人，博（硕）士35人",
        "section": "海外华人职业与学历段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0297.txt:30-34 raw 作加人、博（硕）土",
            "workbench/ocr/paddle_ocr/下/part01/page_0297.txt:30-34 PaddleOCR 作加入、博(硕)士",
        ],
    },
    {
        "old": "按照党和政府对归侨、侨着“一视同仁，不得歧视，根据特点，适当照顾”的侨务政策",
        "new": "按照党和政府对归侨、侨眷“一视同仁，不得歧视，根据特点，适当照顾”的侨务政策",
        "section": "归侨侨眷政策段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0298.txt:14 raw 作侨着",
            "workbench/ocr/paddle_ocr/下/part01/page_0298.txt:14 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "三、侨据1990年统计，连云港市侨着（含港澳同胞着属，下同）共997户，4336人。其中市区2730人，东海县627人，灌云县552人，赣榆县427人。全市大部分侨着与海外亲友保持通信、通话、通汇的联系。全市的侨券分布在各条战线上，为连云港市的经济建设和对外开放作出了贡献。其中有许多人走上领导岗位，担任县处级以上职务的10人，获高级职称的32人，受到省级以上表彰的有14人。市区具有中专以上文化程度的侨着",
        "new": "三、侨眷据1990年统计，连云港市侨眷（含港澳同胞眷属，下同）共997户，4336人。其中市区2730人，东海县627人，灌云县552人，赣榆县427人。全市大部分侨眷与海外亲友保持通信、通话、通汇的联系。全市的侨眷分布在各条战线上，为连云港市的经济建设和对外开放作出了贡献。其中有许多人走上领导岗位，担任县处级以上职务的10人，获高级职称的32人，受到省级以上表彰的有14人。市区具有中专以上文化程度的侨眷",
        "section": "侨眷统计段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0298.txt:19-26 raw 多处作侨着/侨券/着属",
            "workbench/ocr/paddle_ocr/下/part01/page_0298.txt:19-26 PaddleOCR 作侨眷/眷属",
        ],
    },
    {
        "old": "市辖三县的1600多名侨着，由于历史和文化程度不高等原因",
        "new": "市辖三县的1600多名侨眷，由于历史和文化程度不高等原因",
        "section": "三县侨眷段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0298.txt:27 raw 作侨着",
            "workbench/ocr/paddle_ocr/下/part01/page_0298.txt:27 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "消除归侨、侨着的各种顾虑。在登记填表阶段，市侨办人员克服全市归侨、侨券居住分散的困难",
        "new": "消除归侨、侨眷的各种顾虑。在登记填表阶段，市侨办人员克服全市归侨、侨眷居住分散的困难",
        "section": "侨情普查登记顾虑段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0299.txt:10-12 raw 作侨着/侨券",
            "workbench/ocr/paddle_ocr/下/part01/page_0299.txt:10-12 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "全市共有归侨23户，侨卷154户。港澳同胞亲属217户",
        "new": "全市共有归侨23户，侨眷154户。港澳同胞亲属217户",
        "section": "1980年侨情普查户数段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0299.txt:16 raw 作侨卷",
            "workbench/ocr/paddle_ocr/下/part01/page_0299.txt:16 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "共有归侨53人，侨着190户1018人，港澳同胞着属322户1318人。旅居海外人员1116户2954人，分布在22个国家和地区。全市归侨、侨誉中各类知识分子194人",
        "new": "共有归侨53人，侨眷190户1018人，港澳同胞眷属322户1318人。旅居海外人员1116户2954人，分布在22个国家和地区。全市归侨、侨眷中各类知识分子194人",
        "section": "1983年侨情补查段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0299.txt:19-21 raw 作侨着/着属/侨誉",
            "workbench/ocr/paddle_ocr/下/part01/page_0299.txt:19-21 PaddleOCR 作侨眷/眷属",
        ],
    },
    {
        "old": "截至1987年底，全市共有归侨、侨着4394人",
        "new": "截至1987年底，全市共有归侨、侨眷4394人",
        "section": "1987年侨情调查段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0299.txt:23 raw 作侨着",
            "workbench/ocr/paddle_ocr/下/part01/page_0299.txt:23 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "支持和帮助侨寻亲、认亲",
        "new": "支持和帮助侨眷寻亲、认亲",
        "section": "侨眷寻亲认亲段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0299.txt:26 raw 漏眷字",
            "workbench/ocr/paddle_ocr/下/part01/page_0299.txt:26 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "根据对归侨、侨着“一视同仁，不得歧视，根据特点，适当照顾”的原则",
        "new": "根据对归侨、侨眷“一视同仁，不得歧视，根据特点，适当照顾”的原则",
        "section": "权益维护原则段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0299.txt:28 raw 作侨着",
            "workbench/ocr/paddle_ocr/下/part01/page_0299.txt:28 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "挫伤了归侨、侨和旅外侨胞的感情",
        "new": "挫伤了归侨、侨眷和旅外侨胞的感情",
        "section": "文革侨务政策感情段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0299.txt:30 raw 漏眷字",
            "workbench/ocr/paddle_ocr/下/part01/page_0299.txt:30 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "维护归侨、侨着的合法权益",
        "new": "维护归侨、侨眷的合法权益",
        "section": "合法权益段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0299.txt:31 raw 作侨着",
            "workbench/ocr/paddle_ocr/下/part01/page_0299.txt:31 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "先后没收归侨、侨着王某某、李某某等5人汇款",
        "new": "先后没收归侨、侨眷王某某、李某某等5人汇款",
        "section": "归侨侨眷汇款退还段",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0299.txt:32 raw 作侨着",
            "workbench/ocr/paddle_ocr/下/part01/page_0299.txt:32 PaddleOCR 作侨眷",
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
        "note": "只修下册侨务 page_0297-page_0299 raw/PaddleOCR 可闭合的侨眷等短片段；未全局替换。未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第三十八批：侨务侨眷短片段",
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
        "- 只处理 page_0297-page_0299 已核实段，不全局替换 `侨着/侨券/侨卷/侨眷`。",
        "- 未处理其它卷章中尚未回源核证的同类词。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Batch 39: PaddleOCR-backed qiaojuan and Sakai residue fixes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch39_qiao_sakai_residues_20260706.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch39_qiao_sakai_residues_20260706.json"

CHANGES = [
    {
        "old": "3月9~14日在日本市举办“中国连云港物产展”",
        "new": "3月9~14日在日本堺市举办“中国连云港物产展”",
        "section": "外经物产展地点",
        "evidence": [
            "workbench/ocr/raw/上/part01/page_0119.txt:5 raw 作日本市",
            "workbench/ocr/paddle_ocr/上/part01/page_0119.txt:5 PaddleOCR 作日本堺市",
        ],
    },
    {
        "old": "连云港港与日本泉北港，连云港市与日本市、澳大利亚科雷奥郡",
        "new": "连云港港与日本堺泉北港，连云港市与日本堺市、澳大利亚科雷奥郡",
        "section": "外事侨务概述友好港友城",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0284.txt:11 作日本堺泉北港、日本堺市",
        ],
    },
    {
        "old": "放宽了对归侨和侨券出国、出境探亲、定居、留学等政策",
        "new": "放宽了对归侨和侨眷出国、出境探亲、定居、留学等政策",
        "section": "外事侨务概述侨眷出境政策",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0284.txt:17 作归侨和侨眷",
        ],
    },
    {
        "old": "1980年9月，连云港市召开第一次归侨、侨着代表大会，成立归侨、侨卷联合小组。",
        "new": "1980年9月，连云港市召开第一次归侨、侨眷代表大会，成立归侨、侨眷联合小组。",
        "section": "外事侨务概述归侨侨眷代表大会",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0284.txt:25 作归侨、侨眷代表大会/侨眷联合小组",
        ],
    },
    {
        "old": "使这个侨着集资办的公司转亏为盈",
        "new": "使这个侨眷集资办的公司转亏为盈",
        "section": "致公党社会服务侨眷集资",
        "evidence": [
            "workbench/ocr/raw/中/part02/page_0474.txt:13 raw 作侨着",
            "workbench/ocr/paddle_ocr/中/part02/page_0474.txt:13 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "1981年，市侨办根据《关于善始善终地复查纠正归侨、侨着中冤假错案工作的通知》精神，会同有关部门对“文化大革命”中造成的冤假错案以及历史遗留下来的老案，逐人逐户进行了清理和复查。至1987年，全市归侨、侨着及港澳同胞亲属在“文化大革命”期间，因海外关系而造成的冤假错案24起",
        "new": "1981年，市侨办根据《关于善始善终地复查纠正归侨、侨眷中冤假错案工作的通知》精神，会同有关部门对“文化大革命”中造成的冤假错案以及历史遗留下来的老案，逐人逐户进行了清理和复查。至1987年，全市归侨、侨眷及港澳同胞亲属在“文化大革命”期间，因海外关系而造成的冤假错案24起",
        "section": "落实侨务政策冤假错案",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0300.txt:3-5 raw 作侨着",
            "workbench/ocr/paddle_ocr/下/part01/page_0300.txt:3-5 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "根据《关于抓紧清理归侨、侨着档案工作的补充通知》精神，市侨办会同有关部门从1984年开始清理归侨、侨着的人事档案。至1985年底",
        "new": "根据《关于抓紧清理归侨、侨眷档案工作的补充通知》精神，市侨办会同有关部门从1984年开始清理归侨、侨眷的人事档案。至1985年底",
        "section": "落实侨务政策清理档案",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0300.txt:8-10 raw 作侨着",
            "workbench/ocr/paddle_ocr/下/part01/page_0300.txt:8-10 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "落实归侨、侨着知识分子政策。1987年全市有归侨、侨券知识分子286人",
        "new": "落实归侨、侨眷知识分子政策。1987年全市有归侨、侨眷知识分子286人",
        "section": "落实归侨侨眷知识分子政策",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0300.txt:30 raw 作侨着/侨券",
            "workbench/ocr/paddle_ocr/下/part01/page_0300.txt:30 作侨眷/侨眷",
        ],
    },
    {
        "old": "化工部化工矿山设计研究院，有11名归侨、侨先后获得国家级、部级优秀工程设计奖和科技进步奖。",
        "new": "化工部化工矿山设计研究院，有11名归侨、侨眷先后获得国家级、部级优秀工程设计奖和科技进步奖。",
        "section": "归侨侨眷获奖人员",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0300.txt:36 raw 漏眷字",
            "workbench/ocr/paddle_ocr/下/part01/page_0300.txt:36 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "赣榆县对归侨、侨着和港澳同胞在“文化大革命”期间因海外关系而造成的7起冤假错案，全部给予平反昭雪。清理了归侨、侨脊档案，清理出不实部分76件。对在土改和历次运动中被占用的7户393平方米华侨私房全部退赔。对8名归侨、侨着知识分子在工作上给予优先安排，生活、住房等方面给适当照顾。",
        "new": "赣榆县对归侨、侨眷和港澳同胞在“文化大革命”期间因海外关系而造成的7起冤假错案，全部给予平反昭雪。清理了归侨、侨眷档案，清理出不实部分76件。对在土改和历次运动中被占用的7户393平方米华侨私房全部退赔。对8名归侨、侨眷知识分子在工作上给予优先安排，生活、住房等方面给予适当照顾。",
        "section": "赣榆县落实侨务政策",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0300.txt:37-40 raw 作侨着/侨脊",
            "workbench/ocr/paddle_ocr/下/part01/page_0300.txt:37-40 PaddleOCR 作侨眷/侨眷档案/给予适当照顾",
        ],
    },
    {
        "old": "给4户侨着知识分子家属子女办理了农转非户口，11名侨知识分子家属安排了就业，有3名侨着知识分子加入了中国共产党。",
        "new": "给4户侨眷知识分子家属子女办理了农转非户口，11名侨眷知识分子家属安排了就业，有3名侨眷知识分子加入了中国共产党。",
        "section": "灌云县侨眷知识分子",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0301.txt:3-4 raw 作侨着/侨",
            "workbench/ocr/paddle_ocr/下/part01/page_0301.txt:3-4 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "清理归侨、侨卷档案29件。对土改及历次运动中被占用的房屋已落实4户，203平方米，全部赔款。协助有关部门解决了18名归侨、侨着知识分子的职称",
        "new": "清理归侨、侨眷档案29件。对土改及历次运动中被占用的房屋已落实4户，203平方米，全部赔款。协助有关部门解决了18名归侨、侨眷知识分子的职称",
        "section": "东海县侨眷档案与职称",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0301.txt:8-10 raw 作侨卷/侨着",
            "workbench/ocr/paddle_ocr/下/part01/page_0301.txt:8-10 PaddleOCR 作侨眷",
        ],
    },
    {
        "old": "“日本市青年会议所友好访问团”、“市国际青年友好访问团”",
        "new": "“日本堺市青年会议所友好访问团”、“堺市国际青年友好访问团”",
        "section": "青联堺市青年访问团",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0326.txt:5-6 raw 漏堺",
            "workbench/ocr/paddle_ocr/下/part01/page_0326.txt:5-6 PaddleOCR 作日本堺市/堺市",
        ],
    },
    {
        "old": "组织“台侨着属青年夏令营”、“中秋赏月思亲会”",
        "new": "组织“台侨眷属青年夏令营”、“中秋赏月思亲会”",
        "section": "青联台侨眷属青年夏令营",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0326.txt:7 raw 作台侨着属",
            "workbench/ocr/paddle_ocr/下/part01/page_0326.txt:7 作台侨眷属",
        ],
    },
    {
        "old": "于5月7日在日本市博物馆展出。",
        "new": "于5月7日在日本堺市博物馆展出。",
        "section": "青联书法摄影展地点",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0326.txt:9 raw 作日本市",
            "workbench/ocr/paddle_ocr/下/part01/page_0326.txt:9 作日本堺市",
        ],
    },
    {
        "old": "市妇联对原国民党军政人员誉属、女归侨、侨着及女爱国知名人士进行调查",
        "new": "市妇联对原国民党军政人员眷属、女归侨、侨眷及女爱国知名人士进行调查",
        "section": "妇联统战调查对象",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0337.txt:18 raw 作誉属/侨着",
            "workbench/ocr/paddle_ocr/下/part01/page_0337.txt:18 作眷属/侨眷",
        ],
    },
    {
        "old": "在市第七次妇女代表大会上，1名女侨券当选为市妇联常委",
        "new": "在市第七次妇女代表大会上，1名女侨眷当选为市妇联常委",
        "section": "妇联女侨眷当选常委",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0337.txt:22 raw 作女侨券",
            "workbench/ocr/paddle_ocr/下/part01/page_0337.txt:22 作女侨眷",
        ],
    },
    {
        "old": "市妇联先后接待日本市民间妇女代表团一行37人、日本市女性团体联络协会访问团34人。",
        "new": "市妇联先后接待日本堺市民间妇女代表团一行37人、日本堺市女性团体联络协会访问团34人。",
        "section": "妇联堺市妇女代表团",
        "evidence": [
            "workbench/ocr/raw/下/part01/page_0337.txt:23-24 raw 作日本市",
            "workbench/ocr/paddle_ocr/下/part01/page_0337.txt:23-24 作日本堺市",
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
        "note": "只修 raw/PaddleOCR 可闭合的侨眷、眷属、堺市/堺泉北港残留；未全局替换。未展示、未嵌入页图。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第三十九批：侨眷与堺市残留",
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
        "- 每项旧串均要求唯一命中。",
        "- 未处理尚未定位源页的 `侨务工作。建国后` 概述残留和其它疑似词。",
        "- 未展示、未嵌入页图。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Eighth batch of high-confidence OCR typo repairs backed by page-level PaddleOCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch8_paddle_backed_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch8_paddle_backed_20260705.json"

CHANGES = [
    ("仍历历在自", "仍历历在目", "workbench/ocr/paddle_ocr/中/part02/page_0114.txt"),
    ("1990年并始兑付", "1990年开始兑付", "workbench/ocr/paddle_ocr/中/part02/page_0380.txt"),
    ("三项费用拨人数为2610.6万元", "三项费用拨入数为2610.6万元", "workbench/ocr/paddle_ocr/中/part02/page_0302.txt"),
    ("直人海州境内", "直入海州境内", "workbench/ocr/paddle_ocr/下/part02/page_0344.txt"),
    ("南朱绍兴三十一年", "南宋绍兴三十一年", "workbench/ocr/paddle_ocr/下/part01/page_0158.txt; workbench/ocr/paddle_ocr/下/part02/page_0345.txt"),
    ("绝不能与其为伍，助为虐", "绝不能与其为伍，助纣为虐", "workbench/ocr/paddle_ocr/下/part01/page_0158.txt"),
    ("巍胜攻取海州后", "魏胜攻取海州后", "workbench/ocr/paddle_ocr/下/part01/page_0158.txt"),
    ("急派蒙恬镇国领兵余攻海州", "急派蒙恬镇国领兵万余攻海州", "workbench/ocr/paddle_ocr/下/part01/page_0158.txt"),
    ("魏胜身先土卒", "魏胜身先士卒", "workbench/ocr/paddle_ocr/下/part01/page_0158.txt"),
    ("率先冲人敌阵", "率先冲入敌阵", "workbench/ocr/paddle_ocr/下/part01/page_0158.txt"),
    ("魏胜（1120～1165）学彦威", "魏胜（1120～1165）字彦威", "workbench/ocr/paddle_ocr/下/part02/page_0345.txt"),
    ("聚集三干义士抗金", "聚集三千义士抗金", "workbench/ocr/paddle_ocr/下/part02/page_0345.txt"),
    ("收复水，攻克海州", "收复涟水，攻克海州", "workbench/ocr/paddle_ocr/下/part02/page_0345.txt"),
    ("派十兵攻海州", "派十万兵攻海州", "workbench/ocr/paddle_ocr/下/part02/page_0345.txt"),
    ("于是魏巍胜名声大振", "于是魏胜名声大振", "workbench/ocr/paddle_ocr/下/part02/page_0345.txt"),
    ("先派兵数方攻打海州", "先派兵数万攻打海州", "workbench/ocr/paddle_ocr/下/part02/page_0345.txt"),
    ("后金劝降巍胜", "后金劝降魏胜", "workbench/ocr/paddle_ocr/下/part02/page_0345.txt"),
    ("可载辙重", "可载辎重", "workbench/ocr/paddle_ocr/下/part02/page_0345.txt"),
    ("车发射，可射200步远", "弩车发射，可射200步远", "workbench/ocr/paddle_ocr/下/part02/page_0345.txt"),
    ("驻防楚州淮安）清河口", "驻防楚州（淮安）清河口", "workbench/ocr/paddle_ocr/下/part02/page_0345.txt"),
    ("阻击金军于阳，激战一夫后", "阻击金军于淮阳，激战一天后", "workbench/ocr/paddle_ocr/下/part02/page_0345.txt"),
]

DEFERRED = [
    "新编书自：疑似应为新编书目，但暂未找到页级 OCR 直接证据，本批不改。",
    "攻人会稽：语义疑似攻入会稽，但暂未找到页级 OCR 直接证据，本批不改。",
    "金兵主师蒙恬镇国：页级 OCR 仍为主师，本批不按常识改为主帅。",
    "宋军人，金兵拒战：页级 OCR 仍为宋军人，且可能缺谓语，本批不猜补。",
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for old, new, evidence in CHANGES:
        count = html.count(old)
        if count < 1:
            raise RuntimeError(f"missing expected text: {old!r}")
        html = html.replace(old, new)
        applied.append({"old": old, "new": new, "evidence": evidence, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "deferred": DEFERRED,
        "note": "逐条以页级 PaddleOCR 或明确 OCR 对照为证据；不做整段重写。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第八批：PaddleOCR 对照项",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- `{item['old']}` -> `{item['new']}`（命中 {item['count']} 处；证据：`{item['evidence']}`）")
    lines += ["", "## 暂缓项", ""]
    for item in DEFERRED:
        lines.append(f"- {item}")
    lines += ["", "## 边界", "", "- 只修页级 OCR 明确支持的短片段。", "- 不按常识重写人物传略中仍需底本核对的人名、官名和缺谓语句。", ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

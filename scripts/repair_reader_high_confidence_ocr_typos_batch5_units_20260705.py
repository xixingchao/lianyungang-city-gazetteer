# -*- coding: utf-8 -*-
"""Fifth batch of high-confidence OCR typo repairs: unit confusions."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch5_units_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch5_units_20260705.json"

CHANGES = [
    ("250公厅芦笋良种", "250公斤芦笋良种", "种子重量语境"),
    ("每公厅1.1元猛升至5元", "每公斤1.1元猛升至5元", "海带价格按公斤计价"),
    ("葱65万公厅", "葱65万公斤", "蔬菜收购量上下文均为万公斤"),
    ("板栗种子350公厅", "板栗种子350公斤", "种子重量语境"),
    ("人均年产不足50公厅", "人均年产不足50公斤", "公粮征收按产粮公斤计"),
    ("人均月定量17.8公厅", "人均月定量17.8公斤", "居民粮食月定量语境"),
    ("由13公厅恢复到13.5公斤", "由13公斤恢复到13.5公斤", "居民口粮恢复标准语境"),
    ("均140公厅", "均140公斤", "困难时期口粮/粮食语境"),
    ("600万公厅", "600万公斤", "公粮征收数量语境"),
    ("0.6万公厅酒精", "0.6万公斤酒精", "危险物品重量语境"),
    ("11.3万公厅炸药", "11.3万公斤炸药", "危险物品重量语境"),
    ("3.5至7.5公厅小麦", "3.5至7.5公斤小麦", "工资折粮按公斤计"),
    ("90公厅挺举", "90公斤挺举", "举重项目重量语境"),
    ("788方公斤", "788万公斤", "全年征收粮食数量语境"),
    ("4.5方公斤", "4.5万公斤", "农业税人均收入阈值语境"),
    ("1250方公斤", "1250万公斤", "妇女运肥数量语境，与运稻200万公斤同列"),
    ("红娘鱼3方多担", "红娘鱼3万多担", "海产品年产量同列均为万担"),
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for old, new, reason in CHANGES:
        count = html.count(old)
        if count < 1:
            raise RuntimeError(f"missing expected text: {old!r}")
        html = html.replace(old, new)
        applied.append({"old": old, "new": new, "reason": reason, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "sources": [
            "output/final_reader/连云港市志_全书.html matched contexts",
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:8958-8970,14195-14245,19870-19900,21695",
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md:3417,4060,13938,16517,17023",
            "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:3996,5953",
        ],
        "note": "只修单位上下文清楚的公斤/万公斤/万多担；未修需页图判读的方吨类数值。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第五批：单位混淆",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- `{item['old']}` -> `{item['new']}`（{item['reason']}；命中 {item['count']} 处）")
    lines += [
        "",
        "## 边界",
        "",
        "- 未处理 `方吨` 中地质储量、工业能力、港口吞吐等数值，许多源 OCR 同样不可靠，需要页图或底本专项核对。",
        "- `办公厅` 保留为合法词。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

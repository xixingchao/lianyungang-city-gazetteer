# -*- coding: utf-8 -*-
"""Fourth batch of high-confidence OCR typo repairs: 入/人 confusions."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch4_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch4_20260705.json"

CHANGES = [
    ("迁出、迁人手续", "迁出、迁入手续", "户口迁出、迁入登记固定表述"),
    ("人社农户为66.15万户", "入社农户为66.15万户", "供销合作社社员统计语境"),
    ("人社股金不足", "入社股金不足", "贫民合作基金贷款帮助入社语境"),
    ("18万人全部人社", "18万人全部入社", "人民公社化语境"),
    ("农民在人社以后", "农民在入社以后", "农业合作社材料语境"),
    ("在没有人社以前", "在没有入社以前", "农业合作社材料语境"),
    ("自从人社以后", "自从入社以后", "农业合作社材料语境"),
    ("流人城市", "流入城市", "精简职工对象语境"),
    ("徽剧、京剧的流人", "徽剧、京剧的流入", "戏曲传播语境"),
    ("京剧遂南下流人海州", "京剧遂南下流入海州", "戏曲传播语境"),
    ("吕剧流人后", "吕剧流入后", "戏曲传播语境"),
    ("动员工9.7万人", "动员9.7万人", "修复铁路动员群众语境"),
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
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md:175,3889,13362",
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:9781,31833",
            "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:478,548,21741,21808,21816",
        ],
        "note": "只修入/人混淆中语境明确的固定片段；未处理古代人物段内源文残缺处。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第四批",
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
        "- 未处理魏胜等古代人物段内 `宋军人`、`南朱` 等残缺句，源文缺损更重，需另行按页图或底本核对。",
        "- `人社` 中 `工人社会保险`、`非法人社会团体` 是合法跨字命中，保留。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

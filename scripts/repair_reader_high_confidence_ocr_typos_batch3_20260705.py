# -*- coding: utf-8 -*-
"""Third small batch of high-confidence OCR typo repairs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch3_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch3_20260705.json"

CHANGES = [
    ("招工、调人等方式", "招工、调入等方式", "合作商业充实职工队伍语境"),
    ("调人镀锌</p>\n<p>铁皮8吨", "调入镀锌</p>\n<p>铁皮8吨", "五金公司调拨物资语境"),
    ("调人各粮15282.5吨", "调入各粮15282.5吨", "粮食公司调运统计语境"),
    ("可引进调人", "可引进调入", "技术工人引进调配语境"),
    ("抗百民主政府", "抗日民主政府", "同段多处为抗日民主政府，字形误识"),
    ("包围瘦捕", "包围搜捕", "国民党县政府逮捕共产党人语境"),
    ("精简穴员", "精简人员", "整顿编制、精简人员固定表述"),
    ("早好儿百年", "早好几百年", "现代白话固定表述"),
    ("认着自己的亲友", "认作自己的亲友", "掩护散兵语境，动词误识"),
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
        "note": "第三批只处理复扫残留中上下文可直接确认的短错字，不触碰治调人员、抽调人员等合法命中。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第三批",
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
        "- `调人` 余项中包含 `治调人员`、`抽调人员` 等合法词组，不作替换。",
        "- 仍未处理需要页图判读的数值单位错字。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

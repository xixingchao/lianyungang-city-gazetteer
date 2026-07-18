# -*- coding: utf-8 -*-
"""Eleventh batch of high-confidence OCR repairs: units and bingru phrases."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch11_paddle_units_bingru_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch11_paddle_units_bingru_20260705.json"

CHANGES = [
    ("露天锥形发酵罐、方吨啤酒灌装线", "露天锥形发酵罐、万吨啤酒灌装线", "食品工业设备", "workbench/ocr/paddle_ocr/中/part01/page_0092.txt"),
    ("城市房地产税附加并人正税征收", "城市房地产税附加并入正税征收", "房地产税", "workbench/ocr/paddle_ocr/中/part02/page_0322.txt"),
    ("营业税并人工商统一税", "营业税并入工商统一税", "税务", "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md; workbench/ocr/paddle_ocr/中/part02/page_0318.txt"),
    ("货物税及商品流通税并人工商统一税", "货物税及商品流通税并入工商统一税", "税务", "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md; workbench/ocr/paddle_ocr/中/part02/page_0318.txt"),
    ("盐税并人工商税", "盐税并入工商税", "盐税", "workbench/body_chapters/上/第十卷至第十六卷（part03）.md; workbench/ocr/paddle_ocr/merged/连云港市志_上_part03_PaddleOCR汇总.md"),
]

DEFERRED = [
    "`并人固定资产更新...并人科学技术三项费用` 页级 PaddleOCR 未直接给出清晰 `并入`，本批不改。",
    "`战船干余艘` 暂无直接页级 OCR 证据，不改。",
    "`阁门抵侯`、`宋军人，金兵拒战`、`金兵主师蒙恬镇国` 仍缺强证据，不改。",
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    already_clean = []
    for old, new, section, evidence in CHANGES:
        count = html.count(old)
        if count < 1:
            if new in html:
                already_clean.append({"old": old, "new": new, "section": section, "evidence": evidence, "count": 0})
                continue
            raise RuntimeError(f"missing expected text: {old!r}")
        html = html.replace(old, new)
        applied.append({"old": old, "new": new, "section": section, "evidence": evidence, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "already_clean": already_clean,
        "deferred": DEFERRED,
        "note": "精确短片段替换；只修已获页级 OCR 或章节正文旁证支持的残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第十一批：单位与并入残留",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- `{item['old']}` -> `{item['new']}`（{item['section']}；命中 {item['count']} 处；证据：`{item['evidence']}`）")
    if already_clean:
        lines += ["", "## 已清理项", ""]
        for item in already_clean:
            lines.append(f"- `{item['old']}` 当前阅读版已为 `{item['new']}`（{item['section']}；证据：`{item['evidence']}`）")
    lines += ["", "## 暂缓项", ""]
    for item in DEFERRED:
        lines.append(f"- {item}")
    lines += ["", "## 边界", "", "- 不全局替换 `并人`，只修精确短语。", "- 不修 OCR 证据不足的历史战事和官职残留。", ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

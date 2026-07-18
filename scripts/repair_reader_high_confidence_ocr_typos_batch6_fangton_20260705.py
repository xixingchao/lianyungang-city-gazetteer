# -*- coding: utf-8 -*-
"""Sixth batch of high-confidence OCR typo repairs: fang/wan ton confusions."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch6_fangton_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch6_fangton_20260705.json"

CHANGES = [
    (
        "仅食盐积压5方吨",
        "仅食盐积压5万吨",
        "水运货物积压按万吨计；同类盐、煤、矿石运输数量上下文均用万吨",
        "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:2315-2322; page-anchor LYG-1475",
    ),
    (
        "求得水晶矿地质储量药17方吨",
        "求得水晶矿地质储量约17万吨",
        "地质储量单位为万吨；药/约、方/万为同句 OCR 错识",
        "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md:24901-24908; page-anchor LYG-2413",
    ),
    (
        "探明矿工业储量2253方吨",
        "探明矿工业储量2253万吨",
        "矿石工业储量同段均按万吨计",
        "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md:24924-24931; page-anchor LYG-2414",
    ),
    (
        "探明矿石工业储量1076方吨",
        "探明矿石工业储量1076万吨",
        "矿石工业储量同段均按万吨计",
        "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md:24932-24936; page-anchor LYG-2414",
    ),
    (
        "下层远景储量83方吨",
        "下层远景储量83万吨",
        "远景储量同段与暂不能利用储量均按万吨计",
        "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md:24935-24937; page-anchor LYG-2414",
    ),
]

DEFERRED = [
    {
        "text": "露天锥形发酵罐、方吨啤酒灌装线",
        "reason": "设备名缺失前置数字，且同段产品年产能力为啤酒1500吨，不能据单位模式直接补成万吨。",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:4993-5004; page-anchor LYG-0995",
    }
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for old, new, reason, source in CHANGES:
        count = html.count(old)
        if count != 1:
            raise RuntimeError(f"expected one match for {old!r}, got {count}")
        html = html.replace(old, new)
        applied.append({"old": old, "new": new, "reason": reason, "source": source, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "deferred": DEFERRED,
        "note": "只修主阅读版中上下文可确定为万吨的方吨错识；啤酒设备项缺数字，保留待底本核对。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第六批：方吨/万吨混淆",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- `{item['old']}` -> `{item['new']}`（{item['reason']}；{item['source']}）")
    lines += [
        "",
        "## 暂缓项",
        "",
    ]
    for item in DEFERRED:
        lines.append(f"- `{item['text']}`：{item['reason']}依据位置：{item['source']}。")
    lines += [
        "",
        "## 边界",
        "",
        "- 未做全局 `方吨` -> `万吨` 替换；只处理主阅读版中 5 个可由上下文确定的固定片段。",
        "- `药17方吨` 同时修为 `约17万吨`，因为该处为地质储量估算语境。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

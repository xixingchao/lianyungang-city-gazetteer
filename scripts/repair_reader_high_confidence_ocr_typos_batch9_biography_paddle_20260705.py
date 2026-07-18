# -*- coding: utf-8 -*-
"""Ninth batch of high-confidence OCR repairs in biography sections backed by PaddleOCR."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch9_biography_paddle_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch9_biography_paddle_20260705.json"

CHANGES = [
    ("白宝山（1878～1941）字峻青", "白宝山（1878～1941）字峻青", "anchor", "workbench/ocr/paddle_ocr/下/part02/page_0351.txt"),
    ("先当张勋马弃", "先当张勋马弁", "白宝山传", "workbench/ocr/paddle_ocr/下/part02/page_0351.txt"),
    ("民国16年，北伐军攻入海州，白宝山残部投降", "民国16年，北伐军攻入海州，白宝山残部投降", "anchor", "workbench/ocr/paddle_ocr/下/part02/page_0351.txt"),
    ("墟沟北固山大楼", "墟沟北崮山大楼", "白宝山传", "workbench/ocr/paddle_ocr/下/part02/page_0351.txt"),
    ("辗转入川", "辗转入川", "anchor", "workbench/ocr/paddle_ocr/下/part02/page_0351.txt"),
    ("宋球（18841942）", "宋球（1884～1942）", "宋球传", "workbench/ocr/paddle_ocr/下/part02/page_0351.txt"),
    ("灌云县白人。民国2年", "灌云县白蚬人。民国2年", "宋球传", "workbench/ocr/paddle_ocr/下/part02/page_0351.txt"),
    ("乡人在小柴墅盐河堆上为其立捍卫乡间纪念碑", "乡人在小柴墅盐河堆上为其立捍卫乡闾纪念碑", "宋球传", "workbench/ocr/paddle_ocr/下/part02/page_0351.txt"),
    ("在白乡忆帆河西苑庄埋伏堵击", "在白蚬乡忆帆河西茆庄埋伏堵击", "宋球传", "workbench/ocr/paddle_ocr/下/part02/page_0351.txt"),
    ("敦料被国民政府灌云县县长董建华撤了区长职务", "孰料被国民政府灌云县县长董建华撤了区长职务", "宋球传", "workbench/ocr/paddle_ocr/下/part02/page_0351.txt"),
    ("宋球叹日“国家兴亡", "宋球叹曰“国家兴亡", "宋球传", "workbench/ocr/paddle_ocr/下/part02/page_0351.txt"),
    ("宋球对书法有较深造谐", "宋球对书法有较深造诣", "宋球传", "workbench/ocr/paddle_ocr/下/part02/page_0352.txt"),
    ("有其重来东磊”题刻", "有其“重来东磊”题刻", "宋球传", "workbench/ocr/paddle_ocr/下/part02/page_0352.txt"),
    ("唐雨生（1906～1942）", "唐雨生（1906～1942）", "anchor", "workbench/ocr/paddle_ocr/下/part02/page_0363.txt"),
    ("受党的派遣，镶转包头、宁夏等地", "受党的派遣，辗转包头、宁夏等地", "唐雨生传", "workbench/ocr/paddle_ocr/下/part02/page_0363.txt"),
    ("他用扁担和持枪岁徒搏斗", "他用扁担和持枪歹徒搏斗", "唐雨生传", "workbench/ocr/paddle_ocr/下/part02/page_0363.txt"),
    ("奋力击毙一名岁徒", "奋力击毙一名歹徒", "唐雨生传", "workbench/ocr/paddle_ocr/下/part02/page_0363.txt"),
    ("因失面过多", "因失血过多", "唐雨生传", "workbench/ocr/paddle_ocr/下/part02/page_0363.txt"),
    ("打入伪军内部担任连长", "打入伪军内部担任连长", "anchor", "workbench/ocr/paddle_ocr/下/part02/page_0363.txt"),
    ("沿圩河扫荡盐城抗日根据地", "沿贾圩河扫荡盐城抗日根据地", "唐雨生传", "workbench/ocr/paddle_ocr/下/part02/page_0363.txt"),
    ("文用左手指挥", "又用左手指挥", "唐雨生传", "workbench/ocr/paddle_ocr/下/part02/page_0363.txt"),
    ("壮烈牺。</p>", "壮烈牺牲。</p>", "唐雨生传", "workbench/ocr/paddle_ocr/下/part02/page_0363.txt"),
]

DEFERRED = [
    "白宝山传中 `白随陈调元辗转入川` 语义可读，本批不改。",
    "宋球传中涉及地名的修复只按 PaddleOCR 明确短语处理，不扩展到其它 `白人` 命中。",
    "唐雨生传中 `打入伪军内部` 已为正确文本，脚本仅用作锚点检查。",
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for old, new, section, evidence in CHANGES:
        count = html.count(old)
        if count < 1:
            raise RuntimeError(f"missing expected text: {old!r}")
        if old != new:
            html = html.replace(old, new)
        applied.append({"old": old, "new": new, "section": section, "evidence": evidence, "count": count, "changed": old != new})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": [item for item in applied if item["changed"]],
        "anchors": [item for item in applied if not item["changed"]],
        "deferred": DEFERRED,
        "note": "人物传略局部短片段修复；证据来自页级 PaddleOCR，不做整段重写。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第九批：人物传略 PaddleOCR 对照",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        if item["changed"]:
            lines.append(f"- `{item['old']}` -> `{item['new']}`（{item['section']}；命中 {item['count']} 处；证据：`{item['evidence']}`）")
    lines += ["", "## 锚点检查", ""]
    for item in applied:
        if not item["changed"]:
            lines.append(f"- `{item['old']}` 存在（{item['section']}；命中 {item['count']} 处；证据：`{item['evidence']}`）")
    lines += ["", "## 暂缓项", ""]
    for item in DEFERRED:
        lines.append(f"- {item}")
    lines += ["", "## 边界", "", "- 只修白宝山、宋球、唐雨生三段中页级 OCR 明确支持的短片段。", "- 不因同形残留做全局替换。", ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied if item['changed'])}")
    print(f"anchors={sum(item['count'] for item in applied if not item['changed'])}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

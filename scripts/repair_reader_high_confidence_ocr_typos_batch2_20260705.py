# -*- coding: utf-8 -*-
"""Second batch of high-confidence OCR typo repairs in the main reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch2_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch2_20260705.json"

EXACT_CHANGES = [
    ("自已的实际情况", "自己的实际情况", "现代白话固定用法"),
    ("自已安装、调测", "自己安装、调测", "现代白话固定用法"),
    ("自已采购", "自己采购", "现代白话固定用法"),
    ("自已零售", "自己零售", "现代白话固定用法"),
    ("自已组织运输力量", "自己组织运输力量", "现代白话固定用法"),
    ("自已备有盐", "自己备有盐", "现代白话固定用法"),
    ("宣传了自已", "宣传了自己", "现代白话固定用法"),
    ("认识自已", "认识自己", "现代白话固定用法"),
    ("发表自已的意见", "发表自己的意见", "现代白话固定用法"),
    ("自已的亲友", "自己的亲友", "现代白话固定用法"),
    ("除自已行使辩护权外", "除自己行使辩护权外", "现代白话固定用法"),
    ("自已的历史问题", "自己的历史问题", "现代白话固定用法"),
    ("发了自已的愤世激情", "发了自己的愤世激情", "现代白话固定用法"),
    ("演出自已创作的剧目", "演出自己创作的剧目", "现代白话固定用法"),
    ("扩大自已在社会中影响", "扩大自己在社会中影响", "现代白话固定用法"),
    ("献出了自已的生命", "献出了自己的生命", "现代白话固定用法"),
    ("自已才撤离阵地", "自己才撤离阵地", "现代白话固定用法"),
    ("表达自已忠于共产主义", "表达自己忠于共产主义", "现代白话固定用法"),
    ("她自已带头实行", "她自己带头实行", "现代白话固定用法"),
    ("否认自已是共产党员", "否认自己是共产党员", "现代白话固定用法"),
    ("自已用手枪自尽", "自己用手枪自尽", "现代白话固定用法"),
    ("自已挨雨淋", "自己挨雨淋", "现代白话固定用法"),
    ("献出自已的高产滩", "献出自己的高产滩", "现代白话固定用法"),
    ("自已带着通信员", "自己带着通信员", "现代白话固定用法"),
    ("有自已特色", "有自己特色", "现代白话固定用法"),
    ("自已确定", "自己确定", "现代白话固定用法"),
    ("除自已多渠道", "除自己多渠道", "现代白话固定用法"),
    ("调人钢材30吨", "调入钢材30吨", "调拨物资语境"),
    ("调人生铁30吨", "调入生铁30吨", "调拨物资语境"),
    ("调人镀锌铁皮8吨", "调入镀锌铁皮8吨", "调拨物资语境"),
    ("调人外地菜933万公斤", "调入外地菜933万公斤", "蔬菜调运语境"),
    ("调人外地菜58万公斤", "调入外地菜58万公斤", "蔬菜调运语境"),
    ("调人外地386.5万公斤", "调入外地386.5万公斤", "蔬菜调运语境"),
    ("从根据地调人大批救济粮", "从根据地调入大批救济粮", "粮食调拨语境"),
    ("贸易公司调人75吨生油", "贸易公司调入75吨生油", "粮油调拨语境"),
    ("大量调人山东的生油", "大量调入山东的生油", "粮油调拨语境"),
    ("地瓜干由东海、赣榆调人", "地瓜干由东海、赣榆调入", "粮食调拨语境"),
    ("稻谷由四川调人", "稻谷由四川调入", "粮食调拨语境"),
    ("由苏北调人山东滨海", "由苏北调入山东滨海", "部队调动语境"),
    ("从老解放区调人千余名干部", "从老解放区调入千余名干部", "干部调配语境"),
    ("调人28人", "调入28人", "干部调配统计语境"),
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for old, new, reason in EXACT_CHANGES:
        count = html.count(old)
        if count < 1:
            raise RuntimeError(f"missing expected text: {old}")
        html = html.replace(old, new)
        applied.append({"old": old, "new": new, "reason": reason, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "sources": [
            "output/final_reader/连云港市志_全书.html matched contexts",
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md around vegetables/grain/materials contexts",
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md around public security/personnel/labor contexts",
            "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md around literature/biographies/appendix contexts",
        ],
        "note": "仅修现代白话中明确应为“自己”和调拨语境中明确应为“调入”的固定片段；保留古文“不能自已”等正确用法。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第二批",
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
        "- 未对 `自已` 做全局替换，保留古文/固定表达 `不能自已`。",
        "- 未处理 `人社`、`纳人`、`公厅` 等混合模式；这些需要按段或按单位专项核对。",
        "- 未改源 OCR/正文汇总文件；本轮只修当前主阅读版并留报告。",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

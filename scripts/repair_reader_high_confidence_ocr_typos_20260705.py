# -*- coding: utf-8 -*-
"""Repair high-confidence OCR typos in the main final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_20260705.json"

CHANGES = [
    {
        "old": "凭并发区管委会的证明",
        "new": "凭开发区管委会的证明",
        "reason": "第二十八卷开发区优惠政策语境；同段多处为开发区管委会。",
    },
    {
        "old": "经并发区管委会批准",
        "new": "经开发区管委会批准",
        "reason": "第二十八卷内联企业优惠待遇语境；审批主体为开发区管委会。",
    },
    {
        "old": "社队企业开始步人健康发展的轨道",
        "new": "社队企业开始步入健康发展的轨道",
        "reason": "固定搭配“步入……轨道”。",
    },
    {
        "old": "步人中国“八大海港”之列",
        "new": "步入中国“八大海港”之列",
        "reason": "固定搭配“步入……之列”。",
    },
    {
        "old": "把小蓬莱写成是步人天庭的必由之路",
        "new": "把小蓬莱写成是步入天庭的必由之路",
        "reason": "固定搭配“步入天庭”。",
    },
    {
        "old": "对外贸易步人了新的阶段",
        "new": "对外贸易步入了新的阶段",
        "reason": "固定搭配“步入……阶段”。",
    },
    {
        "old": "1357方公斤，其中大白菜1187.5万公斤",
        "new": "1357万公斤，其中大白菜1187.5万公斤",
        "reason": "蔬菜收购量上下文均以万公斤计；分项 1187.5 万公斤支撑总量为 1357 万公斤。",
    },
    {
        "old": "贸易粮5方公斤",
        "new": "贸易粮5万公斤",
        "reason": "同句优待粮、救济粮均为万公斤，粮食救济数量单位语境明确。",
    },
    {
        "old": "市第届人民代表大会一次会议召开",
        "new": "市第一届人民代表大会一次会议召开",
        "reason": "1954 年首次人民代表大会制度确立，后文称至 1965 年历经五届。",
    },
    {
        "old": "国家第个五年计划时期内的全面规划",
        "new": "国家第一个五年计划时期内的全面规划",
        "reason": "同章历届人大原文为《国家第一个五年计划时期内的全面规划（草案）》；固定历史术语。",
    },
    {
        "old": "国家第个五年计划时期的规划",
        "new": "国家第一个五年计划时期的规划",
        "reason": "同章政务纪要和历届人大上下文均为第一个五年计划。",
    },
    {
        "old": "一、第届人民代表大会第一次会议",
        "new": "一、第一届人民代表大会第一次会议",
        "reason": "小节标题为历届人民代表大会，下一项为第二届；此处为第一届。",
    },
    {
        "old": "海州区第届人民代表大会于1953年11月2～3日召开",
        "new": "海州区第一届人民代表大会于1953年11月2～3日召开",
        "reason": "后文接续二、三、四、五、六届海州区人民代表大会。",
    },
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for change in CHANGES:
        count = html.count(change["old"])
        if count < 1:
            raise RuntimeError(f"missing expected text: {change['old']}")
        html = html.replace(change["old"], change["new"])
        applied.append({**change, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "sources": [
            "output/final_reader/连云港市志_全书.html matched contexts",
            "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:23968-24012",
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:31890-31900",
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:32874-32888",
            "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:33490-33505",
        ],
        "note": "仅修逐条核验的 OCR 错字；未对全书“方吨/方公斤”等模式做泛替换。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修",
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
        "- 未批量替换 `方吨`、`方公斤`；只处理数字、单位和上下文都清楚的 `1357万公斤` 与 `贸易粮5万公斤`。",
        "- 未改源 OCR/正文汇总文件；本轮只修当前主阅读版并留报告。",
        "",
        "## 源证据",
        "",
        "- `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:23968-24012`",
        "- `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:31890-31900`",
        "- `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:32874-32888`",
        "- `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:33490-33505`",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

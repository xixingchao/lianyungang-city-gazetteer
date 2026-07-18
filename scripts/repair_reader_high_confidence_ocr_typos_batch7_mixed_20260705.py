# -*- coding: utf-8 -*-
"""Seventh batch of high-confidence OCR typo repairs: mixed fixed phrases."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch7_mixed_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch7_mixed_20260705.json"

CHANGES = [
    ("并始产异型玻璃瓶", "开始生产异型玻璃瓶", "企业生产沿革语境"),
    ("广内设5个职能科室", "厂内设5个职能科室", "厂内机构固定搭配"),
    ("广内设15个职能科室", "厂内设15个职能科室", "厂内机构固定搭配"),
    ("广内设6个职能科室", "厂内设6个职能科室", "厂内机构固定搭配"),
    ("省政府须发的“明星企业”证书", "省政府颁发的“明星企业”证书", "证书颁发固定搭配"),
    ("铁工广相继开业", "铁工厂相继开业", "机械工业企业名词"),
    ("华兴铁工广迁往徐州市", "华兴铁工厂迁往徐州市", "企业名称"),
    ("华兴铁工广副经理", "华兴铁工厂副经理", "企业名称"),
    ("国家地质、治金、化工", "国家地质、冶金、化工", "行业名称"),
    ("国家治金工业部", "国家冶金工业部", "部委名称"),
    ("治金用B+C+D级", "冶金用B+C+D级", "矿石用途"),
    ("形成治金、煤炭炼焦", "形成冶金、煤炭炼焦", "工业门类"),
    ("治金、化学工业较少", "冶金、化学工业较少", "工业卫生行业名称"),
    ("辽宁省治金厅厅长", "辽宁省冶金厅厅长", "机构名称"),
    ("根据化学工屏”的决定", "根据化学工业部的决定", "上下文为化学工业部找矿决定"),
    ("1986年，并始实施", "1986年，开始实施", "科技计划管理机制语境"),
    ("获江苏省科技一一、二等奖", "获江苏省科技一、二等奖", "奖项等级表达"),
    ("第一批已批推下达九十项", "第一批已批准下达九十项", "项目审批语境"),
    ("我们考到现有企业", "我们考虑到现有企业", "常用表达"),
    ("排人课表", "排入课表", "课程安排固定搭配"),
    ("汇人蕃薇河", "汇入蕃薇河", "河流汇入固定搭配"),
    ("北伐军攻人海州", "北伐军攻入海州", "军事行动固定搭配"),
    ("开门迎魏胜军人城", "开门迎魏胜军入城", "入城固定搭配"),
    ("其余长驱直人", "其余长驱直入", "长驱直入成语"),
    ("落人重围", "落入重围", "落入固定搭配"),
]

DEFERRED = [
    "露天锥形发酵罐、方吨啤酒灌装线：缺前置数字，继续待底本核对。",
    "魏胜人物传中仍有若干疑难处，如字号、兵数、地名和整句缺字，未在本批重写。",
    "蕃薇河/蔷薇河在不同历史语境中混用，本批不做河名统一。",
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
        "deferred": DEFERRED,
        "note": "固定片段精确替换；不对同形词做全局规则化。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第七批：混合固定词组",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- `{item['old']}` -> `{item['new']}`（{item['reason']}；命中 {item['count']} 处）")
    lines += ["", "## 暂缓项", ""]
    for item in DEFERRED:
        lines.append(f"- {item}")
    lines += ["", "## 边界", "", "- 不修古文、地名和整句缺损中证据不足的项。", "- 不批量替换 `人/入`，只修固定搭配。", ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

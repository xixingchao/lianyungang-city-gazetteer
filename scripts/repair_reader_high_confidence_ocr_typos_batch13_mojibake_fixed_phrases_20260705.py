# -*- coding: utf-8 -*-
"""Thirteenth batch of high-confidence OCR repairs: mojibake and fixed phrases."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch13_mojibake_fixed_phrases_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch13_mojibake_fixed_phrases_20260705.json"

CHANGES = [
    ("广长（经理）负责制", "厂长（经理）负责制", "企业改革固定词", "workbench/ocr/merged/连云港市志_中_part01_OCR汇总.md:25666; workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:22986"),
    ("被船家视为長途", "被船家视为畏途", "凤凰山景区固定词", "workbench/ocr/merged/连云港市志_中_part02_OCR汇总.md:7939; 语义固定搭配"),
    ("顽敌迄未得}", "顽敌迄未得逞", "万寿山石刻跋文", "同段已有 `顽寇迄未得暹` OCR 形近；固定词 `得逞`"),
    ("未能得ä", "未能得逞", "吴辟初传", "乱码残留；上下文为敌方建立据点未能成功"),
    ("抗甘民族统一战线", "抗日民族统一战线", "王子成传", "统一战线固定词"),
    ("苏中抗甘根据地", "苏中抗日根据地", "惠浴宇传", "抗日根据地固定词"),
    ("在谈判桌上签学", "在谈判桌上签字", "惠浴宇传", "固定搭配"),
    ("化装潜人新浦", "化装潜入新浦", "徐竞传", "固定搭配"),
    ("撕碎抛人河中", "撕碎抛入河中", "孙德南传", "固定搭配"),
    ("孙敏不長艰险", "孙敏不畏艰险", "孙敏传", "固定搭配"),
    ("陷人敌人重围", "陷入敌人重围", "孙敏传", "固定搭配"),
]

DEFERRED = [
    "`参加暴动大楼` 仍缺直接底本文字证据，本批不改。",
    "石刻段 `顽寇迄未得暹` 可能同为 `得逞`，但为碑刻引文且 OCR 原文也作 `暹`，暂不改。",
    "`加人中国共产党`、`考人某校` 命中很多，虽多半为 `加入/考入`，需要分批按人物条目核对。",
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    applied = []
    for old, new, section, evidence in CHANGES:
        count = html.count(old)
        if count < 1:
            raise RuntimeError(f"missing expected text: {old!r}")
        html = html.replace(old, new)
        applied.append({"old": old, "new": new, "section": section, "evidence": evidence, "count": count})
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": applied,
        "deferred": DEFERRED,
        "note": "精确短片段替换；修主阅读版中固定搭配和明显乱码残留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第十三批：乱码与固定词残留",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for item in applied:
        lines.append(f"- `{item['old']}` -> `{item['new']}`（{item['section']}；命中 {item['count']} 处；证据：`{item['evidence']}`）")
    lines += ["", "## 暂缓项", ""]
    for item in DEFERRED:
        lines.append(f"- {item}")
    lines += ["", "## 边界", "", "- 不批量替换 `人/入`，只修本批精确短语。", "- 不改中间 OCR 原文文件，只修主阅读版。", ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Twelfth batch of high-confidence OCR repairs: biography structure residues."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch12_biography_structure_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch12_biography_structure_20260705.json"

CHANGES = [
    (
        "胡文臣壮烈牺缪秋杰（1889～1966）",
        "胡文臣壮烈牺牲。</p><p>缪秋杰（1889～1966）",
        "胡文臣/缪秋杰传记断段",
        "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:17289-17290; workbench/ocr/merged/连云港市志_下_part02_OCR汇总.md page-anchor LYG-2785",
    ),
    (
        "壮烈牺牲。民国朱仲琴（1897～1976）",
        "壮烈牺牲。</p><p>朱仲琴（1897～1976）",
        "吴辟初/朱仲琴传记断段",
        "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md:17413-17415; workbench/ocr/merged/连云港市志_下_part02_OCR汇总.md page-anchor LYG-2788",
    ),
    ("民国13年（1924）年人海州崇真中学", "民国13年（1924年）入海州崇真中学", "刘锡九传", "同页传记年份格式和固定搭配"),
    ("民国15年（民国26年）人海州崇真中学读书", "民国15年（1926年）入海州崇真中学读书", "钱霖传", "1912年生平与民国15年换算；固定搭配"),
    ("被捕人狱", "被捕入狱", "武同儒传等", "固定搭配"),
    ("逮捕人狱", "逮捕入狱", "惠浴宇传", "固定搭配"),
    ("奔赴延安，人抗日军政大学学习", "奔赴延安，入抗日军政大学学习", "惠浴宇传", "固定搭配"),
    ("符竹庭人抗日军政大学学习", "符竹庭入抗日军政大学学习", "符竹庭传", "固定搭配"),
    ("东北第一第二橡胶广广长", "东北第一第二橡胶厂厂长", "钱霖传", "职务固定搭配"),
    ("山东橡胶总厂广长", "山东橡胶总厂厂长", "钱霖传", "职务固定搭配"),
]

DEFERRED = [
    "`未能得ä` 缺失字无法仅凭 OCR 合并稿确认，本批不补。",
    "`参加暴动大楼`、`不長艰险`、`陷人敌人重围` 等仍需更强页图或底本文字证据。",
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
        "note": "人物传略结构断裂和固定搭配精确替换；不补缺字。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第十二批：人物传略结构残留",
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
    lines += ["", "## 边界", "", "- 只修人物传略中的断段、固定搭配和职务词。", "- 不依据常识补全缺失汉字。", ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={sum(item['count'] for item in applied)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()

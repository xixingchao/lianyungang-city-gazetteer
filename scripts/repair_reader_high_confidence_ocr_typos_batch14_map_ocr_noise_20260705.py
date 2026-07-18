# -*- coding: utf-8 -*-
"""Fourteenth batch: remove map OCR noise from the main reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch14_map_ocr_noise_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_high_confidence_ocr_typos_batch14_map_ocr_noise_20260705.json"

OLD = "<p>临洪河新沭河香塔山黄水库庄è龙青鲁兰ó出告尾淡沙汪海河连云港市朱①赣榆县西河蔷河青稽日镇河州e湾范薇盐河石梁河水库胸山水井e沭新河临洪e沭墟沟水井石河河河乌淡排龙河烧海鲁兰河龙香连云港市烧安 28河作香梁沭西双湖水库善盐河东海县河河牛山镇27善后河薇e新五安峰水库车河轴图环境监测の泊河河河河叮河当灌云县二0伊山镇e沂图例e门河河东小鸭河新河流、水库①地表水断面及编号①地下水断面及编号图 6—1 地表水、地下水监测断面点位图秦山岛0 111101110临洪东西口连e岛临洪墟沟河图6—2 近海海域监测站位图</p>"
NEW = "<p>图6-1 地表水、地下水监测断面点位图</p><p>图6-2 近海海域监测站位图</p>"

EVIDENCE = [
    "workbench/body_chapters/上/第四卷至第十卷（part02）.md:7267",
    "workbench/body_chapters/上/第四卷至第十卷（part02）.md:7286",
    "workbench/ocr/raw/上/part02/page_0118.txt:56",
    "workbench/ocr/raw/上/part02/page_0119.txt:15",
    "workbench/ocr/paddle_ocr/上/part02/page_0118.txt:167",
]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    count = html.count(OLD)
    if count != 1:
        raise RuntimeError(f"expected one map-noise paragraph, found {count}")
    html = html.replace(OLD, NEW)
    HTML.write_text(html, encoding="utf-8")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "reader": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changes": [{"old_excerpt": OLD[:120] + "...", "new": NEW, "count": count, "evidence": EVIDENCE}],
        "note": "将第六卷环境监测两张地图的图内 OCR 噪声压回规范图题；不删除正文叙述。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第十四批：环境监测地图 OCR 噪声",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
        "- 将第六卷环境监测页中一整段地图内地名/编号 OCR 噪声，替换为两个规范图题段：`图6-1 地表水、地下水监测断面点位图`、`图6-2 近海海域监测站位图`。",
        "- 该段原文来自图内标注，不应作为连续正文交付；正文源和 raw/PaddleOCR 均可确认应保留图题。",
        "",
        "## 证据",
        "",
    ]
    for item in EVIDENCE:
        lines.append(f"- `{item}`")
    lines += ["", "## 边界", "", "- 只替换主阅读版中的单个噪声段，不改中间 OCR 源文件。", "- 不嵌入或展示页图。", ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print("changed=1")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
